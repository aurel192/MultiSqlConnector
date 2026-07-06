-- --------------------------------------------------------
-- Gazdagép:                     127.0.0.1
-- Szerver verzió:               10.4.32-MariaDB - mariadb.org binary distribution
-- Szerver OS:                   Win64
-- HeidiSQL Verzió:              12.15.0.7171
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Adatbázis struktúra mentése a test_db_02.
CREATE DATABASE IF NOT EXISTS `test_db_02` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `test_db_02`;

-- Struktúra mentése tábla test_db_02. testtable
CREATE TABLE IF NOT EXISTS `testtable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value1` int(11) DEFAULT NULL,
  `value2` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tábla adatainak mentése test_db_02.testtable: ~4 rows (hozzávetőleg)
DELETE FROM `testtable`;
INSERT INTO `testtable` (`id`, `value1`, `value2`) VALUES
	(10, 19, 'test_db_02_2026-07-06T16:31:12.981530'),
	(11, 40, 'test_db_02_2026-07-06T16:32:12.606449'),
	(12, 30, 'test_db_02_2026-07-06T16:34:06.992797'),
	(13, 64, 'test_db_02_2026-07-06T16:35:17.268969');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
