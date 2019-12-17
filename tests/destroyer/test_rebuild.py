import pytest
import os


def test_rebuild(mock_rebuild):
    assert mock_rebuild is not None


def test_creates_save_file(mock_rebuild):
    mock_rebuild._save()
    assert os.path.exists("rebuild")


def test_loads_save_file(mock_rebuild):
    mock_rebuild._load()

    assert True


def test_cleanup(mock_rebuild):
    mock_rebuild._clean_up()

    assert not os.path.exists("rebuild")
