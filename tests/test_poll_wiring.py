from unittest.mock import Mock

from app.avalon_client import AvalonClient
from app.controller import Controller
from app.db import DB


def _make_controller(tmp_path):
    db = DB(tmp_path / "controller.db")
    miner = db.create_miner(name="Q", host="192.0.2.1")
    return Controller(db), miner


def test_poll_sync_reads_telemetry_from_litestats_not_stats(
    tmp_path,
    monkeypatch,
    litestats_response,
    empty_stats_response,
    summary_response,
    pools_response,
):
    controller, miner = _make_controller(tmp_path)

    stats_mock = Mock(return_value=empty_stats_response)
    litestats_mock = Mock(return_value=litestats_response)
    summary_mock = Mock(return_value=summary_response)
    pools_mock = Mock(return_value=pools_response)

    monkeypatch.setattr(AvalonClient, "stats", stats_mock)
    monkeypatch.setattr(AvalonClient, "litestats", litestats_mock)
    monkeypatch.setattr(AvalonClient, "summary", summary_mock)
    monkeypatch.setattr(AvalonClient, "pools", pools_mock)

    status = controller._poll_sync(miner.id)

    # The regression this pins: the poll loop must read the MM telemetry from
    # ``litestats`` (populated), never from ``stats`` (empty on Avalon Q).
    stats_mock.assert_not_called()
    litestats_mock.assert_called_once()

    assert status["online"] is True
    assert status["stats"]["workmode"] == 1
    assert status["stats"]["workmode_name"] == "standard"
    assert status["stats"]["load_w"] == 1301.0
    assert status["stats"]["temp_max"] == 90.0
    assert status["stats"]["fan_pct"] == 59.0
    assert status["stats"]["pool_url"] == "stratum+tcp://pool.example.com:3333"