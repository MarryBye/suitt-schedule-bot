CREATE TABLE IF NOT EXISTS "teachers" (
	"id"	INTEGER,
	"name"	TEXT,
	"lastname"	TEXT,
	"surname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "disciplines" (
	"id"	INTEGER,
	"name"	TEXT,
	"is_exam"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	INTEGER,
	"day_of_week"	TEXT,
	"time"	TEXT,
	"teacher_id"	INTEGER,
	"discipline_id"	INTEGER,
	"zoom_link"	TEXT,
	"period"	TEXT,
	"additional_info"	TEXT,
	"type"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("discipline_id") REFERENCES "disciplines"("id"),
	FOREIGN KEY("teacher_id") REFERENCES "teachers"("id")
);

CREATE TABLE IF NOT EXISTS "messages" (
	"id"	INTEGER,
	"author_id"	INTEGER,
	"author_name"	TEXT,
	"author_username"	TEXT,
	"creation_date"	TEXT,
	"creation_time"	TEXT,
	"chat_id"	INTEGER,
	"chat_type"	TEXT,
	"text"	TEXT,
	"is_answer"	INTEGER,
	"answerred_text"	TEXT,
	"answerred_author_id"	INTEGER,
	"answerred_author_name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "ai_chat_notes" (
	"id"	INTEGER,
	"chat_id"	INTEGER,
	"note_text"	TEXT,
	"note_date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
