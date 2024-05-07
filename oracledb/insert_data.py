from sqlalchemy import create_engine
import sqlalchemy as sa
import pandas as pd


df = pd.read_parquet(r"../UNSW-NB15/Network-Flows/UNSW_Flow.parquet")
print(df.head(1))

# we convert this to strings, oracle cannot deal with pandas floats
# df = df.astype(str)
# print(len(df))
dtyp = {}

# convert to right types
for column in df.columns:
    # print(df[column].dtype)
    if df[column].dtype == 'string':
        dtyp[column] = sa.types.VARCHAR(df[column].astype(str).str.len().max())
    elif df[column].dtype in ['float', 'Float64']:
        dtyp[column] = sa.FLOAT


engine = create_engine("oracle+oracledb://LOADER:LOADER@localhost:1521/?service_name=FREEPDB1")
df.to_sql('UNSW_Flow', schema='LOADER', con = engine, chunksize=50000, index=False, if_exists='replace', dtype=dtyp)

print("upload done !")