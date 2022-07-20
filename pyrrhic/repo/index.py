import json

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


def get_index(path: str, key: MasterKey) -> dict[str, dict]:
    with open(path, "rb") as f:
        bs = f.read()
        plain = decrypt_mac(key, bs)
    return json.loads(plain)
