import os
from waitress import serve
from app import create_app

app = create_app()

print("📡 DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)