from sqlalchemy import create_engine
import pandas as pd
import timeit


df = pd.read_parquet(r"../UNSW-NB15/Network-Flows/UNSW_Flow.parquet")
print(df.head(1))

engine = create_engine("db2+ibm_db://db2inst1:loader@localhost:50000/dlt_data")
connection = engine.connect()
start_time = timeit.default_timer()

# db2 records operations in a transaction log
# data is chunked to allow periodic committing, preventing the transaction from running out of space
chunksize = 20
for start in range(0, df.shape[0], chunksize):
    try:
        transaction = connection.begin()

        end = min(start + chunksize, df.shape[0])
        chunk = df.iloc[start:end]

        disposition = 'replace' if start == 0 else 'append' # Ensure that the data is only being replaced in the first iteration

        chunk.to_sql('unsw_flow', schema='db2inst1', con=engine, method='multi', chunksize=chunksize, index=False, if_exists=disposition)

        transaction.commit() # commit the changes to reset the logs
        print("INSERTING CHUNK")
        
    except Exception as e:
        # print(e)
        transaction.rollback() 

connection.close()
print(f"successfully finished upload in {timeit.default_timer() - start_time}s") # time taken: ~2700 seconds
engine.dispose() 
