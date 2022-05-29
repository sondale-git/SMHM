import requests
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from typing import Union

from SMHM.utils.validation import (
    validate_startPeriod_endPeriod,
    validate_format,
    validate_labelLanguages,
    validate_BFSCode,
    validate_includeUnmodified,
    validate_includeTerritoryExchange,
    validate_escapeChars,
)


def TerminalCodeFrequencies(df, inplace=False) -> pd.DataFrame:
    if inplace == False:
        df = df.copy()
    else:
        pass
    df["TerminalCodeFrequencies"] = np.nan
    for municipality_code in df.TerminalCode.unique():
        df.loc[(df.TerminalCode == municipality_code), "TerminalCodeFrequencies"] = (
            df.TerminalCode == municipality_code
        ).sum()
    if inplace == False:
        return df.TerminalCodeFrequencies
    else:
        return pd.DataFrame()


def InitialCodeFrequencies(df, inplace=False) -> pd.DataFrame:
    if inplace == False:
        df = df.copy()
    else:
        pass
    for municipality_code in df.InitialCode.unique():
        df.loc[(df.InitialCode == municipality_code), "InitialCodeFrequencies"] = (
            df.InitialCode == municipality_code
        ).sum()
    if inplace == False:
        return df.InitialCodeFrequencies
    else:
        return pd.DataFrame()


