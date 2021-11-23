from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
con = sqlite3.connect("accounts.db", check_same_thread=False)
cur = con.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    Error = None

    dbEmails = cur.execute('SELECT email FROM accounts WHERE email = ?;', (email,)).fetchall()
    dbUserPassword = cur.execute('SELECT hash FROM accounts WHERE email = ?;', (email,)).fetchall()

    # Handel Invalid Input Data
    if request.method == "POST":
        ### -> check if blank
        if len(password) == 0 or len(email) == 0:
            Error = "Error: there is empty field/fields... Please try again"
            return render_template("login.html", Error=Error)

        ### -> check email not exists
        if email != dbEmails[0][0]:
            Error = "Error: Email is invalid... Please try again"
            return render_template("login.html", Error=Error)

        ### -> check if password is wrong
        password_hash = check_password_hash(dbUserPassword[0][0], password)
        if password_hash == False:
            Error = "Error: Password is invalid... Please try again"
            return render_template("login.html", Error=Error)
        
        # Create Session
        session["user_id"] = cur.execute('SELECT id FROM accounts WHERE email = ?;', (email,)).fetchall()
        return redirect(url_for("dashboard"))

        

    return render_template("login.html")

@app.route("/rest")
def rest():
    return render_template("rest.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # collect data
    first_name = request.form.get("firstname")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    Error = None

    dbEmails = cur.execute('SELECT COUNT(email) FROM accounts WHERE email = ?;', (email,)).fetchall()



    # Handel Invalid Input Data
    if request.method == "POST":
        ## -> Generate password hash
        password_hash = generate_password_hash(password)

        ### -> Check if blank
        if len(first_name) == 0 or len(email) == 0 or len(password) == 0 or len(confirmation) == 0:
            Error = "Error: there is empty field/fields... Please try again"
            return render_template("signup.html", Error=Error)

        ### -> Check if email exists
        if dbEmails[0][0] != 0:
            Error = "Error: Email already exists... Please try again"
            return render_template("signup.html", Error=Error)

        ### -> Check if password = confirmation
        if password != confirmation :
            Error = "Error: Passwords does't match... Please try again"
            return render_template("signup.html", Error=Error)

        ### -> Check password lenght
        if len(password) < 6:
            Error = "Error: Password must be at least 6 characters... Please try again"
            return render_template("signup.html", Error=Error)

        ### -> Check special characters
        password_status = {
            0 : 'Very Bad',
            1 : 'Weak',
            2 : 'Not Bad',
            3 : 'Ok',
            4 : 'Perfect',
        }
        password_strength = {
            "special_characters" : 0,
            "upper_case" : 0,
            "lower_case" : 0,
            "numbers" : 0,
        }

        def check_strength():
            status = 0
            for key, value in password_strength.items():
                status += value
            return password_status[status]

        special_chars = ["<", ">", "@", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "[", "]", "{", "}", "?", ":", ";", "|", "\'", "\\", "\"", "\\", ",", ".", "/", "~", "`", "-", "=", " "]
        for char in range(len(special_chars)):
            if special_chars[char] in password:
                password_strength["special_characters"] = 1
        
        if password_strength["special_characters"] == 0:
            Error = "Error: Password must have special character... Please try again"
            check_strength = check_strength()
            return render_template("signup.html", Error=Error, check_strength=check_strength)

        ### -> Check upper case
        if re.search(r"[A-Z]", password):
            password_strength["upper_case"] = 1

        if password_strength["upper_case"] == 0:
            Error = "Error: Password must have upper case characters... Please try again"
            check_strength = check_strength()
            return render_template("signup.html", Error=Error, check_strength=check_strength)

        ### -> Check lower case
        if re.search(r"[a-z]", password):
            password_strength["lower_case"] = 1

        if password_strength["lower_case"] == 0:
            Error = "Error: Password must have lower case characters... Please try again"
            check_strength = print(check_strength())
            return render_template("signup.html", Error=Error, check_strength=check_strength)

        ### -> Check numbers 
        if re.search(r"[0-9]", password):
            password_strength["numbers"] = 1

        if password_strength["numbers"] == 0:
            Error = "Error: Password must have numbers... Please try again"
            return render_template("signup.html", Error=Error)

        cur.execute('''INSERT INTO accounts(first_name, email, hash) VALUES(?, ?, ?)''', (first_name, email, password_hash))
        con.commit()

        msg = "Account has been created successfully"
        return redirect(url_for("login", msg=msg))



    return render_template("signup.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Check if user not logged in
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Get user data useing Sessions
    user_id = session["user_id"][0][0]
    user_name = cur.execute('SELECT first_name FROM accounts WHERE id = ?;', (user_id,)).fetchall()[0][0]
    user_notes = cur.execute('SELECT * FROM notes WHERE accounts_id = ?;', (user_id,)).fetchall()

    # Collect Data From -Add New Note-
    if request.method == "POST":
        # Add new note
        if request.form["addbtn"] == "addbtn":
            note_status = request.form.get("note_status")
            new_note = request.form.get("new_note")

            cur.execute('''INSERT INTO notes(accounts_id, lable, note) VALUES(?, ?, ?)''', (user_id, note_status, new_note))
            con.commit()
    
    return render_template("dashboard.html", user_name=user_name, user_notes=user_notes, user_id=user_id)

@app.route("/dashboard/<int:id>", methods=["GET", "POST"])
def noteopen(id):
    # Get user data useing Sessions
    user_id = session["user_id"][0][0]
    user_name = cur.execute('SELECT first_name FROM accounts WHERE id = ?;', (user_id,)).fetchall()[0][0]
    user_notes = cur.execute('SELECT * FROM notes WHERE accounts_id = ?;', (user_id,)).fetchall()
    clicked_note = cur.execute('SELECT * FROM notes WHERE note_id = ?;', (id,)).fetchall()

    clicked_note_lable = request.form.get("edit_note_status")
    clicked_note_note = request.form.get("edit_note")
    clicked_note_id = request.form.get("note_id")

    if request.method == "POST":
        # Update note
        if request.form["updatebtn"] == "updatebtn":

            cur.execute('''UPDATE notes SET lable=?, note=? WHERE note_id=?;''', (clicked_note_lable, clicked_note_note, clicked_note_id))
            con.commit()

        # Delete note
        if request.form["deletebtn"] == "deletebtn":

            cur.execute('''DELETE FROM notes WHERE note_id=?;''', (clicked_note_id,))
            con.commit()

    return render_template("dashboard.html", clicked_note=clicked_note, note_id=id, open=True, user_name=user_name, user_notes=user_notes, user_id=user_id)


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()

# con.close()