import dlt
from dlt.destinations import mssql
from pyarrow.parquet import read_table, ParquetFile


data_iter = ParquetFile("../UNSW-NB15/Network-Flows/UNSW_Flow.parquet").iter_batches(batch_size=128*1024)

pipeline = dlt.pipeline(
    pipeline_name="unsw_upload",
    destination=mssql("mssql://loader:loader-xXx$%@localhost/dlt_data?encrypt=no"),
    progress="log"
)
# print(pipeline.sync_destination())
# print(pipeline.list_normalized_load_packages())
# pipeline.config.restore_from_destination = False
# pipeline.load()
pipeline.run(data_iter, dataset_name="speed_test", write_disposition="replace", table_name="unsw_flow")


# df = pd.read_parquet(r"UNSW-NB15/Network-Flows/UNSW_Flow.parquet")
# df.to_sql()


# data = read_table("UNSW-NB15/Network-Flows/UNSW_Flow.parquet")

# print(data)
# print(data["ct_flw_http_mthd"][1023196])
# print(data.schema.field("ct_flw_http_mthd").nullable)
# print(data.num_rows)
# exit()

# info = dlt.run(data, , dataset_name="speed_test", table_name="unsw_flow", pipelines)