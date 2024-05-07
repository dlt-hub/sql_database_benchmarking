import os

import dlt
from sql_database import sql_table

from dlt.destinations import filesystem

unsw_table = sql_table(
    "mssql+pyodbc://loader:loader-xXx$%@localhost/dlt_data?encrypt=no&driver=ODBC+Driver+18+for+SQL+Server",
    "unsw_flow",
    "speed_test",
    # this is ignored by connectorx
    chunk_size=100000,
    backend="pyarrow",
    # keep source data types
    # detect_precision_hints=True,
    # just to demonstrate how to setup a separate connection string for connectorx
    # backend_kwargs={"conn": "postgresql://loader:loader@localhost:5432/dlt_data"},
)

pipeline = dlt.pipeline(
    pipeline_name="mssql_unsw_pyarrow",
    # destination='filesystem',
    destination=filesystem(os.path.abspath("../_storage/mssql_unsw")),
    progress="log",
)

info = pipeline.run(
    unsw_table,
    dataset_name="mssql_unsw_pyarrow_data",
    table_name="unsw_flow",
    loader_file_format="parquet",
)
print(info)