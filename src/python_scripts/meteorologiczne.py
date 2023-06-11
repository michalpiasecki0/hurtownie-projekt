import numpy as np
import pandas as pd
import pymssql

SERVER = 'MIKOLAJ2'
LOGIN = 'wtykacz'
PASSWORD = 'zcakytw'



def get_kd_data_for_date(month, year=2022):
    kd_cols = ['kod_stacji', 'nazwa_stacji', 'rok', 'miesiąc', 'dzień', 'tmax', 'tmax_status',
               'tmin', 'tmin_status', 'tavg', 'tavg_status', 'tmin_grunt', 'tmin_grunt_status',
               'opady_mm', 'opady_mm_status', 'rodzaj_opadu', 'wysokosc_pokrywy_snieznej', 'wps_status']
    a = pd.read_csv(f'data_met/k_d_{month:0>2}_{year}.csv', header=None, names=kd_cols, encoding='ISO-8859-2')
    a.loc[a['tmax_status'] == 8, 'tmax'] = np.NaN
    a.loc[a['tmax_status'] == 9, 'tmax'] = 0
    a.loc[a['tmin_status'] == 8, 'tmin'] = np.NaN
    a.loc[a['tmin_status'] == 9, 'tmin'] = 0
    a.loc[a['tavg_status'] == 8, 'tavg'] = np.NaN
    a.loc[a['tavg_status'] == 9, 'tavg'] = 0
    a.loc[a['wps_status'] == 8, 'wysokosc_pokrywy_snieznej'] = np.NaN
    a.loc[a['wps_status'] == 9, 'wysokosc_pokrywy_snieznej'] = 0
    a.drop(columns=[column for column in a.columns if column.endswith('status')], inplace=True)
    return a
def kdt_data(month, year=2022):
    kdt_cols = ['kod_stacji', 'nazwa_stacji', 'rok', 'miesiąc', 'dzień', 'tavg_kdt', 'tavg_kdt_status',
               'wilgotnosc', 'wilgotnosc_status', 'wiatr', 'wiatr_status', 'chmury', 'chmury_status']
    a = pd.read_csv(f'data_met\k_d_t_{month:0>2}_{year}.csv', header=None, names=kdt_cols, encoding='ISO-8859-2')
    a.fillna(0)
    a.loc[a['tavg_kdt_status'] == 8, 'tavg_kdt'] = np.NaN
    a.loc[a['wilgotnosc_status'] == 8, 'wilgotnosc'] = np.NaN
    a.loc[a['wiatr_status'] == 8, 'wiatr'] = np.NaN
    a.loc[a['chmury_status'] == 8, 'chmury'] = np.NaN
    a.drop(columns=[column for column in a.columns if column.endswith('status')], inplace=True)
    a.drop(columns='tavg_kdt')
    return a
kd=[]
kdt=[]
for i in range(1,13):
    kd.append(get_kd_data_for_date(i))
    kdt.append(kdt_data(i))
a = pd.concat(kd)
b = pd.concat(kdt)
a = a.set_index(['kod_stacji', 'nazwa_stacji', 'rok', 'miesiąc', 'dzień'])
b = b.set_index(['kod_stacji', 'nazwa_stacji', 'rok', 'miesiąc', 'dzień'])
c = pd.concat([a,b], axis=1)
c = c.reset_index()
c.dropna(axis=0, inplace=True)
conn = pymssql.connect(SERVER, LOGIN, PASSWORD, 'Operacyjna', charset='utf8')
cursor = conn.cursor()
for _,row in c.iterrows():
    sql = f'INSERT INTO Klimat (measurementdate , stacja, tmin, tavg, tmax, opad) VALUES' \
          " (%s, %s, %d, %d, %d, %d)"
    print(sql)
    sql = sql.replace(', nan', ', null')
    cursor.execute(sql, (f'{row.rok}-{row.miesiąc:0>2}-{row.dzień:0>2}', row.nazwa_stacji, row.tmin, row.tavg, row.tmax, row.opady_mm))
conn.commit()
conn.close()
