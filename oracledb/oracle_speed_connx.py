import os

import dlt
from sql_database import sql_table

from dlt.destinations import filesystem

unsw_table = sql_table(
    "oracle+oracledb://LOADER:LOADER@localhost:1521/?service_name=FREEPDB1",
    "UNSW_Flow",
    "LOADER",
    # this is ignored by connectorx
    chunk_size=100000,
    backend="connectorx",
    # keep source data types
    detect_precision_hints=True,
    # just to demonstrate how to setup a separate connection string for connectorx
    backend_kwargs={"conn": "oracle://LOADER:LOADER@localhost:1521/FREEPDB1"},
)

pipeline = dlt.pipeline(
    pipeline_name="oracle_unsw_connectorx",
    # destination='filesystem',
    destination=filesystem(os.path.abspath("../_storage/unsw")),
    progress="log",
)

info = pipeline.run(
    unsw_table,
    dataset_name="oracle_unsw_connectorx_data",
    table_name="unsw_flow",
    loader_file_format="parquet",
)
print(info)