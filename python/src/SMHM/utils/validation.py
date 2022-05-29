from datetime import datetime
from typing import Tuple, Union

def validate_startPeriod_endPeriod(
    start: str,
    end: str,
    str_format_start: str,
    str_format_end: str,
    str_format_out: str,
    verbose=True,
)-> Tuple:
    # parameter validation
    try:

        start_ = datetime.strptime(start, str_format_start)
        end_ = datetime.strptime(end, str_format_end)

        start_ = start_.strftime(str_format_out)
        end_ = end_.strftime(str_format_out)
        return start_, end_
    except Exception as e:
        print(e)
        raise e



def validate_format(format) -> str:
    if format not in ["Excel", "csv"]:
        raise ValueError('format has to either be "Excel" or "csv"')
    else:
        return format


def validate_labelLanguages(language):
    if language not in ["fr", "en", "it", "de"]:
        raise ValueError("language has to either be 'fr', 'en','it', 'de'")
    else:
        return language


def validate_BFSCode(bfs_value):
    if bfs_value not in ["true", "false"]:
        raise ValueError("bfs_value has to be either set to 'true' or 'false'")
    else:
        return bfs_value


def validate_includeUnmodified(includeUnmodified):
    if includeUnmodified not in ["true", "false"]:
        raise ValueError(
            'includeUnmodified_value has to be either set to "true" or "false"'
        )
    else:
        return includeUnmodified


def validate_includeTerritoryExchange(includeTerritory):
    if includeTerritory not in ["true", "false"]:
        raise ValueError(
            'includeTerritoryExchange_value has to be either set to "true" or "false"'
        )
    else:
        return includeTerritory


def validate_escapeChars(value):
    return value
