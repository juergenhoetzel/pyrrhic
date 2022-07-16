# Restic implementation in Python

[![image](https://github.com/juergenhoetzel/pyrrhic/workflows/main/badge.svg?branch=master)](https://github.com/juergenhoetzel/pyrrhic/actions?workflow=main)
[![image](https://codecov.io/gh/juergenhoetzel/pyrrhic/branch/master/graph/badge.svg)](https://codecov.io/gh/juergenhoetzel/pyrrhic)
## Pre-Alpha Relase

Not much here yet.

You can just `cat` the masterkey:
```bash
pyrrhic masterkey restic_test_repository/keys/98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb 

```

```
{'encrypt': 'Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E=',
 'mac': {'k': 'aSbwRFL8rIOOxL4W+mAW1w==', 'r': 'hQYBDSD/JwpU8XMDIJmAAg=='}}
```

Don't use this in production.

## Why is it called pyrrhic

Needed a name starting with `py` containing `r` and ending with `ic`:

```bash
grep ^py.*r.*ic$ /usr/share/dict/cracklib-small
```

## Limitations

- Supports repository format version 2 only (current restic version).
