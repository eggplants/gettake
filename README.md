# gettake

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
[+] Target:     https://webcomicgamma.takeshobo.co.jp/manga/madeinabyss/
[+] Host:       webcomicgamma.takeshobo.co.jp
[+] Slug:       madeinabyss
[+] 0074 chapter(s) found!
...
[+] Done!

$ tree -dL 1 ./madeinabyss
madeinabyss
├── 001
├── 002
...
└── 067
74 directories
```

## Help

```shellsession
$ gettake -h
usage: gettake [-h] [-d DIR] [-o] [-V] url

Get and save images from webcomicgamma.

positional arguments:
  url                    target url

options:
  -h, --help             show this help message and exit
  -d DIR, --save-dir DIR
                         directory to save downloaded images (default: .)
  -o, --overwrite        overwrite (default: False)
  -V, --version          show program's version number and exit

available urls:
  - https://webcomicgamma.takeshobo.co.jp
```

## License

MIT
