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

CREATE TABLE datedim (
    id INT PRIMARY KEY,
    FullDate DATE,
    Day INT,
    Month INT,
    Year INT,
    DayOfWeek INT,
    DayName VARCHAR(20),
    MonthName VARCHAR(20),
    Quarter INT,
    IsWeekend BIT
);

GO

DECLARE @StartDate DATE = '2020-01-01';
DECLARE @EndDate DATE = '2040-12-31';

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO datedim (
        id,
        FullDate,
        Day,
        Month,
        Year,
        DayOfWeek,
        DayName,
        MonthName,
        Quarter,
        IsWeekend
    )
    VALUES (
        CONVERT(INT, CONVERT(VARCHAR(8), @StartDate, 112)),
        @StartDate,
        DAY(@StartDate),
        MONTH(@StartDate),
        YEAR(@StartDate),
        DATEPART(WEEKDAY, @StartDate),
        DATENAME(WEEKDAY, @StartDate),
        DATENAME(MONTH, @StartDate),
        DATEPART(QUARTER, @StartDate),
        CASE WHEN DATEPART(WEEKDAY, @StartDate) IN (1, 7) THEN 1 ELSE 0 END
    );

    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END;



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

