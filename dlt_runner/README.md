# dlt runner

1. This runner re-uses dlt ability to run `dbt` commands in separate processes
2. Please install `dlt` `0.4.11a` or above: `pip install -r requirements.txt`. We improved our runner to pass both stdout and stderr. That was not needed for dbt that uses `stdout` for logging (which is actually not Pythonic)
3. The example will run `chess_pipeline.py` in separate processes. Also demonstrates passing additional arguments and environment variables.
4. The same runner may be used to run dlt in isolated virtual environments (via. `Venv` class)