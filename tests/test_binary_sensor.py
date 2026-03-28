"""Tests for SPC binary sensor entities."""

from unittest.mock import MagicMock

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from custom_components.spcbridge.binary_sensor import (
    SpcAreaFireBinarySensor,
    SpcAreaIntrusionBinarySensor,
    SpcAreaProblemBinarySensor,
    SpcAreaTamperBinarySensor,
    SpcAreaVerifiedBinarySensor,
    SpcPanelFireBinarySensor,
    SpcPanelIntrusionBinarySensor,
    SpcPanelProblemBinarySensor,
    SpcPanelTamperBinarySensor,
    SpcPanelVerifiedBinarySensor,
    SpcZoneAlarmBinarySensor,
    SpcZoneInhibitedBinarySensor,
    SpcZoneIsolatedBinarySensor,
    SpcZoneProblemBinarySensor,
    SpcZoneStateBinarySensor,
    SpcZoneTamperBinarySensor,
    _get_device_class,
)


class TestGetDeviceClass:
    def test_motion_returns_motion_class(self):
        assert _get_device_class("motion") == BinarySensorDeviceClass.MOTION

    def test_door_returns_door_class(self):
        assert _get_device_class("door") == BinarySensorDeviceClass.DOOR

    def test_window_returns_window_class(self):
        assert _get_device_class("window") == BinarySensorDeviceClass.WINDOW

    def test_smoke_returns_smoke_class(self):
        assert _get_device_class("smoke") == BinarySensorDeviceClass.SMOKE

    def test_other_returns_none(self):
        assert _get_device_class("other") is None

    def test_exclude_returns_none(self):
        assert _get_device_class("exclude") is None

    def test_unknown_returns_none(self):
        assert _get_device_class("unknown_type") is None


def _make_entry():
    entry = MagicMock()
    entry.unique_id = "test-serial"
    entry.options = {}
    return entry


def _make_panel(**kwargs):
    panel = MagicMock()
    panel.id = 1
    panel.type = "SPC5350"
    panel.serial = "ABC123"
    panel.firmware = "3.8.0"
    for k, v in kwargs.items():
        setattr(panel, k, v)
    return panel


def _make_area(**kwargs):
    area = MagicMock()
    area.id = 1
    area.name = "Main Area"
    for k, v in kwargs.items():
        setattr(area, k, v)
    return area


def _make_zone(**kwargs):
    zone = MagicMock()
    zone.id = 1
    zone.name = "Front Door"
    for k, v in kwargs.items():
        setattr(zone, k, v)
    return zone


class TestPanelBinarySensors:
    def test_intrusion_is_on_when_panel_intrusion_true(self):
        entry = _make_entry()
        panel = _make_panel(intrusion=True)
        sensor = SpcPanelIntrusionBinarySensor(entry, panel)
        assert sensor.is_on is True

    def test_intrusion_is_off_when_panel_intrusion_false(self):
        entry = _make_entry()
        panel = _make_panel(intrusion=False)
        sensor = SpcPanelIntrusionBinarySensor(entry, panel)
        assert sensor.is_on is False

    def test_fire_is_on_when_panel_fire_true(self):
        entry = _make_entry()
        panel = _make_panel(fire=True)
        sensor = SpcPanelFireBinarySensor(entry, panel)
        assert sensor.is_on is True

    def test_fire_is_off_when_panel_fire_false(self):
        entry = _make_entry()
        panel = _make_panel(fire=False)
        sensor = SpcPanelFireBinarySensor(entry, panel)
        assert sensor.is_on is False

    def test_tamper_is_on(self):
        entry = _make_entry()
        panel = _make_panel(tamper=True)
        sensor = SpcPanelTamperBinarySensor(entry, panel)
        assert sensor.is_on is True

    def test_tamper_is_off(self):
        entry = _make_entry()
        panel = _make_panel(tamper=False)
        sensor = SpcPanelTamperBinarySensor(entry, panel)
        assert sensor.is_on is False

    def test_problem_is_on(self):
        entry = _make_entry()
        panel = _make_panel(problem=True)
        sensor = SpcPanelProblemBinarySensor(entry, panel)
        assert sensor.is_on is True

    def test_problem_is_off(self):
        entry = _make_entry()
        panel = _make_panel(problem=False)
        sensor = SpcPanelProblemBinarySensor(entry, panel)
        assert sensor.is_on is False

    def test_verified_is_on(self):
        entry = _make_entry()
        panel = _make_panel(verified=True)
        sensor = SpcPanelVerifiedBinarySensor(entry, panel)
        assert sensor.is_on is True

    def test_verified_is_off(self):
        entry = _make_entry()
        panel = _make_panel(verified=False)
        sensor = SpcPanelVerifiedBinarySensor(entry, panel)
        assert sensor.is_on is False


