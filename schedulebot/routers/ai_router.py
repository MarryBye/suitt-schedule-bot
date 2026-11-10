from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from schedulebot.apps import Apps
from schedulebot.functions import command_args_to_kvalues
from schedulebot.schedulebot import ScheduleBot

router: Router = Router(name=__name__)


@router.message(Command("custom_prompt"))
async def custom_prompt(
    msg: Message,
    command: CommandObject,
    bot: ScheduleBot,
    session: dict,
    apps: Apps,
) -> None:
    if not command.args or not command.args.strip():
        await msg.reply(
            'Please specify a prompt. Example: /custom_prompt prompt="Summarize the lecture"'
        )
        return

    command_args_string: str = command.args.strip()
    kvalues = command_args_to_kvalues(command_args_string)

    if "prompt" in kvalues:
        prompt_text = kvalues["prompt"]
    else:
        prompt_text = command_args_string

    response = apps.ai_controller.generate_content(f"{prompt_text}.")
    await msg.reply(str(response))
