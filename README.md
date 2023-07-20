<!-- markdownlint-disable -->
<p align="center">
  <img src="docs/images/SVG/Transparent/logo-thin.svg#gh-light-mode-only" alt="NIAPI Logo - Light" width="100%" height="auto" />
  <img src="docs/images/SVG/Transparent/logo-dark-thin.svg#gh-dark-mode-only" alt="NIAPI Logo - Dark" width="100%" height="auto" />
</p>
<!-- markdownlint-restore -->

<div align="center">

<!-- prettier-ignore-start -->

| Project   |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|-----------|:----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD     |     | [![Latest Release](https://github.com/JacobCoffee/niapi/actions/workflows/publish.yaml/badge.svg)](https://github.com/JacobCoffee/niapi/actions/workflows/publish.yaml) [![ci](https://github.com/JacobCoffee/niapi/actions/workflows/ci.yaml/badge.svg)](https://github.com/JacobCoffee/niapi/actions/workflows/ci.yaml) [![Documentation Building](https://github.com/JacobCoffee/niapi/actions/workflows/docs.yaml/badge.svg)](https://github.com/JacobCoffee/niapi/actions/workflows/docs.yaml) [![CodeQL](https://github.com/JacobCoffee/niapi/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/JacobCoffee/niapi/actions/workflows/github-code-scanning/codeql)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Package   |     | [![PyPI - Version](https://img.shields.io/pypi/v/niapi)](https://badge.fury.io/py/niapi) ![PyPI - Support Python Versions](https://img.shields.io/pypi/pyversions/niapi)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Quality   |     | [![codecov](https://codecov.io/gh/JacobCoffee/niapi/branch/main/graph/badge.svg?token=SFT67X4MEQ)](https://codecov.io/gh/JacobCoffee/niapi) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=JacobCoffee_niapi&metric=coverage)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=JacobCoffee_niapi&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=JacobCoffee_niapi&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=JacobCoffee_niapi&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=JacobCoffee_niapi&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi) [![Known Vulnerabilities](https://snyk.io/test/github/JacobCoffee/niapi/badge.svg)](https://snyk.io/test/github/JacobCoffee/niapi) |
| Community |     | [![Twitter](https://img.shields.io/twitter/follow/_scriptr?style=social&logo=twitter)](https://twitter.com/_scriptr)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Meta      |     | [![Litestar Framework](https://img.shields.io/badge/Litestar%20Framework-%E2%AD%90%20Litestar-202235.svg)](https://github.com/JacobCoffee/niapi) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-85c7f2.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-85c7f2.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/JacobCoffee?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/JacobCoffee)                                                                                                                                                                                                                                                                                                                                                                                                        |

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=JacobCoffee_niapi)

<!-- prettier-ignore-end -->

</div>

# `niapi` - Network Information API

[//]: # "TODO"

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Screenshots](#screenshots)

## About

[//]: # "TODO"

## Installation

```console
pip install niapi
```

## Usage

[//]: # "TODO"

Install the project:

```console
pip install -e .
```

Run the project:

> **NOTE:** From within the virtual environment

```console
app run -r --debug
```

Using the CLI:

```console
# via curl
➜ curl --request GET \
        --url 'http://0.0.0.0:8000/calculator/ip?ip=4.8.15.16&prefix=23' \
        --header 'Content-Type: application/json'
# via App CLI
# TODO
app calculate "10.248.15.39/29"
```

Using the API

1. Browse to:
   - [Swagger](http://127.0.0.1:8000/api/swagger#/)
   - [Elements](http://127.0.0.1:8000/api/elements/)
2. Use the auto-generated API docs to interact with the API

From around the web:

Browse to https://niapi.app/ and use the front page form, API, or `curl`
to interact with the API.

## Contributing

See [CONTRIBUTING.rst](CONTRIBUTING.rst) for more information.

Start the app:

```console
app run-all
```

Start the TailwindCSS watcher:

```console
tailwindcss -i niapi/domain/web/resources/input.css -o niapi/domain/web/resources/style.css --watch
```

## Contributors

[//]: # "TODO"

## License

[MIT](LICENSE)

## Acknowledgements

- Built on Litestar and Pydantic
- Using https://feathericons.dev/
- Using TailwindCSS

## Screenshots

[//]: # "TODO"

![home.png](docs/images/index.png)
![home-dark.png](docs/images/index-dark.png)
![img.png](docs/images/output.png)
