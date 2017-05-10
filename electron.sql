create database electron charset=utf8;

create table `github`(
  `id`  INT(11) AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255),
  `url` VARCHAR(255),
  `desc` text,
  `start` VARCHAR(255)
)