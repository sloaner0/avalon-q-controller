import pytest

from app.avalon_client import parse_stats, parse_summary


def test_parse_stats_reads_litestats_mm_blob(litestats_response):
    out = parse_stats(litestats_response)
    assert out["workmode"] == 1
    assert out["workmode_name"] == "standard"
    assert out["state"] == 1
    assert out["system_status"] == "Work: In Work, Hash Board: 1"
    assert out["temp_chassis"] == 25.0
    assert out["temp_max"] == 90.0
    assert out["temp_avg"] == 80.0
    assert out["fan_pct"] == 59.0
    assert out["load_w"] == 1301.0
    assert out["ths"] == pytest.approx(83.8377)
    assert out["pool_url"] is None


def test_parse_stats_empty_mm_blob_yields_none(empty_stats_response):
    out = parse_stats(empty_stats_response)
    assert out["workmode"] is None
    assert out["workmode_name"] is None
    assert out["state"] is None
    assert out["temp_max"] is None
    assert out["fan_pct"] is None
    assert out["load_w"] is None
    assert out["ths"] is None


def test_parse_stats_state_idle_maps_to_standby():
    blob = "'STATS':{Ver[X] STATE[2] WORKMODE[1]}"
    out = parse_stats({"STATS": [{"MM ID0:Summary": blob}]})
    assert out["state"] == 2
    assert out["workmode_name"] == "standby"


def test_parse_summary(summary_response):
    out = parse_summary(summary_response)
    assert out["elapsed_s"] == 440820
    assert out["mhs_av"] == 63677463.04
    assert out["mhs_5s"] == 96051745.88
    assert out["mhs_1m"] == 88242768.48
    assert out["accepted"] == 49867
    assert out["rejected"] == 150
    assert out["hardware_errors"] == 3


def test_parse_summary_missing_fields_yield_none():
    out = parse_summary({})
    assert out["elapsed_s"] is None
    assert out["mhs_av"] is None
    assert out["accepted"] is None