# Restic implementation in Python

[![image](https://github.com/juergenhoetzel/pyrrhic/workflows/main/badge.svg?branch=master)](https://github.com/juergenhoetzel/pyrrhic/actions?workflow=main)
[![image](https://codecov.io/gh/juergenhoetzel/pyrrhic/branch/master/graph/badge.svg)](https://codecov.io/gh/juergenhoetzel/pyrrhic)
## Pre-Alpha Relase

All cat commands implemented.
```bash
pyrrhic --repo restic_test_repositories/restic_test_repository cat masterkey

```

```
{'encrypt': 'Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E=',
 'mac': {'k': 'aSbwRFL8rIOOxL4W+mAW1w==', 'r': 'hQYBDSD/JwpU8XMDIJmAAg=='}}
```
## Additional features missing in golang restic implementation

- pretty-print all objects
- `pyrrhic cat pack SNAPSHOT_ID --header` prints parsed header

## Why is it called pyrrhic

Needed a name starting with `py` containing `r` and ending with `ic`:

```bash
grep ^py.*r.*ic$ /usr/share/dict/cracklib-small
```

## Limitations

- Supports repository format version 2 only (current restic version).
