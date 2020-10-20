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


def test_get_release_rejected_status(mock_client):

    release_status = mock_client.get_release_status("Test_Project", 321, 123)
    assert release_status == "rejected"
