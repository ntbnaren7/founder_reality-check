import pytest
from app.services.user_validator import validate_target_user
from app.services.channel_enforcer import enforce_channel

# Mock LLM client would be ideal here, but for now we'll test the logic structure
# or rely on the real LLM if keys are present (integration test style).
# To keep it simple and fast without burning tokens on every test run, 
# we might want to mock, but the instructions imply using the real environment.
# I will add basic structure tests.

def test_user_validator_short_input():
    result = validate_target_user("bad")
    assert result["is_valid"] is False
    assert "too short" in result["reason"]

def test_channel_enforcer_empty():
    result = enforce_channel("")
    assert result["primary_channel_type"] is None
    assert "No distribution channel" in result["issues"][0]
