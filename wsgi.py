from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint} -> URL: {rule.rule}")
