import os
from pyrrhic.crypto.keys import get_masterkey


def get_dir_masterkey(keys_dir: str, password: str):
    last_err = None
    for kf in os.listdir(keys_dir):
        try:
            masterkey = get_masterkey(
                os.path.join(keys_dir, kf), password.encode("utf8")
            )
            return masterkey
        except ValueError as err:
            last_err = err
    raise last_err
