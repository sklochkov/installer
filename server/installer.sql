set names utf8;

CREATE TABLE `servers` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`discover_date` datetime DEFAULT NULL,
	`mac` varchar(100) NOT NULL,
	`hostname` varchar(200) DEFAULT '',
	`status` int(11) NOT NULL DEFAULT 0,
	`profile_id` int(11) DEFAULT NULL,
	PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `server_info` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`server_id` int(11) NOT NULL,
	`name` varchar(100),
	`value` text,
	PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `server_parameters` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`server_id` int(11) NOT NULL,
	`name` varchar(100),
	`value` text,
	PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `profiles` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(150),
	`status` int(11) NOT NULL DEFAULT 0,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`name`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `profile_parameters` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
	`profile_id` int(11) NOT NULL,
        `name` varchar(150),
	`value` text,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`profile_id`, `name`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `server_statuses` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(100),
	PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `server_parameter_types` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100),
	PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `profile_parameter_types` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100),
        PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `repositories` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100),
	`url` varchar(500),
        PRIMARY KEY (`id`),
	UNIQUE KEY (`name`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

CREATE TABLE `profiles_repositories` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`profile_id` int(11) NOT NULL,
	`repo_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`profile_id`, `repo_id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ENGINE innodb;

INSERT INTO `server_statuses` (`id`, `name`) VALUES 
	(1, 'new'),
	(2, 'configured'),
	(3, 'installing'),
	(4, 'installed');

INSERT INTO `server_parameter_types` (`id`, `name`) VALUES 
	(1, 'cpu'),
	(2, 'mem'),
	(3, 'iface'),
	(4, 'disk');

INSERT INTO `profile_parameter_types` (`id`, `name`) VALUES 
        (1, 'hostname'),
        (2, 'network'),
        (3, 'disks'),
        (4, 'packages'),
	(5, 'repos'),
	(6, 'preinstall'),
	(7,'postinstall');

INSERT INTO `repositories` (`id`, `name`, `url`) VALUES
    (1, 'iqbuzz-6', 'http://bz-repo.srv.iqbuzz.ru/rhel/6/x86_64/');

