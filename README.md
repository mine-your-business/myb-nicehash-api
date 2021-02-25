# myb-nicehash-api
 An API client for the NiceHash API

## Installation

The package is availble via PyPi and can be installed with the following command:
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

## Testing

To run tests, simply run the following command:

```
pytest --verbose
```

## Releases

Releases should follow a [Semantic Versioning](https://semver.org/) scheme. 

When changes have been made that warrant a new release that should be published, modify the `__version__` in [`setup.py`](setup.py) 

After the change is merged to the `main` branch, go to [releases](https://github.com/mine-your-business/myb-nicehash-api/releases) and `Draft a new release`. The `Tag version` should follow the pattern `v1.0.0` and should `Target` the `main` branch. 

The `Release title` should not include the `v` from the tag and should have a reasonably detailed description of the new release's changes. 

Once the release has been published, the [`.github/workflows/python-publish.yml`](.github/workflows/python-publish.yml) GitHub Actions Workflow should trigger and automatically upload the new version to [PyPi](https://pypi.org/) using GitHub secrets credentials stored with the [Mine Your Business GitHub Organization](https://github.com/mine-your-business).
