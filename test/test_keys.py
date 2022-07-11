import pytest
from pyrrhic.keys import load_key, get_masterkey, Key


# FIXME: Hardcoded
KEYFILE = "restic_test_repository/keys/98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"


def test_load_key():
    key = load_key(KEYFILE)
    assert type(key) == Key


def test_get_masterkey():
    masterkey = get_masterkey(KEYFILE, b"password")
    assert type(masterkey) == dict
    assert masterkey == {
        "mac": {"k": "aSbwRFL8rIOOxL4W+mAW1w==", "r": "hQYBDSD/JwpU8XMDIJmAAg=="},
        "encrypt": "Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E=",
    }


def test_get_masterkey_with_invalid_password():
    with pytest.raises(ValueError):
        get_masterkey(KEYFILE, b"password2")
