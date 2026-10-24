from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from app.scheduler import Rule, Schedule, _date_in_season, _time_in_window


def test_time_in_window_normal():
    assert _time_in_window(time(9, 0), time(9, 0), time(17, 0)) is True
    assert _time_in_window(time(16, 59), time(9, 0), time(17, 0)) is True
    assert _time_in_window(time(17, 0), time(9, 0), time(17, 0)) is False
    assert _time_in_window(time(8, 59), time(9, 0), time(17, 0)) is False


def test_time_in_window_overnight():
    assert _time_in_window(time(22, 0), time(22, 0), time(6, 0)) is True
    assert _time_in_window(time(23, 0), time(22, 0), time(6, 0)) is True
    assert _time_in_window(time(3, 0), time(22, 0), time(6, 0)) is True
    assert _time_in_window(time(6, 0), time(22, 0), time(6, 0)) is False
    assert _time_in_window(time(12, 0), time(22, 0), time(6, 0)) is False


def test_time_in_window_zero_width_is_never():
    assert _time_in_window(time(12, 0), time(12, 0), time(12, 0)) is False


def test_date_in_season_within():
    assert _date_in_season(date(2026, 7, 1), (6, 1), (9, 30)) is True
    assert _date_in_season(date(2026, 10, 1), (6, 1), (9, 30)) is False


def test_date_in_season_wraps_year():
    assert _date_in_season(date(2026, 1, 15), (12, 1), (2, 28)) is True
    assert _date_in_season(date(2026, 3, 1), (12, 1), (2, 28)) is False


def test_date_in_season_unbounded_is_always():
    assert _date_in_season(date(2026, 1, 1), None, None) is True


def test_schedule_evaluate_default_action_when_no_rules():
    sched = Schedule(timezone="UTC", enabled=True, default_action="eco", rules=[])
    now = datetime(2026, 7, 1, 12, 0, tzinfo=ZoneInfo("UTC"))
    action, rule = sched.evaluate(now)
    assert action == "eco"
    assert rule is None


def test_schedule_evaluate_highest_priority_rule_wins():
    now = datetime(2026, 7, 1, 12, 0, tzinfo=ZoneInfo("UTC"))
    wd = now.weekday()
    rules = [
        Rule(
            id="low",
            name="low",
            action="eco",
            days=[wd],
            start=time(0, 0),
            end=time(23, 59),
            priority=1,
        ),
        Rule(
            id="high",
            name="high",
            action="super",
            days=[wd],
            start=time(0, 0),
            end=time(23, 59),
            priority=5,
        ),
    ]
    sched = Schedule(timezone="UTC", enabled=True, default_action="none", rules=rules)
    action, rule = sched.evaluate(now)
    assert action == "super"
    assert rule.id == "high"