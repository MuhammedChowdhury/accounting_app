import os
from app import create_app  # ✅ Import Flask app factory

# ✅ Create Flask app instance
app = create_app()

# ✅ Local Development Mode
if __name__ == "__main__":
    app.run(debug=True)  # ✅ This makes Flask run on your computer
