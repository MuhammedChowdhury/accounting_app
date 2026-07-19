import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # 🔒 PRODUCTION PORT BINDING: Pull Render's port (10000) or fallback to local 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
