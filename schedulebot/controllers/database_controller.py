import logging
import sqlite3 as sql
from datetime import datetime
from pathlib import Path
from typing import Any

from schedulebot.singleton import Singleton

logger = logging.getLogger(__name__)


class DatabaseController(metaclass=Singleton):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection: sql.Connection | None = None
        self.cursor: sql.Cursor | None = None
        self.scripts: dict[str, str] = {}
        self.load_scripts()

    def load_scripts(self) -> None:
        scripts_folder = Path(__file__).resolve().parent.parent / "database"
        if scripts_folder.exists():
            for script_path in scripts_folder.glob("*.sql"):
                with open(script_path, encoding="utf-8") as file:
                    self.scripts[script_path.name] = file.read()

    def get_script(self, script_name: str) -> str:
        return self.scripts.get(script_name, "")

    def connect(self) -> None:
        if self.connection is not None:
            return
        # Ensure parent directory exists if db_name includes directories
        db_path = Path(self.db_name)
        if db_path.parent and str(db_path.parent) != ".":
            db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sql.connect(self.db_name)
        self.connection.row_factory = sql.Row
        self.cursor = self.connection.cursor()
        self.init_tables()
        self.seed_initial_data()

    def init_tables(self) -> None:
        """Create database tables if they do not exist."""
        script = self.get_script("create_tables.sql")
        if script and self.connection:
            try:
                self.connection.executescript(script)
                self.connection.commit()
                logger.info("Database tables initialized successfully.")
            except Exception as e:
                logger.error(f"Error initializing tables: {e}")

    def seed_initial_data(self) -> None:
        """Seed default disciplines, teachers, and timetable if database is empty."""
        if not self.cursor or not self.connection:
            return
        try:
            self.cursor.execute("SELECT COUNT(*) FROM teachers")
            count = self.cursor.fetchone()[0]
            if count == 0:
                script = self.get_script("seed_data.sql")
                if script:
                    self.connection.executescript(script)
                    self.connection.commit()
                    logger.info("Database seeded with initial SUITT schedule data.")
        except Exception as e:
            logger.warning(f"Could not check or seed initial data: {e}")

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, script_name: str, *args: Any, fetch_count: int = -1) -> Any | None:
        result = None
        if self.cursor is None or self.connection is None:
            self.connect()

        script = self.get_script(script_name)
        if not script:
            logger.error(f"SQL script not found: {script_name}")
            return None

        try:
            self.cursor.execute(script, args)
            self.connection.commit()
            match fetch_count:
                case -1:
                    result = self.cursor.fetchall()
                case 1:
                    result = self.cursor.fetchone()
                case _:
                    result = self.cursor.fetchmany(fetch_count)
        except Exception as e:
            logger.error(f"Error with script {script_name}: {e}")
            if self.connection:
                self.connection.rollback()
        return result

    def add_new_lesson(
        self,
        day_of_week: int,
        time: str,
        teacher_id: int,
        discipline_id: int,
        zoom_link: str,
        period: str,
        additional_info: str,
        type: int,
    ):
        return self.execute(
            "add_new_lesson.sql",
            day_of_week,
            time,
            teacher_id,
            discipline_id,
            zoom_link,
            period,
            additional_info,
            type,
        )

    def clear_lessons(self):
        return self.execute("clear_schedule.sql")

    def recreate_tables(self):
        return self.init_tables()

    def get_day_lessons(self, week_day: int = -1):
        if week_day == -1:
            week_day = datetime.now().weekday()
        return self.execute("get_day_lessons.sql", week_day)

    def get_next_lesson(self, week_day: int = -1, after_time: str = "now"):
        if week_day == -1:
            week_day = datetime.now().weekday()
        if after_time == "now":
            after_time = datetime.now().strftime("%H:%M")
        return self.execute("get_next_lesson.sql", week_day, after_time, fetch_count=1)
