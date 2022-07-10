import json
from pydantic import BaseModel
from datetime import datetime
from base64 import b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import poly1305
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms

# mask for key, (cf. http://cr.yp.to/mac/poly1305-20050329.pdf)
_POLY1305KEYMASK = b"\xff\xff\xff\x0f\xfc\xff\xff\x0f\xfc\xff\xff\x0f\xfc\xff\xff\x0f"


class Key(BaseModel):
    """Class that contain all data that is needed to derive the repository's master encryption and message authentication keys from a user's password.."""

    hostname: str
    username: str
    kdf: str
    N: int
    r: int
    p: int
    created: datetime
    data: bytes
    salt: bytes


def load_key(key_path: str) -> Key:
    with open(key_path, "r") as f:
        j = json.load(f)
        # FIXME: This should by done using pydantic
        j["salt"] = b64decode(j["salt"])
        j["data"] = b64decode(j["data"])
        return Key(**j)


def _decrypt(aes_key: bytes, nonce: bytes, ciphertext: bytes):
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


def get_masterkey(key: Key, password: bytes):
    kdf = Scrypt(key.salt, 64, key.N, key.r, key.p, backend=default_backend)
    derived_key = kdf.derive(password)
    poly_k = derived_key[32:48]
    poly_r = derived_key[48:]
    nonce = key.data[:16]
    message = key.data[16:-16]
    mac = key.data[-16:]
    _poly1305_validate(nonce, poly_k, poly_r, message, mac)

    return json.loads(_decrypt(derived_key[:32], nonce, message))
