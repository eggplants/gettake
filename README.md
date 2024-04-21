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
