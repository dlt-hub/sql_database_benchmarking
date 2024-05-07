# Using `sql_database` dlt source with pip installable drivers

`requirements.txt` contains dependencies needed to get data from SQL Server, DB2 and Oracle without any additional binaries installed. 

It was tested both on Windows and Linux. No problems or performance issues were encountered during testing after switching to those dialects.

## Oracle

[oracledb](https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#installing-python-oracledb) - official Oracle Python driver.

```
pip install oraclebd
```

Example connection string:

```
"oracle+oracledb://LOADER:LOADER@localhost:1521/?service_name=FREEPDB1"
```

Full code example can be found in [test_oracledb_connection.py](oracledb/test_oracledb_connection.py)

## DB2

[ibm_db_sa](https://pypi.org/project/ibm-db-sa/) - official IBM Python driver. We recommend using version `3.1.4`.

```
pip install ibm_db_sa==3.1.4
```

Example connection string:

```     
"db2+ibm_db://db2inst1:loader@localhost:50000/dlt_data"
```
Full code example can be found in [test_db2_connection.py](db2/test_db2_connection.py)

### Windows installation

A note on Windows install. IBM will download a right driver on Windows and place it together with a Python package. If you want to use package above version `3.1.4`, 
additional code must be placed at the beginning of the script.

```python
# this is only needed when installing ibm_db > 3.1.4 + Windows
import os
if os.name == "nt":   
    import site
    os.add_dll_directory(os.path.join(site.getsitepackages()[0],r"Lib\site-packages\clidriver\bin"))
```

In these tests `ibm_db_sa==3.1.4` was used, which works fine for all our cases.

## MSSQL

[pymssql](https://www.pymssql.org/) - official SQLAlchemy dialect for SQL Server, but different from official Microsoft one.

```
pip install ibm_db_sa==3.1.4
```

Example connection string:

```
"mssql+pymssql://loader:loader-xXx$%@localhost/dlt_data"
```

Full code example can be found in [test_db2_connection.py](mssql/test_pymssql_connection.py).
