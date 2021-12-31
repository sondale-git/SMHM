import os
import sys
import time
from pathlib import Path
import pandas as pd
# path = Path(__file__).parent.parent
sys.path.insert(0, '../src/SMHM/')

from HistoricalMunicipalMapper import MunicipalityMapper

a = MunicipalityMapper()

path, table, url = a.download_table(startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
#
# print(url)
#
time.sleep(10)
path, table, url = a.download_table(filepath = './mutations_test.csv', startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
#
time.sleep(12)
path3,table_2003_2020_snapshots, url3 = a.download_table(filepath='./snapshots_test.csv',table = 'Snapshots',startPeriod_value = '2003',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
#
time.sleep(8)

path3,table_2003_2020_correspondances, url3 = a.download_table(filepath='./correspondances_test.csv',table = 'Correspondances',startPeriod_value = '2003',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')

# table_2003_2020_correspondances = pd.read_csv('./correspondances_test.csv')
print(table_2003_2020_correspondances)


print("testing flags. Sum of the sum of flag columns should be equal to the number of rows.")
flags = ["flag_merged_in_new_municipality", "flag_merged_in_existing_municipality",
         "flag_changed_code_not_municipality", "flag_existing_merge_group_main",
         "flag_changed_name_only", "flag_split_in_new_municipality" , "flag_split_in_existing_municipality", "flag_no_change", "flag_merged_in_existing_municipality_and_changed_code_main", "flag_merge_and_split"]
print("Flags sum = {}, shape = {}".format(table_2003_2020_correspondances[flags].to_numpy().sum(), table_2003_2020_correspondances.shape[0]))
if table_2003_2020_correspondances[flags].to_numpy().sum() == table_2003_2020_correspondances.shape[0]:
    print("First test passed")
else:
    table_2003_2020_correspondances["row_sum"] = 0
    table_2003_2020_correspondances["row_sum"] = table_2003_2020_correspondances[flags].sum(axis=1)
    flags.append("row_sum")
    print("First test Failed")
    print("Overlap rows beginning\n{}".format(table_2003_2020_correspondances.loc[index,table_2003_2020_correspondances.columns[0:9]]))
    print("Overlap rows ending\n{}".format(table_2003_2020_correspondances.loc[index,flags[5:len(flags)]]))

flag_merged_in_new_municipality = (table_2003_2020_correspondances.flag_merged_in_new_municipality==0)
flag_merged_in_existing_municipality = (table_2003_2020_correspondances.flag_merged_in_existing_municipality==0)
flag_changed_code_not_municipality = (table_2003_2020_correspondances.flag_changed_code_not_municipality==0)
flag_existing_merge_group_main = (table_2003_2020_correspondances.flag_existing_merge_group_main==0)
flag_changed_name_only = (table_2003_2020_correspondances.flag_changed_name_only==0)
flag_split_in_new_municipality = (table_2003_2020_correspondances.flag_split_in_new_municipality==0)
flag_split_in_existing_municipality = (table_2003_2020_correspondances.flag_split_in_existing_municipality==0)
flag_merged_in_existing_municipality_and_changed_code_main = (table_2003_2020_correspondances.flag_merged_in_existing_municipality_and_changed_code_main==0)
flag_no_change = (table_2003_2020_correspondances.flag_no_change==0)
flag_merge_and_split = (table_2003_2020_correspondances.flag_merge_and_split==0)
to_export = table_2003_2020_correspondances.loc[flag_changed_name_only & flag_existing_merge_group_main & flag_changed_code_not_municipality & flag_merged_in_existing_municipality & flag_merged_in_new_municipality & flag_changed_name_only & flag_split_in_new_municipality & flag_split_in_existing_municipality & flag_no_change & flag_merged_in_existing_municipality_and_changed_code_main & flag_merge_and_split]
index = (table_2003_2020_correspondances[flags].sum(axis = 1)>1)


if to_export.shape[0]==0:
    print("2nd Test Success")
else:
    print("2nd test failed")
