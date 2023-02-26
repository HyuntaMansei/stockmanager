show databases;
use stock;
show grants;

drop table if exists STOCK_BASIC_INFO_TB;
create table STOCK_BASIC_INFO_TB (
    id int not null auto_increment,
    stock_code varchar(10) not null unique,
    stock_name varchar(255) null,
    market_clas varchar(20) null,
    created_date datetime not null,
    is_updated char(1) null,
    updated_date datetime,
    primary key (id)
);

alter table STOCK_BASIC_INFO_TB add column market_clas varchar(20) default null;
alter table STOCK_BASIC_INFO_TB

modify market_clas varchar(20)
after stock_name;

insert into STOCK_BASIC_INFO_TB (stock_code, stock_name, market_clas, created_date)
values ('123456', '메롱메롱메롱', 'etf', now())
on duplicate key update stock_name = values(stock_name), market_clas = values(market_clas), is_updated = 'y', updated_date = now();

drop table if exists STOCK_BASIC_INFO_TB;

use stock;
desc STOCK_BASIC_INFO_TB;
select * from STOCK_BASIC_INFO_TB where market_clas = 'kospi';

delete from STOCK_BASIC_INFO_TB where id=1;