# SMHM

## Swiss Municipalities Historical Mapper

This project is mainly a wrapper around the federal statistical office "Liste historisée des communes"
 REST API.

Municipalities in Switzerland merge frequently, this package aims to download
and create historical Municipalities mapping tables in a simple way.

## Disclaimer

This package is not officially related to the FSO (Federal Statistical Office).

This project is intended to making downloading processing easier only.
The project contributors take no responsibility for use of the FSO downloaded data
which would be not compliant with FSO terms of use\*.

\*["Service Rest du répertoire officiel des communes de Suisse"](https://www.bfs.admin.ch/bfs/fr/home/bases-statistiques/repertoire-officiel-communes-suisse/liste-historisee-communes.assetdetail.15224055.html)
 terms of use are precised on the page under list item named "Conditions d’utilisation".

## Development

First clone the repository:

```console
[user@desktop ~]$ git clone https://github.com/sondale-git/SMHM.git
```

Go to directory:

```console
[user@desktop ~]$ cd SMHM/ 
```

### Building and installing with pip :

```console
[user@desktop SMHM]$ cd python/
```

```console
[user@desktop python]$ pip install .
```

### Building and installing with conda :

First activate the environment in which you want to build and install SMHM:

```console
[user@desktop SMHM]$ conda activate SMHM
```

(We supposed that an environment SMHM existed)

Install conda building tools

```console
(SMHM) [user@desktop SMHM]$ conda install conda-build conda-verify
```

Build :

```console
(SMHM) [user@desktop SMHM]$ conda build .
```

Install :
 
```console
(SMHM) [user@desktop SMHM]$ conda install --use-local smhm
```

For the moment it's not possible to install the locally built package in a different environment.

If the previous command fails to find package `smhm`, first make sure you run the command in the same environment than the one you built the package.
If this is not the issue run :

```console
(SMHM) [user@desktop SMHM]$ conda install -c file://${CONDA_PREFIX}/conda-bld/ --offline smhm
```


## Testing :

```console
(SMHM) [user@desktop SMHM]$ pytest python/ 
```


## Using :

```python
>>> from SMHM.HistoricalMunicipalMapper import MunicipalityMapper
>>> a = MunicipalMapper()
>>> path, table, url = a.download_table(startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
```

By default `MunicipalityMapper.download_table(...)` has the parameter `add_flags` set to `True`. If the parameter `table='Correspondances'`, then 
non-overlapping flags are created and columns `TerminalCodeFrequencies` and `InitialCodeFrequencies` are added. There meaning are summarized down below :

|Column|Definition|
|---|---|
|InitialCodeFrequencies |Frequencies of values from `InitialCode` are reported with potential repeated reported frequencies|
|TerminalCodeFrequencies|Frequencies of values from `TerminalCode` are reported with potential repeated reported frequencies|
|flag_merged_in_new_municipality|Values set to `1` if the municipalities merged in a new municipality|
|flag_merged_in_existing_municipality|Value set to `1` for municipalities who merged in and existing municipality not including the main municipality (the one who merged with itself)|
|flag_existing_merge_group_main|Value set to `1` for municipalities who merged in an existing municipality and are the main municipalities|
|flag_changed_code_not_municipality|Value set to `1` for municipalities who only changed code (no renaming, merge or split)|
|flag_merged_in_existing_municipality_and_changed_code_main|Value set to `1` for municipalities who merged in existing municipality and the corresponding main municipality changed code|
|flag_changed_name_only| Value set to `1` for municipalities who changed only their name|
|flag_split_in_new_municipality| Value set to `1` for municipalities who were splitted in new municipalities|
|flag_split_in_existing_municipality|Value set to `1` for municipalities who were splitted in existing municipalities|
|flag_merge_and_split| Value set to `1` for municipalities who merged and splitted|
|flag_no_change      | Value set to `1`for municipalities who didn't change.|

This project being far from stable, it's recommended to check that the flags do not overlap although successful tests have already been driven.

Here is an example:

```python
>>> path, table, url = a.download_table(table='Correspondances',startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
>>> flags = ["flag_merged_in_new_municipality","flag_merged_in_existing_municipality",
             "flag_existing_merge_group_main", "flag_changed_code_not_municipality", 
             "flag_merged_in_existing_municipality_and_changed_code_main", 
             "flag_changed_name_only", "flag_split_in_new_municipality", 
             "flag_split_in_existing_municipality", "flag_merge_and_split", "flag_no_change"]
>>> table[flags].sum(axis=1) == table.shape[0]
True
```

If value returned is `True` then there's no overlap.

\***Note**: Correspondances table store all mutations that occured in the time period from year `startPeriod_value +1` to the end of this year and maps them with `endPeriod_value`.
If you want to have the mutations that occured in `2011`, `startPeriod_value` has to be set to `2010`.
Therefore when mapping values it's not necessary to call multiple time for the same year.
The best is to specify a bigger time frame in one single call, rather than multiple call, indeed 
the REST API is not fast no matter the size of the queried data.

To double check that you specified the right period you can compare results visually with `table="Mutations"`:

```python
>>> path, table, url = a.download_table(table="Mutations", filepath = './mutations_test.csv', startPeriod_value = '2011',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y') 
```

## Conda uninstalling:

To uninstall:

```console
(SMHM) [user@desktop SMHM]$ conda remove smhm
```

If you want to clean the build directory (note that it will also remove other packages that you built in the environment):

```console
(SMHM) [user@desktop SMHM]$ conda build purge
```

```console
(SMHM) [user@desktop SMHM]$ conda build purge-all
```



## Contribute

New functionalities contribution, code review, language ports are more than welcome.

## Other information

For R alternative [ValValetl/SMMT](https://github.com/ValValetl/SMMT) GitHub repository may be an option.


## References :

FSO (2020). Service Rest du répertoire officiel des communes de Suisse. Accessible at : https://www.bfs.admin.ch/bfs/fr/home/bases-statistiques/repertoire-officiel-communes-suisse/liste-historisee-communes.assetdetail.15224055.html
