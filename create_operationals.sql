

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'Operacyjna')
BEGIN
    CREATE DATABASE Operacyjna;
END

GO

USE Operacyjna;

CREATE TABLE LokalizacjeMiast (
	nazwa nvarchar(50) not null primary key,
	wojewodztwo nvarchar(50),
	szerokosc float not null,
	dlugosc float not null
)


CREATE TABLE LokalizacjeStacji (
	nazwa nvarchar(50) not null primary key,
	szerokosc float not null,
	dlugosc float not null
)


-- operacyjna dla 
-- CAMS European air quality forecasts

CREATE TABLE AirQuality (
	id int not null primary key identity(1,1),
	measurementdate date not null,
	pmten float not null,
	pmtwofive float not null,
	pmtenwildfires float not null,
	nitrogen float not null,
	dust float not null,
)





-- polski instytut meteorologiczny klimat

CREATE TABLE Klimat (
	id int not null primary key identity(1,1),
	measurementdate date not null,
	stacja nvarchar(50) not null references lokalizacjestacji(nazwa),
	tmin float,
	tavg float,
	tmax float,
	opad float

)
/*
Rok                                     4
Miesiąc                                 2
Dzień                                   2
Maksymalna temperatura dobowa [°C]      6/1
Status pomiaru TMAX                     1
Minimalna temperatura dobowa [°C]       6/1
Status pomiaru TMIN                     1
Średnia temperatura dobowa [°C]         8/1
Status pomiaru STD                      1
Temperatura minimalna przy gruncie [°C] 6/1
Status pomiaru TMNG                     1
Suma dobowa opadów [mm]                 8/1
Status pomiaru SMDB                     1
Rodzaj opadu  [S/W/ ]                   1
Wysokość pokrywy śnieżnej [cm]          5
Status pomiaru PKSN                     1
*/


-- CAMS global atmospheric composition forecasts
-- mozna dodac wiecej 
CREATE TABLE gacf (
	id int not null primary key identity(1,1),
	measurementdate date not null,
	szerokosc float not null,
	dlugosc float not null,
	uwind float,
	vwind float,
	tenuwind float,
	tenvwind float
)