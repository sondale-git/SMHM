import os
import sys
import time
from pathlib import Path
# path = Path(__file__).parent.parent
sys.path.insert(0, '../src/SMHM/')

from HistoricalMunicipalMapper import MunicipalityMapper

a = MunicipalityMapper()

path, table, url = a.download_table(startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')

print(url)

print(table.loc[table["InitialName"]=='Brenles'])
time.sleep(10)
path, table, url = a.download_table(filepath = './test.csv', startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')

time.sleep(12)
path3,table_2003_2020_snapshots, url3 = a.download_table(table = 'Snapshots',startPeriod_value = '2003',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')

