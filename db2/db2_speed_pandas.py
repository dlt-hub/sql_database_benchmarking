import os

import dlt
from sql_database import sql_table

from dlt.destinations import filesystem

unsw_table = sql_table(
    "db2+ibm_db://db2inst1:loader@localhost:50000/dlt_data",
    "unsw_flow",
    "db2inst1",
    # this is ignored by connectorx
    chunk_size=100000,
    backend="pandas",
    # keep source data types
    # detect_precision_hints=True,
    # just to demonstrate how to setup a separate connection string for connectorx
    # backend_kwargs={"return_type": "pandas"},
)

pipeline = dlt.pipeline(
    pipeline_name="db2_unsw_pandas",
    # destination='filesystem',
    destination=filesystem(os.path.abspath("../_storage/mssql_unsw")),
    progress="log",
)

info = pipeline.run(
    unsw_table,
    dataset_name="speed_test",
    table_name="db2_unsw_pandas_data",
    loader_file_format="parquet",
)
print(info)