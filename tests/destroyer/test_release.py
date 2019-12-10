from collections import namedtuple

import pytest

import destroyer.release


def test_api_release_client_is_setup(mock_client):
    assert mock_client.release_client is not None


def test(mock_client):
    result = mock_client.get_latest_release()

    assert result == (123, 321)