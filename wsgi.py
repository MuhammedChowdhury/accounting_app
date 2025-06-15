from waitress import serve
from app import create_app  # ✅ Import Flask app factory

# ✅ Create Flask app instance
app = create_app()

# ✅ Use Waitress with the required port (from Render settings)
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)  # 🚀 Render expects this setup
