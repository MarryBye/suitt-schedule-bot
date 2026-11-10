import csv
import os
from typing import Any


class MessageHistory:
    def __init__(self, history_file: str):
        self.history_file = history_file
        self.rows: list[dict[str, Any]] = []
        if not os.path.exists(history_file):
            with open(history_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "author_id",
                        "author_name",
                        "author_username",
                        "creation_date",
                        "creation_time",
                        "chat_id",
                        "chat_type",
                        "text",
                        "is_answer",
                        "answerred_text",
                        "answerred_author_id",
                        "answerred_author_name",
                    ]
                )
        else:
            with open(history_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)

    def get_last_page(self, n: int = 25) -> int:
        return len(self.rows) // n

    def show_page(self, page: int, n: int = 25) -> list[dict[str, Any]]:
        last_page = self.get_last_page(n)
        if page < 0 or page > last_page:
            page = last_page
        start = page * n
        return self.rows[start : start + n]
