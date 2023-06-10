import tabula
import pandas as pd
t = tabula.read_pdf('C:\\users\\mikol\\Desktop\\mapa_zawartosci_klimat.pdf')
df = t[0]
df.drop(0, inplace=True)
df['stacja']=df['Kod METEO Nazwa stacji'].str.split(' ').str[-1]
df.drop('Kod METEO Nazwa stacji', axis=1, inplace=True)

df['dl'] = df['Dł.g.'].str.split(' ').apply(lambda x: float(x[0]) + float(x[1])/60)
df['sz'] = df['Sz.g.'].str.split(' ').apply(lambda x: float(x[0]) + float(x[1])/60)
df.drop(['Dł.g.', 'Sz.g.', 'Nazwa rzeki'], axis= 1, inplace = True)
df.drop_duplicates(subset='stacja', inplace=True)
df.to_excel('data/wsp_stacji.xlsx')