from typing import Any
from homeassistant.components.switch import SwitchEntity
from greeclimateapi.greeStatusData import GreeStatusData
from .greeClimate import GreeClimate

class GreeFullFreshAir(SwitchEntity):
    def __init__(self, name, gree_climate : GreeClimate, logger) -> None:
        self._logger = logger
        self._logger.info("Initialize the GREE climate device - fresh air")
        super().__init__()
        self._name = name
        self._gree_climate = gree_climate
        self._status = GreeStatusData()

    @property
    def available(self) -> bool:
        return self._gree_climate.initialized

    @property
    def name(self):
        return self._name + ".freshair"

    @property
    def unique_id(self) -> str:
        return str(self.name)

    @property
    def is_on(self) -> bool:
        self._logger.info("Get fresh air status: " + str(self._gree_climate.greeClimateApi.statusData.freshAir))
        return self._gree_climate.greeClimateApi.statusData.freshAir

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._logger.info("Turn on fresh air")
        await self._gree_climate.greeClimateApi.fresh_air(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._logger.info("Turn off fresh air")
        await self._gree_climate.greeClimateApi.fresh_air(False)

    def update(self):
        if (not self._gree_climate.initialized):
            return
        self._status = self._gree_climate.greeClimateApi.statusData
