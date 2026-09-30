# Changelog

All notable changes to this project are documented in this file.

## [0.7.6] - 2026-09-30

### Fixed

- Removed the deprecation warnings logged by Home Assistant 2026.9 about `device_registry.async_get_device` and the `via_device` parameter. The integration now uses `async_get_device_by_identifier` and `via_device_id`, so it keeps working when the old calls are removed in Home Assistant 2027.8.

### Changed

- The minimum required Home Assistant version is now 2026.8.0 (previously 2026.3.2), as the new device registry calls are not available in older versions.

[0.7.6]: https://github.com/briis/spcbridge/compare/v0.7.5...v0.7.6
