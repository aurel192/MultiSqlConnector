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

-- Tábla adatainak mentése test_db_02.testtable: ~10 rows (hozzávetőleg)
INSERT INTO `testtable` (`id`, `value1`, `value2`) VALUES
	(75, 84, 'test_db_02_2026-07-06T16:31:12.972024'),
	(76, 51, 'test_db_02_2026-07-06T16:32:12.563790'),
	(77, 82, 'test_db_02_2026-07-06T16:32:12.584160'),
	(78, 58, 'test_db_02_2026-07-06T16:32:12.596965'),
	(79, 13, 'test_db_02_2026-07-06T16:34:06.949240'),
	(80, 27, 'test_db_02_2026-07-06T16:34:06.970602'),
	(81, 47, 'test_db_02_2026-07-06T16:34:06.983286'),
	(82, 73, 'test_db_02_2026-07-06T16:35:17.226610'),
	(83, 4, 'test_db_02_2026-07-06T16:35:17.244734'),
	(84, 12, 'test_db_02_2026-07-06T16:35:17.257572');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
