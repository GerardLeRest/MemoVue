PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS eleves_classes_options;
DROP TABLE IF EXISTS eleves;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS options;

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classe TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eleves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    photo TEXT
);

CREATE TABLE IF NOT EXISTS options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    option TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eleves_classes_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_eleve INTEGER,
    id_classe INTEGER,
    id_option INTEGER,
    FOREIGN KEY (id_eleve) REFERENCES eleves(id),
    FOREIGN KEY (id_classe) REFERENCES classes(id),
    FOREIGN KEY (id_option) REFERENCES options(id)
);
