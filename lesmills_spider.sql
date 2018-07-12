/*
 Navicat Premium Data Transfer

 Source Server         : ss
 Source Server Type    : MySQL
 Source Server Version : 50640
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 50640
 File Encoding         : 65001

 Date: 12/07/2018 19:08:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for club
-- ----------------------------
DROP TABLE IF EXISTS `club`;
CREATE TABLE `club` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `province` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `detail_area` varchar(255) DEFAULT NULL,
  `club_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=498 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for club_coach
-- ----------------------------
DROP TABLE IF EXISTS `club_coach`;
CREATE TABLE `club_coach` (
  `club_id` int(11) NOT NULL,
  `coach_id` int(11) NOT NULL,
  KEY `cl` (`club_id`),
  KEY `co` (`coach_id`),
  CONSTRAINT `cl` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `co` FOREIGN KEY (`coach_id`) REFERENCES `coach` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for club_lesson
-- ----------------------------
DROP TABLE IF EXISTS `club_lesson`;
CREATE TABLE `club_lesson` (
  `club_id` int(11) NOT NULL,
  `lesson_id` int(11) NOT NULL,
  KEY `club` (`club_id`),
  KEY `lesson` (`lesson_id`),
  CONSTRAINT `club` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for coach
-- ----------------------------
DROP TABLE IF EXISTS `coach`;
CREATE TABLE `coach` (
  `name` varchar(255) DEFAULT NULL,
  `id` int(255) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=991 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lesson
-- ----------------------------
DROP TABLE IF EXISTS `lesson`;
CREATE TABLE `lesson` (
  `name` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `icon` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lesson_coach
-- ----------------------------
DROP TABLE IF EXISTS `lesson_coach`;
CREATE TABLE `lesson_coach` (
  `lesson_id` int(255) DEFAULT NULL,
  `coach_id` int(255) DEFAULT NULL,
  KEY `les` (`lesson_id`),
  KEY `coa` (`coach_id`),
  CONSTRAINT `coa` FOREIGN KEY (`coach_id`) REFERENCES `coach` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `les` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
