from enum import StrEnum
from typing import Any
from homeassistant.components.select import SelectEntity
from greeclimateapi.greeStatusData import GreeStatusData, HorizontalSwing
from .greeClimate import GreeClimate

class HorizontalSwingModes(StrEnum):
    LEFT = "Left"
    LEFT_MID = "Left - Middle"
    MIDDLE = "Middle"
    RIGHT_MID = "Right - Middle"
    RIGHT = "Right"
    FULL = "Full (Swing)"
    DEFAULT = "Default"

HORIZONTAL_SWING_MODES = [HorizontalSwingModes.FULL, HorizontalSwingModes.LEFT, HorizontalSwingModes.LEFT_MID, HorizontalSwingModes.MIDDLE, HorizontalSwingModes.RIGHT_MID, HorizontalSwingModes.RIGHT, HorizontalSwingModes.DEFAULT]

class GreeFullHorizontalSwing(SelectEntity):
    def __init__(self, name, gree_climate : GreeClimate, logger) -> None:
        self._logger = logger
        self._logger.info("Initialize the GREE climate device - horizontal swing")
        super().__init__()
        self._name = name
        self._gree_climate = gree_climate
        self._status = GreeStatusData()

    @property
    def available(self) -> bool:
        return self._gree_climate.initialized

    @property
    def name(self):
        return self._name + ".horizontalswing"

    @property
    def unique_id(self) -> str:
        return str(self.name)

    @property
    def options(self) -> list:
        return HORIZONTAL_SWING_MODES

    async def async_select_option(self, option: str) -> None:
        self._logger.info("Select horizontal swing mode " + option)
        selectedOption : HorizontalSwing
        if (option == HorizontalSwingModes.LEFT):
            selectedOption = HorizontalSwing.left
        elif (option == HorizontalSwingModes.LEFT_MID):
            selectedOption = HorizontalSwing.leftMid
        elif (option == HorizontalSwingModes.MIDDLE):
            selectedOption = HorizontalSwing.mid
        elif (option == HorizontalSwingModes.RIGHT_MID):
            selectedOption = HorizontalSwing.rightMid
        elif (option == HorizontalSwingModes.RIGHT):
            selectedOption = HorizontalSwing.right
        elif (option == HorizontalSwingModes.FULL):
            selectedOption = HorizontalSwing.full
        else:
            selectedOption = HorizontalSwing.default
        await self._gree_climate.greeClimateApi.horizontal_swing(selectedOption)

    @property
    def current_option(self) -> str:
        currentOption : str
        if (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.left):
            currentOption = HorizontalSwingModes.LEFT
        elif (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.leftMid):
            currentOption = HorizontalSwingModes.LEFT_MID
        elif (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.mid):
            currentOption = HorizontalSwingModes.MIDDLE
        elif (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.rightMid):
            currentOption = HorizontalSwingModes.RIGHT_MID
        elif (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.right):
            currentOption = HorizontalSwingModes.RIGHT
        elif (self._gree_climate.greeClimateApi.statusData.horizontalSwing == HorizontalSwing.full):
            currentOption = HorizontalSwingModes.FULL
        else:
            currentOption = HorizontalSwingModes.DEFAULT
        self._logger.info("Get current horizontal swing mode: " + currentOption)
        return currentOption

    async def async_update(self):
        if (not self._gree_climate.initialized):
            return
        await self._gree_climate.async_update()
        self._status = self._gree_climate.greeClimateApi.statusData