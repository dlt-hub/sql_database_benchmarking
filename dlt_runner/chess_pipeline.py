import sys
import dlt
from dlt.sources.helpers import requests

print(f"script arguments: {sys.argv}")
print("-------------")

@dlt.resource
def players_data():
    for player in ["magnuscarlsen", "rpragchess"]:
        response = requests.get(f"https://api.chess.com/pub/player/{player}")
        yield response.json()

# Create a dlt pipeline that will load
# chess player data to the DuckDB destination
pipeline = dlt.pipeline(
    pipeline_name="chess_pipeline", destination="duckdb", dataset_name="player_data", progress="log"
)


# Extract, normalize, and load the data
load_info = pipeline.run(players_data(), table_name="player")
print(load_info)