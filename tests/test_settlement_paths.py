from db import (
    find_trade,
    find_settlement_status,
    find_ssi,
    find_error_logs,
)


# =========================================================
# TX1001
# Expected:
# Trade exists
# → Not SETTLED
# → Settlement reason = SSI_MISMATCH
# → SSI investigation path
# =========================================================

def test_tx1001_goes_to_ssi_path():
    trade = find_trade("TX1001")

    assert trade is not None, "TX1001 should exist"
    assert trade["status"] != "SETTLED"

    settlement = find_settlement_status("TX1001")

    assert settlement is not None
    assert settlement["reason_code"] == "SSI_MISMATCH"

    ssi = find_ssi("TX1001")

    assert ssi is not None, "TX1001 should have SSI data"


# =========================================================
# TX1002
# Expected:
# Trade exists
# → Already SETTLED
# → Investigation should stop
# =========================================================

def test_tx1002_is_already_settled():
    trade = find_trade("TX1002")

    assert trade is not None, "TX1002 should exist"
    assert trade["status"] == "SETTLED"


# =========================================================
# TX1003
# Expected:
# Trade exists
# → Not SETTLED
# → Settlement reason = SYSTEM_ERROR
# → Error Log investigation path
# =========================================================

def test_tx1003_goes_to_error_log_path():
    trade = find_trade("TX1003")

    assert trade is not None, "TX1003 should exist"
    assert trade["status"] != "SETTLED"

    settlement = find_settlement_status("TX1003")

    assert settlement is not None
    assert settlement["reason_code"] == "SYSTEM_ERROR"

    logs = find_error_logs("TX1003")

    assert logs, "TX1003 should have at least one error log"


# =========================================================
# TX9999
# Expected:
# Trade does not exist
# → Investigation should stop immediately
# =========================================================

def test_tx9999_trade_not_found():
    trade = find_trade("TX9999")

    assert trade is None