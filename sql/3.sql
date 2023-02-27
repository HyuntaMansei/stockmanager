USE stock;
SHOW COLUMNS FROM testing;
show tables;

select * from temp_tb;
SELECT * FROM daily_stock_price_tb where market = 'KONEX';
SELECT * FROM data_matching_information_tb;

TRUNCATE TABLE daily_stock_price_tb;

DROP TABLE IF EXISTS data_matching_information_tb;
CREATE TABLE data_matching_information_tb (
    `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`from_table_name` VARCHAR(50) NOT NULL,
	`from_column_name` VARCHAR(50) NOT NULL,
	`to_table_name` VARCHAR(50) NOT NULL,
	`to_column_name` VARCHAR(50) NOT NULL,
	`created_date` DATETIME NOT NULL,
	`is_updated` CHAR(1) DEFAULT NULL,
	`updated_date` DATETIME DEFAULT NULL,
	`dup_test` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `dup_test` (`dup_test`)
);
SELECT * FROM data_matching_information_tb;
update table data_matching_information_tb
set to_column_name = 'listed_shares' where dup_test = '상장주식수 from temp_tb from daily_stock_price_tb';
SHOW PROCESSLIST;
KILL 27526;