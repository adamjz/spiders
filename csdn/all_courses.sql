/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 127.0.0.1
 Source Database       : csdndb

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : utf-8

 Date: 07/02/2018 17:59:47 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `all_courses`
-- ----------------------------
DROP TABLE IF EXISTS `all_courses`;
CREATE TABLE `all_courses` (
  `id` int(16) NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `hours` int(16) DEFAULT NULL,
  `forwho` varchar(256) DEFAULT NULL,
  `joined_num` int(16) DEFAULT NULL,
  `price` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
