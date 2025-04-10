# gettake

[![PyPI version](
  <https://badge.fury.io/py/gettake.svg>
  )](
  <https://badge.fury.io/py/gettake>
) [![Maintainability](
  <https://qlty.sh/badges/4d764657-5fa2-45b7-b86d-9e9feed55c3e/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/gettake>
) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/gettake/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/gettake/master>
) [![Code Coverage](
  <https://qlty.sh/badges/4d764657-5fa2-45b7-b86d-9e9feed55c3e/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/gettake>
) [![Test](
  <https://github.com/eggplants/gettake/actions/workflows/test.yml/badge.svg>
  )](
  <https://github.com/eggplants/gettake/actions/workflows/test.yml>
)

[![ghcr latest](
  <https://ghcr-badge.egpl.dev/eggplants/gettake/latest_tag?trim=major&label=latest>
 ) ![ghcr size](
  <https://ghcr-badge.egpl.dev/eggplants/gettake/size>
)](
  <https://github.com/eggplants/gettake/pkgs/container/gettake>
)

Get and save images from [webcomicgamma](https://webcomicgamma.takeshobo.co.jp)

_Note: Redistribution of downloaded image data is prohibited. Please keep it to private use._

## Install

```bash
pip install gettake
```

OR:

```bash
pipx install gettake
```

## Run

```shellsession
$ gettake https://webcomicgamma.takeshobo.co.jp/manga/madeinabyss/
[+] Target: https://webcomicgamma.takeshobo.co.jp/manga/madeinabyss/
[+] Host:   webcomicgamma.takeshobo.co.jp
[+] Slug:   madeinabyss
[+] 0072 chapter(s) found!
[-] Now: '001' [0001 / 0072] .....saved!
[-] Now: '002' [0002 / 0072] .....saved!
[-] Now: '003' [0003 / 0072] .....saved!
...
[+] Done!

$ tree -dL 1 ./madeinabyss
./madeinabyss
├── 001
├── 002
├── 003
...
└── 067

73 directories
```

## Help

```shellsession
$ gettake -h
usage: gettake [-h] [-d DIR] [-o] [-q] [-V] url

Get and save images from webcomicgamma.

positional arguments:
  url                    target url

options:
  -h, --help             show this help message and exit
  -d DIR, --save-dir DIR
                         directory to save downloaded images (default: .)
  -o, --overwrite        overwrite (default: False)
  -q, --quiet            keep stdout quiet (default: False)
  -V, --version          show program's version number and exit

available urls:
  - https://webcomicgamma.takeshobo.co.jp
```

## License

MIT
