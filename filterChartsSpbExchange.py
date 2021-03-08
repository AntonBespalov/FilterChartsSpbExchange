# coding: utf-8
import pandas as pd
import os
import configparser
from pathlib import Path

# файл с тикерами Санкт-Петербургской биржи берётся здесь: https://spbexchange.ru/ru/listing/securities/list/
df = pd.read_csv('ListingSecurityList.csv', delimiter=';', encoding='windows-1251')

spbex_tickers = df['s_RTS_code'].tolist()
print(f'Все тикеры, которые торгуются на Санкт-Петербургской бирже: {spbex_tickers}')

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')
path_to_charts = config.get('path', 'path')

deleted_tickers = []
directory = Path(path_to_charts)
for root, _, f_names in os.walk(directory):
    for f in f_names:
        if f.endswith('.png'):
            if 'MMH OI' in root:
                ticker = f.split('-')[0]
            else:
                ticker = f.split('_')[0]
            if ticker not in spbex_tickers:
                os.remove(os.path.join(root, f))
                if ticker not in deleted_tickers:
                    deleted_tickers.append(ticker)

print(f'Удаленные тикеры, которые отсутствуют на Санкт-Петербургской бирже: {str(deleted_tickers)}')
