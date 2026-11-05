# Copyright (c) 2026 @briis
"""Compatibility helpers for supporting multiple Home Assistant versions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import MAJOR_VERSION, MINOR_VERSION

# Home Assistant 2026.10 replaced voluptuous with probatio, a drop-in
# replacement with the same API. Use whichever library the running Home
# Assistant validates with: 2026.9 already ships probatio but still uses
# voluptuous internally, so the choice is made on version, not availability.
if TYPE_CHECKING or (MAJOR_VERSION, MINOR_VERSION) >= (2026, 10):
    import probatio as vol
else:
    import voluptuous as vol

__all__ = ["vol"]
