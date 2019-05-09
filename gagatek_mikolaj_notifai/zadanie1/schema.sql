-- Zadanie rekrutacyjne Daftcode, Notif.AI.
-- Zadanie 1.
-- Autor: Mikolaj Gagatek
-- email: mikolaj.gagatek@gmail.com
CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  done BOOLEAN,
  author_ip TEXT,
  created_date TIMESTAMP,
  done_date TIMESTAMP
);
