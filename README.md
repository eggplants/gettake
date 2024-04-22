# gettake

[![PyPI version](
  <https://badge.fury.io/py/gettake.svg>
  )](
  <https://badge.fury.io/py/gettake>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/659f70e5eb40b4eb5ab4/maintainability>
  )](
  <https://codeclimate.com/github/eggplants/gettake/maintainability>
) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/gettake/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/gettake/master>
) [![Test Coverage](
  <https://api.codeclimate.com/v1/badges/659f70e5eb40b4eb5ab4/test_coverage>
  )](
  <https://codeclimate.com/github/eggplants/gettake/test_coverage>
) [![Test](
  <https://github.com/eggplants/gettake/actions/workflows/test.yml/badge.svg>
  )](
  <https://github.com/eggplants/gettake/actions/workflows/test.yml>
)

[![ghcr latest](
  <https://ghcr-badge.deta.dev/eggplants/gettake/latest_tag?trim=major&label=latest>
 ) ![ghcr size](
  <https://ghcr-badge.deta.dev/eggplants/gettake/size>
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

$ tree -dL 1 ./madeinabyss
```

## Help

```shellsession
$ gettake -h
```

## License

MIT
