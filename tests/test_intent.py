import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.intent.parser import parser, Intent

def test_intent_parsing():
    result = parser.parse("please read my latest email")
    assert result["intent"] == Intent.READ_LATEST.value

    result = parser.parse("can you search invoices")
    assert result["intent"] == Intent.SEARCH.value
    assert "invoices" in result["entities"].get("query", "")

    result = parser.parse("send email to john")
    assert result["intent"] == Intent.SEND.value

    result = parser.parse("mark this as read")
    assert result["intent"] == Intent.MARK_READ.value
