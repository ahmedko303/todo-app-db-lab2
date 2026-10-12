from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="303120",
    database="registration"
)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if name.strip() == "":
        return "Name is required"

    if email.strip() == "":
        return "Email is required"

    if password.strip() == "":
        return "Password is required"

    if confirm_password.strip() == "":
        return "Confirm password is required"

    if password != confirm_password:
        return "Passwords do not match"

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return "Email Already Exists"

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, email, password_hash)
        VALUES (%s, %s, %s)
        """,
        (
            name,
            email,
            hashed_password.decode("utf-8")
        )
    )

    db.commit()

    session["user_id"] = cursor.lastrowid
    session["name"] = name

    return redirect("/dashboard")


@app.route("/login_user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    if email.strip() == "":
        return "Email is required"

    if password.strip() == "":
        return "Password is required"

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user:

        if bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            return redirect("/dashboard")

    return "Invalid email or password"


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM todos
        WHERE user_id=%s
        ORDER BY todo_id DESC
        """,
        (session["user_id"],)
    )

    todos = cursor.fetchall()

    open_tasks = 0

    for todo in todos:
        if todo["is_done"] == 0:
            open_tasks += 1

    return render_template(
        "dashboard.html",
        name=session["name"],
        todos=todos,
        open_tasks=open_tasks
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/add_todo", methods=["POST"])
def add_todo():

    if "user_id" not in session:
        return redirect("/")

    title = request.form["title"]

    if title.strip() == "":
        return "Title is required"

    if len(title) > 200:
        return "Title is too long"

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO todos (user_id, title)
        VALUES (%s, %s)
        """,
        (
            session["user_id"],
            title
        )
    )

    db.commit()

    return redirect("/dashboard")


@app.route("/edit_todo/<int:id>", methods=["POST"])
def edit_todo(id):

    title = request.form["title"]

    if title.strip() == "":
        return "Title is required"

    if len(title) > 200:
        return "Title is too long"

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE todos
        SET title=%s
        WHERE todo_id=%s
        AND user_id=%s
        """,
        (
            title,
            id,
            session["user_id"]
        )
    )

    db.commit()

    return redirect("/dashboard")


@app.route("/toggle_done/<int:id>")
def toggle_done(id):

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE todos
        SET is_done = NOT is_done
        WHERE todo_id=%s
        AND user_id=%s
        """,
        (
            id,
            session["user_id"]
        )
    )

    db.commit()

    return redirect("/dashboard")


@app.route("/delete_todo/<int:id>")
def delete_todo(id):

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM todos
        WHERE todo_id=%s
        AND user_id=%s
        """,
        (
            id,
            session["user_id"]
        )
    )

    db.commit()

    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)