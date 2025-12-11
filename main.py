# This file helps Railway detect this as a Python project
# The actual application is in the backend/ directory
import sys
import os

# Change to backend directory
os.chdir('backend')
sys.path.insert(0, os.getcwd())

# Import and run the actual app
from main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

