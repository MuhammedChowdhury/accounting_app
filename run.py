from flask import Flask
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == "__main__":
    app.run(debug=True)
