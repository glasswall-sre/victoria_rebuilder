import pytest
import os
from munch import munchify


def test_rebuild(mock_rebuild):
    assert mock_rebuild is not None


def test_creates_save_file(mock_rebuild):
    mock_rebuild._save()
    assert os.path.exists("rebuild")


def test_loads_save_file(mock_rebuild):
    mock_rebuild._load()

    assert True


def test_wait_updates_release_complete(mock_rebuild):
    release = {
        "release_id": 321,
        "environment_id": 432,
        "name": "Test_release",
        "complete": False
    }
    releases = [munchify(release)]
    releases = mock_rebuild.wait_to_complete(releases, 1)

    assert releases[0].complete == True


def test_run_releases_removes_unfound(mock_rebuild):
    release = {
        "name": "Platform.IDontExist",
        "complete": False,
        "release_id": 0
    }
    releases = [munchify(release)]
    releases = mock_rebuild.run_releases(releases, "pent")

    assert not releases


def test_cleanup(mock_rebuild):
    mock_rebuild._clean_up()

    assert not os.path.exists("rebuild")
