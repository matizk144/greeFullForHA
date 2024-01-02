import logging
from typing import Any, Coroutine
from homeassistant.const import CONF_NAME

from .entities.verticalswing import GreeFullVerticalSwing
from .entities.horizontalswing import GreeFullHorizontalSwing
from .const import DOMAIN, CONF_CLIENT_API

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    _LOGGER.info("Setting up Gree climates platform")

    climates = list()

    for instance in hass.data[DOMAIN]:
        climates.append(GreeFullVerticalSwing(instance[CONF_NAME], instance[CONF_CLIENT_API], _LOGGER))
        climates.append(GreeFullHorizontalSwing(instance[CONF_NAME], instance[CONF_CLIENT_API], _LOGGER))

    async_add_devices(climates)