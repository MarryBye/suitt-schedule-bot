import os
from datetime import date, timedelta
from json import load as json_load
from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from schedulebot.apps import Apps
from schedulebot.functions import form_day_schedule, form_next_lesson, get_week
from schedulebot.language import lessons_time, week_days
from schedulebot.schedulebot import ScheduleBot

router: Router = Router(name=__name__)


async def form_schedule(d: date, apps: Apps):
    week_day = d.weekday()
    week_number = get_week(d)
    day_schedule = apps.database_controller.get_day_lessons(week_day)
    text_title = (
        f"📆 <b>{week_days.get(week_day, '')}, {d.strftime('%d.%m.%Y')}, "
        f"Тиждень #{week_number}</b>\n"
    )
    msg_text = text_title + form_day_schedule(day_schedule, d)
    keyboard = apps.keyboards_controller.get_keyboard("show_schedule")
    return msg_text, keyboard


@router.message(Command("start"))
@router.message(Command("help"))
async def start_help(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    help_text = (
        "👋 <b>SUITT Schedule & AI Notes Assistant</b>\n\n"
        "Available commands:\n"
        "• /show_schedule — View class schedule with interactive day navigation\n"
        "• /next_lesson — Display the next upcoming lesson for today\n"
        "• /custom_prompt <code>&lt;prompt&gt;</code> — "
        "Ask Google Gemini AI about classes or lecture notes\n"
        "• /help — Show this help message"
    )
    await msg.reply(text=help_text, parse_mode="HTML")


@router.message(Command("show_schedule"))
async def show_schedule(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    today_date = date.today()
    session["date"] = today_date

    msg_text, keyboard = await form_schedule(today_date, apps)
    await msg.reply(
        text=msg_text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@router.callback_query(lambda call: bool(call.data and call.data.startswith("schedule_selector|")))
async def schedule_change_day(
    call: CallbackQuery, bot: ScheduleBot, session: dict, apps: Apps
) -> None:
    await call.answer()
    current_date = session.get("date")
    if current_date is None:
        current_date = date.today()
        session["date"] = current_date

    parts = call.data.split("|")
    action = parts[1] if len(parts) > 1 else ""

    if action == "plus_day":
        session["date"] = current_date + timedelta(days=1)
    elif action == "minus_day":
        session["date"] = current_date - timedelta(days=1)

    msg_text, keyboard = await form_schedule(session["date"], apps)
    if call.message:
        await call.message.edit_text(
            text=msg_text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=keyboard,
        )


@router.message(Command("next_lesson"))
async def next_lesson(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    next_lesson_data = apps.database_controller.get_next_lesson()
    msg_text = form_next_lesson(next_lesson_data)
    await msg.reply(msg_text, parse_mode="HTML", disable_web_page_preview=True)


@router.message(Command("load_new_schedule"))
async def load_new_schedule(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    if not os.path.exists("schedule.json"):
        await msg.reply("Error: <code>schedule.json</code> not found on server.", parse_mode="HTML")
        return

    apps.database_controller.clear_lessons()

    try:
        with open("schedule.json", encoding="UTF-8") as file:
            data: list[list[dict[str, Any] | None]] = json_load(file)

            for day in range(len(data)):
                day_lessons = data[day]
                for lesson in range(len(day_lessons)):
                    lesson_data = day_lessons[lesson]
                    if lesson_data is None:
                        continue

                    apps.database_controller.add_new_lesson(
                        day,
                        lessons_time[lesson],
                        lesson_data["teacher_id"],
                        lesson_data["discipline_id"],
                        lesson_data["zoom_link"],
                        lesson_data["period"],
                        lesson_data.get("info", ""),
                        lesson_data["type"],
                    )

        await msg.reply("Schedule reloaded successfully from schedule.json.", parse_mode="HTML")
    except Exception as e:
        await msg.reply(f"Failed to load schedule: {e}")