class MunicipalityMapper:
    url = "https://sms.bfs.admin.ch/WcfBFSSpecificService.svc/AnonymousRest/communes/"
    useBfsCode_string = "useBfsCode"
    includeUnmodified_string = "includeUnmodified"
    includeTerritoryExchange_string = "includeTerritoryExchange"
    labelLanguages_string = "labelLanguages"
    escapeChars_string = "escapeChars"
    startPeriod_string = "startPeriod"
    endPeriod_string = "endPeriod"
    format_string = "format"

    def __init__(
        self,
        language: str = "fr",
        format: str = "csv",
        str_out_format: str = "%d-%m-%Y",
    ):
        language = validate_labelLanguages(language)
        format = validate_format(format)
        today = datetime.today()
        try:
            today.strftime(str_out_format)
        except Exception as e:
            print(e)
        start = today - timedelta(days=1)
        self.startPeriod_value, self.endPeriod_value = start.strftime(
            str_out_format
        ), today.strftime(str_out_format)
        self.labelLanguages_value = language
        self.useBfsCode_value = "false"
        self.includeUnmodified_value = "false"
        self.includeTerritoryExchange_value = "false"
        self.format_value = format
        self.escapeChars_value = None

        self.str_out_format = str_out_format
        self.str_format_start = None
        self.str_format_end = None

        self.table_df = None

        self.table = None

    def download_table(
        self,
        filepath=None,
        add_flags=True,
        table: str = "Mutations",
        startPeriod_value: Union[str, None] = None,
        endPeriod_value: Union[str, None] = None,
        str_format_start: Union[str, None] = None,
        str_format_end: Union[str, None] = None,
        **kwargs,
    ):
        list_of_tables = [
            "Mutations",
            "Correspondances",
            "Geographic levels",
            "Snapshots",
        ]
        if add_flags not in [True, False]:
            raise ValueError("add_flags must be boolean value : True or False.")
        if table not in list_of_tables:
            raise ValueError(f"{table} is not in choices : {list_of_tables}")
        if table == "Geographic levels":
            extension = "levels"
        else:
            extension = table.lower()

        if startPeriod_value is not None:
            self.startPeriod_value = startPeriod_value
        if endPeriod_value is not None:
            self.endPeriod_value = endPeriod_value
        if str_format_start is not None:
            self.str_format_start = str_format_start
        else:
            self.str_format_start = self.str_out_format
        if str_format_end is not None:
            self.str_format_end = str_format_end
        else:
            self.str_format_end = self.str_out_format

        self.startPeriod_value, self.endPeriod_value = validate_startPeriod_endPeriod(
            start=self.startPeriod_value,
            end=self.endPeriod_value,
            str_format_start=self.str_format_start,
            str_format_end=self.str_format_end,
            str_format_out=self.str_out_format,
        )

        self.labelLanguages_value = validate_labelLanguages(
            kwargs.get("labelLanguages_value", self.labelLanguages_value)
        )
        self.useBfsCode_value = validate_BFSCode(
            kwargs.get("useBfsCode_value", self.useBfsCode_value)
        )
        self.includeUnmodified_value = validate_includeUnmodified(
            kwargs.get("includeUnmodified_value", self.includeUnmodified_value)
        )
        self.includeTerritoryExchange_value = validate_includeTerritoryExchange(
            kwargs.get(
                "includeTerritoryExchange_value",
                self.includeTerritoryExchange_value,
            )
        )
        self.format_value = validate_format(
            format=kwargs.get("format_value", self.format_value)
        )
        self.escapeChars_value = validate_escapeChars(
            kwargs.get("escapeChars_value", self.escapeChars_value)
        )

        parameters = None
        if table == "Mutations":
            # Mutations

            if self.escapeChars_value is not None:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.format_string: self.format_value,
                    MunicipalityMapper.escapeChars_string: self.escapeChars_value,
                }
            else:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.format_string: self.format_value,
                }

        elif table == "Correspondances":
            # Correspondances
            if self.escapeChars_value is not None:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.includeUnmodified_string: self.includeUnmodified_value,
                    MunicipalityMapper.format_string: self.format_value,
                    MunicipalityMapper.escapeChars_string: self.escapeChars_value,
                }
            else:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.includeUnmodified_string: self.includeUnmodified_value,
                    MunicipalityMapper.format_string: self.format_value,
                }

        elif table == "Geographic levels":
            # Geographic levels
            if self.escapeChars_value is not None:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.useBfsCode_string: self.useBfsCode_value,
                    MunicipalityMapper.includeTerritoryExchange_string: self.includeTerritoryExchange_value,
                    MunicipalityMapper.labelLanguages_string: self.labelLanguages_value,
                    MunicipalityMapper.format_string: self.format_value,
                    MunicipalityMapper.escapeChars_string: self.escapeChars_value,
                }
            else:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.useBfsCode_string: self.useBfsCode_value,
                    MunicipalityMapper.includeTerritoryExchange_string: self.includeTerritoryExchange_value,
                    MunicipalityMapper.labelLanguages_string: self.labelLanguages_value,
                    MunicipalityMapper.format_string: self.format_value,
                }

        elif table == "Snapshots":
            # Snapshots
            if self.escapeChars_value is not None:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.useBfsCode_string: self.useBfsCode_value,
                    MunicipalityMapper.format_string: self.format_value,
                    MunicipalityMapper.escapeChars_string: self.escapeChars_value,
                }
            else:
                parameters = {
                    MunicipalityMapper.startPeriod_string: self.startPeriod_value,
                    MunicipalityMapper.endPeriod_string: self.endPeriod_value,
                    MunicipalityMapper.useBfsCode_string: self.useBfsCode_value,
                    MunicipalityMapper.format_string: self.format_value,
                }
        print("requesting table {} with parameters : {}".format(table, parameters))
        finalrequest = requests.get(
            MunicipalityMapper.url + extension, params=parameters
        )
        # Save to disk if not none
        if self.format_value == "csv":
            table_df = pd.read_csv(finalrequest.url)
        elif self.format_value == "Excel":
            table_df = pd.read_excel(finalrequest.url)
        else:
            # This condition never happens, since the format is validated above.
            # Line use for avoiding pylint errors.
            table_df = pd.DataFrame()
        # closing connection
        finalrequest.close()
        self.table_df = table_df
        self.table = table
        self.type_table = table
        if add_flags == True:
            self.add_flags()
        else:
            pass
        # Saving to disk.
        if filepath is not None:
            self.table_df.to_csv(filepath, index=False)

        return filepath, self.table_df, finalrequest.url

    def add_flags(self):
        try:
            if self.table_df is None:
                raise ValueError(
                    "`self.table_df` is not in memory. Make sure to call self.download_table prior executing `self.add_flags`."
                )
            if self.type_table == "Correspondances":
                self.table_df["InitialCodeFrequencies"] = np.nan
                self.table_df["TerminalCodeFrequencies"] = np.nan
                self.table_df.TerminalCodeFrequencies = TerminalCodeFrequencies(
                    self.table_df
                )
                self.table_df.InitialCodeFrequencies = InitialCodeFrequencies(
                    self.table_df
                )

                # Flagging if the municipalities merged in a non-existing municipality
                self.table_df["flag_merged_in_new_municipality"] = np.nan
                self.table_df["flag_merged_in_new_municipality"] = self.table_df[
                    "flag_merged_in_new_municipality"
                ].astype(pd.Int64Dtype())
                flag_merged_in_new_municipality_locator = (
                    (self.table_df.InitialCode != self.table_df.TerminalCode)
                    & (self.table_df.InitialName != self.table_df.TerminalName)
                    & (self.table_df.TerminalCodeFrequencies > 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                    & (~self.table_df.TerminalName.isin(self.table_df.InitialName))
                )
                self.table_df.loc[
                    flag_merged_in_new_municipality_locator,
                    "flag_merged_in_new_municipality",
                ] = 1
                self.table_df.loc[
                    ~flag_merged_in_new_municipality_locator,
                    "flag_merged_in_new_municipality",
                ] = 0
                # [x] [done]

                # Flagging if the municipalites merged in other existing municipality
                self.table_df["flag_merged_in_existing_municipality"] = np.nan
                self.table_df["flag_merged_in_existing_municipality"] = self.table_df[
                    "flag_merged_in_existing_municipality"
                ].astype(pd.Int64Dtype())
                flag_merged_in_existing_municipality_locator = (
                    (self.table_df.InitialCode != self.table_df.TerminalCode)
                    & (self.table_df.InitialName != self.table_df.TerminalName)
                    & (self.table_df.TerminalCodeFrequencies > 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                    & (self.table_df.TerminalName.isin(self.table_df.InitialName))
                )
                self.table_df.loc[
                    flag_merged_in_existing_municipality_locator,
                    "flag_merged_in_existing_municipality",
                ] = 1
                self.table_df.loc[
                    ~flag_merged_in_existing_municipality_locator,
                    "flag_merged_in_existing_municipality",
                ] = 0
                # [x] [done]

                # Flagging if the municipalities did not merge but changed code
                self.table_df["flag_changed_code_not_municipality"] = np.nan
                self.table_df["flag_changed_code_not_municipality"] = self.table_df[
                    "flag_changed_code_not_municipality"
                ].astype(pd.Int64Dtype())
                flag_changed_code_not_municipality_locator = (
                    (self.table_df.InitialName == self.table_df.TerminalName)
                    & (self.table_df.InitialCode != self.table_df.TerminalCode)
                    & (self.table_df.TerminalCodeFrequencies == 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                )
                self.table_df.loc[
                    flag_changed_code_not_municipality_locator,
                    "flag_changed_code_not_municipality",
                ] = 1
                self.table_df.loc[
                    ~flag_changed_code_not_municipality_locator,
                    "flag_changed_code_not_municipality",
                ] = 0
                # [x] [done]

                # Flagging if the municipalities that merged in an existing municipality and if it's the main municipality --> table_df.TerminalName==table_df.InitialName
                self.table_df["flag_existing_merge_group_main"] = np.nan
                self.table_df["flag_existing_merge_group_main"] = self.table_df[
                    "flag_existing_merge_group_main"
                ].astype(pd.Int64Dtype())
                flag_existing_merge_group_main_locator = (
                    (self.table_df.TerminalCodeFrequencies > 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                    & (self.table_df.InitialCode == self.table_df.TerminalCode)
                )
                self.table_df.loc[
                    flag_existing_merge_group_main_locator,
                    "flag_existing_merge_group_main",
                ] = 1
                self.table_df.loc[
                    ~flag_existing_merge_group_main_locator,
                    "flag_existing_merge_group_main",
                ] = 0
                # [x] [done]

                # Flagging if municipalities merged in existing municipalities and there was a change in code for the main. Flagging only the main.
                # Other flags could be derived by set operations.
                self.table_df[
                    "flag_merged_in_existing_municipality_and_changed_code_main"
                ] = np.nan
                self.table_df[
                    "flag_merged_in_existing_municipality_and_changed_code_main"
                ] = self.table_df[
                    "flag_merged_in_existing_municipality_and_changed_code_main"
                ].astype(
                    pd.Int64Dtype()
                )
                flag_merged_in_existing_municipality_and_changed_code_main_locator = (
                    (self.table_df.InitialCode != self.table_df.TerminalCode)
                    & (self.table_df.InitialName == self.table_df.TerminalName)
                    & (self.table_df.TerminalCodeFrequencies > 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                )
                self.table_df.loc[
                    flag_merged_in_existing_municipality_and_changed_code_main_locator,
                    "flag_merged_in_existing_municipality_and_changed_code_main",
                ] = 1
                self.table_df.loc[
                    ~flag_merged_in_existing_municipality_and_changed_code_main_locator,
                    "flag_merged_in_existing_municipality_and_changed_code_main",
                ] = 0
                # [x] [done]

                # Flagging if the municipality changed_name only
                self.table_df["flag_changed_name_only"] = np.nan
                self.table_df["flag_changed_name_only"] = self.table_df[
                    "flag_changed_name_only"
                ].astype(pd.Int64Dtype())
                flag_changed_name_only_locator = (
                    (self.table_df.TerminalCodeFrequencies == 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                    & (self.table_df.InitialName != self.table_df.TerminalName)
                )
                self.table_df.loc[
                    flag_changed_name_only_locator, "flag_changed_name_only"
                ] = 1
                self.table_df.loc[
                    ~flag_changed_name_only_locator, "flag_changed_name_only"
                ] = 0
                # [x] [done]

                # Flagging municipalities that were split across multiple new municipalities
                self.table_df["flag_split_in_new_municipality"] = np.nan
                self.table_df["flag_split_in_new_municipality"] = self.table_df[
                    "flag_split_in_new_municipality"
                ].astype(pd.Int64Dtype())
                flag_split_in_new_municipality_locator = (
                    (self.table_df.TerminalCode != self.table_df.InitialCode)
                    & (self.table_df.InitialCodeFrequencies > 1)
                    & (~self.table_df.TerminalCode.isin(self.table_df.InitialCode))
                )
                self.table_df.loc[
                    flag_split_in_new_municipality_locator,
                    "flag_split_in_new_municipality",
                ] = 1
                self.table_df.loc[
                    ~flag_split_in_new_municipality_locator,
                    "flag_split_in_new_municipality",
                ] = 0

                # Flagging municipalities that were split in existing municipalities.
                self.table_df["flag_split_in_existing_municipality"] = np.nan
                self.table_df["flag_split_in_existing_municipality"] = self.table_df[
                    "flag_split_in_existing_municipality"
                ].astype(pd.Int64Dtype())
                flag_split_in_existing_municipality_locator = (
                    (self.table_df.TerminalCode != self.table_df.InitialCode)
                    & (self.table_df.InitialCodeFrequencies > 1)
                    & (self.table_df.TerminalCode.isin(self.table_df.InitialCode))
                )
                self.table_df.loc[
                    flag_split_in_existing_municipality_locator,
                    "flag_split_in_existing_municipality",
                ] = 1
                self.table_df.loc[
                    ~flag_split_in_existing_municipality_locator,
                    "flag_split_in_existing_municipality",
                ] = 0

                # Flagging the ones that merge and splitted
                self.table_df["flag_merge_and_split"] = np.nan
                self.table_df["flag_merge_and_split"] = self.table_df[
                    "flag_merge_and_split"
                ].astype(pd.Int64Dtype())
                flag_merge_and_split_locator = (
                    (self.table_df.TerminalCode == self.table_df.InitialCode)
                    & (self.table_df.InitialCodeFrequencies > 1)
                    & (self.table_df.TerminalCodeFrequencies > 1)
                    & (self.table_df.TerminalCode.isin(self.table_df.InitialCode))
                    & self.table_df.InitialCode.isin(self.table_df.TerminalCode)
                )
                self.table_df.loc[
                    flag_merge_and_split_locator, "flag_merge_and_split"
                ] = 1
                self.table_df.loc[
                    ~flag_merge_and_split_locator, "flag_merge_and_split"
                ] = 0

                # # Flagging municipalities that were split between non existing and new municipalities.
                # self.table_df['flag_split_in_new_and_existing_municipality'] = np.nan
                # self.table_df['flag_split_in_new_and_existing_municipality'] = self.table_df['flag_split_in_new_and_existing_municipality'].astype(pd.Int64Dtype())
                # flag_split_in_new_and_existing_municipality_locator = (self.table_df.TerminalCode != self.table_df.InitialCode) & (self.table_df.InitialCodeFrequencies>1) & (self.table_df.TerminalCode.isin(self.table_df.InitialCode))
                # self.table_df.loc[flag_split_in_new_and_existing_municipality_locator,"flag_split_in_new_and_existing_municipality"] = 1
                # self.table_df.loc[~flag_split_in_new_and_existing_municipality_locator,"flag_split_in_new_and_existing_municipality"] = 0

                # Flagging municipalities that didn't change
                self.table_df["flag_no_change"] = np.nan
                self.table_df["flag_no_change"] = self.table_df[
                    "flag_no_change"
                ].astype(pd.Int64Dtype())
                flag_no_change_locator = (
                    (self.table_df.InitialCode == self.table_df.TerminalCode)
                    & (self.table_df.InitialName == self.table_df.TerminalName)
                    & (self.table_df.TerminalCodeFrequencies == 1)
                    & (self.table_df.InitialCodeFrequencies == 1)
                )
                self.table_df.loc[flag_no_change_locator, "flag_no_change"] = 1
                self.table_df.loc[~flag_no_change_locator, "flag_no_change"] = 0
                # [x] [done]
                return self.table_df
            else:
                raise ValueError(
                    '`self.add_flags(...)` works only with "Correspondances" tables'
                )
        except AttributeError as ae:
            print(ae)
