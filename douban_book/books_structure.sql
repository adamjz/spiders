/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 127.0.0.1
 Source Database       : mydb

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : utf-8

 Date: 07/05/2018 15:00:07 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `books`
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `id` bigint(20) unsigned NOT NULL COMMENT 'ID号',
  `title` varchar(255) DEFAULT NULL COMMENT '书名',
  `author` varchar(255) DEFAULT NULL COMMENT '作者',
  `press` varchar(255) DEFAULT NULL COMMENT '出版社',
  `original` varchar(255) DEFAULT NULL COMMENT '原著名',
  `translator` varchar(128) DEFAULT NULL COMMENT '译者',
  `imprint` varchar(255) DEFAULT NULL COMMENT '出版年',
  `pages` int(10) unsigned DEFAULT NULL COMMENT '页数',
  `price` varchar(16) DEFAULT NULL COMMENT '定价',
  `binding` varchar(32) DEFAULT NULL COMMENT '装帧',
  `series` varchar(128) DEFAULT NULL COMMENT '丛书',
  `isbn` varchar(128) DEFAULT NULL COMMENT 'ISBN',
  `score` varchar(128) DEFAULT NULL COMMENT '评分',
  `votes` int(10) DEFAULT NULL COMMENT '评论人数',
  `url` varchar(255) DEFAULT NULL COMMENT 'URL链接',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
