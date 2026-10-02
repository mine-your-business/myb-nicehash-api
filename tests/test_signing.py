import json

import pytest

from nicehash import NiceHashPrivateApi
from tests.conftest import load_fixture

SIGNING_FIXTURES = [
    'signing-docs-example-hashpower-orderbook.json',
    'signing-get-with-query.json',
    'signing-get-no-query.json',
    'signing-post-with-body.json',
]


@pytest.mark.parametrize('fixture_name', SIGNING_FIXTURES)
def test_build_headers_matches_fixture(fixture_name):
    fixture = load_fixture(fixture_name)
    creds = fixture['credentials']
    req = fixture['request']
    api = NiceHashPrivateApi('https://api2.nicehash.com', creds['organization_id'], creds['key'], creds['secret'])

    body_json = json.dumps(req['body']) if req['body'] else None
    headers = api.build_headers(
        req['method'], req['path'], req['query'], body_json,
        xtime=req['x_time'], xnonce=req['x_nonce'], request_id=req['request_id'],
    )

    assert headers == fixture['expected_headers']


def test_build_headers_generates_fresh_time_and_nonces():
    api = NiceHashPrivateApi('https://api2.nicehash.com', 'org', 'key', 'secret')

    first = api.build_headers('GET', '/main/api/v2/mining/miningAddress', '')
    second = api.build_headers('GET', '/main/api/v2/mining/miningAddress', '')

    assert first['X-Nonce'] != second['X-Nonce']
    assert first['X-Request-Id'] != second['X-Request-Id']
    assert int(first['X-Time']) <= int(second['X-Time'])
    assert first['X-Auth'].startswith('key:')


def test_epoch_ms_is_utc_milliseconds():
    import time

    api = NiceHashPrivateApi('https://api2.nicehash.com', 'org', 'key', 'secret')
    before = int(time.time() * 1000)
    now = api.get_epoch_ms_from_now()
    after = int(time.time() * 1000)

    assert before <= now <= after
