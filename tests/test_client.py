import os
import pytest

from nicehash import NiceHashPrivateApi

# TODO - This needs tests!!
# Nice Hash offers a test API which will need to be leveraged for
# this project https://test.nicehash.com/
# Mentioned here: https://www.nicehash.com/docs/

@pytest.fixture(scope='module')
def client():
    return None
    # return NiceHashPrivateApi(host, organisation_id, key, secret)


@pytest.mark.usefixtures('client')
class TestClient(object):

    def test(self, client):
        # TODO!
        assert True
