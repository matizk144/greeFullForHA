"""The Gree Full integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import CONF_HOST, CONF_NAME

from .const import DOMAIN, CONF_CLIENT_API
from .entities.greeClimate import GreeClimate
from greeclimateapi.greeClimateApi import GreeClimateApi

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms

    instances = list()

    for instance in config[DOMAIN]:
        instances.append({
            CONF_NAME: instance[CONF_NAME],
            CONF_CLIENT_API: GreeClimate(GreeClimateApi(instance[CONF_HOST]))
        })


    hass.data[DOMAIN] = instances

    hass.helpers.discovery.load_platform('climate', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('select', DOMAIN, {}, config)

    return True

# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Set up Gree Full from a config entry."""

#     hass.data.setdefault(DOMAIN, {})
#     # TODO 1. Create API instance
#     # TODO 2. Validate the API connection (and authentication)
#     # TODO 3. Store an API object for your platforms to access
#     # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

#     return True


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Unload a config entry."""
#     if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
#         hass.data[DOMAIN].pop(entry.entry_id)

#     return unload_ok
