import os
import sys

# Make the repo root importable so ``import app`` works regardless of how
# pytest is invoked (``pytest`` or ``python -m pytest``).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

# Sanitized stand-in for the Avalon Q ``litestats`` "MM ID0:Summary" blob. The
# shape mirrors a real response (the 'STATS':{...} wrapper and bracket-pair
# KEY[value] tokens) but every value is fictional.
FULL_MM_BLOB = (
    "'STATS':{Ver[Q-TESTFW] LVer[TESTFW] STATE[1] MEMFREE[67264] "
    "SYSTEMSTATU[Work: In Work, Hash Board: 1] Elapsed[441170] "
    "ITemp[25] HBITemp[68] HBOTemp[72] TMax[90] TAvg[80] "
    "Fan1[1806] Fan2[1805] FanR[59%] "
    "PS[0 1216 2335 55 1301 2336 1379] GHSspd[83837.70] MPO[1300] "
    "WORKMODE[1] WORKLEVEL[0] Nonce Mask[25]}"
)


@pytest.fixture
def litestats_response():
    return {"STATS": [{"MM ID0:Summary": FULL_MM_BLOB}]}


@pytest.fixture
def empty_stats_response():
    # What the ``stats`` command returns on Avalon Q firmware: an empty MM blob.
    return {"STATS": [{"ID": "AVALON0", "MM ID0:Summary": "", "HBinfo": ""}]}


@pytest.fixture
def summary_response():
    return {
        "SUMMARY": [
            {
                "Elapsed": 440820,
                "MHS av": 63677463.04,
                "MHS 5s": 96051745.88,
                "MHS 1m": 88242768.48,
                "Accepted": 49867,
                "Rejected": 150,
                "Hardware Errors": 3,
            }
        ]
    }


@pytest.fixture
def pools_response():
    return {"POOLS": [{"URL": "stratum+tcp://pool.example.com:3333", "Status": "Alive"}]}