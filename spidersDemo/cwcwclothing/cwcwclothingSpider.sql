/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80034
 Source Host           : localhost:3306
 Source Schema         : crawled_outside

 Target Server Type    : MySQL
 Target Server Version : 80034
 File Encoding         : 65001

 Date: 14/07/2024 15:49:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cwcwclothing
-- ----------------------------
DROP TABLE IF EXISTS `cwcwclothing`;
CREATE TABLE `cwcwclothing`  (
  `title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品标题',
  `sort` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品分类',
  `num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '产品编号',
  `local_num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '本地产品文件夹编号',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '产品价格',
  `size` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品尺码',
  `color` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品颜色',
  `color_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '产品颜色对应的图片链接',
  `intro` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '产品介绍',
  `main_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '产品首图',
  `detail_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '产品详情图',
  `local_main_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '本地产品首图文件路径',
  `local_detail_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '本地产品详情图文件路径',
  `local_color_img` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL COMMENT '本地产品颜色对应的图片链接文件路径',
  `sale` int(0) NULL DEFAULT NULL COMMENT '产品销量',
  `talk` int(0) NULL DEFAULT NULL COMMENT '产品评价数量',
  `mark` decimal(5, 1) NULL DEFAULT NULL COMMENT '产品分数',
  `seo_title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '产品副标题',
  `seo_intro` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '产品副介绍',
  `seo_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品副关键词',
  `status` int(0) NULL DEFAULT 0 COMMENT '图片下载状态，默认为下载状态0，已下载状态1',
  `create_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `link` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '产品链接'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
