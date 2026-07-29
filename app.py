from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database create
def create_database():

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()


# Home Page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("messages.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages(name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        print("Message Saved!")

    return render_template("index.html")


# Read Messages
@app.route("/messages")
def messages():

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")

    data = cursor.fetchall()

    conn.close()

    return render_template("messages.html", messages=data)


# Delete Message
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM messages WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/messages")


# Edit Message
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        cursor.execute(
            """
            UPDATE messages
            SET name=?, email=?, message=?
            WHERE id=?
            """,
            (name, email, message, id)
        )

        conn.commit()
        conn.close()

        return redirect("/messages")


    cursor.execute(
        "SELECT * FROM messages WHERE id=?",
        (id,)
    )

    data = cursor.fetchone()

    conn.close()

    return render_template("edit.html", message=data)


# Create database
create_database()


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)