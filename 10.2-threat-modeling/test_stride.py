import json
import pytest
from stride import BASE, threats_for, prioritize, total_checks, format_line

MODEL = json.load(open("clinicbook.json"))


def el(element_id):
    return next(e for e in MODEL["elements"] if e["id"] == element_id)


def test_external():
    assert threats_for(el("E1")) == {"S", "R"}


def test_process():
    assert threats_for(el("P1")) == set("STRIDE")


def test_store_plain_and_logs():
    assert threats_for(el("D2")) == {"T", "I", "D"}
    assert threats_for(el("D3")) == {"T", "R", "I", "D"}


def test_flow():
    assert threats_for(el("DF1")) == {"T", "I", "D"}


def test_unknown_type():
    with pytest.raises(ValueError):
        threats_for({"id": "X1", "type": "robot"})


def test_store_order_does_not_leak():
    """Guard for the shared-set bug: the audit log must not add R to every later store."""
    threats_for(el("D3"))
    assert threats_for(el("D2")) == {"T", "I", "D"}
    assert BASE["store"] == {"T", "I", "D"}


def test_holds_logs_false_means_no_r():
    """Guard for the presence-vs-value bug: the key exists, but its value is False."""
    assert threats_for({"id": "D9", "type": "store", "holds_logs": False}) == {"T", "I", "D"}


def test_prioritize():
    assert prioritize(MODEL) == ["DF1", "DF4", "E1", "E2", "P1", "D2", "D3", "DF6"]


def test_total_checks():
    assert total_checks(MODEL) == 2 + 2 + 6 + 3 + 4 + 3 + 3 + 3
    assert total_checks({"elements": []}) == 0


def test_format_line():
    assert format_line("DF1", True, {"T", "I", "D"}) == "DF1   [boundary]  D I T"
    assert format_line("E1", False, {"S", "R"}) == "E1" + " " * 16 + "R S"