# myb-nicehash-api
 A Python client for the [NiceHash API](https://www.nicehash.com/docs/rest).

## Requirements

Python 3.11 or newer (tested on 3.11 through 3.14).

## Installation

The package is available via PyPI and can be installed with the following command:
```
pip3 install myb-nicehash-api
```

To install it from the repo, clone the repo and cd into the directory:

```
git clone https://github.com/mine-your-business/myb-nicehash-api.git
cd myb-nicehash-api
```

You can install this library with `pip`:

```
pip3 install .
```

## Usage

```python
from nicehash import NiceHashPrivateApi, NiceHashPublicApi

public_api = NiceHashPublicApi('https://api2.nicehash.com')
markets = public_api.get_markets()

private_api = NiceHashPrivateApi('https://api2.nicehash.com', organization_id, api_key, api_secret)
accounts = private_api.get_accounts(fiat='USD')
```

API keys are created in the NiceHash dashboard under API Keys. The request signing follows the
[NiceHash REST API documentation](https://www.nicehash.com/docs/rest).

## Testing

Install the development dependencies and run the linter and tests:

```
pip3 install -r requirements-dev.txt -e .
flake8 .
pytest --verbose
```

The unit tests run offline against recorded fixtures in [`tests/fixtures`](tests/fixtures).
Live smoke tests in [`tests/test_live.py`](tests/test_live.py) are skipped by default:

- `NICEHASH_LIVE=1` runs the unauthenticated public API checks.
- `NICEHASH_ORG_ID`, `NICEHASH_API_KEY` and `NICEHASH_API_SECRET` run the private API checks (use a read-only key).
  `NICEHASH_HOST` overrides the host, for example `https://api-test.nicehash.com`.

## Releases

Releases should follow a [Semantic Versioning](https://semver.org/) scheme.

When changes have been made that warrant a new release that should be published, modify the `__version__` in [`setup.py`](setup.py) 

After the change is merged to the `main` branch, go to [releases](https://github.com/mine-your-business/myb-nicehash-api/releases) and `Draft a new release`. The `Tag version` should follow the pattern `v1.0.0` and should `Target` the `main` branch. 

The `Release title` should not include the `v` from the tag and should have a reasonably detailed description of the new release's changes.

Once the release has been published, the [`.github/workflows/python-publish.yml`](.github/workflows/python-publish.yml) GitHub Actions Workflow builds the package and uploads it to [PyPI](https://pypi.org/project/myb-nicehash-api/) using [trusted publishing](https://docs.pypi.org/trusted-publishers/). No API token is stored in GitHub; the PyPI project must have a trusted publisher configured for repository `mine-your-business/myb-nicehash-api`, workflow `python-publish.yml` and environment `pypi`.
