import dlt
from sql_database import sql_table

from dlt.destinations import filesystem


unsw_table = sql_table(
    "oracle+oracledb://LOADER:LOADER@localhost:1521/?service_name=FREEPDB1",
    "UNSW_Flow",
    "LOADER",
    chunk_size=100000,
    backend="pyarrow",
)

pipeline = dlt.pipeline(
    pipeline_name="oracle_unsw_pyarrow",
    destination=filesystem("_storage"),  # it is ok to use relative paths
    progress="log",
)

info = pipeline.run(
    unsw_table,
    dataset_name="oracle_unsw_pyarrow_data",
    table_name="unsw_flow",
    loader_file_format="parquet",
)
print(info)
