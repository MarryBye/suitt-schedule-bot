-- Initial seed data for SUITT Schedule Bot
INSERT OR IGNORE INTO "teachers" ("id", "name", "lastname", "surname") VALUES
(1, 'Сергій', 'Щерба', 'Юрійович'),
(2, 'Людмила', 'Глазунова', 'Володимірівна'),
(3, 'Ігор', 'Перекрестов', 'Сергійович'),
(4, 'Ліаліна', 'Косирєва', 'Олексіївна'),
(5, 'Юрій', 'Бабіч', 'Олегович'),
(6, 'Євгеній', 'Малахов', 'Валерійович'),
(7, 'Тетяна', 'Калініна', 'Олександрівна');

INSERT OR IGNORE INTO "disciplines" ("id", "name", "is_exam") VALUES
(1, 'Дизайн та інтерфейси', 0),
(2, 'Бази даних', 0),
(3, 'Обчислювальні методи', 1),
(4, 'Об''єктно орієнтоване програмування', 1),
(5, 'Веб-програмування', 0);

INSERT OR IGNORE INTO "schedule" ("id", "day_of_week", "time", "teacher_id", "discipline_id", "zoom_link", "period", "additional_info", "type") VALUES
(217, '0', '09:35:00', 1, 1, 'https://us05web.zoom.us/j/8100569779?pwd=IGzcTw3ldY9ERkItB1kFb2kuGF8bY5.1', '31-43', 'No information', 2),
(218, '0', '11:10:00', 3, 1, 'https://us04web.zoom.us/j/77741108085?pwd=7W89XgPs64WT8z8aBBsMCo7yhTN26i.1', '30-40', 'No information', 1),
(219, '1', '08:00:00', 2, 2, 'https://us04web.zoom.us/j/4074773619?pwd=cnd4SWM3Q0ZaME05dWlsdUMrM2NoQT09', '35-43', 'No information', 2),
(220, '1', '09:35:00', 7, 3, 'https://us05web.zoom.us/j/8572022979?pwd=OG5zb0hGYWpyaUVVWEFITkxGZXRjQT09', '30-40', 'No information', 1),
(221, '1', '11:10:00', 2, 2, 'https://us04web.zoom.us/j/4074773619?pwd=cnd4SWM3Q0ZaME05dWlsdUMrM2NoQT09', '32-39', 'Для підгрупи Глазунової', 3),
(222, '1', '14:20:00', 1, 2, 'https://us05web.zoom.us/j/8100569779?pwd=IGzcTw3ldY9ERkItB1kFb2kuGF8bY5.1', '32-39', 'Для підгрупи Щерби', 3),
(223, '2', '08:00:00', 4, 4, 'https://us04web.zoom.us/j/6510832909?pwd=MjQ5blM4NFRQb1BjL3RZV0QvRzluUT09', '30-39', 'Друге посилання: https://us05web.zoom.us/j/3742741320?pwd=4WaOOgvlOe23k2LI3rSfUZIxtoALo2.1', 1),
(224, '2', '09:35:00', 7, 3, 'https://us05web.zoom.us/j/8572022979?pwd=OG5zb0hGYWpyaUVVWEFITkxGZXRjQT09', '30-43', 'No information', 2),
(225, '2', '11:10:00', 7, 3, 'https://us05web.zoom.us/j/8572022979?pwd=OG5zb0hGYWpyaUVVWEFITkxGZXRjQT09', '30-37', 'No information', 2),
(226, '2', '12:45:00', 4, 4, 'https://us04web.zoom.us/j/6510832909?pwd=MjQ5blM4NFRQb1BjL3RZV0QvRzluUT09', '31-39', 'Друге посилання: https://us05web.zoom.us/j/3742741320?pwd=4WaOOgvlOe23k2LI3rSfUZIxtoALo2.1', 2),
(227, '3', '08:00:00', 5, 5, 'https://us05web.zoom.us/j/3188670893?pwd=cDhJcnlmWVp2RkJDemxsZnBFS2dLZz09', '30-40', 'No information', 1),
(228, '3', '12:45:00', 4, 4, 'https://us04web.zoom.us/j/6510832909?pwd=MjQ5blM4NFRQb1BjL3RZV0QvRzluUT09', '31-39', 'Друге посилання: https://us05web.zoom.us/j/3742741320?pwd=4WaOOgvlOe23k2LI3rSfUZIxtoALo2.1', 3),
(229, '4', '08:00:00', 6, 2, 'https://us04web.zoom.us/j/3769997581?pwd=WEtHK0llaWZmTWtmTnhPUlVqRmlGUT09', '30-43', 'Обов''язкова присутність на парі. Не запізнюватись більше ніж на 5 хвилин.', 1),
(230, '4', '09:35:00', 5, 5, 'https://us05web.zoom.us/j/3188670893?pwd=cDhJcnlmWVp2RkJDemxsZnBFS2dLZz09', '32-42', 'No information', 2),
(231, '4', '12:45:00', 1, 1, 'https://us05web.zoom.us/j/8100569779?pwd=IGzcTw3ldY9ERkItB1kFb2kuGF8bY5.1', '31-39', 'No information', 2);
