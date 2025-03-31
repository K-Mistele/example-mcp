import warnings
import os
import sys

# Apply warning filters before any other imports
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"


# Redirect stderr to suppress warnings that bypass the filters
class NullWriter:
    def write(self, *args, **kwargs):
        pass

    def flush(self, *args, **kwargs):
        pass


# Save the original stderr
original_stderr = sys.stderr
# Replace stderr with our null writer
sys.stderr = NullWriter()

# Now import the modules
from mcp_server.mcp_server import serve_stdio

# Restore stderr for normal operation
sys.stderr = original_stderr


def run():
    serve_stdio()


if __name__ == "__main__":
    run()
