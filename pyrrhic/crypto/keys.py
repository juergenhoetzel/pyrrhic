"""
This module contains the crypto primitives used by restic.
"""

import json
from base64 import b64decode, b64encode
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import poly1305
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from pydantic import BaseModel, conbytes, validator

# mask for key, (cf. http://cr.yp.to/mac/poly1305-20050329.pdf)
_POLY1305KEYMASK = b"\xff\xff\xff\x0f\xfc\xff\xff\x0f\xfc\xff\xff\x0f\xfc\xff\xff\x0f"


class WrappedKey(BaseModel):
    """Class that contain all data that is needed to derive the
    repository's master encryption and message authentication keys
    from a user's password."""

    hostname: str
    username: str
    kdf: str
    N: int
    r: int
    p: int
    created: datetime
    data: bytes
    salt: bytes

    @validator("salt")
    def salt_base64(cls, v):
        return b64decode(v)

    @validator("data")
    def data_base64(cls, v):
        return b64decode(v)


class Mac(BaseModel):
    """Class that holdes the Poly1305-AES parameters"""

    k: conbytes(min_length=16, max_length=16)  # type: ignore[valid-type]
    r: conbytes(min_length=16, max_length=16)  # type: ignore[valid-type]


class MasterKey(BaseModel):
    """Class that holds encryption and message authentication keys for a
    repository."""

    mac: Mac
    encryption: conbytes(min_length=32, max_length=32)  # type: ignore[valid-type]

    def restic_json(self):
        """Return restic representation of Masterkey"""
        return {
            "mac": {
                "r": b64encode(self.mac.r).decode(),
                "k": b64encode(self.mac.k).decode(),
            },
            "encrypt": b64encode(self.encryption).decode(),
        }

    def __hash__(self):
        return hash(self.encryption + self.mac.k + self.mac.r)


def load_key(key_path: str) -> WrappedKey:
    with open(key_path) as f:
        j = json.load(f)
        return WrappedKey(**j)


def _poly1305_validate(nonce: bytes, k: bytes, r: bytes, message: bytes, mac: bytes) -> bool:
    r = bytes([(r & m) for r, m in zip(r, _POLY1305KEYMASK)])
    cipher = Cipher(algorithms.AES(k), modes.ECB())
    encryptor = cipher.encryptor()
    aes_ciphertext = encryptor.update(nonce) + encryptor.finalize()
    poly1305_key = r + aes_ciphertext
    p = poly1305.Poly1305(poly1305_key)
    p.update(message)
    return p.finalize() == mac


def _decrypt(aes_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def decrypt_mac(key: MasterKey, restic_blob: bytes) -> bytes:
    """Decrypt 'IV || CIPHERTEXT || MAC' bytes, validate mac and
    return plaintext bytes"""
    nonce = restic_blob[:16]
    mac = restic_blob[-16:]
    ciphertext = restic_blob[16:-16]
    if not _poly1305_validate(nonce, key.mac.k, key.mac.r, ciphertext, mac):
        raise ValueError("ciphertext verification failed")
    return _decrypt(key.encryption, nonce, ciphertext)


def get_masterkey(path: str, password: bytes) -> MasterKey:
    wrapped_key = load_key(path)
    kdf = Scrypt(
        wrapped_key.salt,
        64,
        wrapped_key.N,
        wrapped_key.r,
        wrapped_key.p,
        backend=default_backend,
    )
    derived_key = kdf.derive(password)
    poly_k = derived_key[32:48]
    poly_r = derived_key[48:]
    nonce = wrapped_key.data[0:16]
    message = wrapped_key.data[16:-16]
    mac = wrapped_key.data[-16:]
    if not _poly1305_validate(nonce, poly_k, poly_r, message, mac):
        raise ValueError("Invalid Password")
    j = json.loads(_decrypt(derived_key[:32], nonce, message))
    encryption = b64decode(j["encrypt"])
    r = b64decode(j["mac"]["r"])
    k = b64decode(j["mac"]["k"])
    return MasterKey(encryption=encryption, mac=Mac(k=k, r=r))
