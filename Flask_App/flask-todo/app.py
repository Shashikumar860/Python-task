# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Welcome to TODO App"

# if __name__ == "__main__":
#     app.run(debug=True)

# ------------------------------------------------------------------------

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)

# ------------------------------------------------------------------------

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/add-task")
# def add_task():
#     return render_template("add_task.html")

# if __name__ == "__main__":
#     app.run(debug=True)

# ------------------------------------------------------------------------

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-task")
def add_task():
    return render_template("add_task.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)



'''

project/
│
├── app.py // UI
|
| -- server.py // API
| -- requirements.txt
|
├── templates/
│   └── index.html
|   |....
└── static/
    └── style.css
    |....


'''