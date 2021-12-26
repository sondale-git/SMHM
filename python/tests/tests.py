import os
import sys
from pathlib import Path
# path = Path(__file__).parent.parent
sys.path.insert(0, '../src')

from HistoricalMunicipalMapper import MunicipalityMapper

a = MunicipalityMapper()

path, table, url = a.download_table(startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')

print(url)

print(table.loc[table["InitialName"]=='Brenles'])
