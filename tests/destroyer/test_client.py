import pytest


def test_api_release_client_is_setup(mock_client):
    assert mock_client.release_client is not None


def test_get_latest_successful_release_qa_pent(mock_client):
    result = mock_client.get_latest_successful_release(
        "Platform.Infrastructure", "qa", "pent")

    assert result == (123, 321)


def test_get_latest_successful_release_pent_qa(mock_client):
    result = mock_client.get_latest_successful_release(
        "Platform.Infrastructure", "pent", "qa")

    assert result == (123, 456)


def test_release_complete_exit(mock_client):

    try:
        mock_client.is_release_complete("Test_Project", 321, 123)
        assert (False)
    except SystemExit:
        pass

    assert (True)
