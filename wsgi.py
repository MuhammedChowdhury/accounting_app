import os
from waitress import serve
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # ✅ Uses Render's assigned port dynamically
    serve(app, host="0.0.0.0", port=port)
