import os
from app import create_app  # ✅ Import Flask app factory

# ✅ Create Flask app instance
app = create_app()

# ✅ Local Development Mode
if __name__ == "__main__":
    from waitress import serve  # ✅ Ensure proper indentation
    serve(app, host="0.0.0.0", port=5000)
