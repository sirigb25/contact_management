from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "any_random_secret_key"  # Needed for flash messages


# Function to fetch all contacts
def get_contacts():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return contacts


# Home route
@app.route("/")
def index():
    return render_template("index.html", contacts=get_contacts())


# Add contact (duplicates allowed)
@app.route("/add", methods=["POST"])
def add():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    address = request.form["address"]
    email = request.form["email"]
    phone = request.form["phone"]

    conn = sqlite3.connect("contacts.db")
    conn.execute(
        "INSERT INTO contacts (first_name, last_name, address, email, phone) VALUES (?, ?, ?, ?, ?)",
        (first_name, last_name, address, email, phone)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# Edit contact
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        address = request.form["address"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE contacts
            SET first_name=?, last_name=?, address=?, email=?, phone=?
            WHERE id=?
        """, (first_name, last_name, address, email, phone, id))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", contact=contact)


# Delete contact
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("contacts.db")
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
