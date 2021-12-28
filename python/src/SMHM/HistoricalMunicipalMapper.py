import requests
import os
from datetime import datetime, timedelta
import pandas as pd

def validate_startPeriod_endPeriod(start:str, end:str, str_format_start:str, str_format_end:str, str_format_out:str, verbose =True):
    # parameter validation
    try:

        start = datetime.strptime(start,str_format_start)
        end = datetime.strptime(end, str_format_end)

        start = start.strftime(str_format_out)
        end = end.strftime(str_format_out)
        return start, end
    except Exception as e:
        print(e)
    # https://docs.python.org/3/tutorial/errors.html --> finally executes before try
    finally:
        pass

def validate_format(format):
    if format not in ['Excel', 'csv']:
        raise ValueError('format has to either be "Excel" or "csv"')
    else:
        return format
def validate_labelLanguages(language):
    if language not in ['fr', 'en','it', 'de']:
        raise ValueError("language has to either be 'fr', 'en','it', 'de'")
    else:
        return language
def validate_BFSCode(bfs_value):
    if bfs_value not in ['true', 'false']:
        raise ValueError("bfs_value has to be either set to 'true' or 'false'")
    else:
        return bfs_value
def validate_includeUnmodified(includeUnmodified):
    if includeUnmodified not in ['true', 'false']:
        raise ValueError('includeUnmodified_value has to be either set to "true" or "false"')
    else:
        return includeUnmodified
def validate_includeTerritoryExchange(includeTerritory):
    if includeTerritory not in ['true', 'false']:
        raise ValueError('includeUnmodified_value has to be either set to "true" or "false"')
    else:
        return includeTerritory
def validate_escapeChars(value):
    return value

class MunicipalityMapper:
    url = "https://sms.bfs.admin.ch/WcfBFSSpecificService.svc/AnonymousRest/communes/"
    useBfsCode_string = 'useBfsCode'
    includeUnmodified_string = 'includeUnmodified'
    includeTerritoryExchange_string = 'includeTerritoryExchange'
    labelLanguages_string = 'labelLanguages'
    escapeChars_string = 'escapeChars'
    startPeriod_string = 'startPeriod'
    endPeriod_string = 'endPeriod'
    format_string = 'format'
    def __init__(self,language:str = 'fr', format:str = 'csv', str_out_format:str = '%d-%m-%Y'):
        language = validate_labelLanguages(language)
        format = validate_format(format)
        today  = datetime.today()
        try:
            today.strftime(str_out_format)
        except Exception as e:
            print(e)
        start  = today - timedelta(days = 1)
        self.startPeriod_value, self.endPeriod_value = start.strftime(str_out_format), today.strftime(str_out_format)
        self.labelLanguages_value = language
        self.useBfsCode_value = 'false'
        self.includeUnmodified_value = 'false'
        self.includeTerritoryExchange_value = 'false'
        self.format_value  = format
        self.escapeChars_value = None

        self.str_out_format = str_out_format
    def download_table(self, filepath = None, table:str = 'Mutations',**kwargs):
        list_of_tables = ['Mutations', 'Correspondances', 'Geographic levels','Snapshots']

        if table not in list_of_tables:
            raise ValueError("{} is not in choices : {}".format(table, list_of_tables))
        if table == 'Geographic levels':
            extension = 'levels'
        else:
            extension = table.lower()
        def validatekwargs():
            self.startPeriod_value, self.endPeriod_value = validate_startPeriod_endPeriod(start = kwargs.get('startPeriod_value',self.startPeriod_value), end = kwargs.get('endPeriod_value', self.endPeriod_value), str_format_start = kwargs.get('str_format_start', self.str_out_format), str_format_end = kwargs.get('str_format_end', self.str_out_format), str_format_out =  kwargs.get('str_out_format', self.str_out_format))
            self.labelLanguages_value = validate_labelLanguages(kwargs.get('labelLanguages_value', self.labelLanguages_value))
            self.useBfsCode_value = validate_BFSCode(kwargs.get('useBfsCode_value', self.useBfsCode_value))
            self.includeUnmodified = validate_includeUnmodified(kwargs.get('includeUnmodified_value', self.includeUnmodified_value))
            self.includeTerritoryExchange_value = validate_includeTerritoryExchange(kwargs.get('includeTerritoryExchange_value', self.includeTerritoryExchange_value))
            self.format_value  = validate_format(format = kwargs.get('format_value', self.format_value))
            self.escapeChars_value = validate_escapeChars(kwargs.get('escapeChars_value', self.escapeChars_value))
        validatekwargs()
        if table == list_of_tables[0]:
            # Mutations
            if self.escapeChars_value is not None:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value, MunicipalityMapper.escapeChars_string: self.escapeChars_value}
            else :
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value}

        elif table == list_of_tables[1]:
            # Correspondances
            if self.escapeChars_value is not None:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value, MunicipalityMapper.includeUnmodified_string : self.includeUnmodified_value, MunicipalityMapper.escapeChars_string: self.escapeChars_value}
            else:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value, MunicipalityMapper.includeUnmodified_string : self.includeUnmodified_value}

        elif table == list_of_tables[2]:
            # Geographic levels
            if self.escapeChars_value is not None:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value, MunicipalityMapper.useBfsCode_string:self.useBfsCode_value, MunicipalityMapper.includeTerritoryExchange_string:self.includeTerritoryExchange, MunicipalityMapper.labelLanguages_string:self.labelLanguages_value, MunicipalityMapper.escapeChars_string: self.escapeChars_value}
            else:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format_value, MunicipalityMapper.useBfsCode_string:self.useBfsCode_value, MunicipalityMapper.includeTerritoryExchange_string:self.includeTerritoryExchange, MunicipalityMapper.labelLanguages_string:self.labelLanguages_value}

        elif table == list_of_tables[3]:
            # Snapshots
            if self.escapeChars_value is not None:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format, MunicipalityMapper.useBfsCode_string:self.useBfsCode_value,  MunicipalityMapper.escapeChars_string: self.escapeChars_value}
            else:
                parameters = {MunicipalityMapper.startPeriod_string:self.startPeriod_value, MunicipalityMapper.endPeriod_string :self.endPeriod_value , MunicipalityMapper.format_string:self.format, MunicipalityMapper.useBfsCode_string:self.useBfsCode_value, MunicipalityMapper.includeTerritoryExchange_string:self.includeTerritoryExchange, MunicipalityMapper.labelLanguages_string:self.labelLanguages_value}
        print("requesting table {} with parameters : {}".format(table,parameters))
        finalrequest = requests.get(MunicipalityMapper.url+extension,  params = parameters)
        # Save to disk if not none
        if self.format_value=='csv':
            table_df  = pd.read_csv(finalrequest.url)
        if self.format_value =='Excel':
            table_df = pd.read_excel(finalrequest.url)
        if filepath is not None:
            with open(filepath, 'w') as f:
                f.write(finalrequest.text)
        return filepath, table_df, finalrequest.url
