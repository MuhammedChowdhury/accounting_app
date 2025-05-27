import sys
import os
from app import create_app

# ✅ Ensure Python finds the 'app' module
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ✅ Create Flask app instance
app = create_app()

# ✅ Run the application
if __name__ == "__main__":
    app.run(debug=True)