-- Active la gestion des clés étrangères
PRAGMA foreign_keys = ON;

-- Supprime les tables si elles existent déjà
DROP TABLE IF EXISTS personnes_specialites;
DROP TABLE IF EXISTS specialites;
DROP TABLE IF EXISTS personnes;

-- Table principale : personnes
CREATE TABLE personnes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prenom TEXT NOT NULL,
    nom TEXT NOT NULL,
    structure TEXT NOT NULL,
    photo TEXT
);

-- Table des spécialités (ex-options, responsabilités, etc.)
CREATE TABLE specialites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    specialite TEXT NOT NULL UNIQUE
);

-- Table de liaison personnes <-> spécialités
CREATE TABLE personnes_specialites (
    id_personne INTEGER,
    id_specialite INTEGER,
    PRIMARY KEY (id_personne, id_specialite),
    FOREIGN KEY (id_personne) REFERENCES personnes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_specialite) REFERENCES specialites(id) ON DELETE CASCADE
);

