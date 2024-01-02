import logging
from typing import Any, Coroutine
from greeclimateapi.enums import FanSpeed, OperationMode
from greeclimateapi.greeClimateApi import GreeClimateApi
from greeclimateapi.greeStatusData import GreeStatusData
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.components.climate.const import HVACMode

from .greeClimate import GreeClimate

from .const import (
    FAN_MODE_AUTO,
    FAN_MODE_HIGH,
    FAN_MODE_LOW,
    FAN_MODE_MEDIUM,
    FAN_MODE_MEDIUM_HIGH,
    FAN_MODE_MEDIUM_LOW,
    FAN_MODE_QUIET,
    FAN_MODE_TURBO,
)

# from the remote control and gree app
MIN_TEMP = 16
MAX_TEMP = 30

FAN_MODES = [FAN_MODE_AUTO, FAN_MODE_LOW, FAN_MODE_MEDIUM_LOW, FAN_MODE_MEDIUM, FAN_MODE_MEDIUM_HIGH, FAN_MODE_HIGH, FAN_MODE_TURBO, FAN_MODE_QUIET]

HVAC_MODES = [HVACMode.OFF, HVACMode.AUTO, HVACMode.COOL, HVACMode.HEAT, HVACMode.FAN_ONLY, HVACMode.DRY]

SUPPORT_FLAGS = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE

class GreeFullClimate(ClimateEntity):
    def __init__(self, name, gree_climate : GreeClimate, logger) -> None:
        self._logger = logger
        self._logger.info("Initialize the GREE climate device - climate")
        super().__init__()
        self._name = name
        self._gree_climate = gree_climate
        self._status = GreeStatusData()
        self._initialized = False

    @property
    def available(self) -> bool:
        return self._initialized

    @property
    def name(self):
        return self._name + ".climate"

    @property
    def unique_id(self) -> str:
        return str(self.name)

    @property
    def supported_features(self) -> ClimateEntityFeature:
        return SUPPORT_FLAGS

    async def async_update(self):
        if not self._initialized:
            await self._gree_climate.async_initialize()
            self._initialized = True
        await self._gree_climate.async_update()
        self._status = self._gree_climate.greeClimateApi.statusData

    @property
    def current_temperature(self) -> float | None:
        self._logger.info("Get current temperature: " + str(self._status.currentTemperature))
        return float(self._status.currentTemperature)

    @property
    def target_temperature(self) -> float | None:
        self._logger.info("Get temperature: " + str(self._status.targetTemperature))
        return float(self._status.targetTemperature)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        if kwargs.get(ATTR_TEMPERATURE) is None:
            return
        if not self._status.power:
            return
        self._logger.info("Set temperature: " + str(kwargs.get(ATTR_TEMPERATURE)))
        await self._gree_climate.greeClimateApi.target_temperature(int(kwargs.get(ATTR_TEMPERATURE)))

    @property
    def target_temperature_step(self) -> float | None:
        return 1

    @property
    def fan_mode(self) -> str | None:
        if self._status.quiet:
            return FAN_MODE_QUIET
        if self._status.xFan:
            return FAN_MODE_TURBO
        if self._status.fanSpeed == FanSpeed.auto:
            return FAN_MODE_AUTO
        if self._status.fanSpeed == FanSpeed.low:
            return FAN_MODE_LOW
        elif self._status.fanSpeed == FanSpeed.mediumLow:
            return FAN_MODE_MEDIUM_LOW
        elif self._status.fanSpeed == FanSpeed.medium:
            return FAN_MODE_MEDIUM
        elif self._status.fanSpeed == FanSpeed.mediumHigh:
            return FAN_MODE_MEDIUM_HIGH
        elif self._status.fanSpeed == FanSpeed.high:
            return FAN_MODE_HIGH
        else:
            self._logger.error("Fan mode not supported: " + str(self._status.fanSpeed))

    @property
    def fan_modes(self) -> list[str] | None:
        return FAN_MODES

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if fan_mode == FAN_MODE_QUIET:
            if self._status.xFan:
                await self._gree_climate.greeClimateApi.x_fan(False)
            await self._gree_climate.greeClimateApi.quiet(True)
            return
        if fan_mode == FAN_MODE_TURBO:
            if self._status.quiet:
                await self._gree_climate.greeClimateApi.quiet(False)
            await self._gree_climate.greeClimateApi.x_fan(True)
            return
        if self._status.xFan:
            await self._gree_climate.greeClimateApi.x_fan(False)
        if self._status.quiet:
            await self._gree_climate.greeClimateApi.quiet(False)
        if fan_mode == FAN_MODE_AUTO:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.auto)
        elif fan_mode == FAN_MODE_LOW:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.low)
        elif fan_mode == FAN_MODE_MEDIUM_LOW:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.mediumLow)
        elif fan_mode == FAN_MODE_MEDIUM:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.medium)
        elif fan_mode == FAN_MODE_MEDIUM_HIGH:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.mediumHigh)
        elif fan_mode == FAN_MODE_HIGH:
            await self._gree_climate.greeClimateApi.fan_speed(FanSpeed.high)
        else:
            self._logger.error("Fan mode not supported: " + fan_mode)

    @property
    def hvac_mode(self) -> HVACMode | None:
        if not self._status.power:
            return HVACMode.OFF
        elif self._status.operationMode == OperationMode.cool:
            return HVACMode.COOL
        elif self._status.operationMode == OperationMode.heat:
            return HVACMode.HEAT
        elif self._status.operationMode == OperationMode.fan:
            return HVACMode.FAN_ONLY
        elif self._status.operationMode == OperationMode.dry:
            return HVACMode.DRY
        else:
            return HVACMode.AUTO

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self._gree_climate.greeClimateApi.power(False)
            return
        if not self._status.power:
            await self._gree_climate.greeClimateApi.power(True)
        if (hvac_mode == HVACMode.COOL):
            await self._gree_climate.greeClimateApi.operation_mode(OperationMode.cool)
        elif (hvac_mode == HVACMode.HEAT):
            await self._gree_climate.greeClimateApi.operation_mode(OperationMode.heat)
        elif (hvac_mode == HVACMode.FAN_ONLY):
            await self._gree_climate.greeClimateApi.operation_mode(OperationMode.fan)
        elif (hvac_mode == HVACMode.DRY):
            await self._gree_climate.greeClimateApi.operation_mode(OperationMode.dry)
        else:
            await self._gree_climate.greeClimateApi.operation_mode(OperationMode.auto)

    @property
    def hvac_modes(self) -> list[HVACMode]:
        return HVAC_MODES

    @property
    def max_temp(self) -> float:
        return MAX_TEMP

    @property
    def min_temp(self) -> float:
        return MIN_TEMP

    @property
    def temperature_unit(self) -> str:
        return UnitOfTemperature.CELSIUS

