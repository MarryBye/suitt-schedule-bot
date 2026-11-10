import logging

import aiogram

from schedulebot.config import SQLITE_DBFILE
from schedulebot.controllers.database_controller import DatabaseController

logger = logging.getLogger(__name__)

router: aiogram.Router = aiogram.Router(name=__name__)
db_controller = DatabaseController(SQLITE_DBFILE)


@router.startup()
async def on_startup() -> None:
    logger.info("Bot starting up...")
    db_controller.connect()


@router.shutdown()
async def on_shutdown() -> None:
    logger.info("Bot shutting down...")
    db_controller.disconnect()
