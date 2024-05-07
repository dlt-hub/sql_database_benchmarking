## Installing and setting up db2

1. I install the [db2 community edition (v 11.5.9)](https://www.ibm.com/account/reg/us-en/signup?formid=urx-33669) for Windows.
2. I follow the installation and setup steps as detailed in [this video](https://www.youtube.com/watch?v=ferDfudhaJg&ab_channel=DatabaseGuy).
3. After installation, I open the db2 Admin Command Window and create a database `UNSW` using  
    ```db2 CREATE DATABASE UNSW ```

### Installing in container
Follow: https://www.ibm.com/docs/en/db2/11.5?topic=system-linux

use `db2_container.env` as setup and `/opt/db2` to store the database

```
docker pull icr.io/db2_community/db2
docker run -h db2server --name db2server --restart=always --detach --privileged=true -p 50000:50000 --env-file db2_container.env -v /opt/db2:/database icr.io/db2_community/db2
```
**NOTE** to create a `dlt_data` database takes a long time 

I use the cli provided by container to create 


docker exec -ti db2server bash -c "su - db2inst1"

**NOTE** I could not make the old containers work on WSL2. Database server could not startup - access denied on volume with database. (even not mapped!)
```
docker run -itd --name mydb2 -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=loader -e DBNAME=dlt_data -v /opt/db2:/database ibmcom/db2
docker run -itd --name mydb2 -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=loader -e DBNAME=dlt_data ibmcom/db2
```

## Inserting data into db2

1. The connection string for db2: `db2+ibm_db://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}`
2. To allow the python script to connect to db2, I had to pip install `ibm_db_sa`
3. Before starting, I had already downloaded the data using [`download_data.py`](https://github.com/WangCHEN9/el_benchmark/blob/main/prepare_mssql_db/download_data.py).
4. Uploading the full data at once using [`upload_to_mssql.py`](https://github.com/WangCHEN9/el_benchmark/blob/main/prepare_mssql_db/upload_to_mssql.py) did not work. This is because db2 records operations in its transaction logs, which has limited capacity. The operations resulting with writing ~2M rows exceeds this capacity, and the script throws the following error:  
    ```sqlalchemy.exc.InternalError: (ibm_db_dbi.InternalError) ibm_db_dbi::InternalError: Sending data failed: [IBM][CLI Driver][DB2/NT64] SQL0964C  The transaction log for the database is full.```
5. This can be fixed by either increasing the size of the transaction logs, or by chunking the data and committing the changes after each chunk is uploaded. I uploaded the data in chunks of 150k, and the data took ~45 mins to upload. The script for this is [here](https://github.com/dlt-hub/oracle-db2-mssql-and-benchmarking-tests/tree/main/db2/upload_data_db2.py).

## Connecting to db2 using `dlt`

1. I create a `dlt` project with `dlt init sql_database filesystem --branch rfix/adds-table-backends` 
2. I add the following requirements inside the existing `requirements.txt`: `ibm_db_sa`, `pandas`, `dlt[parquet]`, `connectorx`, and then I run `pip install -r requirements.txt`
3. I add db2 credenials inside `secrets.toml`:  
    ```toml
    [sources.sql_database.credentials]
    drivername = "db2+ibm_db" # please set me up!
    database = "UNSW" # please set me up!
    password = <PASSWORD> # please set me up!
    username = "db2admin" # please set me up!
    host = "localhost" # please set me up!
    port = 25000 # please set me up!

    [destination.filesystem]
    bucket_url = "file:///data" # please set me up!
    ```
4. I update the existing functions inside `sql_database_pipeline.py` to point to the correct tables/schemas.
