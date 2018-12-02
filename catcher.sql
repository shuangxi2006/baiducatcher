/*Table structure for table `catcher` */

DROP TABLE IF EXISTS `catcher`;

CREATE TABLE `catcher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `media` varchar(16) DEFAULT NULL,
  `date` varchar(16) DEFAULT NULL,
  `summary` varchar(128) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`title`),
  UNIQUE KEY `TITLE` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=2143 DEFAULT CHARSET=utf8;
