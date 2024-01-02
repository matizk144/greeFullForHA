from typing import Any
from homeassistant.components.switch import SwitchEntity
from greeclimateapi.greeStatusData import GreeStatusData
from .greeClimate import GreeClimate

class GreeFullLight(SwitchEntity):
    def __init__(self, name, gree_climate : GreeClimate, logger) -> None:
        self._logger = logger
        self._logger.info("Initialize the GREE climate device - light")
        super().__init__()
        self._name = name
        self._gree_climate = gree_climate
        self._status = GreeStatusData()

    @property
    def available(self) -> bool:
        return self._gree_climate.initialized

    @property
    def name(self):
        return self._name + ".light"

    @property
    def unique_id(self) -> str:
        return str(self.name)

    @property
    def is_on(self) -> bool:
        self._logger.info("Get light status: " + str(self._gree_climate.greeClimateApi.statusData.light))
        return self._gree_climate.greeClimateApi.statusData.light

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._logger.info("Turn on light")
        await self._gree_climate.greeClimateApi.light(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._logger.info("Turn off light")
        await self._gree_climate.greeClimateApi.light(False)

    def update(self):
        if (not self._gree_climate.initialized):
            return
        self._status = self._gree_climate.greeClimateApi.statusData
