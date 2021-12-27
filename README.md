# SMHM

## Swiss Municipalities Historical Mapper

This project is mainly a wrapper around the federal statistical office "Liste historisée des communes
" REST API.

Municipalities in Switzerland merge frequently, this package aims to download
and create historical Municipalities mapping tables in an efficient way.

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





## Using :

```python
>>> from SMHM.HistoricalMunicipalMapper import MunicipalityMapper
>>> a = MunicipalMapper()
>>> path, table, url = a.download_table(startPeriod_value = '2000',endPeriod_value = '2020', str_format_start = '%Y', str_format_end = '%Y')
```


## Contribute

New functionalities contribution and language ports are more than welcome.

## Other information

For R alternative [ValValetl/SMMT](https://github.com/ValValetl/SMMT) GitHub repository is maybe an option.


## References :

FSO (2020). Service Rest du répertoire officiel des communes de Suisse. Accessible at : https://www.bfs.admin.ch/bfs/fr/home/bases-statistiques/repertoire-officiel-communes-suisse/liste-historisee-communes.assetdetail.15224055.html
