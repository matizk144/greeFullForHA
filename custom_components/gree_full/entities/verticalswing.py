from enum import StrEnum
from typing import Any
from homeassistant.components.select import SelectEntity
from greeclimateapi.greeStatusData import GreeStatusData, VerticalSwing
from .greeClimate import GreeClimate

class VerticalSwingModes(StrEnum):
    BOTTOM = "Bottom"
    BOTTOM_MID = "Bottom - Middle"
    MIDDLE = "Middle"
    TOP_MID = "Top - Middle"
    TOP = "Top"
    BOTTOM_SWING = "Bottom (Swing)"
    BOTTOM_MID_SWING = "Bottom - Middle (Swing)"
    MIDDLE_SWING = "Middle (Swing)"
    TOP_MID_SWING = "Top - Middle (Swing)"
    TOP_SWING = "Top (Swing)"
    FULL = "Full (Swing)"
    DEFAULT = "Default"

VERTICAL_SWING_MODES = [VerticalSwingModes.FULL, VerticalSwingModes.TOP, VerticalSwingModes.TOP_MID, VerticalSwingModes.MIDDLE, VerticalSwingModes.BOTTOM_MID, VerticalSwingModes.BOTTOM, VerticalSwingModes.TOP_SWING, VerticalSwingModes.TOP_MID_SWING, VerticalSwingModes.MIDDLE_SWING, VerticalSwingModes.BOTTOM_MID_SWING, VerticalSwingModes.BOTTOM_SWING, VerticalSwingModes.DEFAULT]

class GreeFullVerticalSwing(SelectEntity):
    def __init__(self, name, gree_climate : GreeClimate, logger) -> None:
        self._logger = logger
        self._logger.info("Initialize the GREE climate device - vertical swing")
        super().__init__()
        self._name = name
        self._gree_climate = gree_climate
        self._status = GreeStatusData()

    @property
    def available(self) -> bool:
        return self._gree_climate.initialized

    @property
    def name(self):
        return self._name + ".verticalswing"

    @property
    def unique_id(self) -> str:
        return str(self.name)

    @property
    def options(self) -> list:
        return VERTICAL_SWING_MODES

    async def async_select_option(self, option: str) -> None:
        self._logger.info("Select vertical swing mode " + option)
        selectedOption : VerticalSwing
        if (option == VerticalSwingModes.TOP):
            selectedOption = VerticalSwing.top
        elif (option == VerticalSwingModes.TOP_MID):
            selectedOption = VerticalSwing.topMid
        elif (option == VerticalSwingModes.MIDDLE):
            selectedOption = VerticalSwing.mid
        elif (option == VerticalSwingModes.BOTTOM_MID):
            selectedOption = VerticalSwing.bottomMid
        elif (option == VerticalSwingModes.BOTTOM):
            selectedOption = VerticalSwing.bottom
        elif (option == VerticalSwingModes.TOP_SWING):
            selectedOption = VerticalSwing.topSwing
        elif (option == VerticalSwingModes.TOP_MID_SWING):
            selectedOption = VerticalSwing.topMidSwing
        elif (option == VerticalSwingModes.MIDDLE_SWING):
            selectedOption = VerticalSwing.midSwing
        elif (option == VerticalSwingModes.BOTTOM_MID_SWING):
            selectedOption = VerticalSwing.bottomMidSwing
        elif (option == VerticalSwingModes.BOTTOM_SWING):
            selectedOption = VerticalSwing.bottomSwing
        elif (option == VerticalSwingModes.FULL):
            selectedOption = VerticalSwing.full
        else:
            selectedOption = VerticalSwing.default
        await self._gree_climate.greeClimateApi.vertical_swing(selectedOption)

    @property
    def current_option(self) -> str:
        currentOption : str
        if (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.top):
            currentOption = VerticalSwingModes.TOP
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.topMid):
            currentOption = VerticalSwingModes.TOP_MID
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.mid):
            currentOption = VerticalSwingModes.MIDDLE
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.bottomMid):
            currentOption = VerticalSwingModes.BOTTOM_MID
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.bottom):
            currentOption = VerticalSwingModes.BOTTOM
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.topSwing):
            currentOption = VerticalSwingModes.TOP_SWING
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.topMidSwing):
            currentOption = VerticalSwingModes.TOP_MID_SWING
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.midSwing):
            currentOption = VerticalSwingModes.MIDDLE_SWING
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.bottomMidSwing):
            currentOption = VerticalSwingModes.BOTTOM_MID_SWING
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.bottomSwing):
            currentOption = VerticalSwingModes.BOTTOM_SWING
        elif (self._gree_climate.greeClimateApi.statusData.verticalSwing == VerticalSwing.full):
            currentOption = VerticalSwingModes.FULL
        else:
            currentOption = VerticalSwingModes.DEFAULT
        self._logger.info("Get current vertical swing mode: " + currentOption)
        return currentOption

    async def async_update(self):
        if (not self._gree_climate.initialized):
            return
        await self._gree_climate.async_update()
        self._status = self._gree_climate.greeClimateApi.statusData