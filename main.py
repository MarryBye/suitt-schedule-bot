import asyncio
import logging
import sys

from schedulebot.config import BOT_TOKEN
from schedulebot.controllers.database_controller import DatabaseController
from schedulebot.keyboards.show_schedule import KEYBOARD  # noqa: F401
from schedulebot.routers.ai_router import router as ai_router
from schedulebot.routers.commands_router import router as commands_router
from schedulebot.routers.main_router import router as main_router
from schedulebot.schedulebot import ScheduleBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "your_telegram_bot_token":
        logger.error(
            "BOT_TOKEN is not set or using placeholder. "
            "Please configure BOT_TOKEN in your .env file or environment."
        )
        sys.exit(1)

    logger.info("Initializing database...")
    db = DatabaseController()
    db.connect()

    bot = ScheduleBot(token=BOT_TOKEN)
    logger.info("Starting SUITT Schedule Bot...")
    try:
        asyncio.run(bot.run([main_router, commands_router, ai_router]))
    except Exception as e:
        logger.warning(
            "Telegram polling encountered an error (e.g. invalid mock token): %s",
            e,
        )


if __name__ == "__main__":
    main()
