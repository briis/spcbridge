"""Tests for config_flow utility functions."""

import pytest
from pyspcbridge.const import ZoneType

from custom_components.spcbridge.config_flow import (
    include_mode_to_name,
    validate_spc_users_data,
    zone_type_to_name,
)


class TestValidateSpcUsersData:
    """Tests for the validate_spc_users_data function."""

    def _make_users(self, **fields):
        """Helper to build a single-user data dict."""
        user = {"id": 1, "name": "Alice", **fields}
        return {1: user}

    def test_valid_pincode_and_password_produce_no_errors(self):
        users = self._make_users(ha_pincode="1234", spc_password="secret")
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_empty_pincode_is_valid(self):
        users = self._make_users(ha_pincode="", spc_password="secret")
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_empty_password_is_valid(self):
        users = self._make_users(ha_pincode="1234", spc_password="")
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_both_empty_is_valid(self):
        users = self._make_users(ha_pincode="", spc_password="")
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_max_pincode_length_is_valid(self):
        # Max is 10 digits (max value 9999999999)
        users = self._make_users(ha_pincode="9999999999", spc_password="")
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_pincode_too_long_produces_error(self):
        # 11 digits exceeds max value
        users = self._make_users(ha_pincode="99999999999", spc_password="")
        errors = validate_spc_users_data(users)
        assert "pincode_1" in errors

    def test_non_numeric_pincode_produces_error(self):
        users = self._make_users(ha_pincode="abc", spc_password="")
        errors = validate_spc_users_data(users)
        assert "pincode_1" in errors

    def test_password_at_max_length_is_valid(self):
        users = self._make_users(ha_pincode="", spc_password="a" * 16)
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_password_exceeding_max_length_produces_error(self):
        users = self._make_users(ha_pincode="", spc_password="a" * 17)
        errors = validate_spc_users_data(users)
        assert "password_1" in errors

    def test_multiple_users_all_valid(self):
        users = {
            1: {"id": 1, "name": "Alice", "ha_pincode": "1111", "spc_password": "pwd1"},
            2: {"id": 2, "name": "Bob", "ha_pincode": "2222", "spc_password": "pwd2"},
        }
        errors = validate_spc_users_data(users)
        assert errors == {}

    def test_multiple_users_one_invalid_pincode(self):
        users = {
            1: {"id": 1, "name": "Alice", "ha_pincode": "1234", "spc_password": ""},
            2: {"id": 2, "name": "Bob", "ha_pincode": "not_a_number", "spc_password": ""},
        }
        errors = validate_spc_users_data(users)
        assert "pincode_2" in errors
        assert "pincode_1" not in errors

    def test_missing_fields_produce_no_errors(self):
        # Missing ha_pincode and spc_password default to ""
        users = {1: {"id": 1, "name": "Alice"}}
        errors = validate_spc_users_data(users)
        assert errors == {}


class TestIncludeModeToName:
    """Tests for the include_mode_to_name function."""

    def test_include_returns_bold_include(self):
        assert include_mode_to_name("include") == "<b>Include</b>"

    def test_exclude_returns_bold_exclude(self):
        assert include_mode_to_name("exclude") == "<b>Exclude</b>"

    def test_motion_returns_bold_motion_sensor(self):
        assert include_mode_to_name("motion") == "<b>Include as a Motion sensor</b>"

    def test_door_returns_bold_door_sensor(self):
        assert include_mode_to_name("door") == "<b>Include as a Door sensor</b>"

    def test_window_returns_bold_window_sensor(self):
        assert include_mode_to_name("window") == "<b>Include as a Window sensor</b>"

    def test_smoke_returns_bold_smoke_sensor(self):
        assert include_mode_to_name("smoke") == "<b>Include as a Smoke sensor</b>"

    def test_other_returns_bold_other_sensor(self):
        assert include_mode_to_name("other") == "<b>Include as a Other sensor</b>"

    def test_unknown_mode_returns_unknown(self):
        assert include_mode_to_name("something_else") == "Unknown"


class TestZoneTypeToName:
    """Tests for the zone_type_to_name function."""

    def test_returns_title_case_name(self):
        # ZoneType enum values should convert to title-case names
        result = zone_type_to_name(ZoneType.ALARM.value)
        assert isinstance(result, str)
        assert len(result) > 0
        assert result == result.title()

    def test_underscores_replaced_with_spaces(self):
        # All zone type names should use spaces not underscores
        for zone_type in ZoneType:
            result = zone_type_to_name(zone_type.value)
            assert "_" not in result
