from base64 import b64decode

from pyrrhic.crypto.keys import (
    Mac,
    MasterKey,
    WrappedKey,
    get_config,
    get_masterkey,
    load_key,
)

import pytest

REPO_BASE = "restic_test_repositories"
KEY = "98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"
KEYFILE = f"{REPO_BASE}/restic_test_repository/keys/{KEY}"  # noqa: E501
BROKEN_REPO = f"{REPO_BASE}/restic_broken_test_repository"


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


def test_config_with_invalid_mac():
    masterkey = get_masterkey(KEYFILE, b"password")
    with pytest.raises(ValueError, match="ciphertext verification failed"):
        get_config(masterkey, f"{BROKEN_REPO}/config")
