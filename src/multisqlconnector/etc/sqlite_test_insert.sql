-- --------------------------------------------------------
-- Gazdagép:                     C:\CODE\GitHub\MultiSqlConnector\testdb_sqlite_01.db|C:\CODE\GitHub\MultiSqlConnector\testdb_sqlite.db|C:\CODE\GitHub\MultiSqlConnector\test_sqlite.db
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

-- Tábla adatainak mentése testdb_sqlite_01.testtable: 3 rows
/*!40000 ALTER TABLE "testtable" DISABLE KEYS */;
INSERT INTO "testtable" ("id", "value1", "value2") VALUES
	(1, 85, 'test_sqlite.db - 2026-07-06T18:12:33.997757'),
	(2, 23, 'test_sqlite.db - 2026-07-06T18:12:39.527990'),
	(3, 88, 'test_sqlite.db - 2026-07-06T18:12:40.123456'),
	(4, 50, 'test_sqlite.db - 2026-07-06T18:12:40.777777');
/*!40000 ALTER TABLE "testtable" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
