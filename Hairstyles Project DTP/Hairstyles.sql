--
-- File generated with SQLiteStudio v3.4.4 on Wed Apr 9 14:00:00 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Faceshapes
CREATE TABLE IF NOT EXISTS Faceshapes (faceshape_id INTEGER PRIMARY KEY AUTOINCREMENT, faceshape_name TEXT);

-- Table: Hairstyles
CREATE TABLE IF NOT EXISTS Hairstyles (hairstyle_id INTEGER PRIMARY KEY AUTOINCREMENT, hairstyle_name TEXT NOT NULL, hair_type TEXT, hairstyle_length TEXT, image_id INTEGER REFERENCES Images (image_id), faceshape_id INTEGER REFERENCES Faceshapes (faceshape_id));

-- Table: Images
CREATE TABLE IF NOT EXISTS Images (image_id INTEGER PRIMARY KEY AUTOINCREMENT, image_url TEXT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
