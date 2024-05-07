import os

import dlt
from sql_database import sql_table

from dlt.destinations import filesystem

unsw_table = sql_table(
    "postgresql+psycopg2://loader:loader@localhost:5432/dlt_data",
    "unsw_flow",
    "speed_test",
    # this is ignored by connectorx
    chunk_size=100000,
    backend="connectorx",
    # keep source data types
    detect_precision_hints=True,
)

pipeline = dlt.pipeline(
    pipeline_name="postgres_unsw_connectorx",
    # destination='filesystem',
    destination=filesystem(os.path.abspath("../_storage/unsw")),
    progress="log",
)

info = pipeline.run(
    unsw_table,
    dataset_name="postgres_unsw_connectorx_data",
    table_name="unsw_flow",
    loader_file_format="parquet",
)
print(info)