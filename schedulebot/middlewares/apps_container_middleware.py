from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from schedulebot.apps import Apps


class AppsMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["apps"] = Apps()
        return await handler(event, data)
