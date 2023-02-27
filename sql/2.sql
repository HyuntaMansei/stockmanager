USE stock;
SHOW DATABASES;
SHOW TABLES;

ALTER TABLE BASIC_STOCK_INFO_TB RENAME basic_stock_info_tb;
ALTER TABLE DAILY_STOCK_PRICE_TB RENAME daily_stock_price_tb;

SHOW CREATE TABLE BASIC_STOCK_INFO_TB;
SHOW CREATE TABLE DAILY_STOCK_PRICE_TB;

DROP TABLE IF EXISTS `basic_stock_info_tb`;
CREATE TABLE `basic_stock_info_tb` (
   `id` INT(11) NOT NULL AUTO_INCREMENT,
   `ticker` VARCHAR(10) DEFAULT NULL,
   `stock_code` VARCHAR(10) NOT NULL,
   `stock_name` VARCHAR(255) DEFAULT NULL,
   `market` VARCHAR(20) DEFAULT NULL,
   `created_date` DATETIME NOT NULL,
   `is_updated` CHAR(1) DEFAULT NULL,
   `updated_date` DATETIME DEFAULT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `stock_code` (`stock_code`)
 );
SELECT * FROM `basic_stock_info_tb` WHERE market='konex';
 
DROP TABLE IF EXISTS `daily_stock_price_tb`;
CREATE TABLE `daily_stock_price_tb` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `trading_date` DATETIME DEFAULT NULL,
    `ticker` VARCHAR(10) DEFAULT NULL,
    `stock_code` VARCHAR(10) NOT NULL,
    `stock_name` VARCHAR(255) DEFAULT NULL,
    `market` VARCHAR(20) DEFAULT NULL,
    `department` VARCHAR(50) DEFAULT NULL,
    `open_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `high_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `low_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `close_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `cmpared_prev_price` DECIMAL(10 , 2 ) DEFAULT NULL,
    `fluctuation_rate` FLOAT4 DEFAULT NULL,
    `adj1_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `adj2_price` DECIMAL(10 , 2 ) UNSIGNED DEFAULT NULL,
    `trading_volume` BIGINT UNSIGNED DEFAULT NULL,
    `trading_value` BIGINT UNSIGNED DEFAULT NULL,
    `listed_shares` BIGINT UNSIGNED DEFAULT NULL,
    `market_cap` BIGINT UNSIGNED DEFAULT NULL,
    `created_date` DATETIME DEFAULT NULL,
    `is_updated` CHAR(1) DEFAULT NULL,
    `updated_date` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`)
);
SELECT * FROM `daily_stock_price_tb`;

show tables;
select * from daily_stock_price_tb;
show create table testing;

