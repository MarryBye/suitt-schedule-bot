import re
from datetime import date, datetime, timedelta
from typing import Any

from schedulebot.language import (
    discipline_types,
    lesson_text_template,
    lesson_types,
    lessons_time,
    numbers_emojis,
)


def normalize_string(s: str) -> str:
    return " ".join(s.split())


def get_lesson_number(lesson: dict[str, Any]) -> int | None:
    time_str = str(lesson.get("time", ""))
    parts = time_str.split(":")
    if len(parts) >= 2:
        start_time = f"{parts[0]}:{parts[1]}"
        if start_time in lessons_time.values():
            return list(lessons_time.values()).index(start_time)
    return None


def get_week(d: date | None = None) -> int:
    if d is None:
        d = date.today()
    first_week = date(year=2024, month=8, day=5)
    today_week = (d - first_week).days // 7
    return today_week % 52 + 1


def form_lesson(lesson: dict[str, Any]) -> str:
    lesson_idx = get_lesson_number(lesson)
    lesson_number = numbers_emojis.get(lesson_idx, "📌")

    time_str = str(lesson.get("time", "08:00:00"))
    try:
        start_dt = datetime.strptime(time_str, "%H:%M:%S")
    except ValueError:
        try:
            start_dt = datetime.strptime(time_str, "%H:%M")
        except ValueError:
            start_dt = datetime.now()

    end_dt = start_dt + timedelta(hours=1, minutes=20)
    start_time = start_dt.strftime("%H:%M")
    end_time = end_dt.strftime("%H:%M")

    lesson_type = lesson_types.get(lesson.get("type", 1), "Заняття")
    discipline_type = discipline_types.get(lesson.get("is_exam_discipline", 0), "Ні")
    teacher = lesson.get("teacher") or "Не вказано"
    discipline_name = lesson.get("discipline_name") or "Без назви"
    period = lesson.get("period") or "-"
    info = lesson.get("info") or "No information"
    zoom_link = lesson.get("zoom_link") or "#"

    return lesson_text_template % (
        lesson_number,
        discipline_name,
        start_time,
        end_time,
        teacher,
        lesson_type,
        discipline_type,
        period,
        info,
        zoom_link,
    )


def is_actual_lesson(lesson: dict[str, Any], d: date | None = None) -> bool:
    if d is None:
        d = date.today()
    period_str = str(lesson.get("period", ""))
    if "-" in period_str:
        try:
            parts = [int(p.strip()) for p in period_str.split("-")]
            if len(parts) == 2:
                today_week = get_week(d)
                return parts[0] <= today_week <= parts[1]
        except (ValueError, IndexError):
            return True
    return True


def form_day_schedule(day_schedule: list[Any] | None, d: date | None = None) -> str:
    if d is None:
        d = date.today()
    if not day_schedule:
        return "\nСьогодні вихідний"

    msg_text = ""
    for lesson in day_schedule:
        if is_actual_lesson(dict(lesson), d):
            msg_text += form_lesson(dict(lesson))

    return msg_text if msg_text else "\nСьогодні вихідний або пар немає"


def form_next_lesson(lesson: Any | None) -> str:
    if lesson is None:
        return "\nСьогодні більше немає пар!"

    lesson_dict = dict(lesson)
    if is_actual_lesson(lesson_dict):
        return form_lesson(lesson_dict)

    return "\nСьогодні більше немає пар!"


def command_args_to_kvalues(msg: str) -> dict[str, str]:
    kvalue_template = r'(\w+)="([^"]+)"'
    return dict(re.findall(kvalue_template, msg))


def get_rows_from_kvalues(
    rows: list[dict[str, Any]], kvalues: dict[str, Any]
) -> list[dict[str, Any]]:
    filtered = rows
    for key, val in kvalues.items():
        if key in ("creation_date", "author_username", "chat_id"):
            filtered = [r for r in filtered if r.get(key) == val]
        elif key == "creation_time":
            filtered = [r for r in filtered if str(r.get(key, "")) >= str(val)]
    return filtered
