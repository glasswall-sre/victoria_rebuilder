from collections import namedtuple

import pytest

import destroyer.release


def test_api_connection(mock_api):
    assert mock_api.connection is not None
    assert mock_api.credentials is not None
    assert mock_api.release_client is not None
