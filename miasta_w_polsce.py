import bs4
import pandas as pd


def row_to_dict(row):
    tab = [i.find(text=True) for i in row.find_all('td')]
    return {'miasto': tab[0],
     'longitude': tab[1].split(' ')[0],
     'latitude': tab[2].split(' ')[0],
     'wojewodztwo': tab[4]}


with open('dane.html', encoding='iso-8859-2') as file:
    a = file.read()

b = bs4.BeautifulSoup(a)
rows = b.find_all('table')[3].find_all('tr')[1:]
df = pd.DataFrame([row_to_dict(row) for row in rows])
df