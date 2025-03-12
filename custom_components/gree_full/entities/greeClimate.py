from greeclimateapi.greeClimateApi import GreeClimateApi
import asyncio

class GreeClimate:
    def __init__(self, greeClimateApi: GreeClimateApi) -> None:
        self.greeClimateApi = greeClimateApi
        self.semaphore = asyncio.Semaphore()
        self.initialized = False

    async def async_initialize(self):
        await self.semaphore.acquire()
        if self.initialized: return
        await self.greeClimateApi.initialize()
        self.initialized = True
        self.semaphore.release()

    async def async_update(self):
        await self.semaphore.acquire()
        try:
            await self.greeClimateApi.sync_status()
        finally:
            self.semaphore.release()