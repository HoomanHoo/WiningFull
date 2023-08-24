-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: bit
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `bit`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `bit` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `bit`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add win user',7,'add_winuser'),(26,'Can change win user',7,'change_winuser'),(27,'Can delete win user',7,'delete_winuser'),(28,'Can view win user',7,'view_winuser'),(29,'Can add win user account',8,'add_winuseraccount'),(30,'Can change win user account',8,'change_winuseraccount'),(31,'Can delete win user account',8,'delete_winuseraccount'),(32,'Can view win user account',8,'view_winuseraccount'),(33,'Can add win user favorite',9,'add_winuserfavorite'),(34,'Can change win user favorite',9,'change_winuserfavorite'),(35,'Can delete win user favorite',9,'delete_winuserfavorite'),(36,'Can view win user favorite',9,'view_winuserfavorite'),(37,'Can add win user grade',10,'add_winusergrade'),(38,'Can change win user grade',10,'change_winusergrade'),(39,'Can delete win user grade',10,'delete_winusergrade'),(40,'Can view win user grade',10,'view_winusergrade'),(41,'Can add win point his',11,'add_winpointhis'),(42,'Can change win point his',11,'change_winpointhis'),(43,'Can delete win point his',11,'delete_winpointhis'),(44,'Can view win point his',11,'view_winpointhis'),(45,'Can add win review',12,'add_winreview'),(46,'Can change win review',12,'change_winreview'),(47,'Can delete win review',12,'delete_winreview'),(48,'Can view win review',12,'view_winreview'),(49,'Can add win board',13,'add_winboard'),(50,'Can change win board',13,'change_winboard'),(51,'Can delete win board',13,'delete_winboard'),(52,'Can view win board',13,'view_winboard'),(53,'Can add win board img',14,'add_winboardimg'),(54,'Can change win board img',14,'change_winboardimg'),(55,'Can delete win board img',14,'delete_winboardimg'),(56,'Can view win board img',14,'view_winboardimg'),(57,'Can add win comment',15,'add_wincomment'),(58,'Can change win comment',15,'change_wincomment'),(59,'Can delete win comment',15,'delete_wincomment'),(60,'Can view win comment',15,'view_wincomment'),(61,'Can add win board like',16,'add_winboardlike'),(62,'Can change win board like',16,'change_winboardlike'),(63,'Can delete win board like',16,'delete_winboardlike'),(64,'Can view win board like',16,'view_winboardlike'),(65,'Can add win search',17,'add_winsearch'),(66,'Can change win search',17,'change_winsearch'),(67,'Can delete win search',17,'delete_winsearch'),(68,'Can view win search',17,'view_winsearch'),(69,'Can add win search n',18,'add_winsearchn'),(70,'Can change win search n',18,'change_winsearchn'),(71,'Can delete win search n',18,'delete_winsearchn'),(72,'Can view win search n',18,'view_winsearchn'),(73,'Can add win detail view',19,'add_windetailview'),(74,'Can change win detail view',19,'change_windetailview'),(75,'Can delete win detail view',19,'delete_windetailview'),(76,'Can view win detail view',19,'view_windetailview'),(77,'Can add win detail view n',20,'add_windetailviewn'),(78,'Can change win detail view n',20,'change_windetailviewn'),(79,'Can delete win detail view n',20,'delete_windetailviewn'),(80,'Can view win detail view n',20,'view_windetailviewn'),(81,'Can add win wine',21,'add_winwine'),(82,'Can change win wine',21,'change_winwine'),(83,'Can delete win wine',21,'delete_winwine'),(84,'Can view win wine',21,'view_winwine'),(85,'Can add win wine region',22,'add_winwineregion'),(86,'Can change win wine region',22,'change_winwineregion'),(87,'Can delete win wine region',22,'delete_winwineregion'),(88,'Can view win wine region',22,'view_winwineregion'),(89,'Can add win store',23,'add_winstore'),(90,'Can change win store',23,'change_winstore'),(91,'Can delete win store',23,'delete_winstore'),(92,'Can view win store',23,'view_winstore'),(93,'Can add win store excel',24,'add_winstoreexcel'),(94,'Can change win store excel',24,'change_winstoreexcel'),(95,'Can delete win store excel',24,'delete_winstoreexcel'),(96,'Can view win store excel',24,'view_winstoreexcel'),(97,'Can add win store url',25,'add_winstoreurl'),(98,'Can change win store url',25,'change_winstoreurl'),(99,'Can delete win store url',25,'delete_winstoreurl'),(100,'Can view win store url',25,'view_winstoreurl'),(101,'Can add win revenue',26,'add_winrevenue'),(102,'Can change win revenue',26,'change_winrevenue'),(103,'Can delete win revenue',26,'delete_winrevenue'),(104,'Can view win revenue',26,'view_winrevenue'),(105,'Can add win sell',27,'add_winsell'),(106,'Can change win sell',27,'change_winsell'),(107,'Can delete win sell',27,'delete_winsell'),(108,'Can view win sell',27,'view_winsell'),(109,'Can add win purchase',28,'add_winpurchase'),(110,'Can change win purchase',28,'change_winpurchase'),(111,'Can delete win purchase',28,'delete_winpurchase'),(112,'Can view win purchase',28,'view_winpurchase'),(113,'Can add win purchase detail',29,'add_winpurchasedetail'),(114,'Can change win purchase detail',29,'change_winpurchasedetail'),(115,'Can delete win purchase detail',29,'delete_winpurchasedetail'),(116,'Can view win purchase detail',29,'view_winpurchasedetail'),(117,'Can add win cart',30,'add_wincart'),(118,'Can change win cart',30,'change_wincart'),(119,'Can delete win cart',30,'delete_wincart'),(120,'Can view win cart',30,'view_wincart'),(121,'Can add win cart detail',31,'add_wincartdetail'),(122,'Can change win cart detail',31,'change_wincartdetail'),(123,'Can delete win cart detail',31,'delete_wincartdetail'),(124,'Can view win cart detail',31,'view_wincartdetail'),(125,'Can add win receive code',32,'add_winreceivecode'),(126,'Can change win receive code',32,'change_winreceivecode'),(127,'Can delete win receive code',32,'delete_winreceivecode'),(128,'Can view win receive code',32,'view_winreceivecode');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$5NbTZRRS2le9hnWxJQMndJ$d0aVNZwLGyYLceTrW3IVi0CS0Ce6upPMn63AIKlsbKQ=','2023-08-21 18:12:39.591581',1,'admin','','','',1,1,'2023-08-16 16:48:47.824082');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-08-16 16:49:20.183299','1','WinUserGrade object (1)',1,'[{\"added\": {}}]',10,1),(2,'2023-08-16 16:49:28.110860','2','WinUserGrade object (2)',1,'[{\"added\": {}}]',10,1),(3,'2023-08-16 17:08:57.192986','test1111','WinUser object (test1111)',2,'[{\"changed\": {\"fields\": [\"User profile img\"]}}]',7,1),(4,'2023-08-17 11:13:29.128040','1','WinWineRegion object (1)',1,'[{\"added\": {}}]',22,1),(5,'2023-08-17 11:13:36.110227','2','WinWineRegion object (2)',1,'[{\"added\": {}}]',22,1),(6,'2023-08-17 11:13:43.073892','3','WinWineRegion object (3)',1,'[{\"added\": {}}]',22,1),(7,'2023-08-17 11:15:24.568497','1','WinWine object (1)',1,'[{\"added\": {}}]',21,1),(8,'2023-08-17 11:16:10.781319','2','WinWine object (2)',1,'[{\"added\": {}}]',21,1),(9,'2023-08-17 11:16:52.701825','3','WinWine object (3)',1,'[{\"added\": {}}]',21,1),(10,'2023-08-17 11:37:08.769867','3','WinWine object (3)',3,'',21,1),(11,'2023-08-17 11:37:08.795142','2','WinWine object (2)',3,'',21,1),(12,'2023-08-17 11:37:08.815134','1','WinWine object (1)',3,'',21,1),(13,'2023-08-17 11:37:16.776101','3','WinWineRegion object (3)',3,'',22,1),(14,'2023-08-17 11:37:16.796293','2','WinWineRegion object (2)',3,'',22,1),(15,'2023-08-17 11:37:16.812520','1','WinWineRegion object (1)',3,'',22,1),(16,'2023-08-17 11:40:47.014438','1','WinWineRegion object (1)',1,'[{\"added\": {}}]',22,1),(17,'2023-08-17 11:40:52.939141','2','WinWineRegion object (2)',1,'[{\"added\": {}}]',22,1),(18,'2023-08-17 11:40:58.855948','3','WinWineRegion object (3)',1,'[{\"added\": {}}]',22,1),(19,'2023-08-17 11:41:07.007365','4','WinWineRegion object (4)',1,'[{\"added\": {}}]',22,1),(20,'2023-08-17 11:41:12.015841','5','WinWineRegion object (5)',1,'[{\"added\": {}}]',22,1),(21,'2023-08-17 11:41:18.401400','6','WinWineRegion object (6)',1,'[{\"added\": {}}]',22,1),(22,'2023-08-17 11:43:18.371044','test2222','WinUser object (test2222)',1,'[{\"added\": {}}]',7,1),(23,'2023-08-17 11:43:52.384295','test3333','WinUser object (test3333)',1,'[{\"added\": {}}]',7,1),(24,'2023-08-17 11:44:40.005533','1','WinStore object (1)',1,'[{\"added\": {}}]',23,1),(25,'2023-08-17 11:44:57.591468','2','WinStore object (2)',1,'[{\"added\": {}}]',23,1),(26,'2023-08-17 11:45:33.002521','1','WinSell object (1)',1,'[{\"added\": {}}]',27,1),(27,'2023-08-17 11:45:46.126387','2','WinSell object (2)',1,'[{\"added\": {}}]',27,1),(28,'2023-08-17 11:45:58.816944','3','WinSell object (3)',1,'[{\"added\": {}}]',27,1),(29,'2023-08-17 11:46:09.026774','4','WinSell object (4)',1,'[{\"added\": {}}]',27,1),(30,'2023-08-17 11:46:25.056341','5','WinSell object (5)',1,'[{\"added\": {}}]',27,1),(31,'2023-08-17 11:46:36.077371','6','WinSell object (6)',1,'[{\"added\": {}}]',27,1),(32,'2023-08-17 11:46:43.722349','7','WinSell object (7)',1,'[{\"added\": {}}]',27,1),(33,'2023-08-17 11:46:52.630078','8','WinSell object (8)',1,'[{\"added\": {}}]',27,1),(34,'2023-08-17 11:47:02.448402','9','WinSell object (9)',1,'[{\"added\": {}}]',27,1),(35,'2023-08-17 11:47:14.190546','10','WinSell object (10)',1,'[{\"added\": {}}]',27,1),(36,'2023-08-17 11:48:16.602418','1','WinSell object (1)',2,'[{\"changed\": {\"fields\": [\"Sell price\"]}}]',27,1),(37,'2023-08-19 17:13:08.420513','4','WinStore object (4)',1,'[{\"added\": {}}]',23,1),(38,'2023-08-21 10:48:27.315674','1','WinUserGrade object (1)',2,'[{\"changed\": {\"fields\": [\"User grade name\"]}}]',10,1),(39,'2023-08-21 10:48:33.487455','2','WinUserGrade object (2)',2,'[{\"changed\": {\"fields\": [\"User grade name\"]}}]',10,1),(40,'2023-08-21 10:49:24.953604','test0810','WinUser object (test0810)',2,'[{\"changed\": {\"fields\": [\"User point\"]}}]',7,1),(41,'2023-08-21 16:38:18.612330','2','WinReview object (2)',1,'[{\"added\": {}}]',12,1),(42,'2023-08-21 16:38:20.914447','2','WinReview object (2)',2,'[]',12,1),(43,'2023-08-21 16:38:33.555531','3','WinReview object (3)',1,'[{\"added\": {}}]',12,1),(44,'2023-08-21 16:38:48.193681','4','WinReview object (4)',1,'[{\"added\": {}}]',12,1),(45,'2023-08-21 16:39:00.330948','5','WinReview object (5)',1,'[{\"added\": {}}]',12,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(13,'board','winboard'),(14,'board','winboardimg'),(16,'board','winboardlike'),(15,'board','wincomment'),(5,'contenttypes','contenttype'),(19,'detail','windetailview'),(20,'detail','windetailviewn'),(21,'detail','winwine'),(22,'detail','winwineregion'),(30,'purchasing','wincart'),(31,'purchasing','wincartdetail'),(28,'purchasing','winpurchase'),(29,'purchasing','winpurchasedetail'),(32,'purchasing','winreceivecode'),(17,'search','winsearch'),(18,'search','winsearchn'),(6,'sessions','session'),(26,'store','winrevenue'),(27,'store','winsell'),(23,'store','winstore'),(24,'store','winstoreexcel'),(25,'store','winstoreurl'),(11,'user','winpointhis'),(12,'user','winreview'),(7,'user','winuser'),(8,'user','winuseraccount'),(9,'user','winuserfavorite'),(10,'user','winusergrade');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-08-16 12:38:39.277964'),(2,'auth','0001_initial','2023-08-16 12:38:41.091848'),(3,'admin','0001_initial','2023-08-16 12:38:41.507695'),(4,'admin','0002_logentry_remove_auto_add','2023-08-16 12:38:41.528205'),(5,'admin','0003_logentry_add_action_flag_choices','2023-08-16 12:38:41.550180'),(6,'contenttypes','0002_remove_content_type_name','2023-08-16 12:38:41.788451'),(7,'auth','0002_alter_permission_name_max_length','2023-08-16 12:38:41.958668'),(8,'auth','0003_alter_user_email_max_length','2023-08-16 12:38:42.008908'),(9,'auth','0004_alter_user_username_opts','2023-08-16 12:38:42.029853'),(10,'auth','0005_alter_user_last_login_null','2023-08-16 12:38:42.176745'),(11,'auth','0006_require_contenttypes_0002','2023-08-16 12:38:42.189024'),(12,'auth','0007_alter_validators_add_error_messages','2023-08-16 12:38:42.210008'),(13,'auth','0008_alter_user_username_max_length','2023-08-16 12:38:42.407888'),(14,'auth','0009_alter_user_last_name_max_length','2023-08-16 12:38:42.585764'),(15,'auth','0010_alter_group_name_max_length','2023-08-16 12:38:42.646323'),(16,'auth','0011_update_proxy_permissions','2023-08-16 12:38:42.686810'),(17,'auth','0012_alter_user_first_name_max_length','2023-08-16 12:38:42.855960'),(18,'sessions','0001_initial','2023-08-16 12:38:42.970600'),(22,'user','0001_initial','2023-08-16 16:40:44.391590'),(23,'board','0001_initial','2023-08-16 16:40:45.575035'),(24,'detail','0001_initial','2023-08-16 16:40:46.256919'),(25,'store','0001_initial','2023-08-16 16:40:47.503732'),(26,'purchasing','0001_initial','2023-08-16 16:40:48.894420'),(27,'search','0001_initial','2023-08-16 16:40:49.177928'),(28,'detail','0002_windetailview_user','2023-08-16 16:43:25.288434'),(29,'user','0002_winreview_sell','2023-08-16 16:43:25.514151'),(30,'user','0003_alter_winuser_user_profile_img','2023-08-16 17:08:12.406860');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0fhg3guueu1zhyyzecpzqax5qa68wi0d','.eJxVjDsOwjAQBe_iGlnrz3pjSnrOEK3jDQ6gWIqTCnF3iJQC2jcz76V63tbSb02WfsrqrIw6_W6Jh4fMO8h3nm9VD3VelynpXdEHbfpaszwvh_t3ULiVb-3sYDMaC96whC5KIkCfO-LRQerAIIWMMBL4xIRBxDmEaMg7S9EE9f4AuhI2Sw:1qWDIv:5k2E_UHEHE3AAzuGZx6JblvflpOBpwQRgClKUq5iaGQ','2023-08-30 18:59:05.842850'),('3403x3rwe922vqqpr85qy00i0fhs1uwj','eyJtZW1pZCI6InRlc3QxMTExIn0:1qWyjp:vhwjU3DiSmpnagiS-dIzA-eXmvApkWdDDJBbexHJ4U8','2023-09-01 21:38:01.118123'),('8o3w5pej6rrcy81kw6hib4auk247cn02','eyJtZW1pZCI6InRlc3QxMTExIn0:1qWaK7:OKTWGdjc4AievJ88062vwenJzs6f-R916p47sHfdcyk','2023-08-31 19:33:51.021065'),('cbd6gqwvq1bb2d9lnbfgeuhvergj22t6','eyJtZW1pZCI6InRlc3QwODEwIn0:1qXI24:KMg2h7UEIyHK3nuNUhDuaqljeCE141rrSHAh0rLq8Qg','2023-09-02 18:14:08.081357'),('hoe2pzpzugpe917jgtkw5t1wykyb5k05','eyJtZW1pZCI6InRlc3QxMTExIn0:1qWZA6:b26BGZyKxR1NJ8De4aBbrWXuTUYsnfHsU3JBSt_ng78','2023-08-31 18:19:26.653861'),('mhhqzpqb2aeoi91uvwvxai25t1vb70my','.eJxVj8tOwzAQRf8laxT5Eccxu6QIQQWKEA8VNpEfk0eL7Sp22gXi33FFF-0sz71zRvOTdXKJY7cEmLvJZLcZzm4umZJ6B-4UmK10g8-1d3GeVH6q5Oc05M_ewHdz7l4JRhnGtE2JJoZhggosoawEKI5YYSoue4pUhTDjpWGo56hQkrMSgFKGBOYFJVzgMkml1hBC9-bTkWS8r8POEOcOdvloh5d2ddz0Fm_31Wuj39df4e5hpu3RP60mt94MdV1_-uYgxGMyRbD7_28jhMjSJGjBXqPfP3YXWzc:1qWa81:-IBQ9ogUpWzGGVUalXSg24LN-Bt8Ue2l8bOvKX542SM','2023-08-31 19:21:21.423095'),('qygp6uc13pva77az6zeqfwgd2bh98cg4','.eJxVjDsOwjAQBe_iGlnrz3pjSnrOEK3jDQ6gWIqTCnF3iJQC2jcz76V63tbSb02WfsrqrIw6_W6Jh4fMO8h3nm9VD3VelynpXdEHbfpaszwvh_t3ULiVb-3sYDMaC96whC5KIkCfO-LRQerAIIWMMBL4xIRBxDmEaMg7S9EE9f4AuhI2Sw:1qXGKW:qqrY_ygFthmDyWxLMUdHq1cRVsWCxi4IHQ4w4cdQrY4','2023-09-02 16:25:04.971332'),('s378io1f6wev5eet6y5ini6b11vfnqxk','.eJxVUMtqwzAQ_Bedg9HTsnuLA6WHFEobCDkJPda2mtgKlpwQSv-9cptDs8eZ2ZlhvpDSc-rVHGFS3qEnRNDqP2a0PcK4EO5Tj10obBjT5E2xSIo7G4vX4ODU3LUPBr2Off5m1FInCMWcaCirGozEgrtK6pZhU2EiZOkEbiXmRktRAjAmcE0kZ1TWpMymQ3C-9eDUOcT0W5askLYWYlS7kJNzzE68H5ptN9g6SS70NfXzdbzQ9Usn0_PevHmlL3jaNhsfTsd1vkPYf8y3W7ZPMJz_JkgQE67ossQAwyP0_QOAmmLc:1qXzjg:JOasDytku1356KDPJergv0BoMQGFLJvrQyaVWFFw4UY','2023-09-04 16:54:04.206117'),('uy6ewb6nn7ey8pgl8z3j6gefp5qq92u8','.eJxdjMsOgjAQRf-la9NMn1NcuucbyJQOggpNaFkZ_10xbHR7zzn3KWaepyTOonKpELQSJ9HRVsduK7x2X_S3RervvOwg3Wi5Ztnnpa5TlLsiD1pkmxM_Lof7czBSGT-10b1OTmmwitiHhiOCsykgDQZiAOXQJwcDgo2EzjMb46BRaI3GRnnxegOp7DvQ:1qY3SZ:t5moZgd686vL3h-wEJIRFqhJIViiZ-Uvx6clseHSyn8','2023-09-04 20:52:39.065335'),('w2c95944ixo573pz0vasbc9hcihkwk0v','.eJxVjDsOwjAQBe_iGlnrz3pjSnrOEK3jDQ6gWIqTCnF3iJQC2jcz76V63tbSb02WfsrqrIw6_W6Jh4fMO8h3nm9VD3VelynpXdEHbfpaszwvh_t3ULiVb-3sYDMaC96whC5KIkCfO-LRQerAIIWMMBL4xIRBxDmEaMg7S9EE9f4AuhI2Sw:1qWyif:uvZgTXr-EPcgzmFlQ4xGiVXPsSeJfD9yZIzRyKRdyGs','2023-09-01 21:36:49.808361'),('w3sng9un4upmo3dfaaq7s8ahiafuwano','.eJxVjDsOwjAQBe_iGlnrz3pjSnrOEK3jDQ6gWIqTCnF3iJQC2jcz76V63tbSb02WfsrqrIw6_W6Jh4fMO8h3nm9VD3VelynpXdEHbfpaszwvh_t3ULiVb-3sYDMaC96whC5KIkCfO-LRQerAIIWMMBL4xIRBxDmEaMg7S9EE9f4AuhI2Sw:1qWynj:jzH9Wak6EPenxTBvH29t4tv55q8o69V1t88nbkjxZMk','2023-09-01 21:42:03.002255'),('yoel22ai7wwp4ofip2tt0rwpei85l56p','.eJxdjM0OgjAQhN-lZ9Nsf7d49O4zkG27CCqQ0HIyvrtguOgc5_tmXmLkccjiLCqXqraIk2hprX27Fl7aL_rrIqUHTzvId5pus0zzVJchyl2RBy3yOmd-Xg7356Cn0m9ro5POTmmwitiHhiOCszkgdQZiAOXQZwcdgo2EzjMb46BRaI3GRnnx_gClJTvJ:1qWSrM:pWzkGDSyemayNIKZ6_d3QEzY9TpkQw55a4if1MrjVnI','2023-08-31 11:35:40.066142'),('yy95gnkgbpt134mqnm32ovxvcp2m6mba','.eJxVjztPwzAUhf9LZoj8iO2ELWVokRLKUIayRH7ckKSNjWpb9CH-O67oQNfvnPNd3UvWyRiGLno4dKPJnjKcPfxnSuod2GtgJmk_Xa6dDYdR5ddKfkt93joD-8WteycYpB_SmhJNDMMEFVgCLytQArHClEL2FKkSYSa4YagXqFBSMA5AKUMVFgUlosI8SaXW4H23celIMr62etKNdWezVYJ-NDauh0ZPj32cX461Xa3j6W3Jq9Xz6Pbv33Vdb11LxOKYTAHmr79vA_iASowSnGG-Rz-_e5ZbPQ:1qXHik:OVq_eBCxdAv7QAY9FQM8LUv8HkVOphNuXjkZWEHh1x8','2023-09-02 17:54:10.169338');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_board`
--

DROP TABLE IF EXISTS `win_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_board` (
  `board_id` int NOT NULL AUTO_INCREMENT,
  `board_title` varchar(150) NOT NULL,
  `board_reg_time` datetime(6) NOT NULL,
  `board_content` longtext NOT NULL,
  `board_read_count` int NOT NULL,
  `board_ip` varchar(20) NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`board_id`),
  KEY `win_board_user_id_b70e74df_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_board_user_id_b70e74df_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_board`
--

LOCK TABLES `win_board` WRITE;
/*!40000 ALTER TABLE `win_board` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_board_img`
--

DROP TABLE IF EXISTS `win_board_img`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_board_img` (
  `board_img_id` int NOT NULL AUTO_INCREMENT,
  `board_image` varchar(150) NOT NULL,
  `board_id` int NOT NULL,
  PRIMARY KEY (`board_img_id`),
  KEY `win_board_img_board_id_fec1a52f_fk_win_board_board_id` (`board_id`),
  CONSTRAINT `win_board_img_board_id_fec1a52f_fk_win_board_board_id` FOREIGN KEY (`board_id`) REFERENCES `win_board` (`board_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_board_img`
--

LOCK TABLES `win_board_img` WRITE;
/*!40000 ALTER TABLE `win_board_img` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_board_img` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_board_like`
--

DROP TABLE IF EXISTS `win_board_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_board_like` (
  `board_like_id` int NOT NULL AUTO_INCREMENT,
  `board_like_time` datetime(6) NOT NULL,
  `board_id` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`board_like_id`),
  KEY `win_board_like_board_id_3d1b6ca4_fk_win_board_board_id` (`board_id`),
  KEY `win_board_like_user_id_e744930e_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_board_like_board_id_3d1b6ca4_fk_win_board_board_id` FOREIGN KEY (`board_id`) REFERENCES `win_board` (`board_id`),
  CONSTRAINT `win_board_like_user_id_e744930e_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_board_like`
--

LOCK TABLES `win_board_like` WRITE;
/*!40000 ALTER TABLE `win_board_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_board_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_cart`
--

DROP TABLE IF EXISTS `win_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `cart_time` datetime(6) NOT NULL,
  `cart_state` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `win_cart_user_id_3b370ddb_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_cart_user_id_3b370ddb_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_cart`
--

LOCK TABLES `win_cart` WRITE;
/*!40000 ALTER TABLE `win_cart` DISABLE KEYS */;
INSERT INTO `win_cart` VALUES (1,'2023-08-17 11:48:24.000000',-1,'test1111'),(2,'2023-08-21 11:10:09.000000',-1,'test0810'),(3,'2023-08-21 12:59:32.000000',-1,'test0810');
/*!40000 ALTER TABLE `win_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_cart_detail`
--

DROP TABLE IF EXISTS `win_cart_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_cart_detail` (
  `cart_det_id` int NOT NULL AUTO_INCREMENT,
  `cart_det_qnty` int NOT NULL,
  `cart_id` int NOT NULL,
  `sell_id` int NOT NULL,
  PRIMARY KEY (`cart_det_id`),
  KEY `win_cart_detail_cart_id_8e7ab089_fk_win_cart_cart_id` (`cart_id`),
  KEY `win_cart_detail_sell_id_ad11f854_fk_win_sell_sell_id` (`sell_id`),
  CONSTRAINT `win_cart_detail_cart_id_8e7ab089_fk_win_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `win_cart` (`cart_id`),
  CONSTRAINT `win_cart_detail_sell_id_ad11f854_fk_win_sell_sell_id` FOREIGN KEY (`sell_id`) REFERENCES `win_sell` (`sell_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_cart_detail`
--

LOCK TABLES `win_cart_detail` WRITE;
/*!40000 ALTER TABLE `win_cart_detail` DISABLE KEYS */;
INSERT INTO `win_cart_detail` VALUES (1,5,1,1),(3,8,2,43),(4,5,3,43);
/*!40000 ALTER TABLE `win_cart_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_comment`
--

DROP TABLE IF EXISTS `win_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `comment_content` varchar(500) NOT NULL,
  `comment_reg_time` datetime(6) NOT NULL,
  `content_ip` varchar(20) NOT NULL,
  `board_id` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `win_comment_board_id_aa41e30c_fk_win_board_board_id` (`board_id`),
  KEY `win_comment_user_id_50a5b283_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_comment_board_id_aa41e30c_fk_win_board_board_id` FOREIGN KEY (`board_id`) REFERENCES `win_board` (`board_id`),
  CONSTRAINT `win_comment_user_id_50a5b283_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_comment`
--

LOCK TABLES `win_comment` WRITE;
/*!40000 ALTER TABLE `win_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_detail_view`
--

DROP TABLE IF EXISTS `win_detail_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_detail_view` (
  `detail_view_id` int NOT NULL AUTO_INCREMENT,
  `detail_view_time` datetime(6) NOT NULL,
  `wine_id` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`detail_view_id`),
  KEY `win_detail_view_wine_id_8fd2bac7_fk_win_wine_wine_id` (`wine_id`),
  KEY `win_detail_view_user_id_3ba6ce50_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_detail_view_user_id_3ba6ce50_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`),
  CONSTRAINT `win_detail_view_wine_id_8fd2bac7_fk_win_wine_wine_id` FOREIGN KEY (`wine_id`) REFERENCES `win_wine` (`wine_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_detail_view`
--

LOCK TABLES `win_detail_view` WRITE;
/*!40000 ALTER TABLE `win_detail_view` DISABLE KEYS */;
INSERT INTO `win_detail_view` VALUES (1,'2023-08-17 11:41:44.000000',1,'test1111'),(2,'2023-08-17 11:41:54.000000',171,'test1111'),(3,'2023-08-17 11:42:23.000000',384,'test1111'),(4,'2023-08-17 11:47:46.000000',1,'test1111'),(5,'2023-08-17 01:14:16.000000',384,'test1111'),(6,'2023-08-19 05:52:36.000000',92,'test0810'),(7,'2023-08-19 05:52:58.000000',1,'test0810'),(8,'2023-08-21 10:14:13.000000',92,'test0810'),(9,'2023-08-21 10:14:24.000000',92,'test0810'),(10,'2023-08-21 10:14:31.000000',92,'test0810'),(11,'2023-08-21 10:17:20.000000',1,'test0810'),(12,'2023-08-21 10:49:01.000000',2,'test0810'),(13,'2023-08-21 10:50:59.000000',92,'test0810'),(14,'2023-08-21 10:51:06.000000',1,'test0810'),(15,'2023-08-21 10:52:01.000000',1,'test0810'),(16,'2023-08-21 11:36:10.000000',1,'test0810'),(17,'2023-08-21 11:50:10.000000',92,'test0810'),(18,'2023-08-21 11:50:25.000000',1,'test0810'),(19,'2023-08-21 11:52:09.000000',1,'test0810');
/*!40000 ALTER TABLE `win_detail_view` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_detail_view_n`
--

DROP TABLE IF EXISTS `win_detail_view_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_detail_view_n` (
  `detail_view_n_id` int NOT NULL AUTO_INCREMENT,
  `detail_view_n_time` datetime(6) NOT NULL,
  `wine_id` int NOT NULL,
  PRIMARY KEY (`detail_view_n_id`),
  KEY `win_detail_view_n_wine_id_4f9d9f2d_fk_win_wine_wine_id` (`wine_id`),
  CONSTRAINT `win_detail_view_n_wine_id_4f9d9f2d_fk_win_wine_wine_id` FOREIGN KEY (`wine_id`) REFERENCES `win_wine` (`wine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_detail_view_n`
--

LOCK TABLES `win_detail_view_n` WRITE;
/*!40000 ALTER TABLE `win_detail_view_n` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_detail_view_n` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_point_his`
--

DROP TABLE IF EXISTS `win_point_his`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_point_his` (
  `point_his_id` int NOT NULL AUTO_INCREMENT,
  `point_reg` datetime(6) NOT NULL,
  `point_add` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`point_his_id`),
  KEY `win_point_his_user_id_a29bc0f5_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_point_his_user_id_a29bc0f5_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_point_his`
--

LOCK TABLES `win_point_his` WRITE;
/*!40000 ALTER TABLE `win_point_his` DISABLE KEYS */;
INSERT INTO `win_point_his` VALUES (1,'2023-08-17 10:19:34.000000',100000,'test1111');
/*!40000 ALTER TABLE `win_point_his` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_purchase`
--

DROP TABLE IF EXISTS `win_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_purchase` (
  `purchase_id` int NOT NULL AUTO_INCREMENT,
  `purchase_time` datetime(6) NOT NULL,
  `purchase_number` int NOT NULL,
  `purchase_price` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`purchase_id`),
  KEY `win_purchase_user_id_8f563def_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_purchase_user_id_8f563def_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_purchase`
--

LOCK TABLES `win_purchase` WRITE;
/*!40000 ALTER TABLE `win_purchase` DISABLE KEYS */;
INSERT INTO `win_purchase` VALUES (1,'2023-08-17 11:48:30.000000',5,5,'test1111'),(2,'2023-08-21 10:49:29.000000',1,2,'test0810'),(3,'2023-08-21 10:51:15.000000',3,3,'test0810'),(4,'2023-08-21 11:36:51.000000',8,8,'test0810'),(5,'2023-08-21 11:42:02.000000',8,8,'test0810'),(6,'2023-08-21 11:42:25.000000',7,7,'test0810'),(7,'2023-08-21 11:44:14.000000',3,3,'test0810'),(8,'2023-08-21 11:48:58.000000',3,3,'test0810'),(9,'2023-08-21 11:50:31.000000',1,1,'test0810'),(10,'2023-08-21 12:59:43.000000',5,5,'test0810');
/*!40000 ALTER TABLE `win_purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_purchase_detail`
--

DROP TABLE IF EXISTS `win_purchase_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_purchase_detail` (
  `purchase_detail_id` int NOT NULL AUTO_INCREMENT,
  `purchase_det_number` int NOT NULL,
  `purchase_det_price` int NOT NULL,
  `purchase_det_state` int NOT NULL,
  `purchase_id` int NOT NULL,
  `sell_id` int NOT NULL,
  PRIMARY KEY (`purchase_detail_id`),
  KEY `win_purchase_detail_purchase_id_315e7c9a_fk_win_purch` (`purchase_id`),
  KEY `win_purchase_detail_sell_id_7208981c_fk_win_sell_sell_id` (`sell_id`),
  CONSTRAINT `win_purchase_detail_purchase_id_315e7c9a_fk_win_purch` FOREIGN KEY (`purchase_id`) REFERENCES `win_purchase` (`purchase_id`),
  CONSTRAINT `win_purchase_detail_sell_id_7208981c_fk_win_sell_sell_id` FOREIGN KEY (`sell_id`) REFERENCES `win_sell` (`sell_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_purchase_detail`
--

LOCK TABLES `win_purchase_detail` WRITE;
/*!40000 ALTER TABLE `win_purchase_detail` DISABLE KEYS */;
INSERT INTO `win_purchase_detail` VALUES (1,5,5,1,1,1),(2,1,2,1,2,2),(3,3,3,2,3,43),(4,8,8,1,4,43),(5,8,8,1,5,43),(6,7,7,1,6,43),(7,3,3,1,7,43),(8,3,3,1,8,43),(9,1,1,1,9,43),(10,5,5,1,10,43);
/*!40000 ALTER TABLE `win_purchase_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_receive_code`
--

DROP TABLE IF EXISTS `win_receive_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_receive_code` (
  `receive_code_id` int NOT NULL AUTO_INCREMENT,
  `receive_code` longblob NOT NULL,
  `purchase_detail_id` int NOT NULL,
  PRIMARY KEY (`receive_code_id`),
  KEY `win_receive_code_purchase_detail_id_44eac487_fk_win_purch` (`purchase_detail_id`),
  CONSTRAINT `win_receive_code_purchase_detail_id_44eac487_fk_win_purch` FOREIGN KEY (`purchase_detail_id`) REFERENCES `win_purchase_detail` (`purchase_detail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_receive_code`
--

LOCK TABLES `win_receive_code` WRITE;
/*!40000 ALTER TABLE `win_receive_code` DISABLE KEYS */;
INSERT INTO `win_receive_code` VALUES (1,_binary 'MHgxWWZScnV2ZnpnMQ==',1),(2,_binary 'MHgycVB1dUdIRnJCMQ==',2),(3,_binary 'MHgzWVdNemFyZHlyMQ==',3),(4,_binary 'MHg0a1ZrZUZYT1NNMQ==',4),(5,_binary 'MHg1V1JxalRzd1JiMQ==',5),(6,_binary 'MHg2cEpjT0NLaXdTMQ==',6),(7,_binary 'MHg3dmFnSFZBTUlVMQ==',7),(8,_binary 'MHg4YnRmUG9xelBCMQ==',8),(9,_binary 'MHg5a0VFTndYa3ZFMQ==',9),(10,_binary 'MHhhSGhzTFZZc0Iy',10);
/*!40000 ALTER TABLE `win_receive_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_revenue`
--

DROP TABLE IF EXISTS `win_revenue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_revenue` (
  `revenue_id` int NOT NULL AUTO_INCREMENT,
  `revenue_value` int NOT NULL,
  `revenue_date` datetime(6) NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`revenue_id`),
  KEY `win_revenue_store_id_2afd1ab2_fk_win_store_store_id` (`store_id`),
  CONSTRAINT `win_revenue_store_id_2afd1ab2_fk_win_store_store_id` FOREIGN KEY (`store_id`) REFERENCES `win_store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_revenue`
--

LOCK TABLES `win_revenue` WRITE;
/*!40000 ALTER TABLE `win_revenue` DISABLE KEYS */;
INSERT INTO `win_revenue` VALUES (1,5,'2023-08-17 11:48:30.000000',1),(2,2,'2023-08-21 10:49:29.000000',1),(3,3,'2023-08-21 10:51:15.000000',5),(4,8,'2023-08-21 11:36:51.000000',5),(5,8,'2023-08-21 11:42:02.000000',5),(6,7,'2023-08-21 11:42:25.000000',5),(7,3,'2023-08-21 11:44:14.000000',5),(8,3,'2023-08-21 11:48:58.000000',5),(9,1,'2023-08-21 11:50:31.000000',5),(10,5,'2023-08-21 12:59:43.000000',5);
/*!40000 ALTER TABLE `win_revenue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_review`
--

DROP TABLE IF EXISTS `win_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `review_content` varchar(500) NOT NULL,
  `review_score` decimal(2,1) NOT NULL,
  `review_reg_time` datetime(6) NOT NULL,
  `user_id` varchar(30) NOT NULL,
  `sell_id` int NOT NULL,
  PRIMARY KEY (`review_id`),
  KEY `win_review_user_id_cd8b63d3_fk_win_user_user_id` (`user_id`),
  KEY `win_review_sell_id_166681f7_fk_win_sell_sell_id` (`sell_id`),
  CONSTRAINT `win_review_sell_id_166681f7_fk_win_sell_sell_id` FOREIGN KEY (`sell_id`) REFERENCES `win_sell` (`sell_id`),
  CONSTRAINT `win_review_user_id_cd8b63d3_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_review`
--

LOCK TABLES `win_review` WRITE;
/*!40000 ALTER TABLE `win_review` DISABLE KEYS */;
INSERT INTO `win_review` VALUES (1,'괜찮음',5.0,'2023-08-21 10:51:57.000000','test0810',43),(2,'o',0.1,'2023-08-21 16:38:17.000000','test0810',61),(3,'o',0.1,'2023-08-21 16:38:31.000000','test0821',61),(4,'o',1.0,'2023-08-21 16:38:46.000000','test2222',61),(5,'o',1.0,'2023-08-21 16:38:59.000000','test0810',61),(6,'o',1.0,'2023-08-21 16:45:50.000000','test0810',61),(7,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(8,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(9,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(10,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(11,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(12,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(13,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(14,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(15,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(16,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(17,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(18,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(19,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(20,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(21,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(22,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(23,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(24,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(25,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(26,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(27,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(28,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(29,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(30,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(31,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(32,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(33,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(34,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(35,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(36,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(37,'o',1.0,'2023-08-21 16:46:30.000000','test0810',61),(38,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(39,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(40,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(41,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(42,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(43,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(44,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(45,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(46,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(47,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(48,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(49,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(50,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(51,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(52,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(53,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(54,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(55,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(56,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(57,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(58,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(59,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(60,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(61,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(62,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(63,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(64,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(65,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(66,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(67,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(68,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(69,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(70,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(71,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(72,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(73,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(74,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(75,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(76,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(77,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(78,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(79,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(80,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(81,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(82,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(83,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(84,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(85,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(86,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(87,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(88,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(89,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(90,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(91,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(92,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(93,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(94,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(95,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(96,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(97,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(98,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(99,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(100,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(101,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(102,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(103,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(104,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(105,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(106,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(107,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(108,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(109,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(110,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(111,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(112,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(113,'o',1.0,'2023-08-21 16:46:31.000000','test0810',61),(114,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(115,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(116,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(117,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(118,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(119,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(120,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(121,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(122,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(123,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(124,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(125,'o',1.0,'2023-08-21 16:46:32.000000','test0810',61),(126,'o',1.0,'2023-08-21 16:46:35.000000','test0810',61);
/*!40000 ALTER TABLE `win_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_search`
--

DROP TABLE IF EXISTS `win_search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_search` (
  `search_id` int NOT NULL AUTO_INCREMENT,
  `search_word` varchar(200) NOT NULL,
  `search_time` datetime(6) NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`search_id`),
  KEY `win_search_user_id_103e676d_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_search_user_id_103e676d_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_search`
--

LOCK TABLES `win_search` WRITE;
/*!40000 ALTER TABLE `win_search` DISABLE KEYS */;
INSERT INTO `win_search` VALUES (1,'프랑스와인1','2023-08-17 11:17:05.000000','test1111'),(2,'프랑스와인1','2023-08-17 11:19:09.000000','test1111'),(3,'엘 카스티야 가르나차','2023-08-17 11:42:21.000000','test1111'),(4,'칸티나 사바, 리포타 피노 그리지오','2023-08-17 11:47:44.000000','test1111'),(5,'엘 카스티야 가르나차','2023-08-17 01:14:15.000000','test1111'),(6,'엘 카스티야 가르나차','2023-08-17 01:18:02.000000','test1111'),(7,'몽 발롱, 까베르네 소비뇽','2023-08-19 05:52:29.000000','test0810'),(8,'장 로롱, 장 피노 누아','2023-08-19 05:52:31.000000','test0810'),(9,'8','2023-08-19 05:52:34.000000','test0810'),(10,'','2023-08-19 05:52:55.000000','test0810'),(11,'까르페니 말볼티, 1868 프로세코 수페리오레','2023-08-21 10:14:11.000000','test0810'),(12,'까르페니 말볼티, 1868 프로세코 수페리오레','2023-08-21 10:14:30.000000','test0810'),(13,'칸티나 사바, 리포타 피노 그리지오','2023-08-21 10:17:19.000000','test0810'),(14,'8','2023-08-21 10:50:57.000000','test0810'),(15,'칸티나 사바, 리포타 피노 그리지오','2023-08-21 10:51:05.000000','test0810'),(16,'Cantina Sava, Riporta Pinot Grigio','2023-08-21 11:36:05.000000','test0810'),(17,'까르페니 말볼티, 1868 프로세코 수페리오레','2023-08-21 11:50:08.000000','test0810'),(18,'Cantina Sava, Riporta Pinot Grigio','2023-08-21 11:50:17.000000','test0810'),(19,'까르페니 말볼티, 1868 프로세코 수페리오레','2023-08-21 11:50:21.000000','test0810'),(20,'칸티나 사바, 리포타 피노 그리지오','2023-08-21 11:50:23.000000','test0810'),(21,'칸티나 사바, 리포타 피노 그리지오','2023-08-21 11:52:07.000000','test0810');
/*!40000 ALTER TABLE `win_search` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_search_n`
--

DROP TABLE IF EXISTS `win_search_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_search_n` (
  `search_n_id` int NOT NULL AUTO_INCREMENT,
  `search_n_word` varchar(200) NOT NULL,
  `search_n_time` datetime(6) NOT NULL,
  PRIMARY KEY (`search_n_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_search_n`
--

LOCK TABLES `win_search_n` WRITE;
/*!40000 ALTER TABLE `win_search_n` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_search_n` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_sell`
--

DROP TABLE IF EXISTS `win_sell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_sell` (
  `sell_id` int NOT NULL AUTO_INCREMENT,
  `sell_reg_time` datetime(6) NOT NULL,
  `sell_price` int NOT NULL,
  `sell_promot` longtext NOT NULL,
  `sell_state` int NOT NULL,
  `store_id` int NOT NULL,
  `wine_id` int NOT NULL,
  PRIMARY KEY (`sell_id`),
  KEY `win_sell_store_id_a9e4fc3c_fk_win_store_store_id` (`store_id`),
  KEY `win_sell_wine_id_3a22238a_fk_win_wine_wine_id` (`wine_id`),
  CONSTRAINT `win_sell_store_id_a9e4fc3c_fk_win_store_store_id` FOREIGN KEY (`store_id`) REFERENCES `win_store` (`store_id`),
  CONSTRAINT `win_sell_wine_id_3a22238a_fk_win_wine_wine_id` FOREIGN KEY (`wine_id`) REFERENCES `win_wine` (`wine_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_sell`
--

LOCK TABLES `win_sell` WRITE;
/*!40000 ALTER TABLE `win_sell` DISABLE KEYS */;
INSERT INTO `win_sell` VALUES (1,'2023-08-17 11:45:22.000000',1,'1',1,1,1),(2,'2023-08-17 11:45:37.000000',2,'2',1,1,2),(3,'2023-08-17 11:45:22.000000',3,'3',1,1,3),(4,'2023-08-17 11:46:04.000000',4,'4',1,1,4),(5,'2023-08-17 11:46:19.000000',5,'5',1,1,5),(6,'2023-08-17 11:46:33.000000',1,'1',1,2,1),(7,'2023-08-17 11:46:40.000000',2,'2',1,2,2),(8,'2023-08-17 11:46:49.000000',3,'3',1,2,3),(9,'2023-08-17 11:46:59.000000',4,'4',1,2,4),(10,'2023-08-17 11:47:09.000000',5,'5',1,2,5),(11,'2023-08-17 13:37:02.000000',1,'1',1,3,1),(12,'2023-08-17 13:37:02.000000',2,'2',1,3,2),(13,'2023-08-17 13:37:02.000000',3,'3',1,3,3),(14,'2023-08-17 13:37:02.000000',4,'4',1,3,4),(15,'2023-08-17 13:37:02.000000',5,'5',1,3,5),(16,'2023-08-17 13:37:02.000000',6,'6',1,3,6),(17,'2023-08-17 13:37:02.000000',7,'7',1,3,7),(18,'2023-08-17 13:37:02.000000',8,'8',1,3,8),(19,'2023-08-17 13:37:02.000000',9,'9',1,3,9),(20,'2023-08-17 13:37:02.000000',10,'10',1,3,10),(21,'2023-08-17 13:37:02.000000',11,'11',1,3,11),(22,'2023-08-17 13:37:02.000000',12,'12',1,3,12),(23,'2023-08-17 13:37:02.000000',13,'13',1,3,15),(24,'2023-08-17 13:37:02.000000',14,'14',1,3,16),(25,'2023-08-17 13:37:02.000000',15,'15',1,3,17),(26,'2023-08-17 13:37:02.000000',16,'16',1,3,18),(27,'2023-08-17 13:37:02.000000',17,'17',1,3,19),(28,'2023-08-17 13:37:02.000000',18,'18',1,3,20),(29,'2023-08-17 13:37:02.000000',19,'19',1,3,21),(30,'2023-08-17 13:37:02.000000',20,'20',1,3,22),(31,'2023-08-17 13:37:02.000000',21,'21',1,3,23),(32,'2023-08-17 13:37:02.000000',22,'22',1,3,24),(33,'2023-08-17 13:37:02.000000',23,'23',1,3,25),(34,'2023-08-17 13:37:02.000000',24,'24',1,3,27),(35,'2023-08-17 13:37:02.000000',25,'25',1,3,60),(36,'2023-08-17 13:37:02.000000',26,'26',1,3,58),(37,'2023-08-17 13:37:02.000000',27,'27',1,3,57),(38,'2023-08-17 13:37:02.000000',28,'28',1,3,55),(39,'2023-08-17 13:37:02.000000',29,'29',1,3,53),(40,'2023-08-17 13:37:02.000000',30,'30',1,3,51),(41,'2023-08-17 13:37:02.000000',31,'31',1,3,49),(42,'2023-08-17 13:37:02.000000',32,'32',1,3,47),(43,'2023-08-19 17:15:03.000000',1,'12',1,5,1),(44,'2023-08-19 17:15:03.000000',2,'3',1,5,2),(45,'2023-08-19 17:15:03.000000',3,'4',1,5,3),(46,'2023-08-19 17:15:03.000000',4,'5',1,5,4),(47,'2023-08-19 17:15:03.000000',5,'67',1,5,5),(48,'2023-08-19 17:15:03.000000',6,'8',1,5,6),(49,'2023-08-19 17:15:03.000000',7,'9',1,5,7),(50,'2023-08-21 13:14:23.000000',1,'칸티나 사바, 리포타 피노 그리지오',1,6,1),(51,'2023-08-21 13:14:23.000000',2,'칸티나 사바, 리포타 네로 다볼라',1,6,2),(52,'2023-08-21 13:14:23.000000',3,'비니 토논, 스푸만테 로쏘 돌체 마지아 피오레',1,6,3),(53,'2023-08-21 13:14:23.000000',4,'비니 토논, 스푸만테 비앙코 세쿠 엑스트라 드라이 마지아 피오레',1,6,4),(54,'2023-08-21 13:14:23.000000',5,'비니 토논, 스푸만테 비앙코 돌체 마지아 피오레',1,6,5),(55,'2023-08-21 13:14:23.000000',6,'에노이탈리아, 소피오 오로 3 밀레지마토 스푸만테',1,6,6),(56,'2023-08-21 13:14:23.000000',7,'노떼 로사, 프리미티보 로사토',1,6,7),(57,'2023-08-21 13:14:23.000000',8,'노떼 로사, 프리미티보 살렌토',1,6,8),(58,'2023-08-21 13:14:23.000000',10,'에노이탈리아, 소피오 오로 블랑 드 블랑',1,6,10),(59,'2023-08-21 13:14:23.000000',11,'47AD, 프로세코 엑스트라 드라이 블랙',1,6,11),(60,'2023-08-21 13:14:23.000000',12,'칸티, 핑크 블라썸 스위트 1',1,6,12),(61,'2023-08-21 13:14:23.000000',13,'칸티나 테를란, 피노 비앙코',1,6,183);
/*!40000 ALTER TABLE `win_sell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_store`
--

DROP TABLE IF EXISTS `win_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_store` (
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_address` varchar(200) NOT NULL,
  `store_name` varchar(100) NOT NULL,
  `store_reg_num` varchar(20) NOT NULL,
  `store_email` varchar(50) NOT NULL,
  `store_state` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`store_id`),
  KEY `win_store_user_id_6e64120e_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_store_user_id_6e64120e_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_store`
--

LOCK TABLES `win_store` WRITE;
/*!40000 ALTER TABLE `win_store` DISABLE KEYS */;
INSERT INTO `win_store` VALUES (1,'2222','2222','123-345-678','1111@3444.com',1,'test2222'),(2,'3333','3333','3333','33333@3333.com',1,'test3333'),(3,'부산 기장군 장안읍 판곡길 2@101호','111','123-32-12345','2142342@trrewte.com',0,'test5555'),(4,'qwwerwr','werqerweq','43214123','fsdfs@ewrwe.com',0,'test5555'),(5,'대전 동구 판교3길 1@1호','판교술집','123-32-23434','42312@12411.com',0,'test0810'),(6,'부산 기장군 장안읍 판곡길 2@1호','판곡길 술집','123-09-12345','vksrhrrlf@tnfwlq.com',0,'test0821');
/*!40000 ALTER TABLE `win_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_store_excel`
--

DROP TABLE IF EXISTS `win_store_excel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_store_excel` (
  `store_excel_id` int NOT NULL AUTO_INCREMENT,
  `store_excel` varchar(300) NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`store_excel_id`),
  KEY `win_store_excel_store_id_ecd4d2ae_fk_win_store_store_id` (`store_id`),
  CONSTRAINT `win_store_excel_store_id_ecd4d2ae_fk_win_store_store_id` FOREIGN KEY (`store_id`) REFERENCES `win_store` (`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_store_excel`
--

LOCK TABLES `win_store_excel` WRITE;
/*!40000 ALTER TABLE `win_store_excel` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_store_excel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_store_url`
--

DROP TABLE IF EXISTS `win_store_url`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_store_url` (
  `store_url_id` int NOT NULL AUTO_INCREMENT,
  `store_map_url` varchar(300) NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`store_url_id`),
  KEY `win_store_url_store_id_ed9d699d_fk_win_store_store_id` (`store_id`),
  CONSTRAINT `win_store_url_store_id_ed9d699d_fk_win_store_store_id` FOREIGN KEY (`store_id`) REFERENCES `win_store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_store_url`
--

LOCK TABLES `win_store_url` WRITE;
/*!40000 ALTER TABLE `win_store_url` DISABLE KEYS */;
INSERT INTO `win_store_url` VALUES (1,'http://localhost12313.com',3),(2,'http://192.168.0.3/store/registration',5),(3,'',6);
/*!40000 ALTER TABLE `win_store_url` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_user`
--

DROP TABLE IF EXISTS `win_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_user` (
  `user_id` varchar(30) NOT NULL,
  `user_passwd` varchar(30) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_email` varchar(50) NOT NULL,
  `user_tel` varchar(20) NOT NULL,
  `user_reg_date` datetime(6) NOT NULL,
  `user_point` int unsigned NOT NULL,
  `user_profile_img` varchar(300) NOT NULL,
  `user_grade` int NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `win_user_user_grade_238c1396_fk_win_user_grade_user_grade` (`user_grade`),
  CONSTRAINT `win_user_user_grade_238c1396_fk_win_user_grade_user_grade` FOREIGN KEY (`user_grade`) REFERENCES `win_user_grade` (`user_grade`),
  CONSTRAINT `win_user_chk_1` CHECK ((`user_point` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_user`
--

LOCK TABLES `win_user` WRITE;
/*!40000 ALTER TABLE `win_user` DISABLE KEYS */;
INSERT INTO `win_user` VALUES ('test0810','1111','1111','whqjarn111@gmail.com','1111','2023-08-19 17:14:18.000000',9968,'profile/코드.png',2),('test0821','1111','1111','whqjarn111@gmail.com','1111','2023-08-21 13:12:22.000000',0,'profile/addPointHis.png',2),('test1111','1111','1111','whqjarn111@gmail.com','1111','2023-08-16 16:49:32.000000',99995,'profile/220px-Parkerpen_textlogo.png',1),('test2222','1111','1111','1111@1111.com','111-1111-1111','2023-08-17 11:43:13.000000',30000,'',2),('test3333','1111','1111','1111@1111.com','111-1111-1111','2023-08-17 11:43:48.000000',1,'',2),('test5555','1111','1111','whqjarn111@gmail.com','1111','2023-08-17 13:28:14.000000',0,'profile/다운로드_2.jfif',2);
/*!40000 ALTER TABLE `win_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_user_account`
--

DROP TABLE IF EXISTS `win_user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_user_account` (
  `user_account_id` int NOT NULL AUTO_INCREMENT,
  `user_account_default` int NOT NULL,
  `user_account1` varchar(80) NOT NULL,
  `user_account2` varchar(80) NOT NULL,
  `user_account3` varchar(80) NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`user_account_id`),
  KEY `win_user_account_user_id_51aefa12_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_user_account_user_id_51aefa12_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_user_account`
--

LOCK TABLES `win_user_account` WRITE;
/*!40000 ALTER TABLE `win_user_account` DISABLE KEYS */;
INSERT INTO `win_user_account` VALUES (1,1,'SC제일 - 123123123','','','test1111'),(2,1,'부산 - 3414231334','','','test0810');
/*!40000 ALTER TABLE `win_user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_user_favorite`
--

DROP TABLE IF EXISTS `win_user_favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_user_favorite` (
  `fav_user_id` int NOT NULL AUTO_INCREMENT,
  `fav_wine_color` int NOT NULL,
  `fav_alc` int NOT NULL,
  `fav_numbwith` int NOT NULL,
  `fav_sweet` int NOT NULL,
  `fav_bitter` int NOT NULL,
  `fav_sour` int NOT NULL,
  `fav_season` int NOT NULL,
  `fav_food` int NOT NULL,
  `fav_first_priority` int NOT NULL,
  `fav_second_priority` int NOT NULL,
  `fav_third_priority` int NOT NULL,
  `user_id` varchar(30) NOT NULL,
  PRIMARY KEY (`fav_user_id`),
  KEY `win_user_favorite_user_id_6fe874de_fk_win_user_user_id` (`user_id`),
  CONSTRAINT `win_user_favorite_user_id_6fe874de_fk_win_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `win_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_user_favorite`
--

LOCK TABLES `win_user_favorite` WRITE;
/*!40000 ALTER TABLE `win_user_favorite` DISABLE KEYS */;
INSERT INTO `win_user_favorite` VALUES (1,0,0,0,3,3,3,0,0,0,0,0,'test1111');
/*!40000 ALTER TABLE `win_user_favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_user_grade`
--

DROP TABLE IF EXISTS `win_user_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_user_grade` (
  `user_grade` int NOT NULL,
  `user_grade_name` varchar(30) NOT NULL,
  PRIMARY KEY (`user_grade`),
  UNIQUE KEY `user_grade_name` (`user_grade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_user_grade`
--

LOCK TABLES `win_user_grade` WRITE;
/*!40000 ALTER TABLE `win_user_grade` DISABLE KEYS */;
INSERT INTO `win_user_grade` VALUES (1,'유저'),(2,'점주');
/*!40000 ALTER TABLE `win_user_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_wine`
--

DROP TABLE IF EXISTS `win_wine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_wine` (
  `wine_id` int NOT NULL AUTO_INCREMENT,
  `wine_name` varchar(150) NOT NULL,
  `wine_name_eng` varchar(150) NOT NULL,
  `wine_sort` int NOT NULL,
  `wine_capacity` int DEFAULT NULL,
  `wine_alc` decimal(3,1) NOT NULL,
  `wine_dangdo` int NOT NULL,
  `wine_sando` int NOT NULL,
  `wine_tannin` int NOT NULL,
  `wine_food` int NOT NULL,
  `wine_image` varchar(200) NOT NULL,
  `wine_region_id` int NOT NULL,
  PRIMARY KEY (`wine_id`),
  KEY `win_wine_wine_region_id_8f6186d1_fk_win_wine_` (`wine_region_id`),
  CONSTRAINT `win_wine_wine_region_id_8f6186d1_fk_win_wine_` FOREIGN KEY (`wine_region_id`) REFERENCES `win_wine_region` (`wine_region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=406 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_wine`
--

LOCK TABLES `win_wine` WRITE;
/*!40000 ALTER TABLE `win_wine` DISABLE KEYS */;
INSERT INTO `win_wine` VALUES (1,'칸티나 사바, 리포타 피노 그리지오','Cantina Sava, Riporta Pinot Grigio',2,750,13.0,1,3,1,4,'../../media/images/wine/01001.png',2),(2,'칸티나 사바, 리포타 네로 다볼라','Cantina Sava, Riporta Nero d\'Avola',1,750,14.0,1,3,3,1,'../../media/images/wine/01002.png',2),(3,'비니 토논, 스푸만테 로쏘 돌체 마지아 피오레','Vini Tonon, Spumante Rosso Dolce Magia Fiore',4,750,10.0,2,3,2,2,'../../media/images/wine/01003.png',2),(4,'비니 토논, 스푸만테 비앙코 세쿠 엑스트라 드라이 마지아 피오레','Vini Tonon, Spumante Bianco Secco Extra-dry Magia Fiore',4,750,12.0,1,4,1,2,'../../media/images/wine/01004.png',2),(5,'비니 토논, 스푸만테 비앙코 돌체 마지아 피오레','Vini Tonon, Spumante Bianco Dolce Magia Fiore',4,750,10.0,2,4,1,2,'../../media/images/wine/01005.png',2),(6,'에노이탈리아, 소피오 오로 3 밀레지마토 스푸만테','Enoitalia, Soffio ORO Rose Millesimato Spumante',4,750,12.0,2,3,1,3,'../../media/images/wine/01006.png',2),(7,'노떼 로사, 프리미티보 로사토','Notte Rossa, Primitivo Rosato',3,750,13.0,1,3,2,2,'../../media/images/wine/01007.png',2),(8,'노떼 로사, 프리미티보 살렌토','Notte Rossa, Primitivo Salento',1,750,15.0,2,2,2,1,'../../media/images/wine/01008.png',2),(9,'노떼 로사, 바시아 로쏘 살렌토','Notte Rossa, Bascia Rosso Salento',1,750,15.0,1,3,3,1,'../../media/images/wine/01009.png',2),(10,'에노이탈리아, 소피오 오로 블랑 드 블랑','Enoitalia, Soffio Oro Blanc de Blancs',4,750,12.0,2,3,1,2,'../../media/images/wine/01010.png',2),(11,'47AD, 프로세코 엑스트라 드라이 블랙','47AD, Prosecco extra-dry Black',4,750,12.0,2,4,1,4,'../../media/images/wine/01011.png',2),(12,'칸티, 핑크 블라썸 스위트 1','Canti, Pink Blossom Sweet Red',1,750,5.5,1,3,2,1,'../../media/images/wine/01012.jpg',2),(13,'미라벤토, 모스카토 리치','Miravento, Moscato Lychee',4,750,6.0,3,3,1,2,'../../media/images/wine/01013.png',2),(14,'미라벤토, 모스카토 피치','Miravento, Mocato Peach',4,750,6.0,3,3,1,5,'../../media/images/wine/01014.png',2),(15,'미라벤토, 모스카토 스트로베리','Miravento, Moscato Strawberry',4,750,6.0,3,3,1,4,'../../media/images/wine/01015.png',2),(16,'미라벤토, 모스카토 핑크','Miravento, Moscato Pink',4,750,7.0,3,3,1,1,'../../media/images/wine/01016.png',2),(17,'체비코, 르미유 비노 로쏘 미디엄 스윗','Cevico, Lemieux Vino Rosso Medium Sweet',1,750,10.5,1,3,2,1,'../../media/images/wine/01017.png',2),(18,'체비코, 스위트 키스','Cevico, Sweet Kiss Rosso',1,750,9.0,1,3,3,1,'../../media/images/wine/01018.png',2),(19,'체비코, 드라이 키스','Cevico, Dry Kiss Rosso',1,750,11.5,1,2,3,1,'../../media/images/wine/01019.png',2),(20,'발레벨보, 피에몬테 모스까또 D.O.C','Vallebelbo, Piemonte Moscato D.O.C',2,750,5.0,2,3,1,4,'../../media/images/wine/01020.png',2),(21,'쉬즈 올웨이즈 3','She\'s Always Rose Sparkling',4,750,12.0,1,3,2,2,'../../media/images/wine/01021.png',2),(22,'스가르지 루이지, 레티자 2','Sgarzi Luigi, Letizia White',2,750,10.0,1,3,1,3,'../../media/images/wine/01022.png',2),(23,'스가르지 루이지, 레티자 1','Sgarzi Luigi, Letizia Red',1,750,18.0,2,3,4,4,'../../media/images/wine/01023.png',2),(24,'뜨레 세콜리, 모스카토 다스티','Tre Secoli, Moscato d\'Asti',2,750,6.0,4,1,1,2,'../../media/images/wine/01024.png',2),(25,'뜨레 세콜리, 브라케토 다퀴','Tre Secoli, Brachetto d\'Acqui',4,750,6.0,3,1,1,4,'../../media/images/wine/01025.png',2),(26,'까비로, 아프리몬도 아파시멘토 산지오베제','Caviro, Aprimondo Appassimento Sangiovese',1,750,15.0,2,3,3,1,'../../media/images/wine/01026.png',2),(27,'몬테 델 프라, 까델마그로 쿠스토자 수페리오레','Monte del Fra, Ca del Magro Custoza Superiore',2,750,14.0,1,3,1,3,'../../media/images/wine/01027.png',2),(28,'피치니, 피노키오','Piccini, Pinocchio',1,750,14.0,1,3,3,1,'../../media/images/wine/01028.jpg',2),(29,'카시나 치쿠, 랑게 네비올로','Cascina Chicco, Langhe Nebbiolo',1,750,15.0,1,3,3,1,'../../media/images/wine/01029.png',2),(30,'카시나 치쿠, 로에로 아르네이스','Cascina Chicco, Roero Arneis Anterisio',2,750,15.0,1,4,1,4,'../../media/images/wine/01030.jpg',2),(31,'47AD, 그랑 뀌베 스푸만떼 골드','47AD, Grand Cuvee Spumante Gold',4,750,12.0,2,3,1,1,'../../media/images/wine/01031.png',2),(32,'47AD, 프로세코 3','47AD, Prosecco Rose',4,750,12.0,2,3,2,2,'../../media/images/wine/01032.png',2),(33,'47AD, 프로세코 엑스트라 브룻 민트','47AD, Prosecco extra-brut',4,750,12.0,2,3,1,2,'../../media/images/wine/01033.png',2),(34,'47AD, 프로세코 엑스트라 드라이 블랙','47AD, Prosecco extra-dry Black',4,750,12.0,2,4,1,2,'../../media/images/wine/01034.png',2),(35,'발레벨보, 르필레르 모스까또 다스띠 D.O.C.G','Vallebelbo, Le Pilere Moscato D\'Asti D.O.C.G',2,750,5.5,1,4,1,1,'../../media/images/wine/01035.png',2),(36,'우마니 론끼, 비고르 2','Umani Ronchi, Vigor White',2,750,12.0,1,3,1,2,'../../media/images/wine/01036.png',2),(37,'또스띠, 모스까또 블랙에디션','Tosti, Moscato Black Edition',4,750,6.5,2,3,1,1,'../../media/images/wine/01037.png',2),(38,'또스띠, 버터플라이 4','Tosti, Butterfly Sparkling',4,750,9.5,1,4,1,2,'../../media/images/wine/01038.png',2),(39,'일 팔라지오, 뉴 데이 로사토','Il Palagio, New Day Rosato',3,750,12.5,1,3,2,4,'../../media/images/wine/01039.png',2),(40,'일 팔라지오, 웬 위 댄스','Il Palagio, When We Dance',1,750,13.0,1,3,3,4,'../../media/images/wine/01040.png',2),(41,'스트레브 모스카토 다스티 DOCG','Strev Moscato d\'Asti DOCG',2,750,6.0,3,3,1,5,'../../media/images/wine/01041.png',2),(42,'칸티, 프리미엄 브라케토','Canti, Premium Brachetto',1,750,7.0,4,3,3,2,'../../media/images/wine/01042.png',2),(43,'와인컵, 샤도네이','Wine Cup, Chardonnay',2,187,13.0,1,3,1,1,'../../media/images/wine/01043.png',2),(44,'와인컵, 메를로','Wine Cup, Merlot',1,187,13.0,1,3,4,4,'../../media/images/wine/01044.png',2),(45,'마세리아 트라조네, 네로 다볼라','Masseria Trajone, Nero d\'Avola',1,750,13.0,1,3,4,2,'../../media/images/wine/01045.png',2),(46,'마세리아 트라조네, 피노 그리지오','Masseria Trajone, Pinot Grigio',2,750,13.0,1,3,1,2,'../../media/images/wine/01046.png',2),(47,'알루메아 로쏘 테레 디 키에티 오가닉','Allumea Rosso',1,750,14.0,1,3,3,4,'../../media/images/wine/01047.png',2),(48,'알루메아 네로 다볼라 시칠리아 오가닉','Allumea Nero d\'Avola',1,750,14.0,1,3,3,1,'../../media/images/wine/01048.png',2),(49,'알루메아 네로 다볼라 메를로 시칠리아 오가닉','Allumea Nero d\'Avola Merlot',1,750,14.0,1,3,3,2,'../../media/images/wine/01049.png',2),(50,'알루메아 그릴로 샤도네이 시칠리아 오가닉','Allumea Grillo Chardonnay',2,750,13.0,1,3,1,1,'../../media/images/wine/01050.png',2),(51,'토소, 브뤼 밀레시마토','Toso, Brut Millesimato',4,750,13.0,1,4,1,1,'../../media/images/wine/01051.png',2),(52,'알루메아 샤도네이 테레 시칠리아네 오가닉','Allumea Chardonnay Terre Siciliane Organic',2,750,13.0,1,3,1,2,'../../media/images/wine/01052.png',2),(53,'알레니코 프리미티보 디 만두리아','Allenico Primitivo di Manduria',1,750,15.0,1,4,5,1,'../../media/images/wine/01053.png',2),(54,'파소 세그레토 아파시멘토 산지오베제','Passo Segreto Appasimento Sangiovese',1,750,15.0,1,3,3,4,'../../media/images/wine/01054.png',2),(55,'파소 세그레토 아파시멘토 로쏘','Passo Segreto Appasimento Rosso',1,750,16.0,1,4,3,1,'../../media/images/wine/01055.png',2),(56,'파모소 루비코네','Famoso Rubicone',2,750,13.0,1,3,1,2,'../../media/images/wine/01056.png',2),(57,'노비볼레 로마냐 스푸만테 비앙코','Novebolle Romagna Spumante Bianco',4,750,12.0,2,4,1,1,'../../media/images/wine/01057.png',2),(58,'로마냐 트레비아노','Romagna Trebbiano',2,750,13.0,1,3,1,3,'../../media/images/wine/01058.png',2),(59,'오로펠라, 3 엑스트라 드라이 스푸만테 밀레지마토','Oroperla, Rose Extra Dry Spumante Millesimato',4,750,13.0,1,4,2,5,'../../media/images/wine/01059.png',2),(60,'리파 디 소토, 진판델','Ripa di Sotto, Zinfandel',1,750,16.0,1,3,5,1,'../../media/images/wine/01060.png',2),(61,'노비볼레 로마냐 스푸만테 로사토','Caviro, Novebolle Romagna Spumante Rosato',4,750,12.0,1,3,2,2,'../../media/images/wine/01061.png',2),(62,'콜레프리지오, 비그나쿼드라 페코리노','Collefrisio, Vignaqudra Pecorino',2,750,14.0,1,3,1,4,'../../media/images/wine/01062.png',2),(63,'콜레프리지오, 테누타 줄리아노','Collefrisio, Tenuta Giuliano',1,750,15.0,1,3,3,5,'../../media/images/wine/01063.png',2),(64,'로마냐 산지오베제 수페리오레 리제르바','Romagna Sangiovese Superiore Riserva',1,750,15.0,1,3,3,1,'../../media/images/wine/01064.png',2),(65,'칸티네 산 마르코, 프로그 비노 비안코','Cantine San Marco, Frog Vino Bianco',2,750,13.0,1,3,1,1,'../../media/images/wine/01065.png',2),(66,'칸티네 산 마르코, 프로그 비노 로쏘','Cantine San Marco, Frog Vino Rosso',1,750,13.0,1,3,3,2,'../../media/images/wine/01066.png',2),(67,'칸티나 꼴리 에오가네이, 피노 그리지오 델레 베네치에','Cantina Colli Euganei, Pinot Grigio delle Venezie',2,750,13.0,1,3,1,1,'../../media/images/wine/01067.png',2),(68,'카사 세코, 모스카토 다스티','Casa Secco, Moscato d\'Asti',2,750,6.0,3,3,1,1,'../../media/images/wine/01068.png',2),(69,'깔린 드 파올로, 바르베라 다스티 \'에드 리비텀\'','Carlin de Paolo, Barbera d\'Asti \'Ad Libitvm\'',1,750,14.0,1,3,3,2,'../../media/images/wine/01069.png',2),(70,'페로 13, 해커','Ferro 13, Hacker',1,750,12.0,1,3,3,1,'../../media/images/wine/01070.png',2),(71,'페로 13, 젠틀맨','Ferro 13, Gentleman',1,750,13.0,1,3,2,2,'../../media/images/wine/01071.png',2),(72,'페로 13, 해쉬태그','Ferro 13, Hashtag',2,750,13.0,1,4,1,4,'../../media/images/wine/01072.png',2),(73,'페로 13, 더 레이디','Ferro 13, The Lady',2,750,13.0,1,3,2,4,'../../media/images/wine/01073.png',2),(74,'페로 13, 너드','Ferro 13, Nerd',1,750,14.0,1,3,3,2,'../../media/images/wine/01074.png',2),(75,'페로 13, 힙스터','Ferro 13, Hipster',1,750,14.0,1,3,3,4,'../../media/images/wine/01075.png',2),(76,'트룰리, 프리미티보','Trulli, Primitivo',1,750,14.0,1,3,3,1,'../../media/images/wine/01076.png',2),(77,'테누타 산 안토니오, 소아베 폰타나','Tenuta Sant\' Antonio, Soave Fontana',2,750,13.0,1,3,1,1,'../../media/images/wine/01077.png',2),(78,'시스티나 몬테풀치아노 다부르쪼 리제르바','Sistina Montepulciano d\'Abruzzo Riserva',1,750,15.0,1,3,3,1,'../../media/images/wine/01078.png',2),(79,'시스티나 몬테풀치아노 다부르쪼','Sistina Montepulciano d\'Abruzzo',1,750,14.0,1,3,3,1,'../../media/images/wine/01079.png',2),(80,'시스티나 아파시멘토','Sistina Appassimento',1,750,15.0,1,3,3,1,'../../media/images/wine/01080.png',2),(81,'산 마르티노, 피노 네로 로사토','San Martino, Pinot Nero Rosato Brut',4,750,13.0,1,4,1,2,'../../media/images/wine/01081.png',2),(82,'테누타 살바테라, 팔리아 3','Tenuta Salvaterra, Falia Rose',3,750,13.0,1,3,1,5,'../../media/images/wine/01082.png',2),(83,'테누타 살바테라, 팔리아 비앙코','Tenuta Salvaterra, Falia Bianco',2,750,13.0,1,3,1,4,'../../media/images/wine/01083.png',2),(84,'테누타 살바테라, 팔리아 로쏘','Tenuta Salvaterra, Falia Rosso',1,750,14.0,1,3,3,2,'../../media/images/wine/01084.png',2),(85,'아스트랄, 키안티 리제르바','Astrale, Chianti Riserva',1,750,14.0,1,3,4,2,'../../media/images/wine/01085.png',2),(86,'아스트랄, 키안티','Astral, Chianti',1,750,13.0,1,3,4,3,'../../media/images/wine/01086.png',2),(87,'아스트랄, 로쏘','Astrale, Rosso',1,750,15.0,1,4,4,2,'../../media/images/wine/01087.png',2),(88,'아스트랄, 비앙코','Astrale, Bianco',2,750,14.0,1,4,1,4,'../../media/images/wine/01088.png',2),(89,'아스트랄, 스푸만테 엑스트라 드라이','Astrale, Spumante Extra Dry',4,750,12.0,1,3,1,4,'../../media/images/wine/01089.png',2),(90,'리포타 프리미티보','Riporta Primitivo',1,750,15.0,1,3,4,1,'../../media/images/wine/01090.png',2),(91,'까르페니 말볼티, 프로세코 트레비소','Carpene Malvolti, Prosecco Treviso',4,750,11.0,1,3,1,5,'../../media/images/wine/01091.png',2),(92,'까르페니 말볼티, 1868 프로세코 수페리오레','Carpene Malvolti, 1868 Prosecco Superiore',4,750,12.0,1,3,1,5,'../../media/images/wine/01092.png',2),(93,'노떼 로사, 베르멘티노 살렌토','Notte Rossa, Vermentino Salento',2,750,13.0,1,4,1,5,'../../media/images/wine/01093.png',2),(94,'노떼 로사, 프리미티보 풀리아 바이오','Notte Rossa, Primitivo Puglia Bio',1,750,14.5,1,3,3,1,'../../media/images/wine/01094.png',2),(95,'노떼 로사, 네그로아마로 디 테라 도트란토','Notte Rossa, Negroamaro di Terra d\'Otranto',1,750,14.5,1,3,3,4,'../../media/images/wine/01095.png',2),(96,'노떼 로사, 프리미티보 디 만두리아','Notte Rossa, Primitivo di Manduria',1,750,15.0,1,3,4,1,'../../media/images/wine/01096.png',2),(97,'프레스코발디, 포미노 비앙코','Frescobaldi, Pomino Bianco',2,750,13.0,1,4,1,2,'../../media/images/wine/01097.png',2),(98,'프레스코발디, 테누타 카스틸리오니 키안티','Frescobaldi, Tenuta Castiglioni Chianti',1,750,14.0,1,3,4,1,'../../media/images/wine/01098.png',2),(99,'프레스코발디, 키안티 클라시코 파우나에','Frescobaldi, Chianti Classico Faunae',1,750,14.0,1,3,4,1,'../../media/images/wine/01099.jpg',2),(100,'프레스코발디, 알리에 3','Frescobaldi, Alie Rose',3,750,13.0,1,3,2,4,'../../media/images/wine/01100.png',2),(101,'칸티네 체치, 주세페 베르디 말바시아 브륏','Cantine Ceci, Giuseppe Verdi Malvasia Brut',4,750,12.0,1,4,1,5,'../../media/images/wine/01101.png',2),(102,'칸티네 체치, 주세페 베르디 람브루스코 로사 아마빌레','Cantine Ceci, Giuseppe Verdi Lambrusco Rosa Amabile',4,750,9.0,3,3,1,5,'../../media/images/wine/01102.png',2),(103,'로르나노, 키안티 클라시코','Lornano, Chianti Classico',1,750,15.0,1,3,3,4,'../../media/images/wine/01103.png',2),(104,'발비 소프라니, 가비','Balbi Soprani, Gavi',2,750,13.0,1,4,1,4,'../../media/images/wine/01104.png',2),(105,'발비 소프라니, 로에로 아르네이스','Balbi Soprani, Roero Arneis',2,750,14.0,1,4,1,2,'../../media/images/wine/01105.png',2),(106,'콜라브리고, 프로세코 수페리오레 브뤼','Collalbrigo, Prosecco Superiore Brut',4,750,12.0,1,3,1,4,'../../media/images/wine/01106.png',2),(107,'콜라브리고, 프로세코 엑스트라 드라이','Collalbrigo, Prosecco Extra Dry',4,750,12.0,1,4,1,4,'../../media/images/wine/01107.png',2),(108,'콜라브리고, 프로세코 브뤼','Collalbrigo, Prosecco Brut',4,750,12.0,1,3,1,4,'../../media/images/wine/01108.png',2),(109,'발레벨보, 까띠나 모스까또 다스티','Vallebelbo, Catina Moscato d\'Asti _x000B_',2,750,6.0,3,3,1,1,'../../media/images/wine/01109.png',2),(110,'아리온, 마마망고','Arione, Mama mango',4,750,6.0,3,3,1,4,'../../media/images/wine/01110.png',2),(111,'산 제노네 로쏘 토스카나','San Zenone Rosso Toscana',1,750,14.0,1,3,3,2,'../../media/images/wine/01111.png',2),(112,'라르카, 프리미티보 풀리아','L\'Arca, Primitivo Puglia',1,750,14.0,1,3,3,1,'../../media/images/wine/01112.png',2),(113,'라르카, 네그로아마로 풀리아','L\'Arca, Negroamaro Puglia',1,750,14.0,2,3,3,5,'../../media/images/wine/01113.png',2),(114,'고베르노 디 카스텔라레','Governo di Castellare',1,750,13.0,1,3,2,4,'../../media/images/wine/01114.png',2),(115,'보데가스 베르데쿠르즈, 꼴리 세미세코','Bodegas Verduguez, Coeli Semisco',4,750,11.5,2,3,1,1,'../../media/images/wine/01115.png',2),(116,'산 마르코, 투스쿨룸 비노 비앙코','San Marco, Tusculum Vino Bianco',2,750,13.0,1,4,1,2,'../../media/images/wine/01116.png',2),(117,'산 마르코, 폰테 가이아 비노 로쏘','San Marco, Fonte Gaia Vino Rosso',1,750,13.0,1,4,3,1,'../../media/images/wine/01117.png',2),(118,'크리스마스 아스티','Christmas Asti',4,750,6.0,4,2,1,4,'../../media/images/wine/01118.png',2),(119,'바스티오니 델라 로카, 프리미티보','Bastioni della Rocca, Primitivo',1,750,15.0,1,3,4,1,'../../media/images/wine/01119.png',2),(120,'두게싸 리아, 아스티 세코','Duchessa Lia, Asti Secco',4,750,11.0,4,3,1,1,'../../media/images/wine/01120.png',2),(121,'코스타 메디아나 아마로네 델라 발폴리첼라','Costa Mediana Amarone dell Valpolicella',1,750,16.0,1,3,4,5,'../../media/images/wine/01121.png',2),(122,'단티, 프리미티보','Danti, Primitivo',1,750,15.0,1,3,4,2,'../../media/images/wine/01122.png',2),(123,'트룰리, 루깔레 아파시멘토','rulli, Lucale Appasimento',1,750,15.0,1,3,4,1,'../../media/images/wine/01123.png',2),(124,'투 보틀 돌체 비앙코','Two Bottle Dolce Bianco',2,750,6.0,4,2,1,2,'../../media/images/wine/01124.png',2),(125,'페트라, 징가리 비앙코','Petra Zingari Bianco',2,750,13.0,1,3,1,5,'../../media/images/wine/01125.png',2),(126,'페트라, 징가리 로사토','Petra, Zingari Rosato',3,750,14.0,1,3,2,5,'../../media/images/wine/01126.png',2),(127,'일 보로, 3 델 보로','Il Borro, Rose del Borro',3,750,14.0,1,3,1,2,'../../media/images/wine/01127.png',2),(128,'꼬모 모스카토','Como Moscato',2,750,6.0,4,3,1,2,'../../media/images/wine/01128.png',2),(129,'토레 라치나','Torre Rracina',1,750,12.0,1,3,3,1,'../../media/images/wine/01129.png',2),(130,'마쏘 안티코 피아노','Masso Antico Fiano',2,750,14.0,1,4,1,5,'../../media/images/wine/01130.png',2),(131,'지오다노, 셀바토 토스카나 로쏘','Giordano, Selvato Toscana Rosso',1,750,14.0,1,4,3,1,'../../media/images/wine/01131.png',2),(132,'소마리바, 꼬넬리아노 발도비아데네 프로세코 수페리오레 드라이','Sommariva, Conegliano Valdobbiadene Prosecco Superiore Dry',4,750,11.0,1,3,1,2,'../../media/images/wine/01132.jpg',2),(133,'칸티나 테를란, 샤르도네','Cantina Terlan, Chardonnay',2,750,14.0,1,3,1,4,'../../media/images/wine/01133.png',2),(134,'카잘 파르네토, 베르디끼오','Casal Farneto, Verdicchio',2,750,14.0,1,4,1,5,'../../media/images/wine/01134.jpg',2),(135,'카잘 파르네토, 몬테풀치아노','Casal Farneto, Montepulciano',1,750,14.0,1,3,3,1,'../../media/images/wine/01135.jpg',2),(136,'탈라몬티, 꼴레 꼬르비아노 몬테풀치아노','Talamonti, Colle Corviano Montepulciano d\'Abruzzo',1,750,14.0,1,4,3,1,'../../media/images/wine/01136.jpg',2),(137,'폴리지아노, 모렐리노 디 스칸사노','Poliziano, Morellino di Scansano',1,750,14.0,1,3,4,1,'../../media/images/wine/01137.jpg',2),(138,'폴리지아노,로쏘 디 몬테풀치아노','Poliziano, Rosso di Montepulciano',1,750,14.0,1,3,3,3,'../../media/images/wine/01138.jpg',2),(139,'두카 디 사락냐노, 빠쇼네','Duca di Saragnano, Passone',1,750,14.0,1,4,4,1,'../../media/images/wine/01139.jpg',2),(140,'칸티나 꼴리 에오가네이, 모스카토 스푸만테 돌체','Cantina Colli Euganei, Moscato Spumante Dolce',4,750,7.0,4,1,1,2,'../../media/images/wine/01140.jpg',2),(141,'르 꼰떼쎄, 피노 3 스푸만테 퀴베 브뤼','Le Contesse, Pinot Rose Spumante Cuvee Brut',4,750,11.0,1,3,1,5,'../../media/images/wine/01141.png',2),(142,'르 꼰떼쎄, 스푸만테 퀴베 엑스트라 드라이','Le Contesse, Spumate Cuvee Extra Dry',4,750,13.0,1,4,1,4,'../../media/images/wine/01142.png',2),(143,'르 꼰떼쎄, 라보소 3 스푸만테 브뤼','Le Contesse, Raboso Rose Spumante Brut',4,750,13.0,1,4,1,1,'../../media/images/wine/01143.jpg',2),(144,'포지오 알 기우죠, 볼타치노 비앙코','Poggio al Chiuso, Voltaccino Bianco',2,750,13.0,1,3,1,1,'../../media/images/wine/01144.jpg',2),(145,'포지오 알 기우죠, 볼타치노 로쏘 토스카나','Poggio al Chiuso, Voltaccino Rosso Toscana',1,750,14.0,1,3,3,2,'../../media/images/wine/01145.jpg',2),(146,'까디 라오, 모스카토','Ca\'di Rajo, Moscato',2,750,7.0,4,2,1,2,'../../media/images/wine/01146.jpg',2),(147,'까디 라오, 프로세코 브뤼','Ca\'di Rajo, Prosecco Brut',4,750,12.0,1,4,1,4,'../../media/images/wine/01147.jpg',2),(148,'까디 라오, 피노 그리지오','Ca\'di Rajo, Pinot Grigio',2,750,13.0,1,3,1,2,'../../media/images/wine/01148.png',2),(149,'까디 라오, 트라미너','Ca\'di Rajo, Traminer',2,750,13.0,1,3,1,5,'../../media/images/wine/01149.png',2),(150,'까디 라오, 카베르네 프랑','Ca\'di Rajo, Cabernet Franc',1,750,13.0,1,4,4,1,'../../media/images/wine/01150.png',2),(151,'까디 라오, 카베르네 소비뇽','Ca\'di Rajo, Cabernet Sauvignon',1,750,13.0,1,4,4,1,'../../media/images/wine/01151.png',2),(152,'마쩨이, 테라 마쩨이','Mazzei, Terra Mazzei',1,750,14.0,1,3,4,2,'../../media/images/wine/01152.jpg',2),(153,'아덴기, 발도미노 뀌베 브뤼','Ardenghi, Valdomino Cuvee Brut',4,750,12.0,1,3,1,2,'../../media/images/wine/01153.jpg',2),(154,'보시오, 트로피칼 모스카토 패션 후르츠','Bosio, Tropical Moscato Passion Fruit',2,750,5.5,4,2,1,1,'../../media/images/wine/01154.jpg',2),(155,'보시오, 트로피칼 모스카토 망고','Bosio, Tropical Moscato Mango',2,750,5.5,4,2,1,1,'../../media/images/wine/01155.jpg',2),(156,'카사 비앙카, 트레비아노 다브루쪼','Casabianca, Trebbiano d\'Abruzzo',2,750,13.0,1,4,1,1,'../../media/images/wine/01156.jpg',2),(157,'카사비앙카, 몬테풀치아노 다브루쪼','Casabianca, Montepulciano d\'Abruzzo',1,750,14.0,1,3,3,5,'../../media/images/wine/01157.jpg',2),(158,'치엘로 나인 프리잔테 로사토','Cielo 9 Frizzante Rosato',4,750,9.0,2,3,1,1,'../../media/images/wine/01158.jpg',2),(159,'치엘로 나인 프리잔테 비앙코','Cielo 9 Frizzante Bianco',4,750,9.0,1,3,1,1,'../../media/images/wine/01159.jpg',2),(160,'피플','People',2,750,13.0,2,3,1,5,'../../media/images/wine/01160.jpg',2),(161,'발레벨보, 핑크 모스카토 스푸만테','Vallebelbo, Pink Moscato Spumante',4,750,7.0,4,2,1,2,'../../media/images/wine/01161.jpg',2),(162,'레 모레, 스위트 2','Le Morre, Sweet White',4,750,6.0,4,1,1,1,'../../media/images/wine/01162.jpg',2),(163,'마쏘 안티코 프리미티보','Masso Antico Primitivo',1,750,15.0,2,2,3,3,'../../media/images/wine/01163.jpg',2),(164,'우마니 론끼, 요리오 S','Umani Ronchi, Jorio S',1,750,13.5,1,4,3,1,'../../media/images/wine/01164.jpg',2),(165,'까잘리 델 바로네 150 + 1 피에몬테 바르베라','Casali del Barone 150 + 1 Piemonte Barbera',1,750,14.0,1,4,2,2,'../../media/images/wine/01165.jpg',2),(166,'두카 디 사락냐노, 떼레 시칠리아네','Duca di Saragnano, Terre Siciliane',1,750,15.0,1,3,3,2,'../../media/images/wine/01166.png',2),(167,'고젤리노 비니, 브릭 다 루 모스카토 다스티','Gozzelino Vini, Bric da Lu Moscato d\'Asti',2,750,5.5,4,2,1,3,'../../media/images/wine/01167.png',2),(168,'페우디, 프리미티보 디 만두리아','Feudi, Primitivo di Manduria',1,750,14.5,1,3,3,2,'../../media/images/wine/01168.png',2),(169,'페우디, 라크리마 크리스티 비앙코','Feudi, Lacryma Christi del Vesuvio Bianco',2,750,12.6,1,3,1,4,'../../media/images/wine/01169.png',2),(170,'페우디, 라크리마 크리스티 로쏘','Feudi, Lacryma Christi Rosso',1,750,13.4,1,3,3,4,'../../media/images/wine/01170.png',2),(171,'지오그라피코, 파보 네로','Geografico, Pavo Nero',1,750,15.0,1,3,4,1,'../../media/images/wine/01171.jpg',2),(172,'미켈레 끼아를로, 루나 모스카토 다스티','Michele Chiarlo, Luna Moscato d\'Asti',2,750,6.0,4,2,1,2,'../../media/images/wine/01172.png',2),(173,'만텔라시, 일 카네토','Mantellassi, Il Canneto',1,750,14.0,1,3,3,1,'../../media/images/wine/01173.png',2),(174,'만텔라시, 사쏘 비앙코','Mantellassi, Sasso Bianco',2,750,13.0,1,3,1,1,'../../media/images/wine/01174.png',2),(175,'만텔라시, 마에스트랄레','Mantellassi, Maestrale',1,750,14.0,1,3,3,1,'../../media/images/wine/01175.png',2),(176,'꽁까 도로, 스푸만떼 돌체 벨레노 모스카토/라보소 드미 섹','Conca d,oro, Spumante Dolce Veleno Moscasto/Raboso Demi Sec',4,750,11.0,4,2,1,5,'../../media/images/wine/01176.jpg',2),(177,'꽁까 도로, 프로세코 뀌베 노빌레 브뤼','Conca d\'oro, Prosecco Cuvee Nobile Brut',4,750,12.0,1,3,1,1,'../../media/images/wine/01177.jpg',2),(178,'꽁까 도로, 프로세코 뀌베 오로 엑스트라 드라이 밀레시마또','Conca d\'Oro, Prosecco Cuvee Oro Extra Dry Millesimato',4,750,11.5,1,3,1,3,'../../media/images/wine/01178.jpg',2),(179,'그라치아노 델라 세타, 로쏘 디 몬테풀치아노','Gracciano Della Seta, Rosso di Motepulciano',1,750,14.0,1,3,3,1,'../../media/images/wine/01179.jpg',2),(180,'자카니니, 크리스탈 트위그 트레비아노 다부르쪼','Zaccagnini, Crystal Twig Trebbiano d\'Aburzzo',2,750,12.0,1,4,1,1,'../../media/images/wine/01180.jpg',2),(181,'칸티나 테를란, 뮐러 투르가우','Cantina Terlan, Müller Thurgau',2,750,12.5,1,3,1,4,'../../media/images/wine/01181.jpg',2),(182,'칸티나 테를란, 게뷔르츠트라미너','Cantina Terlan, Gewurztraminer',2,750,14.0,1,3,1,2,'../../media/images/wine/01182.jpg',2),(183,'칸티나 테를란, 피노 비앙코','Cantina Terlan, Pinot Bianco',2,750,13.0,1,3,1,5,'../../media/images/wine/01183.jpg',2),(184,'룽가로티, 루','Lungarotti, L\'U',1,750,14.0,1,3,2,4,'../../media/images/wine/01184.jpg',2),(185,'테사리, 그리셀라 소아베 클라시코','Tessari, Grisela Soave Classico',2,750,13.0,1,4,1,1,'../../media/images/wine/01185.jpg',2),(186,'콜리 페사레시 산지오베제','Colli Pesaresi Sangiovese',1,750,13.0,1,3,2,1,'../../media/images/wine/01186.jpg',2),(187,'비앙켈로 델 메타우로','Bianchello del Metauro',2,750,12.0,1,3,1,1,'../../media/images/wine/01187.jpg',2),(188,'아카데미아, 리몬첼로','Accademia, Limoncello',5,750,30.0,4,2,1,2,'../../media/images/wine/01188.jpg',2),(189,'지오그라피코, 보스코 델 그릴로 고베르노','Geografico, Bosco del Grillo Governo',1,750,14.0,1,3,3,1,'../../media/images/wine/01189.png',2),(190,'팔라찌 블랑 드 블랑 밀레시마토','Palazzi Blanc de Blancs Millesimato',4,750,11.0,1,3,1,5,'../../media/images/wine/01190.jpg',2),(191,'루메지오 디 비앙코 콘트로구에라','Lumeggio di Bianco Controguerra',2,750,13.0,1,3,1,1,'../../media/images/wine/01191.jpg',2),(192,'챠오 스프리츠','Ciao Sfritz',2,200,6.9,4,2,1,1,'../../media/images/wine/01192.jpg',2),(193,'챠오 모스카토','Ciao Moscato',2,200,8.0,4,2,1,2,'../../media/images/wine/01193.jpg',2),(194,'챠오 레몬 피치','Ciao Lemon Peach',4,200,5.0,4,2,1,1,'../../media/images/wine/01194.jpg',2),(195,'챠오 비앙코','Ciao Bianco',2,200,10.5,2,2,1,2,'../../media/images/wine/01195.jpg',2),(196,'산 마르짜노, 벨리타 로쏘','San Marzano, Belita Rosso',1,750,14.0,3,2,3,2,'../../media/images/wine/01196.jpg',2),(197,'산 마르짜노, 벨리타 비앙코','San Marzano, Belita Bianco',2,750,12.0,3,2,1,3,'../../media/images/wine/01197.jpg',2),(198,'까스텔로 반피, 폰타넬레 샤르도네','Castello Banfi, Fontanelle Chardonnay',2,750,15.0,1,3,1,2,'../../media/images/wine/01198.jpg',2),(199,'코르테 지아라, 메를로 코르비나','Corte Giara, Merlot Corvina',1,750,13.0,1,3,2,2,'../../media/images/wine/01199.jpg',2),(200,'칸티, 브라케토 핑크 에디션','Canti, Brachetto Pink Edition',1,750,6.0,4,1,2,1,'../../media/images/wine/01200.jpg',2),(201,'칸티, 피에몬테 브라케토','Canti, Piemonte Brachetto',1,750,6.0,4,1,2,2,'../../media/images/wine/01201.jpg',2),(202,'깐티네 포베로, 모스카토 다스티 \'캄포 델 팔리오\'','Cantine Povero, Moscato d\'Asti \'Campo del Palio\'',2,750,5.5,4,2,1,1,'../../media/images/wine/01202.jpg',2),(203,'네스폴리, 르 코스테','Poderi dal Nespoli, Le Coste',2,750,13.0,1,3,1,4,'../../media/images/wine/01203.jpg',2),(204,'네스폴리, 피코 그란데','Poderi dal Nespoli, Fico Grande',1,750,14.0,1,4,3,1,'../../media/images/wine/01204.jpg',2),(205,'네스폴리, 파가데빗','Poderi dal Nespoli, Pagadebit',2,750,13.0,1,3,1,5,'../../media/images/wine/01205.jpg',2),(206,'네스폴리, 네스폴리노 비앙코','Poderi dal Nespoli, Nespolino Bianco',2,750,12.0,1,3,1,4,'../../media/images/wine/01206.png',2),(207,'몬탈토 까따라또 바이오','Montalto Cataratto Bio',2,750,12.0,1,3,1,1,'../../media/images/wine/01207.jpg',2),(208,'몬탈토 네로다볼라 바이오','Montalto Nero d\'Avola Bio',1,750,13.0,1,3,2,3,'../../media/images/wine/01208.jpg',2),(209,'카를로 펠레그리노, 트라이마리','Carlo Pellegrino, Traimari',4,750,12.0,3,2,1,5,'../../media/images/wine/01209.jpg',2),(210,'메짜코로나, 메를로','Mezzacorona, Merlot',1,750,14.0,1,3,3,2,'../../media/images/wine/01210.jpg',2),(211,'코르테 지아라 메를로','Corte Giara Merlot',1,750,13.0,1,2,3,3,'../../media/images/wine/01211.jpg',2),(212,'코르테 지아라 샤르도네','Corte Giara Chardonnay',2,750,13.0,1,3,1,2,'../../media/images/wine/01212.jpg',2),(213,'코르테 지아라, 피노 그리지오','Corte Giara, Pinot Grigio',2,750,13.0,1,3,1,3,'../../media/images/wine/01213.jpg',2),(214,'카사 디 로코 키안티','Casa di Rocco Chianti',1,750,12.5,1,4,2,3,'../../media/images/wine/01214.jpg',2),(215,'엘비오 코뇨, 돌체토 달바','Elvio Cogno, Dolcetto d\'Alba',1,750,14.0,1,4,3,2,'../../media/images/wine/01215.png',2),(216,'베끼아 토레, 살리스 살렌티노 로쏘','Vecchia Torre, Salice Salentino Rosso',1,750,13.5,1,3,3,3,'../../media/images/wine/01216.jpg',2),(217,'아비뇨네지 비앙코 토스카나','Avignonesi Bianco Toscana',2,750,12.5,1,4,1,1,'../../media/images/wine/01217.jpg',2),(218,'아바찌아, 블루문 모스카토','Abbazia, Blue moon Moscato',4,750,8.0,4,2,1,1,'../../media/images/wine/01218.jpg',2),(219,'발레벨보, 모스카토 다스티 라마렝까','Vallebelbo, Moscato d\'Asti La Marenca',2,750,5.5,4,2,1,1,'../../media/images/wine/01219.jpg',2),(220,'테누타 산 안토니오, 스카이아 비앙코','Tenuta Sant\' Antonio, Scaia Bianco',2,750,13.0,1,4,1,2,'../../media/images/wine/01220.jpg',2),(221,'리베라, 프리미티보','Rivera, Primitivo',1,750,14.0,1,3,4,3,'../../media/images/wine/01221.png',2),(222,'콘타리니, 발세 스푸만테 모스카토 돌체','Contarini, Valse Spumante Moscato Dolce',4,750,8.0,4,1,1,4,'../../media/images/wine/01222.jpg',2),(223,'세르지오 그리말디, 모스카토 다스티','Sergio Grimaldi, Moscato d\'Asti',2,750,5.0,4,2,1,2,'../../media/images/wine/01223.jpg',2),(224,'판티니 프리모 말바시아 샤르도네','Fantini Primo Malvasia Chardonnay',2,750,12.0,1,3,1,5,'../../media/images/wine/01224.jpg',2),(225,'라 또르데라, 사오미 프로세코','La Tordera, Saomi Prosecco',4,750,12.0,2,3,1,5,'../../media/images/wine/01225.jpg',2),(226,'토레셀라 산지오베제','Torresella Sangiovese',1,750,13.5,1,4,3,3,'../../media/images/wine/01226.jpg',2),(227,'산테로, 트루아젤 모스카토','Santero, Troisl Moscato',2,750,5.0,4,1,1,5,'../../media/images/wine/01227.jpg',2),(228,'엠 3','M Rose',3,750,3.0,4,1,1,1,'../../media/images/wine/01228.jpg',2),(229,'엠','M',2,750,3.0,4,2,1,2,'../../media/images/wine/01229.jpg',2),(230,'티모라쏘 그루','Timorasso Grue',2,750,14.5,1,3,1,4,'../../media/images/wine/01230.jpg',2),(231,'디레토 2','Diletto White',2,750,13.5,1,4,1,5,'../../media/images/wine/01231.jpg',2),(232,'콜 데 살리치 프로세코','Col de Salici Prosecco',4,750,11.0,2,3,1,4,'../../media/images/wine/01232.jpg',2),(233,'라 마르카, 프로세코','La Marca, Prosecco',4,750,12.0,1,4,1,5,'../../media/images/wine/01233.png',2),(234,'간치아, 피노 디 피노 3','Gancia, Pinot Di Pinot Rose',4,750,11.5,2,2,1,5,'../../media/images/wine/01234.jpg',2),(235,'또스띠, 3%','Tosti, 3%',2,750,4.0,4,2,1,4,'../../media/images/wine/01235.jpg',2),(236,'체사리 보스카렐','Cesari Boscarel',1,750,13.5,1,3,3,1,'../../media/images/wine/01236.jpg',2),(237,'프루노토 & 안티노리 프루노토 모스카토 다스티','Prunotto & Antinori Prunotto Moscato d\'Asti',2,750,5.0,4,2,1,3,'../../media/images/wine/01237.jpg',2),(238,'안티노리, 키안티 클라시코 페폴리','Antinori, Chianti Classico Peppoli',1,750,13.0,1,3,3,2,'../../media/images/wine/01238.png',2),(239,'산타 크리스티나 캄포그란데 오르비에토 클라시코','Santa Cristina Campogrande Orvieto Classico',2,750,12.0,1,3,1,2,'../../media/images/wine/01239.jpg',2),(240,'산타 크리스티나 피노 그리지오','Santa Cristina Pinot Grigio',2,750,11.5,1,3,1,5,'../../media/images/wine/01240.jpg',2),(241,'프레스코발디, 레몰레 로쏘','Frescobaldi, Remole Rosso',1,750,13.0,1,3,4,2,'../../media/images/wine/01241.jpg',2),(242,'카스텔라레, 키안티 클라시코','Castellare, Chianti Classico',1,750,13.5,1,4,3,2,'../../media/images/wine/01242.png',2),(243,'보떼르 모스카토','Botter Moscato',2,750,8.0,4,2,1,2,'../../media/images/wine/01243.jpg',2),(244,'비니 라 델리찌아 마스카레리 프로쎄코','Vini la delizia Mascareri Prosecco',4,750,11.0,1,3,1,5,'../../media/images/wine/01244.jpg',2),(245,'테누타 산 안토니오, 스카이아 코르비나','Tenuta Sant\' Antonio, Scaia Corvina',1,750,14.0,1,3,3,1,'../../media/images/wine/01245.jpg',2),(246,'우마니론끼, 요리오 몬텔풀치아노 다부르쪼','Umani Ronchi, Jorio Montepulciano d\'Abruzzo',1,750,13.5,1,4,3,1,'../../media/images/wine/01246.jpg',2),(247,'우마니 론끼, 비고르','Umani Ronchi, Vigor',1,750,14.0,1,3,4,2,'../../media/images/wine/01247.jpg',2),(248,'우마니 론끼 요리오 2','Umani Ronchi Jorio Bianco',2,750,13.0,1,4,1,5,'../../media/images/wine/01248.jpg',2),(249,'칸티네 젬마 모스카토 다스티 비나 피오리타','Cantine Gemma Moscato d\'Asti Vigna Fiorita',2,750,5.6,4,2,1,2,'../../media/images/wine/01249.jpg',2),(250,'페우디 바실리스코 테오도시오','Feudi Basilisco Teodosio Aglianico del Vulture',1,750,13.5,1,2,4,2,'../../media/images/wine/01250.jpg',2),(251,'브라이다, 일 바치알레 몽페라토 로쏘','Braida, Il Baciale Monferrato Rosso',1,750,13.5,1,4,4,3,'../../media/images/wine/01251.jpg',2),(252,'브라이다, 브라케토 다퀴','Braida, Brachetto d\'Acqui',4,750,5.5,4,1,1,5,'../../media/images/wine/01252.jpg',2),(253,'체사리, 소아베 클라시코','Cesari, Soave Classico',2,750,12.0,1,4,1,2,'../../media/images/wine/01253.jpg',2),(254,'프로두토리 델 바르바레스코 랑게 네비올로','Produttori del Barbaresco Langhe Nebbiolo',1,750,15.0,1,3,4,1,'../../media/images/wine/01254.jpg',2),(255,'끼알리 러브 홀릭 스위트 비앙코','Chiarli Love Holic Sweet Bianco',2,750,4.0,3,1,1,1,'../../media/images/wine/01255.jpg',2),(256,'메디치 에르메테, 퀘르치올리 람브루스코 레지아노 드라이','Medici ERmete, Quercioli Lambrusco Reggiano Dry',4,750,12.0,2,2,1,2,'../../media/images/wine/01256.jpg',2),(257,'메디치 에르메테, 보춀로','Medici Ermete, Bocciolo',4,750,7.5,3,3,1,1,'../../media/images/wine/01257.jpg',2),(258,'센시, 키안티 리제르바 \'달캄포\'','Sensi, Chianti Riserva \'Dalcampo\'',1,750,13.5,1,4,3,2,'../../media/images/wine/01258.jpg',2),(259,'센시, 키안티','Sensi, Chianti',1,750,13.0,1,4,2,2,'../../media/images/wine/01259.jpg',2),(260,'콜리모로, 몬테풀치아노 다부르쪼','Colimoro, Montepulciano d\'Abruzzo',1,750,13.0,1,3,3,4,'../../media/images/wine/01260.jpg',2),(261,'나인 닷 파이브 스위트 모스카토','Nine dot Five 9.5 Cold Wine Sweet Moscato',4,750,7.5,4,1,1,1,'../../media/images/wine/01261.jpg',2),(262,'보르고 라메 비앙코','Borgo lame Bianco',2,750,4.5,4,2,1,2,'../../media/images/wine/01262.jpg',2),(263,'보르고 라메 로소','Borgo Lame Rosso',1,750,6.0,4,1,2,1,'../../media/images/wine/01263.jpg',2),(264,'벨라누 로쏘 돌체','Belanu Rosso Dolce',1,750,10.0,4,1,2,1,'../../media/images/wine/01264.jpg',2),(265,'보르고 라메 모스카토 다스티','Borgo Lame Moscato d\'Asti',2,750,5.5,4,2,1,2,'../../media/images/wine/01265.jpg',2),(266,'파이니스트 볼게리','Finest Bolgheri',1,750,13.5,1,3,3,1,'../../media/images/wine/01266.jpg',2),(267,'원글라스 피노 그리지오','One Glass Pinot Grigio',2,100,12.5,1,4,1,4,'../../media/images/wine/01267.jpg',2),(268,'원글라스 베르멘티노','One Glass Vermentino',2,100,13.0,1,3,1,2,'../../media/images/wine/01268.jpg',2),(269,'원글라스 산지오베제','One Glass Sangiovese',1,100,13.0,1,3,2,1,'../../media/images/wine/01269.jpg',2),(270,'원글라스 까베르네 소비뇽','One Glass Cabernet Sauvignon',1,100,13.0,1,3,3,3,'../../media/images/wine/01270.jpg',2),(271,'포지오 스칼레테, 키안티 클라시코','Poggio Scalette, Chianti Classico',1,750,13.5,1,4,3,2,'../../media/images/wine/01271.png',2),(272,'빌라 엠 3','Villa M Rose',3,750,5.0,4,1,1,2,'../../media/images/wine/01272.jpg',2),(273,'프레스첼로 1 스위트','Freschello Red Sweet',1,750,9.5,5,1,2,1,'../../media/images/wine/01273.jpg',2),(274,'까넬리, 꽈뜨로 비앙코','Canelli, Quattro Bianco',2,750,4.0,4,2,1,1,'../../media/images/wine/01274.jpg',2),(275,'까넬리, 꽈뜨로 로쏘','Canelli, Quattro Rosso',1,750,4.0,4,1,2,4,'../../media/images/wine/01275.jpg',2),(276,'간치아, 프로세코','Gancia, Prosecco',4,750,12.0,2,3,1,5,'../../media/images/wine/01276.jpg',2),(277,'타울레로, 몬테풀치아노 다브루쪼','Thaulero, Montepulciano d\'Abruzzo',1,750,14.0,1,3,3,1,'../../media/images/wine/01277.jpg',2),(278,'타울레로, 트레비아노 다브루쪼','Thaulero, Trebbiano d\'Abruzzo',2,750,13.0,1,4,1,2,'../../media/images/wine/01278.jpg',2),(279,'캐빗, 산비질리오 모스카토 돌체','Cavit, SanVigilio Moscato Dolce',4,750,8.0,4,2,1,2,'../../media/images/wine/01279.jpg',2),(280,'캐빗, 컬렉션 피노 누아','Cavit Collection Pinot Noir',1,750,12.0,1,3,2,2,'../../media/images/wine/01280.jpg',2),(281,'캐빗, 컬렉션 피노 그리지오','Cavit, Collection Pinot Grigio',2,750,12.0,1,4,1,2,'../../media/images/wine/01281.jpg',2),(282,'미켈레 끼아를로, \'니볼레\' 모스카토 다스티','Michele Chiarlo, \'Nivole\' Moscato d\'Asti',2,375,5.0,4,2,1,1,'../../media/images/wine/01282.jpg',2),(283,'카사노 마르살라 파인','Casano Marsala Fine',2,1000,17.0,5,2,2,5,'../../media/images/wine/01283.jpg',2),(284,'도피오 파소 프리미티보','Doppio Passo Primitivo',1,750,13.0,1,2,4,2,'../../media/images/wine/01284.jpg',2),(285,'꽁트리 스푸만티, 코르테 비올라 모스카토 돌체','Contri Spumanti, Corte Viola Moscato Dolce',4,750,7.0,4,1,1,4,'../../media/images/wine/01285.jpg',2),(286,'메짜코로나, 피노그리지오','Mezzacorona, Pinot Grigio',2,750,13.0,1,3,1,2,'../../media/images/wine/01286.jpg',2),(287,'메짜코로나, 까베르네 소비뇽','Mezzacorona, Cabernet Sauvignon',1,750,14.0,1,3,3,2,'../../media/images/wine/01287.jpg',2),(288,'알로이스 라게더, 리프 피노 그리지오','Alois Lageder, Riff Pinot Grigio',2,750,12.5,1,3,1,5,'../../media/images/wine/01288.jpg',2),(289,'알로이스 라게더, 리프 메를로 까베르네','Alois Lageder, Riff Merlot Cabernet',1,750,13.5,1,4,3,2,'../../media/images/wine/01289.jpg',2),(290,'쿠수마노, 인졸리아','Cusumano, Insolia',2,750,14.0,1,3,1,4,'../../media/images/wine/01290.jpg',2),(291,'리카솔리, 키안티 델 바론 리카솔리','Ricasoli, Chianti del Barone Ricasoli',1,750,13.0,1,4,3,2,'../../media/images/wine/01291.jpg',2),(292,'체레토, 모스카토 다스티','Ceretto, Moscato d\'Asti',2,375,5.5,4,2,1,2,'../../media/images/wine/01292.jpg',2),(293,'까삐께라 린토리 베르멘티노','Capichera Lintori Vermentino',2,750,13.5,1,3,1,2,'../../media/images/wine/01293.jpg',2),(294,'로레단 가스파리니, 프로세코 브뤼','Loredan Gasparini, Prosecco Brut',4,750,11.0,1,3,1,4,'../../media/images/wine/01294.jpg',2),(295,'스페리, 발폴리첼라 클라시코','Speri, Valpolicella Classico',1,750,12.5,1,3,3,2,'../../media/images/wine/01295.jpg',2),(296,'티펜브루너, 뮬러 트루가우','Tiefenbrunner, Muller Thurgau',2,750,12.5,1,3,1,2,'../../media/images/wine/01296.jpg',2),(297,'펠시나, 키안티 콜리 세네시','Felsina, Chianti Colli Senesi',1,750,14.0,1,4,3,1,'../../media/images/wine/01297.jpg',2),(298,'발레벨보, 돌체 루나','Vallebelbo, Dolce Luna',2,750,2.0,4,2,1,1,'../../media/images/wine/01298.jpg',2),(299,'발레벨보, 돌체 루체','Vallebelbo, Dolce Luce',4,750,2.0,4,1,1,2,'../../media/images/wine/01299.jpg',2),(300,'또스띠, 핑크 모스카토','Tosti, Pink Moscato',4,750,7.0,4,2,1,1,'../../media/images/wine/01300.png',2),(301,'일 팔라지오, 뉴 데이 로사토','Il Palagio, New Day Rosato',3,750,12.5,1,3,2,4,'../../media/images/wine/01301.png',2),(302,'쥬세페 코르테제, 랑게 돌체토','Giuseppe Cortese, Langhe Dolcetto',1,750,13.0,1,4,3,2,'../../media/images/wine/01302.jpg',2),(303,'아카데미아, 3 스푸만테','Accademia, Rose Spumante',3,750,12.0,2,3,1,2,'../../media/images/wine/01303.jpg',2),(304,'베리 브라더스 & 러드, 프로세코','Berry Bros. & Rudd, Prosecco',4,750,11.0,1,3,1,4,'../../media/images/wine/01304.jpg',2),(305,'베리 브라더스 & 러드, 키안티','Berry Bros. & Rudd, Chianti',1,750,13.0,1,4,3,5,'../../media/images/wine/01305.jpg',2),(306,'베리 브라더스 & & 러드, 네로 다볼라','Berry Bros. & Rudd, Nero d\'Avola',1,750,14.0,1,3,3,1,'../../media/images/wine/01306.jpg',2),(307,'레 모레, 스위트 2','Le Morre, Sweet White',4,750,6.0,4,1,1,1,'../../media/images/wine/01307.jpg',2),(308,'베리 브라더스 & 러드, 피노 그리지오','Berry Bros. & Rudd, Pinot Grigio',2,750,12.0,1,3,1,4,'../../media/images/wine/01308.jpg',2),(309,'모스케토 핑크','Mosketto Pink',3,750,6.0,4,2,1,1,'../../media/images/wine/01309.jpg',2),(310,'칸티, 아스티 세코 뀌베 C.21','Canti, Asti Secco Cuvee C.21',4,750,11.0,1,2,1,3,'../../media/images/wine/01310.jpg',2),(311,'리베라, 프렐루디오 넘버 원 샤도네이','Rivera, Preludio N.1 Chardonnay',2,750,12.0,2,4,1,2,'../../media/images/wine/01311.jpg',2),(312,'틴테로, 소리 그라멜라 모스카토 다스티','Tintero, Sori Gramella Moscato d\'Asti',2,750,6.0,3,3,1,5,'../../media/images/wine/01312.png',2),(313,'소벨로','Sorbello',1,750,10.0,1,3,3,1,'../../media/images/wine/01313.jpg',2),(314,'메디치 에르메테, 퀘르치올리 람브루스코 레지아노 스위트','Medici Ermete, Quercioli Lambrusco Reggiano Sweet',4,750,8.5,4,2,2,1,'../../media/images/wine/01314.jpg',2),(315,'루피노, 토르가이오 토스카나','Ruffino, Torgaio Toscana',1,750,12.5,1,3,2,2,'../../media/images/wine/01315.jpg',2),(316,'루피노, 프로세코 엑스트라 드라이','Ruffino, Prosecco Extra Dry',4,750,11.0,1,3,1,1,'../../media/images/wine/01316.jpg',2),(317,'루피노, 갈레스트로 토스카나','Ruffino, Galestro Toscana',2,750,12.0,1,4,1,3,'../../media/images/wine/01317.jpg',2),(318,'까넬리, 꽈뜨로 3','Canelli, Quattro Rose',3,750,4.0,4,2,1,3,'../../media/images/wine/01318.jpg',2),(319,'까르피네토, 오리지날 토스카노','Carpinetto, Originale Toscano',1,750,13.0,1,3,3,5,'../../media/images/wine/01319.jpg',2),(320,'페스타 로쏘','Festa Rosso',1,750,4.0,4,1,1,1,'../../media/images/wine/01320.jpg',2),(321,'페스타 비앙코','Festa Bianco',2,750,4.0,4,2,1,2,'../../media/images/wine/01321.jpg',2),(322,'빌라 욜란다 모스카토 3','Villa Jolanda Moscato Rose',4,750,6.5,4,2,1,1,'../../media/images/wine/01322.png',2),(323,'슈미트 숀 퓐프 모스카토','Schmitt Sohne Funf Moscato',2,750,9.0,4,2,1,1,'../../media/images/wine/01323.jpg',2),(324,'피키모리','Fichimori',1,750,12.0,1,3,4,1,'../../media/images/wine/01324.jpg',2),(325,'안티노리, 빌라 안티노리 키안티 클라시코 리제르바','Antinori, Villa Antinori Chianti Classico Riserva',1,750,14.0,1,3,3,2,'../../media/images/wine/01325.png',2),(326,'안티노리, 빌라 안티노리 비앙코','Antinori, Villa Antinori Bianco',2,750,12.0,1,3,1,5,'../../media/images/wine/01326.jpg',2),(327,'아템즈, 피노 그리지오','Attems, Pinot Grigio',2,750,13.0,1,3,1,5,'../../media/images/wine/01327.jpg',2),(328,'아템즈, 소비뇽 블랑','Attems, Sauvignon Blanc',2,750,13.0,1,3,1,3,'../../media/images/wine/01328.jpg',2),(329,'발비 소프라니, 갈라로사','Balbi Soprani, Gala Rosa',1,750,5.5,4,2,1,2,'../../media/images/wine/01329.png',2),(330,'자르데또, 프로세코 수페리오레 폰데고 드라이','Zardetto, Prosecco Superiore Fondego Dry',4,750,11.5,1,3,1,4,'../../media/images/wine/01330.jpg',2),(331,'자르데또, 프라이빗 뀌베 브뤼','Zardetto, Private Cuvee Brut',4,750,11.0,1,2,1,5,'../../media/images/wine/01331.jpg',2),(332,'자르데또, 프로세코 엑스트라 드라이','Zardetto, Prosecco Extra Dry',4,750,12.0,1,4,1,1,'../../media/images/wine/01332.jpg',2),(333,'돈나푸가타, 루메라 로자토','Donnafugata, Lumera Rosato',3,750,13.0,1,3,2,5,'../../media/images/wine/01333.jpg',2),(334,'레 그로테 실레노 콘트로라 샤도네이','Le Grotte di Sileno Controra Chardonnay',2,750,16.0,1,3,1,5,'../../media/images/wine/01334.jpg',2),(335,'칼디롤라, 아만떼','Caldirola, Amante',1,750,10.0,4,2,2,3,'../../media/images/wine/01335.jpg',2),(336,'레보비쯔, 람부르스코 아마빌레','LEBOVITZ, Lambrusco Amabile',4,750,8.0,1,2,1,4,'../../media/images/wine/01336.jpg',2),(337,'아르파 시라','Arpa Syrah',1,750,14.0,1,3,3,2,'../../media/images/wine/01337.png',2),(338,'빌라 산디, 프로세코 수페리오레 엑스트라 드라이','Villa Sandi, Prosecco Superiore Extra Dry',4,750,11.0,1,3,1,4,'../../media/images/wine/01338.jpg',2),(339,'베르사노, 몬테올리보 모스카토 다스티','Bersano, Monteolivo Moscato d\'Asti',2,750,5.5,4,2,1,2,'../../media/images/wine/01339.jpg',2),(340,'탈라몬티, 트레비 트레비아노 다부르쪼 비앙코','Talamonti, Trebi Trebbiano d\'Abruzzo Bianco',2,750,13.0,3,3,1,5,'../../media/images/wine/01340.jpg',2),(341,'탈라몬티, 모다 몬테풀치아노 다부르쪼','Talamonti, Moda Montepulciano d\'Abruzzo',1,750,14.0,1,3,3,1,'../../media/images/wine/01341.jpg',2),(342,'제나토 발폴리첼라 수페리오레','Zenato Valpolicella Superiore',1,750,13.5,1,4,2,2,'../../media/images/wine/01342.jpg',2),(343,'제나토 루가나 산 베네데토','Zenato Lugana San Benedetto',2,750,13.0,1,3,1,2,'../../media/images/wine/01343.jpg',2),(344,'플라네타, 플럼바고','Planeta, Plumbago',1,750,14.0,1,3,3,1,'../../media/images/wine/01344.jpg',2),(345,'플라네타, 알라스트로','Planeta, Alastro',2,750,12.5,1,3,1,5,'../../media/images/wine/01345.jpg',2),(346,'플라네타, 라 세그레타 비앙코','Planeta, La Segreta Bianco',2,750,12.5,1,3,1,1,'../../media/images/wine/01346.jpg',2),(347,'플라네타, 라 세그레타 로쏘','Planeta, La Segreta Rosso',1,750,13.0,1,3,3,1,'../../media/images/wine/01347.jpg',2),(348,'프리가 로쏘','Frigga Rosso',1,750,4.0,4,1,2,1,'../../media/images/wine/01348.jpg',2),(349,'프리가 비앙코','Frigga Bianco',2,750,4.0,4,2,1,2,'../../media/images/wine/01349.jpg',2),(350,'산테로 모스카토 스푸만테','Santero Moscato Spumante',4,750,6.5,4,2,1,2,'../../media/images/wine/01350.jpg',2),(351,'토마 스파클링','Toma Sparking',4,750,7.0,1,3,1,2,'../../media/images/wine/2001.png',3),(352,'젠틀 래빗 샤도네이','Gentle Rabbit Chardonnay',2,750,13.5,1,3,1,5,'../../media/images/wine/2002.png',3),(353,'젠틀 래빗 카베르네 소비뇽','Gentle Rabbit Cabernet Sauvignon',1,750,14.5,1,3,3,1,'../../media/images/wine/2003.png',3),(354,'젠틀 래빗 블랙','Gentle Rabbit Black',1,750,14.0,1,3,2,1,'../../media/images/wine/2004.png',3),(355,'까스텔 델 레메이, 시코리스 템프라니요','Castell del Remei, Sicoris Tempranillo',1,750,14.0,1,3,3,3,'../../media/images/wine/2005.png',3),(356,'조셉 마삭스, 까바 브뤼 이모시오','Josep Masach, Cava Brut Emocio',4,750,12.0,1,4,1,5,'../../media/images/wine/2006.png',3),(357,'보데가스 라 레메디아도라, 소비뇽 블랑 라 빌라 레알','Bodegas La Remediadora, Sauvignon Blanc La Villa Real',2,750,12.5,1,3,1,3,'../../media/images/wine/2007.png',3),(358,'보데가스 라 레메디아도라, 스윗 모스카텔 라 빌라 레알','Bodegas La Remediadora, Sweet Moscatel La Villa Real',2,750,11.5,3,2,1,3,'../../media/images/wine/2008.png',3),(359,'보데가스 라 레메디아도라, 로블 템프라니오 라 빌라 레알 ','Bodegas La Remediadora, Roble Tempranillo La Villa Real',1,750,13.5,1,3,2,1,'../../media/images/wine/2009.png',3),(360,'보데가스 라 레메디아도라, 크리안자 카베르네 라 빌라 레알 ','Bodegas La Remediadora, Crianza Cabernet La Villa Real ',1,750,12.5,1,3,3,1,'../../media/images/wine/2010.png',3),(361,'낙낙 화이트 블랜드','Knock Knock White Blend',2,750,12.0,1,3,1,2,'../../media/images/wine/2011.png',3),(362,'낙낙 로제','Knock Knock Rose',3,750,12.0,1,3,2,4,'../../media/images/wine/2012.png',3),(363,'낙낙 레드 블랜드','Knock Knock Red Blend',1,750,13.0,1,3,3,1,'../../media/images/wine/2013.png',3),(364,'보데가스 페나스칼, 코랄 드 페나스칼','Bodegas Penascal, Coral de Penascal',3,750,12.0,1,3,2,2,'../../media/images/wine/2014.png',3),(365,'모나스테리오, 올드 바인 셀렉티드 하베스트','Monasterio, Old Vines Selected Harvest',1,750,14.0,1,3,3,3,'../../media/images/wine/2015.png',3),(366,'보데가스 셀라야, 에라두라 템프라니요 엘레강스','Bodegas Celaya, Herradura Tempranillo Elegance',1,750,7.2,1,3,3,1,'../../media/images/wine/2016.png',3),(367,'보데가스 셀라야, 에라두라 카베르네 소비뇽','Bodegas Celaya, Herradura Cabernet Sauvignon',1,750,12.5,1,3,4,2,'../../media/images/wine/2017.png',3),(368,'뻬레 벤뚜라, 까바 브륏 레세르바 아트 에디션 화이트','Pere Ventura, Cava Brut Reserva Art Edition White',4,750,11.5,2,4,1,2,'../../media/images/wine/2018.png',3),(369,'보데가스 까레, 산타 크루즈 세인트 존','Bodegas Care, Santa Cruz Saint John',1,750,14.0,1,4,3,1,'../../media/images/wine/2019.png',3),(370,'보데가스 까레, 산타 크루즈 세인트 마커스','Bodegas Care, Santa Cruz Saint Marcus',1,750,13.5,2,3,3,2,'../../media/images/wine/2020.png',3),(371,'보데가스 까레, 산타 크루즈 세인트 피터','Bodegas Care, Santa Cruz Saint Peter',1,750,14.0,1,4,3,2,'../../media/images/wine/2021.png',3),(372,'보데가스 까레, 산타 크루즈 세인트 폴','Bodegas Care, Santa Cruz Saint Paul',1,750,14.5,1,3,3,1,'../../media/images/wine/2022.png',3),(373,'보데가스 까레, 블랑코 소브레 리아스','Bodegas Care, Blanco Sobre Lias',2,750,13.0,1,4,1,3,'../../media/images/wine/2023.png',3),(374,'보데가스 까레, 트리오 레드 블렌드','Bodegas Care, Trio Red Blend',1,750,14.0,2,3,4,1,'../../media/images/wine/2024.png',3),(375,'파고 드 아일레스, L 드 아일레스','Pago de Ayles, L de Ayles',3,750,14.5,1,4,1,3,'../../media/images/wine/2025.png',3),(376,'수리올 상 드 드락 울 드 예브레','Suriol Sang de Drac Ull de Llebre',1,750,14.0,1,3,3,1,'../../media/images/wine/2026.png',3),(377,'보데가스 피놀드, 까바 디봉 아이스','Bodegas Pinord, Cava Dibon ICE',4,750,12.0,1,4,1,4,'../../media/images/wine/2027.png',3),(378,'카스텔블랑, 까바 브뤼 리제르바 ','Castellblanc, Cava Brut Reserva',4,750,12.0,1,3,1,2,'../../media/images/wine/2028.png',3),(379,'꼬도르뉴, 안나 아이스 까바 로제 ','Codorniu, Anna Ice Cava Rose',4,750,12.0,1,3,1,4,'../../media/images/wine/2029.png',3),(380,'보데가스 블레다, 까스틸로 데 후미야 오가닉','Bodegas Bleda, Castillo de Jumilla Organico',1,750,15.0,1,4,3,1,'../../media/images/wine/2030.png',3),(381,'풍크툼, 템프라니요','Punctum, Sin Sulfitos Anadidos Barrel Aged Tempranillo',1,750,14.0,1,3,3,2,'../../media/images/wine/2031.png',3),(382,'깜포 비에호, 와인메이커스 아트 ','Campo Viejo, Winemaker\'s Art',1,750,14.0,1,4,4,2,'../../media/images/wine/2032.png',3),(383,'깜포 비에호, 템프라니요','Campo Viejo, Tempranillo',1,750,14.0,1,4,3,1,'../../media/images/wine/2033.png',3),(384,'엘 카스티야 가르나차','El Castilla Garnacha',1,750,15.0,1,3,3,2,'../../media/images/wine/2034.png',3),(385,'엘 꼬또, 세미돌체','El Coto, Semidulce',2,750,12.0,2,3,1,2,'../../media/images/wine/2035.png',3),(386,'보데가스 넬레만, 저스트 화이트','Bodegas Neleman, Just Good Wine White',2,750,14.0,1,3,1,3,'../../media/images/wine/2036.png',3),(387,'보데가스 넬레만, 보발','Bodegas Neleman, Bobal',1,750,15.0,1,3,3,1,'../../media/images/wine/2037.png',3),(388,'보데가스 넬레만, 시그니쳐 크리안자','Bodegas Neleman, Signature Crianza',1,750,15.0,1,3,3,2,'../../media/images/wine/2038.png',3),(389,'보데가스 넬레만, 뉴클리 틴토','Bodegas Neleman, Nucli Tinto',1,750,14.0,1,3,3,2,'../../media/images/wine/2039.png',3),(390,'보데가스 넬레만, 비오그니어 버딜','Bodegas Neleman, Viognier-Verdil',2,750,12.0,1,3,1,4,'../../media/images/wine/2040.png',3),(391,'보데가스 넬레만, 올 데이 롱 템프라니요','Bodegas Neleman, All Day Long Tempranillo',1,750,14.0,1,3,3,2,'../../media/images/wine/2041.png',3),(392,'풍크툼, 포메라도 오렌지','Punctum, Pomelado Orange',2,750,14.0,1,4,2,4,'../../media/images/wine/2042.png',3),(393,'핑카 펠라, 깔라 레이 템프라니요 시라','Finca Fella, Cala Rey Tempranillo Syrah',1,750,14.0,1,3,3,1,'../../media/images/wine/2043.png',3),(394,'핑카 펠라, 깔라 레이 베르데호 소비뇽 블랑','Finca Fella, Cala Rey Verdejo Sauvignon Blanc',2,750,12.0,1,4,1,4,'../../media/images/wine/2044.png',3),(395,'펠릭스 솔리스, 깔리자 SAV','Felix Solis, Caliza SAV',2,750,12.0,1,4,1,4,'../../media/images/wine/2045.png',3),(396,'까스텔 델 레메이, 템프라니요','Castell del Remei, Tempranillo',1,750,14.0,1,3,3,3,'../../media/images/wine/2046.png',3),(397,'나바로 로페즈, 돈 바로소','Navarro Lopez, Don Barroso',1,750,12.0,1,3,3,1,'../../media/images/wine/2047.png',3),(398,'보데가스 까레, 핀카 반칼레스','Bodegas Care, Finca Bancales',1,750,15.0,1,3,3,3,'../../media/images/wine/2048.png',3),(399,'라 보데가스 푸리시마, 아줄러스 화이트','La Bodegas Purisima, Azules White',2,750,13.0,1,3,1,5,'../../media/images/wine/2049.png',3),(400,'보데가스 라 푸리시마, 캄풀러스 라 루비아 화이트','Bodegas La Purisima, Camplues La Rubia White',2,750,13.0,1,3,1,5,'../../media/images/wine/2050.png',3),(401,'보데가스 라 푸리시마, 캄풀러스 엘 모레노 레드','Bodegas La Purisima, Campules El Moreno Red',3,750,14.0,1,3,4,2,'../../media/images/wine/2051.png',3),(402,'토레스, 비냐 에스메랄다 스파클링','Torres, Vina Esmeralda Sparkling',4,750,12.0,1,4,1,5,'../../media/images/wine/2052.png',3),(403,'엘 카스티야 시라','El Castilla Syrah',1,750,15.0,1,3,3,1,'../../media/images/wine/2053.png',3),(404,'펠릭스 솔리스, 폴포 알바리뇨','Felix Solis, Pulpo Albarino',2,750,14.0,1,3,1,5,'../../media/images/wine/2054.png',3),(405,'호메세라, 부케 카바 로제','Jaume Serra, Bouquet Cava Rose',4,750,12.0,1,3,1,2,'../../media/images/wine/2055.png',3);
/*!40000 ALTER TABLE `win_wine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `win_wine_region`
--

DROP TABLE IF EXISTS `win_wine_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_wine_region` (
  `wine_region_id` int NOT NULL,
  `wine_region_name` varchar(100) NOT NULL,
  PRIMARY KEY (`wine_region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_wine_region`
--

LOCK TABLES `win_wine_region` WRITE;
/*!40000 ALTER TABLE `win_wine_region` DISABLE KEYS */;
INSERT INTO `win_wine_region` VALUES (1,'프랑스'),(2,'이탈리아'),(3,'스페인'),(4,'미국'),(5,'칠레'),(6,'other');
/*!40000 ALTER TABLE `win_wine_region` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-24 10:22:24
