## Install mssql in container

1. docker pull mcr.microsoft.com/mssql/server:2019-latest
2. docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=loader12--Axx" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest

The name of dba user is **sa** 
Default database is **master**

I use VSCode SQLTools with SQLServer plugin to connect: localhost/sa/loader12--Axx/master

Use `create.sql` to create test database and user

INSERT VALUE method (`insert_data.py`) is really slow and we need it to improve

## Some results
1. `pyarrow` is as fast as postgres and saturates CPU on Python process vs 20% on `mssql` so reading performance is good. we read test dataset in 50s
2. connectorx same performance as pyarrow

