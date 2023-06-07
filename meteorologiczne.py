import numpy as np
import pandas as pd
def get_kd_data_for_date(month, year=2022):
    kd_cols = ['kod_stacji', 'nazwa_stacji', 'rok', 'miesiąc', 'dzień', 'tmax', 'tmax_status',
               'tmin', 'tmin_status', 'tavg', 'tavg_status', 'tmin_grunt', 'tmin_grunt_status',
               'opady_mm', 'opady_mm_status', 'rodzaj_opadu', 'wysokosc_pokrywy_snieznej', 'wps_status']
    a = pd.read_csv(f'data_met/k_d_{month:0>2}_{year}.csv', header=None, names=kd_cols, encoding='windows-1252')
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
t=[]
for i in range(1,13):
    t.append(get_kd_data_for_date(i))
b = pd.concat(t)
b