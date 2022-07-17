import pytest
from pyrrhic.crypto.keys import load_key, get_masterkey, MasterKey, WrappedKey, Mac
from base64 import b64decode

# FIXME: Hardcoded
KEYFILE = "restic_test_repositories/restic_test_repository/keys/98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"  # noqa: E501


def test_load_key():
    key = load_key(KEYFILE)
    assert type(key) == WrappedKey


def test_get_masterkey():
    masterkey = get_masterkey(KEYFILE, b"password")
    assert masterkey == MasterKey(
        mac=Mac(
            k=b64decode("aSbwRFL8rIOOxL4W+mAW1w=="),
            r=b64decode("hQYBDSD/JwpU8XMDIJmAAg=="),
        ),
        encryption=b64decode("Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E="),
    )


def test_get_masterkey_with_invalid_password():
    with pytest.raises(ValueError):
        get_masterkey(KEYFILE, b"password2")
