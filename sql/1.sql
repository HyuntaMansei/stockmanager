show databases;
use stock;
show grants;

drop table if EXISTS STOCK_BASIC_INFO_TB;
CREATE TABLE STOCK_BASIC_INFO_TB (
  id INT NOT NULL AUTO_INCREMENT,
  stock_code varchar(10) not null unique,
  stock_name VARCHAR(255) null,
  market_clas varchar(20) null,
  created_date datetime not null,
  is_updated char(1) null,
  updated_date DATETIME,
  PRIMARY KEY (id)
);

alter table STOCK_BASIC_INFO_TB add column market_clas varchar(20) default NULL;
alter table STOCK_BASIC_INFO_TB 

MODIFY market_clas varchar(20)
after stock_name;

insert into STOCK_BASIC_INFO_TB (stock_code, stock_name, market_clas, created_date) values ('123456', '메롱메롱메롱', 'ETF', NOW()) as (a, b, c, d)
on DUPLICATE KEY UPDATE stock_code = c;

insert into STOCK_BASIC_INFO_TB (stock_code, stock_name, market_clas, created_date) values ('123456', '메롱메롱메롱', 'ETF', NOW() as y)
on DUPLICATE KEY UPDATE stock_code=0;

insert into STOCK_BASIC_INFO_TB 
(stock_code, stock_name, market_clas, created_date) 
values ('123456', '메롱메롱메롱', 'ETF', NOW())
on duplicate key update 
stock_name = values(stock_name), market_clas = values(market_clas), is_updated = 'y', updated_date = now();

drop table if EXISTS STOCK_BASIC_INFO_TB;
SHOW TABLE STOCK_BASIC_INFO_TB;
DESC STOCK_BASIC_INFO_TB;
SELECT * from STOCK_BASIC_INFO_TB;
