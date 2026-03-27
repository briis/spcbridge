"""Support for SPC alarm control panels."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
)
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from pyspcbridge import SpcBridge
    from pyspcbridge.area import Area

from pyspcbridge.const import ArmMode

from .const import CONF_AREAS_INCLUDE_DATA, CONF_CODE, DEFAULT_CONF_CODE, DOMAIN
from .entity import SpcAreaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up SPC alarm control panels based on config entry."""
    api: SpcBridge = hass.data[DOMAIN][entry.entry_id]
    included_areas = entry.options[CONF_AREAS_INCLUDE_DATA]
    async_add_entities(
        SpcAreaAlarmControlPanel(entry, area)
        for area in api.areas.values()
        if included_areas.get(str(area.id)) == "include"
    )


def _alarm_state(area: Area) -> AlarmControlPanelState | None:
    """Map area arm mode and alarm status to HA alarm state."""
    if area.intrusion or area.fire:
        return AlarmControlPanelState.TRIGGERED

    mode_to_state = {
        ArmMode.UNSET: AlarmControlPanelState.DISARMED,
        ArmMode.PART_SET_A: AlarmControlPanelState.ARMED_HOME,
        ArmMode.PART_SET_B: AlarmControlPanelState.ARMED_NIGHT,
        ArmMode.FULL_SET: AlarmControlPanelState.ARMED_AWAY,
    }
    return mode_to_state.get(area.mode)


class SpcAreaAlarmControlPanel(SpcAreaEntity, AlarmControlPanelEntity):
    """Representation of an SPC area as an alarm control panel."""

    _attr_translation_key = "area_alarm_control_panel"
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.ARM_NIGHT
    )

    def __init__(self, entry: ConfigEntry, area: Area) -> None:
        """Initialize the alarm control panel."""
        super().__init__(entry=entry, area=area, suffix="alarm_control_panel")
        self._default_code: str = entry.options.get(CONF_CODE, DEFAULT_CONF_CODE)

    @property
    def code_arm_required(self) -> bool:
        """Return whether a code is required for arming."""
        return not bool(self._default_code)

    def _effective_code(self, code: str | None) -> str | None:
        """Return the code to use: caller-supplied or the configured default."""
        return code or self._default_code or None

    @property
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the current alarm state."""
        return _alarm_state(self._area)

    @property
    def changed_by(self) -> str:
        """Return the user who last changed the arm mode."""
        return self._area.changed_by

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        """Send disarm command."""
        await self._area.async_command("unset", self._effective_code(code))

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        """Send arm Part Set A command."""
        await self._area.async_command("set_a", self._effective_code(code))

    async def async_alarm_arm_night(self, code: str | None = None) -> None:
        """Send arm Part Set B command."""
        await self._area.async_command("set_b", self._effective_code(code))

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        """Send delayed arm Full Set command."""
        await self._area.async_command("set_delayed", self._effective_code(code))
