from pyarrow.parquet import read_table, ParquetFile

# tbl = read_table("_storage/unsw/speed_test_connx_20240416052526/unsw_flow/1713288326.8787262.f68a610bf7.parquet")
# tbl = read_table("_storage/unsw/speed_test_pandas_20240416050620/unsw_flow/1713287180.5203567.d2182b951d.parquet")
# tbl = read_table("_storage/unsw/speed_test_20240416024311/unsw_flow/1713278591.677001.20c5d888a8.parquet")
tbl = read_table("_storage/mssql_unsw/speed_test_20240417011240/unsw_flow_connx/1713359561.0355039.6130178675.parquet")
print(tbl)