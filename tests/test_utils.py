"""Tests for utility functions in spcbridge."""

from pyspcbridge.const import ArmMode, DoorMode

from custom_components.spcbridge.utils import (
    arm_mode_to_name,
    door_mode_to_name,
    get_host,
)


class TestArmModeToName:
    def test_unset_returns_disarmed(self):
        assert arm_mode_to_name(ArmMode.UNSET) == "disarmed"

    def test_part_set_a_returns_partset_a(self):
        assert arm_mode_to_name(ArmMode.PART_SET_A) == "partset_a"

    def test_part_set_b_returns_partset_b(self):
        assert arm_mode_to_name(ArmMode.PART_SET_B) == "partset_b"

    def test_full_set_returns_armed(self):
        assert arm_mode_to_name(ArmMode.FULL_SET) == "armed"

    def test_partly_set_a_returns_partset_a_partly(self):
        assert arm_mode_to_name(ArmMode.PARTLY_SET_A) == "partset_a_partly"

    def test_partly_set_b_returns_partset_b_partly(self):
        assert arm_mode_to_name(ArmMode.PARTLY_SET_B) == "partset_b_partly"

    def test_partly_full_set_returns_armed_partly(self):
        assert arm_mode_to_name(ArmMode.PARTLY_FULL_SET) == "armed_partly"

    def test_unknown_value_returns_unknown(self):
        # Pass an integer not in the enum to simulate an unknown mode
        assert arm_mode_to_name(999) == "unknown"


class TestDoorModeToName:
    def test_normal_returns_normal(self):
        assert door_mode_to_name(DoorMode.NORMAL) == "normal"

    def test_locked_returns_locked(self):
        assert door_mode_to_name(DoorMode.LOCKED) == "locked"

    def test_unlocked_returns_unlocked(self):
        assert door_mode_to_name(DoorMode.UNLOCKED) == "unlocked"

    def test_unknown_value_returns_unknown(self):
        assert door_mode_to_name(999) == "unknown"


class TestGetHost:
    def test_ipv4_address_returned_as_is(self):
        assert get_host("192.168.1.1") == "192.168.1.1"

    def test_ipv6_address_wrapped_in_brackets(self):
        assert get_host("2001:db8::1") == "[2001:db8::1]"

    def test_ipv6_loopback_wrapped_in_brackets(self):
        assert get_host("::1") == "[::1]"

    def test_hostname_returned_as_is(self):
        assert get_host("my-bridge.local") == "my-bridge.local"

    def test_localhost_returned_as_is(self):
        assert get_host("localhost") == "localhost"

    def test_ipv4_loopback_returned_as_is(self):
        assert get_host("127.0.0.1") == "127.0.0.1"
