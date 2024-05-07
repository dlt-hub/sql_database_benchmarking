import dlt
from sql_database import sql_table

from dlt.destinations import filesystem

unsw_table = sql_table(
    "mssql+pymssql://loader:loader-xXx$%@localhost/dlt_data",
    "unsw_flow",
    "speed_test",
    # this is ignored by connectorx
    chunk_size=100000,
    backend="pyarrow",
)

pipeline = dlt.pipeline(
    pipeline_name="mssql_unsw_pyarrow",
    destination=filesystem("_storage"),
    dataset_name="mssql_unsw_pyarrow_data",
    progress="log",
)

if __name__ == "__main__":
    info = pipeline.run(
        unsw_table,
        table_name="unsw_flow",
    )
    print(info)