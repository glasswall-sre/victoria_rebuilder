import os

import pytest
from munch import munchify


def test_rebuild(mock_rebuild):
    assert mock_rebuild() is not None


def test_creates_save_file(mock_rebuild):
    mock_rebuild()._save()
    assert os.path.exists("rebuild")


def test_runs_if_inprogress(mock_rebuild):
    release = {
        "name": "Platform.Engine",
        "complete": False,
        "release_id": 1,
        "environment_id": 432,
    }
    releases = [munchify(release)]
    releases = mock_rebuild().run_releases(releases, "qa", "pent")

    assert releases


def test_wait_updates_release_complete(mock_rebuild):
    release = {
        "release_id": 321,
        "environment_id": 432,
        "name": "Test_release",
        "complete": False
    }
    releases = [munchify(release)]
    releases = mock_rebuild().wait_to_complete(releases, 1)

    assert releases[0].complete is True


def test_run_releases_removes_unfound(mock_rebuild):
    release = {
        "name": "Platform.IDontExist",
        "complete": False,
        "release_id": 0
    }
    releases = [munchify(release)]
    releases = mock_rebuild().run_releases(releases, "qa", "pent")

    assert not releases


def test_auto_retry_flag_false_asks_for_user_prompt(capsys, monkeypatch, mock_rebuild):

    release_name = 'Test_failed_release'

    release = {
        "release_id": 321,
        "environment_id": 321,
        "name": release_name,
        "complete": False
    }
    release = munchify(release)
    monkeypatch.setattr('builtins.input', lambda: "Y")
    run_again = mock_rebuild(auto_retry=False)._re_run_failed_release(release.release_id, release.environment_id,
                                                                      release.name)
    captured = capsys.readouterr()

    assert len(captured.out) > 0
    assert run_again


def test_auto_retry_flag_true_skips_user_prompt(capsys, monkeypatch, mock_rebuild):

    release = {
        "release_id": 321,
        "environment_id": 321,
        "name": "Test_failed_release",
        "complete": False
    }
    release = munchify(release)
    run_again = mock_rebuild(auto_retry=True)._re_run_failed_release(release.release_id, release.environment_id,
                                                                     release.name)
    captured = capsys.readouterr()

    assert len(captured.out) == 0
    assert run_again


def test_ask_failed_release_re_run_true(monkeypatch, mock_rebuild):
    release = {
        "release_id": 321,
        "environment_id": 321,
        "name": "Test_failed_release",
        "complete": False
    }
    release = munchify(release)

    monkeypatch.setattr('builtins.input', lambda: "Y")

    run_again = mock_rebuild()._re_run_failed_release(release.release_id, release.environment_id, release.name)

    assert run_again


def test_ask_failed_release_re_run_false(monkeypatch, mock_rebuild):
    release = {
        "release_id": 321,
        "environment_id": 321,
        "name": "Test_failed_release",
        "complete": False
    }
    release = munchify(release)

    monkeypatch.setattr('builtins.input', lambda: "N")

    run_again = mock_rebuild()._re_run_failed_release(release.release_id, release.environment_id, release.name)

    assert not run_again


def test_wait_failed_release_not_continue(monkeypatch, mock_rebuild):
    release = {
        "release_id": 321,
        "environment_id": 321,
        "name": "Test_release",
        "complete": False
    }
    releases = [munchify(release)]
    monkeypatch.setattr('builtins.input', lambda: "n")
    releases = mock_rebuild().wait_to_complete(releases, 1)

    assert len(releases) == 1
    assert releases[0].complete is True


def test_query_yes_no_invalid_default(monkeypatch, mock_rebuild):
    with pytest.raises(ValueError):
        mock_rebuild()._query_yes_no("What colour is the sky?", "blue")


def test_query_yes_no_returns_true(monkeypatch, mock_rebuild):
    monkeypatch.setattr('builtins.input', lambda: "Y")
    answer = mock_rebuild()._query_yes_no("What colour is the sky?")

    assert answer


def test_query_yes_no_returns_false(monkeypatch, mock_rebuild):
    monkeypatch.setattr('builtins.input', lambda: "n")
    answer = mock_rebuild()._query_yes_no("What colour is the sky?")

    assert not answer


def test_query_yes_no_valid_output(capsys, monkeypatch, mock_rebuild):
    monkeypatch.setattr('builtins.input', lambda: "y")

    _ = mock_rebuild()._query_yes_no("What colour is the sky?")
    captured = capsys.readouterr()
    assert captured.out == "What colour is the sky? [Y/n] "


def test_query_yes_no_invalid_output(monkeypatch, mock_rebuild):
    responses = iter(['dog', 'Y'])
    monkeypatch.setattr('builtins.input', lambda: next(responses))
    answer = mock_rebuild()._query_yes_no("What colour is the sky?")
    assert answer


def test_cleanup(mock_rebuild):
    mock_rebuild()._clean_up()

    assert not os.path.exists("rebuild")
