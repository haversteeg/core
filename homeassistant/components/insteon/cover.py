"""Support for Insteon covers via PowerLinc Modem."""
import logging
import math

from homeassistant.components.cover import (
    ATTR_POSITION,
    DOMAIN,
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
    CoverEntity,
)

from .insteon_entity import InsteonEntity
from .utils import async_add_insteon_entities

_LOGGER = logging.getLogger(__name__)

SUPPORTED_FEATURES = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_SET_POSITION


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Insteon platform."""
    async_add_insteon_entities(
        hass, DOMAIN, InsteonCoverEntity, async_add_entities, discovery_info
    )


class InsteonCoverEntity(InsteonEntity, CoverEntity):
    """A Class for an Insteon cover entity."""

    @property
    def current_cover_position(self):
        """Return the current cover position."""
        return int(math.ceil(self._insteon_device_group.value * 100 / 255))

    @property
    def supported_features(self):
        """Return the supported features for this entity."""
        return SUPPORTED_FEATURES

    @property
    def is_closed(self):
        """Return the boolean response if the node is on."""
        return bool(self.current_cover_position)

    async def async_open_cover(self, **kwargs):
        """Open cover."""
        await self._insteon_device.async_open()

    async def async_close_cover(self, **kwargs):
        """Close cover."""
        await self._insteon_device.async_close()

    async def async_set_cover_position(self, **kwargs):
        """Set the cover position."""
        position = int(kwargs[ATTR_POSITION] * 255 / 100)
        if position == 0:
            await self._insteon_device.async_close()
        else:
            await self._insteon_device.async_open(
                position=position, group=self._insteon_device_group.group
            )
