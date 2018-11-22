/*
Navicat MySQL Data Transfer

Source Server         : maradb localhost
Source Server Version : 50721
Source Host           : 127.0.0.1:3307
Source Database       : my_data

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-10-30 15:54:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for bt_douban_result
-- ----------------------------
DROP TABLE IF EXISTS `bt_douban_result`;
CREATE TABLE `bt_douban_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bt_type` varchar(25) DEFAULT NULL,
  `bt_num` int(11) DEFAULT NULL,
  `douban_id` int(11) DEFAULT NULL,
  `result` varchar(20000) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2304 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for error_log
-- ----------------------------
DROP TABLE IF EXISTS `error_log`;
CREATE TABLE `error_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `error_type` varchar(50) DEFAULT NULL,
  `error_message` varchar(255) DEFAULT NULL,
  `error_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=958 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for exit_status
-- ----------------------------
DROP TABLE IF EXISTS `exit_status`;
CREATE TABLE `exit_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(25) DEFAULT NULL,
  `param` varchar(25) DEFAULT NULL,
  `other` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
