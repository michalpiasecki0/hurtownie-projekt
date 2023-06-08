if not exists (select name from sys.databases where name = 'dwh')
begin
create database dwh;
end

go

use dwh;

create table miastodim (
	id int not null identity(1,1) primary key,
	nazwa nvarchar(50) not null,
	wojewodztwo nvarchar(50) not null,
	szerokosc float not null,
	dlugosc float not null,
)

create table datedim (
	id int not null identity(1,1) primary key,
	realdate date not null,
	dayofweekval int not null,
	monthval int not null,
	yearval int not null
)


create table KlimatFakt (
	id int not null identity(1,1) primary key,
	dateid int references datedim(id),
	miastoid int references miastodim(id),
	tmin float,
	tavg float,
	tmax float,
	uwind float,
	vwind float,
	tenuwind float,
	tenvwind float,



)

create table qualityfact (
	id int not null identity(1,1) primary key,
	dateid int references datedim(id),
	pmten float not null,
	pmtwofive float not null,
	pmtenwildfires float not null,
	nitrogen float not null,
	dust float not null,
)

