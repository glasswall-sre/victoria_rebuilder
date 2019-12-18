import pytest


def test_api_release_client_is_setup(mock_client):
    assert mock_client.release_client is not None


def test_get_latest_release(mock_client):
    result = mock_client.get_latest_release("Platform.Infrastructure", "pent")

    assert result == (123, 321)


def test_release_complete_exit(mock_client):

    try:
        mock_client.is_release_complete("Test_Project", 321, 123)
        assert (False)
    except SystemExit:
        pass

    assert (True)
