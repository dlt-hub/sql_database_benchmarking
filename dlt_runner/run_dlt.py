import os
from dlt.common.runners.stdout import iter_std
from dlt.common.runners.venv import Venv

# 1. we use Venv.restore_current() to get current virtual (or global) environment
# 2. we run python with -u flag to make sure the output is unbuffered
# 3. we demonstrate how to pass function arguments: "arg1", "arg2"
# 4. we demonstrate that environment variables are passed to the executing script
os.environ["RUNTIME__LOG_LEVEL"] = "INFO"

# iter_std runs the process, connects to stdout and stderr and prints output line by line
# it will raise CalledProcessError if the scripts exits with non 0 code (ie. due to exception)
for line in iter_std(Venv.restore_current(), "python", "-u", "chess_pipeline.py", "arg1", "arg2"):
    print(line[1])
