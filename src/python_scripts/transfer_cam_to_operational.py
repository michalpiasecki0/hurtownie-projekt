import pymssql
import pandas as pd

df = pd.read_csv("data/atmospheric_forecasts/csvki/combined.csv")


SERVER = 'MIKOLAJ2'

USER='wtykacz'
PASSWORD = 'zcakytw'

conn = pymssql.connect(SERVER, USER, PASSWORD, 'Operacyjna')
cursor = conn.cursor()

for index, row in df.iterrows():
    st = row.time.split('-')
    if int(st[0])>=32 or (int(st[1])==2 and int(st[2]) % 4 != 0 and int(st[0]) >= 29) or (int(st[1]) in (4,6,9,11) and int(st[0]) >= 31)  :
        continue



    sql = f"INSERT INTO gacf (measurementdate, szerokosc, dlugosc, tenuwind, tenvwind) VALUES ('{'-'.join(reversed(row.time.split('-')))}', {row.latitude}, {row.longitude}, {row.u10}, {row.v10})"
    print(sql)
    cursor.execute(sql)
    if index % 5000 == 0:
        print(index)
        conn.commit()
conn.close()