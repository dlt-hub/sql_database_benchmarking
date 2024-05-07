import dlt
from dlt.destinations import postgres
from pyarrow.parquet import read_table, ParquetFile


data_iter = ParquetFile("../UNSW-NB15/Network-Flows/UNSW_Flow.parquet").iter_batches(batch_size=128*1024)

pipeline = dlt.pipeline(
    pipeline_name="postgres_unsw_upload_csv",
    destination=postgres("postgres://loader:loader@localhost:5432/dlt_data"),
    progress="log"
)
pipeline.run(data_iter, dataset_name="speed_test", write_disposition="replace", table_name="unsw_flow")