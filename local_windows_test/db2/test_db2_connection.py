
# this is only needed when installing ibm_db > 3.1.4
import os
if os.name == "nt":   
    import site
    os.add_dll_directory(os.path.join(site.getsitepackages()[0],r"Lib\site-packages\clidriver\bin")) 

import dlt
from sql_database import sql_table

from dlt.destinations import filesystem


def connection_pyarrow():

    unsw_table = sql_table(
        "db2+ibm_db://db2inst1:loader@localhost:50000/dlt_data",
        "unsw_flow",
        "db2inst1",
        chunk_size=100000,
        backend="pyarrow",
    )

    pipeline = dlt.pipeline(
        pipeline_name="db2_unsw_pyarrow",
        destination=filesystem("_storage"),
        progress="log",
    )

    info = pipeline.run(
        unsw_table,
        dataset_name="speed_test",
        table_name="db2_unsw_pyarrow_data",
    )
    print(info)


if __name__ == '__main__':
    connection_pyarrow()

