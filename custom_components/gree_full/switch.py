import logging
from typing import Any, Coroutine
from homeassistant.const import CONF_NAME

from .entities.light import GreeFullLight
from .entities.freshair import GreeFullFreshAir
from .entities.health import GreeFullHealth
from .const import DOMAIN, CONF_CLIENT_API

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    _LOGGER.info("Setting up Gree climates platform")

    climates = list()

    for instance in hass.data[DOMAIN]:
        climates.append(GreeFullLight(instance[CONF_NAME], instance[CONF_CLIENT_API], _LOGGER))
        climates.append(GreeFullFreshAir(instance[CONF_NAME], instance[CONF_CLIENT_API], _LOGGER))
        climates.append(GreeFullHealth(instance[CONF_NAME], instance[CONF_CLIENT_API], _LOGGER))

    async_add_devices(climates)