class TestAreaBinarySensors:
    def test_intrusion_is_on(self):
        sensor = SpcAreaIntrusionBinarySensor(_make_entry(), _make_area(intrusion=True))
        assert sensor.is_on is True

    def test_intrusion_is_off(self):
        sensor = SpcAreaIntrusionBinarySensor(
            _make_entry(), _make_area(intrusion=False)
        )
        assert sensor.is_on is False

    def test_fire_is_on(self):
        sensor = SpcAreaFireBinarySensor(_make_entry(), _make_area(fire=True))
        assert sensor.is_on is True

    def test_fire_is_off(self):
        sensor = SpcAreaFireBinarySensor(_make_entry(), _make_area(fire=False))
        assert sensor.is_on is False

    def test_tamper_is_on(self):
        sensor = SpcAreaTamperBinarySensor(_make_entry(), _make_area(tamper=True))
        assert sensor.is_on is True

    def test_problem_is_off(self):
        sensor = SpcAreaProblemBinarySensor(_make_entry(), _make_area(problem=False))
        assert sensor.is_on is False

    def test_verified_is_on(self):
        sensor = SpcAreaVerifiedBinarySensor(_make_entry(), _make_area(verified=True))
        assert sensor.is_on is True


class TestZoneBinarySensors:
    def test_zone_state_is_on_when_open(self):
        zone = _make_zone(state=True)
        sensor = SpcZoneStateBinarySensor(
            _make_entry(), zone, BinarySensorDeviceClass.DOOR
        )
        assert sensor.is_on is True

    def test_zone_state_is_off_when_closed(self):
        zone = _make_zone(state=False)
        sensor = SpcZoneStateBinarySensor(
            _make_entry(), zone, BinarySensorDeviceClass.DOOR
        )
        assert sensor.is_on is False

    def test_zone_state_device_class_set(self):
        zone = _make_zone(state=False)
        sensor = SpcZoneStateBinarySensor(
            _make_entry(), zone, BinarySensorDeviceClass.MOTION
        )
        assert sensor._attr_device_class == BinarySensorDeviceClass.MOTION

    def test_zone_state_device_class_none_for_other(self):
        zone = _make_zone(state=False)
        sensor = SpcZoneStateBinarySensor(_make_entry(), zone, None)
        assert sensor._attr_device_class is None

    def test_zone_alarm_is_on_when_intrusion(self):
        zone = _make_zone(intrusion=True, fire=False)
        sensor = SpcZoneAlarmBinarySensor(_make_entry(), zone)
        assert sensor.is_on is True

    def test_zone_alarm_is_on_when_fire(self):
        zone = _make_zone(intrusion=False, fire=True)
        sensor = SpcZoneAlarmBinarySensor(_make_entry(), zone)
        assert sensor.is_on is True

    def test_zone_alarm_is_off_when_no_alarm(self):
        zone = _make_zone(intrusion=False, fire=False)
        sensor = SpcZoneAlarmBinarySensor(_make_entry(), zone)
        assert sensor.is_on is False

    def test_zone_tamper_is_on(self):
        zone = _make_zone(tamper=True)
        sensor = SpcZoneTamperBinarySensor(_make_entry(), zone)
        assert sensor.is_on is True

    def test_zone_problem_is_off(self):
        zone = _make_zone(problem=False)
        sensor = SpcZoneProblemBinarySensor(_make_entry(), zone)
        assert sensor.is_on is False

    def test_zone_inhibited_is_on(self):
        zone = _make_zone(inhibited=True)
        sensor = SpcZoneInhibitedBinarySensor(_make_entry(), zone)
        assert sensor.is_on is True

    def test_zone_isolated_is_on(self):
        zone = _make_zone(isolated=True)
        sensor = SpcZoneIsolatedBinarySensor(_make_entry(), zone)
        assert sensor.is_on is True
