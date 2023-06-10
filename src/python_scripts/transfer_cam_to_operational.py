import pyodbc
import pandas as pd

df = pd.read_csv("data/air_quality_forecasts/csvki/combined.csv")

CONNECTION_STRING = ''
conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()

for row in df:
    sql = f'INSERT INTO AirQuality (measurementdate, pmten, pmtwofive, pmtenwildfires, nitrogen, dust, sz, dl) VALUES ({df.time}, {df.pm10_conc}, {df.pm2p5_conc}, {df.pmwf_conc}, {df.no2_conc}, {df.dust}, {df.latitude}, {df.longitude})'
    cursor.execute(sql)
cursor.commit()
conn.close()