from unittest.mock import patch

import pytest

from clove.exceptions import ExternalApiRequestLimitExceeded
from clove.utils.external_source import clove_req_json


class FakeResponseOk:
    status_code = 200

    def json(self):
        return {'abc': 123}


class FakeResponseLimitExceeded:
    status_code = 429


@patch('requests.get')
def test_clove_req_json_ok(request_mock):
    request_mock.return_value = FakeResponseOk()

    data = clove_req_json('https://testnet.blockexplorer.com/api/status?q=getInfo')
    assert data == {'abc': 123}


@patch('requests.get')
def test_clove_req_json_limit(request_mock):
    request_mock.return_value = FakeResponseLimitExceeded()

    with pytest.raises(ExternalApiRequestLimitExceeded):
        clove_req_json('https://testnet.blockexplorer.com/api/status?q=getInfo')
