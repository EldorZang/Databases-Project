CREATE DATABASE  IF NOT EXISTS `fungeo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fungeo`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: fungeo
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user1','user1'),(2,'user2','user2'),(3,'user3','user3'),(4,'user4','user4'),(5,'user5','user5'),(6,'user6','user6'),(7,'user7','user7'),(8,'user8','user8'),(9,'user9','user9'),(10,'user10','user10'),(11,'user11','user11'),(12,'user12','user12'),(13,'user13','user13'),(14,'user14','user14'),(15,'user15','user15'),(16,'user16','user16'),(17,'user17','user17'),(18,'user18','user18'),(19,'user19','user19'),(20,'user20','user20'),(21,'user21','user21'),(22,'user22','user22'),(23,'user23','user23'),(24,'user24','user24'),(25,'user25','user25'),(26,'user26','user26'),(27,'user27','user27'),(28,'user28','user28'),(29,'user29','user29'),(30,'user30','user30'),(31,'user31','user31'),(32,'user32','user32'),(33,'user33','user33'),(34,'user34','user34'),(35,'user35','user35'),(36,'user36','user36'),(37,'user37','user37'),(38,'user38','user38'),(39,'user39','user39'),(40,'user40','user40'),(41,'user41','user41'),(42,'user42','user42'),(43,'user43','user43'),(44,'user44','user44'),(45,'user45','user45'),(46,'user46','user46'),(47,'user47','user47'),(48,'user48','user48'),(49,'user49','user49'),(50,'user50','user50'),(51,'user51','user51'),(52,'user52','user52'),(53,'user53','user53'),(54,'user54','user54'),(55,'user55','user55'),(56,'user56','user56'),(57,'user57','user57'),(58,'user58','user58'),(59,'user59','user59'),(60,'user60','user60'),(61,'user61','user61'),(62,'user62','user62'),(63,'user63','user63'),(64,'user64','user64'),(65,'user65','user65'),(66,'user66','user66'),(67,'user67','user67'),(68,'user68','user68'),(69,'user69','user69'),(70,'user70','user70'),(71,'user71','user71'),(72,'user72','user72'),(73,'user73','user73'),(74,'user74','user74'),(75,'user75','user75'),(76,'user76','user76'),(77,'user77','user77'),(78,'user78','user78'),(79,'user79','user79'),(80,'user80','user80'),(81,'user81','user81'),(82,'user82','user82'),(83,'user83','user83'),(84,'user84','user84'),(85,'user85','user85'),(86,'user86','user86'),(87,'user87','user87'),(88,'user88','user88'),(89,'user89','user89'),(90,'user90','user90'),(91,'user91','user91'),(92,'user92','user92'),(93,'user93','user93'),(94,'user94','user94'),(95,'user95','user95'),(96,'user96','user96'),(97,'user97','user97'),(98,'user98','user98'),(99,'user99','user99'),(100,'user100','user100'),(101,'user101','user101'),(102,'user102','user102'),(103,'user103','user103'),(104,'user104','user104'),(105,'user105','user105'),(106,'user106','user106'),(107,'user107','user107'),(108,'user108','user108'),(109,'user109','user109'),(110,'user110','user110'),(111,'user111','user111'),(112,'user112','user112'),(113,'user113','user113'),(114,'user114','user114'),(115,'user115','user115'),(116,'user116','user116'),(117,'user117','user117'),(118,'user118','user118'),(119,'user119','user119'),(120,'user120','user120'),(121,'user121','user121'),(122,'user122','user122'),(123,'user123','user123'),(124,'user124','user124'),(125,'user125','user125'),(126,'user126','user126'),(127,'user127','user127'),(128,'user128','user128'),(129,'user129','user129'),(130,'user130','user130'),(131,'user131','user131'),(132,'user132','user132'),(133,'user133','user133'),(134,'user134','user134'),(135,'user135','user135'),(136,'user136','user136'),(137,'user137','user137'),(138,'user138','user138'),(139,'user139','user139'),(140,'user140','user140'),(141,'user141','user141'),(142,'user142','user142'),(143,'user143','user143'),(144,'user144','user144'),(145,'user145','user145'),(146,'user146','user146'),(147,'user147','user147'),(148,'user148','user148'),(149,'user149','user149'),(150,'user150','user150'),(151,'user151','user151'),(152,'user152','user152'),(153,'user153','user153'),(154,'user154','user154'),(155,'user155','user155'),(156,'user156','user156'),(157,'user157','user157'),(158,'user158','user158'),(159,'user159','user159'),(160,'user160','user160'),(161,'user161','user161'),(162,'user162','user162'),(163,'user163','user163'),(164,'user164','user164'),(165,'user165','user165'),(166,'user166','user166'),(167,'user167','user167'),(168,'user168','user168'),(169,'user169','user169'),(170,'user170','user170'),(171,'user171','user171'),(172,'user172','user172'),(173,'user173','user173'),(174,'user174','user174'),(175,'user175','user175'),(176,'user176','user176'),(177,'user177','user177'),(178,'user178','user178'),(179,'user179','user179'),(180,'user180','user180'),(181,'user181','user181'),(182,'user182','user182'),(183,'user183','user183'),(184,'user184','user184'),(185,'user185','user185'),(186,'user186','user186'),(187,'user187','user187'),(188,'user188','user188'),(189,'user189','user189'),(190,'user190','user190'),(191,'user191','user191'),(192,'user192','user192'),(193,'user193','user193'),(194,'user194','user194'),(195,'user195','user195'),(196,'user196','user196'),(197,'user197','user197'),(198,'user198','user198'),(199,'user199','user199'),(200,'user200','user200');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_user_insert` BEFORE INSERT ON `user` FOR EACH ROW BEGIN
        DECLARE user_count INT;
        
        SELECT COUNT(*) INTO user_count FROM User WHERE username = NEW.username;
        
        IF user_count > 0 THEN
            SIGNAL SQLSTATE '23000' SET MESSAGE_TEXT = 'User already exists';
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-05 23:11:01
