from flask import Flask, render_template, request, redirect

app = Flask(__name__)

todos = []

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("welcome.html")

# ============================================================
# TODO PAGE
# ============================================================

@app.route("/todos")
def todo_page():

    incomplete = [todo for todo in todos if not todo["completed"]]

    complete = [todo for todo in todos if todo["completed"]]

    return render_template(
        "index.html",
        incomplete=incomplete,
        complete=complete
    )

# ============================================================
# ADD TODO
# ============================================================

@app.route("/add", methods=["POST"])
def add_todo():

    task = request.form.get("task")

    if task:

        todo = {
            "id": len(todos),
            "task": task,
            "completed": False
        }

        todos.append(todo)

    return redirect("/todos")

# ============================================================
# COMPLETE TODO
# ============================================================

@app.route("/complete/<int:todo_id>")
def complete_todo(todo_id):

    for todo in todos:

        if todo["id"] == todo_id:

            todo["completed"] = True

            break

    return redirect("/todos")

# ============================================================
# DELETE TODO
# ============================================================

@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):

    global todos

    todos = [
        todo for todo in todos
        if todo["id"] != todo_id
    ]

    return redirect("/todos")

# ============================================================
# BACK TO HOME
# ============================================================

@app.route("/back")
def back():

    return redirect("/")

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)