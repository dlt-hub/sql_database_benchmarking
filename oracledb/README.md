##  Installing and setting up oracle db
(I follow all the steps detailed in this [helpful tutorial](https://youtu.be/gaelhF2us28?feature=shared))
1. I download [Oracle Database 18c Express Edition](https://www.oracle.com/database/technologies/xe18c-downloads.html) for Windows x64.
2. I follow the [installation guide](https://docs.oracle.com/en/database/oracle/oracle-database/18/xeinw/installation-guide.html#GUID-C3C5B05A-3BEB-4373-96D0-80BBADFBD6A4) and set up a local oracle database in my system.
3. I also install the latest [SQL Developer IDE](https://www.oracle.com/database/sqldeveloper/).
4. I connect the SQL Developer IDE with the oracle database.
5. I create a user "rahul" and grant it `CREATE TABLE` privilege. 

    ```GRANT CREATE TABLE TO rahul;```  

6. I also provide the user "rahul" with unlimited quota to accommodate the ~2M rows of ndis dataset.  
```ALTER USER rahul QUOTA UNLIMITED ON USERS;```

### Installation from container

```
docker run -d -p 1521:1521 -e ORACLE_PASSWORD=loader -v oracle-volume:/opt/oracle/oradata-1/ gvenzl/oracle-xe
```

I use Oracle Explorer plugin VS Code. User/password/service: SYS/loader/FREEPDB1
To create user: `create.sql`.

The name of dba user is **SYS** 

### Connectorx Installation 
Oracle client must be installed:
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

This guide worked for me
https://gist.github.com/bmaupin/1d376476a2b6548889b4dd95663ede58


### Some results
1. pyarrow / pandas - 30% faster than connector x (???)
2. not much difference when using **oracledb** (native python) vs. **cx_oracle** (via oracle client)
3. I modified insert script to have typed dataframe. after that **oracledb** stopped working (protocol parsing error) and I had to revert to **cx_oracle** which uses native client!
4. overall speed close to postgres


## Uploading the data into oracledb
1. I use the [`python-oracledb`](https://oracle.github.io/python-oracledb/) driver to connect to the oracle database  
 ```pip install python-oracledb```
2. The connection string for this driver (see [here](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#dialect-oracle-oracledb-connect)): `oracle+oracledb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?service_name={SERVICE_NAME}`
3. I first download the data using script [`prepare_mssql_db/download_data.py`](https://github.com/WangCHEN9/el_benchmark/blob/main/prepare_mssql_db/download_data.py)
4. I then upload the data using a modified version of script [`prepare_mssql_db/upload_to_mssql.py`](https://github.com/WangCHEN9/el_benchmark/blob/main/prepare_mssql_db/upload_to_mssql.py)
    ```python
    from sqlalchemy import create_engine
    import pandas as pd


    df = pd.read_parquet(r"UNSW-NB15/Network-Flows/UNSW_Flow.parquet")
    print(df.head(1))

    df = df.astype(str)
    print(len(df))
    engine = create_engine("oracle+oracledb://rahul:{PASSWORD}@localhost:1521/?service_name=XEPDB1")
    df.to_sql('UNSW_Flow', schema='rahul', con = engine, chunksize=20, index=False, if_exists='replace')

    print("upload done !")
    ```
5. Note on the above implementation: doing a DataFrame upload with `method='multi'` is not supported for oracledb, and without this, it took ~10 mins for the data upload to complete.

## Connecting to `dlt`
1. I create a dlt project using `dlt init sql_database duckdb`
2. I add requirement `oracledb` inside `requirements.txt`
3. I add the connection string inside `.dlt/secrets.toml`  
    ``` sources.sql_database.credentials = "oracle+oracledb://rahul:{PASSWORD}@localhost:1521/?service_name=XEPDB1"```
4. I specify the resource inside `sql_database_pipeline.py`
5. With this, I'm already able to successfully run my pipeline `sql_database.py`
