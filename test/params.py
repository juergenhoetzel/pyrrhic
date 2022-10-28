from pathlib import Path

from pyrrhic.repo.repository import Repository, get_masterkey

params = [
    {
        "repo": Repository(
            Path("restic_test_repositories/restic_test_repository"), get_masterkey(Path("restic_test_repositories/restic_test_repository"), "password")
        ),
        "config": {"chunker_polynomial": "3833148ec41f8d", "id": "2ec6792a9c75a017ec4665a5e7733f45f8bffb67c7d0f3c9ec6cc96e58c6386b", "version": 1},
        "masterkey": {"mac": {"r": "hQYBDSD/JwpU8XMDIJmAAg==", "k": "aSbwRFL8rIOOxL4W+mAW1w=="}, "encrypt": "Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E="},
        "snapshot_id": "dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c",
        "snapshot_json": {
            "time": "2022-07-19T19:52:28.692252Z",
            "tree": "a5dbcc77f63f5dd4f4c67c988aba4a19817aaa9d6c34a6021236a5d40ce653e1",
            "paths": ["/home/juergen/shared/python/pyrrhic/test"],
            "hostname": "shaun",
            "username": "juergen",
            "id": "dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c",
            "uid": 1000,
            "gid": 1000,
            "excludes": None,
            "tags": None,
        },
        "snapshot_cracklib": "d2bbc914",
        "index_id": "bd10c8e85d2cdc3267faae1748cf7a334385d021766059580976882556097c0d",
        "index_substr": """'511d1c632ccad135d5407157154eccc17fcfaf501ad252b231c7ce41175473b9': PackRef(
        id='46771395523ccd6dda16694f0ce775f9508a4c3e4527c385f55d8efafa36807f'""",
        "pack_id": "4b24375f07a164e995d06303bfc26f79f94127e4e5c6e1c476495bbee0af7ccc",
        "pack_blobs": [
            {"id": "82deec86c5611cb5ae02b967e49d7aeaca50a732432bd1a5923787bd5d0fbf80", "length": 1643, "offset": 0},
            {"id": "e20d6400fbd4e602c79c8bab98a88726865b168838cc8107d560da10f19b2ff8", "length": 1467, "offset": 1643},
            {"id": "a5dbcc77f63f5dd4f4c67c988aba4a19817aaa9d6c34a6021236a5d40ce653e1", "length": 413, "offset": 3110},
        ],
    },
    {
        "repo": Repository(
            Path("restic_test_repositories/restic_v2_test_repository"), get_masterkey(Path("restic_test_repositories/restic_v2_test_repository"), "password")
        ),
        "config": {"version": 2, "id": "2c5d1276aa6f58c06883c2a7a2aef35c86ec4a0b57a6ded80e08de3fedc108f8", "chunker_polynomial": "232a535caedb65"},
        "masterkey": {"mac": {"r": "2iQMCQDOPw1UtW0N1C4RAA==", "k": "zpL4Veh3FhT7grSgm0BmCQ=="}, "encrypt": "193cMViwx7TJFtykWOZzEKojzp0fjx4VvaiJ6yMgZ3E="},
        "snapshot_id": "4d9c1f",
        "snapshot_json": {
            "time": "2022-10-18T04:53:22.965183Z",
            "tree": "9178aa841c9fd277478925c7864da28e4500ce236ad89a0ff9a261b1dabbda42",
            "paths": ["/usr/share/cracklib"],
            "hostname": "shaun",
            "username": "juergen",
            "id": "4d9c1f12d69290f6c3cc8984ef08b8e17b233fddc1bb1b0b2f9a669620f17a59",
            "uid": 1000,
            "gid": 1000,
            "excludes": None,
            "tags": None,
        },
        "snapshot_cracklib": "78102f",
        "index_id": "2cd9a598873e58bcb067b1d3f6db488047a2bc168da7550b8340c319f0693d8a",
        "index_substr": """'8696358373607539e46c42a13955e343cd1d66a45b102c3ccf41b5e38d4b1db1': PackRef(
        id='7c42983e65e74be3911ab1c9177e10128bce39d0c29033a2db9de4a6810d0711'""",
        "pack_id": "ed505dcfdd8b9c7cb912be91bc19b711279253e37358f70af65466c92816febb",
        "pack_blobs": [
            {"id": "8072950e2d305ebcfd94912557e06b6a9e1a7ee487470e4d89efd34e749a2505", "offset": 0, "length": 621, "length_uncompressed": 2197},
            {"id": "25fec2e636c582064ea0927886a93acca579ab1436b01311f18c10776aa70fa4", "offset": 621, "length": 256, "length_uncompressed": 373},
            {"id": "b9c28d59a52a1c5406637280aff6f63195fc9dac603d3e070fbd884aaddb6b5f", "offset": 877, "length": 255, "length_uncompressed": 370},
            {"id": "9178aa841c9fd277478925c7864da28e4500ce236ad89a0ff9a261b1dabbda42", "offset": 1132, "length": 253, "length_uncompressed": 368},
        ],
    },
]
