<<<<<<< HEAD
<<<<<<< HEAD
from app import create_app

app = create_app()
=======
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"
>>>>>>> afc1647 (Initialized Git and finalized project structure)

if __name__ == "__main__":
    app.run(debug=True)

<<<<<<< HEAD
=======
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

>>>>>>> dc8cfbe92444c4d49f3be126b10a798f1295dd81
=======
>>>>>>> afc1647 (Initialized Git and finalized project structure)
