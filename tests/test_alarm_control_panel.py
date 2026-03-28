"""Tests for the SPC alarm control panel."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.alarm_control_panel.const import AlarmControlPanelState
from pyspcbridge.const import ArmMode

from custom_components.spcbridge.alarm_control_panel import (
    SpcAreaAlarmControlPanel,
    _alarm_state,
)
from custom_components.spcbridge.const import CONF_CODE, DEFAULT_CONF_CODE


def make_area(mode=ArmMode.UNSET, intrusion=False, fire=False, changed_by=""):
    """Create a mock Area with the given state."""
    area = MagicMock()
    area.id = 1
    area.name = "Test Area"
    area.mode = mode
    area.intrusion = intrusion
    area.fire = fire
    area.changed_by = changed_by
    return area


def make_entry(code=DEFAULT_CONF_CODE):
    """Create a mock ConfigEntry."""
    entry = MagicMock()
    entry.unique_id = "test-serial-123"
    entry.options = {CONF_CODE: code}
    return entry


class TestAlarmState:
    """Tests for the _alarm_state helper function."""

    def test_disarmed_when_unset(self):
        area = make_area(mode=ArmMode.UNSET)
        assert _alarm_state(area) == AlarmControlPanelState.DISARMED

    def test_armed_home_when_part_set_a(self):
        area = make_area(mode=ArmMode.PART_SET_A)
        assert _alarm_state(area) == AlarmControlPanelState.ARMED_HOME

    def test_armed_night_when_part_set_b(self):
        area = make_area(mode=ArmMode.PART_SET_B)
        assert _alarm_state(area) == AlarmControlPanelState.ARMED_NIGHT

    def test_armed_away_when_full_set(self):
        area = make_area(mode=ArmMode.FULL_SET)
        assert _alarm_state(area) == AlarmControlPanelState.ARMED_AWAY

    def test_triggered_when_intrusion(self):
        area = make_area(mode=ArmMode.FULL_SET, intrusion=True)
        assert _alarm_state(area) == AlarmControlPanelState.TRIGGERED

    def test_triggered_when_fire(self):
        area = make_area(mode=ArmMode.UNSET, fire=True)
        assert _alarm_state(area) == AlarmControlPanelState.TRIGGERED

    def test_triggered_takes_priority_over_armed_state(self):
        area = make_area(mode=ArmMode.FULL_SET, intrusion=True, fire=True)
        assert _alarm_state(area) == AlarmControlPanelState.TRIGGERED

    def test_none_for_partly_set_modes(self):
        # Partly-set modes have no direct HA equivalent
        area = make_area(mode=ArmMode.PARTLY_FULL_SET)
        assert _alarm_state(area) is None


class TestSpcAreaAlarmControlPanel:
    """Tests for the SpcAreaAlarmControlPanel entity."""

    def _make_panel(self, code=DEFAULT_CONF_CODE, **area_kwargs):
        entry = make_entry(code=code)
        area = make_area(**area_kwargs)
        with patch(
            "custom_components.spcbridge.alarm_control_panel.SpcAreaEntity.__init__",
            lambda self, entry, area, _suffix: (
                setattr(self, "_area", area) or setattr(self, "_entry", entry)
            ),
        ):
            panel = SpcAreaAlarmControlPanel.__new__(SpcAreaAlarmControlPanel)
            panel._area = area
            panel._entry = entry
            panel._default_code = entry.options.get(CONF_CODE, DEFAULT_CONF_CODE)
        return panel

    def test_code_arm_required_when_no_default_code(self):
        panel = self._make_panel(code="")
        assert panel.code_arm_required is True

    def test_code_arm_not_required_when_default_code_set(self):
        panel = self._make_panel(code="1234")
        assert panel.code_arm_required is False

    def test_effective_code_uses_caller_code(self):
        panel = self._make_panel(code="9999")
        assert panel._effective_code("5678") == "5678"

    def test_effective_code_falls_back_to_default(self):
        panel = self._make_panel(code="9999")
        assert panel._effective_code(None) == "9999"

    def test_effective_code_returns_none_when_no_code_available(self):
        panel = self._make_panel(code="")
        assert panel._effective_code(None) is None

    def test_effective_code_caller_overrides_default(self):
        panel = self._make_panel(code="default_code")
        assert panel._effective_code("caller_code") == "caller_code"

    def test_alarm_state_returns_correct_ha_state(self):
        panel = self._make_panel(mode=ArmMode.FULL_SET)
        assert panel.alarm_state == AlarmControlPanelState.ARMED_AWAY

    def test_alarm_state_triggered(self):
        panel = self._make_panel(mode=ArmMode.FULL_SET, intrusion=True)
        assert panel.alarm_state == AlarmControlPanelState.TRIGGERED

    def test_changed_by_returns_area_changed_by(self):
        panel = self._make_panel(changed_by="Alice")
        assert panel.changed_by == "Alice"

    async def test_async_alarm_disarm_sends_unset_command(self):
        panel = self._make_panel(code="1234")
        panel._area.async_command = AsyncMock()
        await panel.async_alarm_disarm("1234")
        panel._area.async_command.assert_called_once_with("unset", "1234")

    async def test_async_alarm_disarm_uses_default_code(self):
        panel = self._make_panel(code="5678")
        panel._area.async_command = AsyncMock()
        await panel.async_alarm_disarm(None)
        panel._area.async_command.assert_called_once_with("unset", "5678")

    async def test_async_alarm_arm_home_sends_set_a_command(self):
        panel = self._make_panel(code="1234")
        panel._area.async_command = AsyncMock()
        await panel.async_alarm_arm_home("1234")
        panel._area.async_command.assert_called_once_with("set_a", "1234")

    async def test_async_alarm_arm_night_sends_set_b_command(self):
        panel = self._make_panel(code="1234")
        panel._area.async_command = AsyncMock()
        await panel.async_alarm_arm_night("1234")
        panel._area.async_command.assert_called_once_with("set_b", "1234")

    async def test_async_alarm_arm_away_sends_set_delayed_command(self):
        panel = self._make_panel(code="1234")
        panel._area.async_command = AsyncMock()
        await panel.async_alarm_arm_away("1234")
        panel._area.async_command.assert_called_once_with("set_delayed", "1234")
