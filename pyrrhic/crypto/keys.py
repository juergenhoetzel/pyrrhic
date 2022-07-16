import json
from pydantic import BaseModel
from pydantic import conbytes
from datetime import datetime
from base64 import b64decode, b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import poly1305
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms

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


class Mac(BaseModel):
    """Class that holdes the Poly1305-AES parameters"""

    k: conbytes(min_length=16, max_length=16)
    r: conbytes(min_length=16, max_length=16)


class MasterKey(BaseModel):
    """Class that holds encryption and message authentication keys for a
    repository."""

    mac: Mac
    encryption: conbytes(min_length=32, max_length=32)

    def restic_json(self):
        """Return restic representation of Masterkey"""
        return {
            "mac": {
                "r": b64encode(self.mac.r).decode(),
                "k": b64encode(self.mac.k).decode(),
            },
            "encrypt": b64encode(self.encryption).decode(),
        }


def load_key(key_path: str) -> WrappedKey:
    with open(key_path, "r") as f:
        j = json.load(f)
        # FIXME: This should by done using pydantic
        j["salt"] = b64decode(j["salt"])
        j["data"] = b64decode(j["data"])
        return WrappedKey(**j)


def _decrypt(aes_key: bytes, nonce: bytes, ciphertext: bytes):
    # FIXME: Validate
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def _poly1305_validate(
    nonce: bytes, k: bytes, r: bytes, message: bytes, mac: bytes
) -> None:
    r = bytes([(r & m) for r, m in zip(r, _POLY1305KEYMASK)])
    cipher = Cipher(algorithms.AES(k), modes.ECB())
    encryptor = cipher.encryptor()
    aes_ciphertext = encryptor.update(nonce) + encryptor.finalize()
    poly1305_key = r + aes_ciphertext
    p = poly1305.Poly1305(poly1305_key)
    p.update(message)
    if p.finalize() != mac:
        raise ValueError("Invalid password")


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
    _poly1305_validate(nonce, poly_k, poly_r, message, mac)
    j = json.loads(_decrypt(derived_key[:32], nonce, message))
    encryption = b64decode(j["encrypt"])
    r = b64decode(j["mac"]["r"])
    k = b64decode(j["mac"]["k"])
    return MasterKey(encryption=encryption, mac=Mac(k=k, r=r))


# return MasterKey({"encryption": b64decode(j["encrypt"]), "mac": j["r"] + j["k"]})


# FIXME: Use Model for key
# FIXME: Move to config.py
def get_config(masterkey: MasterKey, path: str):
    key = masterkey.encryption
    k, r = masterkey.mac.k, masterkey.mac.r
    with open(path, "rb") as f:
        bs = f.read()
    nonce = bs[:16]
    ciphertext = bs[16:-16]
    plain = _decrypt(key, nonce, ciphertext)
    mac = bs[-16:]
    _poly1305_validate(nonce, k, r, ciphertext, mac)
    return json.loads(plain)
