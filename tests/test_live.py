"""Live smoke tests against the real NiceHash API.

Skipped unless the relevant environment variables are set:

- NICEHASH_LIVE=1 enables the unauthenticated public-API checks.
- NICEHASH_ORG_ID, NICEHASH_API_KEY and NICEHASH_API_SECRET enable the private-API checks
  (use a read-only key). NICEHASH_HOST overrides the host, e.g. https://api-test.nicehash.com.
"""
import os

import pytest

from nicehash import NiceHashPrivateApi, NiceHashPublicApi

HOST = os.environ.get('NICEHASH_HOST', 'https://api2.nicehash.com')
PRIVATE_ENV = ('NICEHASH_ORG_ID', 'NICEHASH_API_KEY', 'NICEHASH_API_SECRET')

live_public = pytest.mark.skipif(os.environ.get('NICEHASH_LIVE') != '1', reason='set NICEHASH_LIVE=1 to run')
live_private = pytest.mark.skipif(
    not all(os.environ.get(name) for name in PRIVATE_ENV),
    reason='set ' + ', '.join(PRIVATE_ENV) + ' to run',
)


@live_public
def test_public_markets():
    assert 'EU' in NiceHashPublicApi(HOST).get_markets()


@live_public
def test_public_algorithms():
    assert NiceHashPublicApi(HOST).get_algorithms()['miningAlgorithms']


@live_private
def test_private_accounts():
    api = NiceHashPrivateApi(
        HOST,
        os.environ['NICEHASH_ORG_ID'],
        os.environ['NICEHASH_API_KEY'],
        os.environ['NICEHASH_API_SECRET'],
    )
    assert 'currencies' in api.get_accounts()
