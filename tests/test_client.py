import json
from unittest import mock

import pytest

from nicehash import NiceHashPrivateApi, NiceHashPublicApi, NiceHashRigAction, NiceHashRigPowerMode
from tests.conftest import load_fixture

HOST = 'https://api2.nicehash.com'


def fake_response(status_code=200, payload=None, reason='OK'):
    response = mock.Mock()
    response.status_code = status_code
    response.reason = reason
    response.content = json.dumps(payload).encode() if payload is not None else b''
    response.json.return_value = payload
    return response


@pytest.fixture
def session_request():
    with mock.patch('nicehash.client.requests.Session.request') as patched:
        patched.return_value = fake_response(payload={})
        yield patched


@pytest.fixture
def private_api():
    return NiceHashPrivateApi(HOST, 'org-id', 'api-key', 'api-secret')


def sent_url(session_request):
    return session_request.call_args.args[1]


@pytest.mark.parametrize('case', load_fixture('private-endpoints.json'), ids=lambda c: c['call'])
def test_private_endpoint_contract(case, private_api, session_request):
    with mock.patch.object(private_api, 'build_headers', wraps=private_api.build_headers) as build_headers:
        getattr(private_api, case['call'])(**case['kwargs'])

    expected_url = HOST + case['path'] + ('?' + case['query'] if case['query'] else '')
    assert session_request.call_args.args[0] == case['method']
    assert sent_url(session_request) == expected_url

    expected_body = case.get('body')
    signed_method, signed_path, signed_query, signed_body = build_headers.call_args.args
    assert (signed_method, signed_path, signed_query) == (case['method'], case['path'], case['query'])
    if expected_body is None:
        assert signed_body is None
        assert 'data' not in session_request.call_args.kwargs
    else:
        assert json.loads(signed_body) == expected_body
        assert session_request.call_args.kwargs['data'] == signed_body


def test_request_sends_signed_headers_and_parses_json(private_api):
    accounts = load_fixture('accounts2-response.json')

    with mock.patch('nicehash.client.requests.Session.request', autospec=True) as patched:
        patched.return_value = fake_response(payload=accounts)
        result = private_api.get_accounts()

    session = patched.call_args.args[0]
    assert result == accounts
    assert session.headers['X-Organization-Id'] == 'org-id'
    assert session.headers['X-Auth'].startswith('api-key:')
    assert session.headers['Content-Type'] == 'application/json'


def test_request_raises_with_status_and_body_on_error(private_api, session_request):
    error = load_fixture('error-401-invalid-session.json')
    session_request.return_value = fake_response(401, error, reason='Unauthorized')

    with pytest.raises(Exception) as excinfo:
        private_api.get_accounts()

    assert str(excinfo.value).startswith('401: Unauthorized: ')
    assert 'Invalid session (1007)' in str(excinfo.value)


def test_request_raises_with_status_when_body_empty(private_api, session_request):
    session_request.return_value = fake_response(503, None, reason='Service Unavailable')

    with pytest.raises(Exception, match=r'^503: Service Unavailable$'):
        private_api.get_accounts()


def test_rig_action_power_mode(private_api, session_request):
    private_api.rig_action('rig-1', 'dev-1', NiceHashRigAction.POWER_MODE, NiceHashRigPowerMode.LOW, group='g')

    assert sent_url(session_request) == HOST + '/main/api/v2/mining/rigs/status2'
    assert json.loads(session_request.call_args.kwargs['data']) == {
        'rigId': 'rig-1',
        'deviceId': 'dev-1',
        'action': 'POWER_MODE',
        'group': 'g',
        'options': ['LOW'],
    }


def test_hashpower_order_uses_algorithm_market_factors(private_api, session_request):
    algo_response = {'miningAlgorithms': [
        {'algorithm': 'SCRYPT', 'marketFactor': '1000000000000', 'displayMarketFactor': 'TH'},
        {'algorithm': 'SHA256', 'marketFactor': '1000000000000000', 'displayMarketFactor': 'PH'},
    ]}

    private_api.create_hashpower_order('EU', 'STANDARD', 'SCRYPT', '0.01', '1', '0.005', 'pool-1', algo_response)

    assert sent_url(session_request) == HOST + '/main/api/v2/hashpower/order/'
    body = json.loads(session_request.call_args.kwargs['data'])
    assert body['marketFactor'] == '1000000000000'
    assert body['displayMarketFactor'] == 'TH'


def test_hashpower_order_rejects_unknown_algorithm(private_api, session_request):
    with pytest.raises(Exception, match='Settings for algorithm not found'):
        private_api.set_price_hashpower_order('order-1', '0.01', 'X16R', {'miningAlgorithms': []})
    session_request.assert_not_called()


def test_public_api_returns_parsed_json(session_request):
    markets = load_fixture('public-mining-markets.json')
    session_request.return_value = fake_response(payload=markets)

    result = NiceHashPublicApi(HOST).get_markets()

    assert result == markets
    assert session_request.call_args.args == ('GET', HOST + '/main/api/v2/mining/markets/')


@pytest.mark.parametrize('call, kwargs, url', [
    ('get_active_orders', {}, '/main/api/v2/public/orders'),
    ('get_active_orders', {'algorithm': 'SCRYPT', 'market': 'EU'}, '/main/api/v2/public/orders?algorithm=SCRYPT&market=EU'),
    ('get_active_orders2', {'algorithm': 'SCRYPT'}, '/main/api/v2/public/orders/active2/?algorithm=SCRYPT'),
    ('get_exchange_trades', {'market': 'BTCUSDT'}, '/exchange/api/v2/info/trades?market=BTCUSDT'),
    ('get_candlesticks', {'market': 'BTCUSDT', 'from_s': 1, 'to_s': 2, 'resolution': 60},
     '/exchange/api/v2/info/candlesticks?market=BTCUSDT&from=1&to=2&resolution=60'),
])
def test_public_endpoint_paths(call, kwargs, url, session_request):
    getattr(NiceHashPublicApi(HOST), call)(**kwargs)

    assert sent_url(session_request) == HOST + url
