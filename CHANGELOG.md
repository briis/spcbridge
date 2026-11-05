# Changelog

All notable changes to this project are documented in this file.

## [0.7.7] - 2026-11-05

### Fixed

- Fixed the type-checker errors reported against Home Assistant 2026.10 and later, which validate forms with `probatio` instead of `voluptuous`. The integration uses `probatio` on 2026.10+ and keeps using `voluptuous` on older versions, so the minimum Home Assistant version is unchanged (2026.8.0).
- Removed the deprecation warning about `CONN_CLASS_LOCAL_PUSH`, which Home Assistant will remove in 2027.5.
- The options flow no longer receives the config entry in its constructor, matching the current Home Assistant pattern.

### Added

- Integration icon and logo, shown by Home Assistant in the integrations list.

## [0.7.6] - 2026-09-30

### Fixed

- Removed the deprecation warnings logged by Home Assistant 2026.9 about `device_registry.async_get_device` and the `via_device` parameter. The integration now uses `async_get_device_by_identifier` and `via_device_id`, so it keeps working when the old calls are removed in Home Assistant 2027.8.

### Changed

- The minimum required Home Assistant version is now 2026.8.0 (previously 2026.3.2), as the new device registry calls are not available in older versions.

[0.7.7]: https://github.com/briis/spcbridge/compare/v0.7.6...v0.7.7
[0.7.6]: https://github.com/briis/spcbridge/compare/v0.7.5...v0.7.6
