import pytest
import time
from pathlib import Path
import pandas as pd

from SMHM.HistoricalMunicipalMapper import MunicipalityMapper


ARGS = [
    ("mutations_test.csv", "Mutations", 10),
    ("snapshots_test.csv", "Snapshots", 12),
    # (, "Geographic levels",) # Not tested
    ("correspondances_test.csv", "Correspondances", 8),
]


@pytest.fixture(scope="class")
def class_mapper(request):
    mapper = MunicipalityMapper(
        language="fr",
        format="csv",
        str_out_format="%d-%m-%Y",
    )
    request.cls.mapper = mapper
    yield


@pytest.mark.usefixtures("class_mapper")
@pytest.mark.parametrize("filepath,table,time_sleep", ARGS)
class TestMunicipalityMapper:
    flags = [
        "flag_merged_in_new_municipality",
        "flag_merged_in_existing_municipality",
        "flag_changed_code_not_municipality",
        "flag_existing_merge_group_main",
        "flag_changed_name_only",
        "flag_split_in_new_municipality",
        "flag_split_in_existing_municipality",
        "flag_no_change",
        "flag_merged_in_existing_municipality_and_changed_code_main",
        "flag_merge_and_split",
    ]

    def test_municipality_mapper(self, filepath, table, time_sleep):
        self.__test_download_table(filepath, table, time_sleep)
        self.__test_add_flags(filepath, table, time_sleep)

    def __test_download_table(self, filepath, table, time_sleep):

        self.mapper.download_table(
            filepath=filepath,
            table=table,
            add_flags=False,
            startPeriod_value="2000",
            endPeriod_value="2020",
            str_format_start="%Y",
            str_format_end="%Y",
        )
        self.filepath = filepath
        # To avoid being excessive on the server.
        time.sleep(time_sleep)

    def __test_add_flags(self, filepath, table, time_sleep):

        if self.mapper.table == "Correspondances":
            # test
            self.mapper.add_flags()
            """
            Testing flags. Sum of the sum of flag columns should be equal to the number of rows.
            """
            assert (
                self.mapper.table_df[self.flags].to_numpy().sum()
                == self.mapper.table_df.shape[0]
            )

            """
            Checking that the intersection of flag columns == 0 creates an empty dataframe.
            In other words, all rows in the correspondances dataframe have at least one flag column set to 1. 
            """
            flag_merged_in_new_municipality = (
                self.mapper.table_df.flag_merged_in_new_municipality == 0
            )
            flag_merged_in_existing_municipality = (
                self.mapper.table_df.flag_merged_in_existing_municipality == 0
            )
            flag_changed_code_not_municipality = (
                self.mapper.table_df.flag_changed_code_not_municipality == 0
            )
            flag_existing_merge_group_main = (
                self.mapper.table_df.flag_existing_merge_group_main == 0
            )
            flag_changed_name_only = self.mapper.table_df.flag_changed_name_only == 0
            flag_split_in_new_municipality = (
                self.mapper.table_df.flag_split_in_new_municipality == 0
            )
            flag_split_in_existing_municipality = (
                self.mapper.table_df.flag_split_in_existing_municipality == 0
            )
            flag_merged_in_existing_municipality_and_changed_code_main = (
                self.mapper.table_df.flag_merged_in_existing_municipality_and_changed_code_main
                == 0
            )
            flag_no_change = self.mapper.table_df.flag_no_change == 0
            flag_merge_and_split = self.mapper.table_df.flag_merge_and_split == 0

            to_export = self.mapper.table_df.loc[
                (flag_changed_name_only)
                & (flag_existing_merge_group_main)
                & (flag_changed_code_not_municipality)
                & (flag_merged_in_existing_municipality)
                & (flag_merged_in_new_municipality)
                & (flag_changed_name_only)
                & (flag_split_in_new_municipality)
                & (flag_split_in_existing_municipality)
                & (flag_no_change)
                & (flag_merged_in_existing_municipality_and_changed_code_main)
                & (flag_merge_and_split)
            ]
            assert to_export.empty is True
        else:
            # This assert can be misleading, it is intern to the test function and not a feature to test.
            # can be commented.
            assert (self.mapper.table is table and self.mapper.table_df is not None)
            with pytest.raises(ValueError):
                self.mapper.add_flags()
