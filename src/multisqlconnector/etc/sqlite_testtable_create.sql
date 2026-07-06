-- --------------------------------------------------------
-- Gazdagép:                     C:\CODE\GitHub\MultiSqlConnector\testdb_sqlite_01.db
-- Szerver verzió:               3.51.0
-- Szerver OS:                   
-- HeidiSQL Verzió:              12.15.0.7171
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Adatbázis struktúra mentése a testdb_sqlite_01.
CREATE DATABASE IF NOT EXISTS "testdb_sqlite_01";
;

-- Struktúra mentése tábla testdb_sqlite_01. testtable
CREATE TABLE IF NOT EXISTS testtable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value1 INTEGER NULL,
    value2 TEXT NULL
);

-- Tábla adatainak mentése testdb_sqlite_01.testtable: 3 rows
/*!40000 ALTER TABLE "testtable" DISABLE KEYS */;
INSERT INTO "testtable" ("id", "value1", "value2") VALUES
	(2, 92, 'testdb_sqlite_01.db - 2026-07-06T17:56:23.377732'),
	(3, 35, 'testdb_sqlite_01.db - 2026-07-06T17:56:27.347186'),
	(4, 24, 'testdb_sqlite_01.db - 2026-07-06T17:56:31.026286');
/*!40000 ALTER TABLE "testtable" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
