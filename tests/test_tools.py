import pytest

from app.tools.error_log_tool import get_error_log
from app.tools.settlement_tool import get_settlement_status
from app.tools.ssi_tool import get_ssi
from app.tools.transaction_tool import get_trade


@pytest.mark.parametrize(
    ("tool", "expected_name"),
    [
        (get_trade, "get_trade"),
        (get_settlement_status, "get_settlement_status"),
        (get_ssi, "get_ssi"),
        (get_error_log, "get_error_log"),
    ],
)
def test_tool_has_expected_name(tool, expected_name):
    assert tool.name == expected_name
