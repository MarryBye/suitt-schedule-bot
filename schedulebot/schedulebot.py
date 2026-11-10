import asyncio
import logging
from datetime import datetime
from typing import Any

import aiogram

from schedulebot.middlewares.apps_container_middleware import AppsMiddleware
from schedulebot.middlewares.bot_middleware import BotMiddleware
from schedulebot.middlewares.session_middleware import SessionMiddleware
from schedulebot.singleton import Singleton

logger = logging.getLogger(__name__)


class ScheduleBot(aiogram.Bot, metaclass=Singleton):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dispatcher = aiogram.Dispatcher()

    async def run(self, routers: list[aiogram.Router] | None = None) -> None:
        if routers:
            self.dispatcher.include_routers(*routers)

        self.dispatcher.update.middleware(BotMiddleware(self))
        self.dispatcher.update.middleware(SessionMiddleware(self))
        self.dispatcher.update.middleware(AppsMiddleware(self))

        asyncio.create_task(self.heart_beat())
        logger.info("Bot polling started.")
        await self.dispatcher.start_polling(self)

    async def heart_beat(self) -> None:
        while True:
            logger.debug("Bot Heart Beat: alive at %s", datetime.now().isoformat())
            sleep_time = 60 - datetime.now().second
            await asyncio.sleep(max(1, sleep_time))
