from __main__ import app 
from flask import url_for , render_template, redirect, flash, request, session

from db_connecter import database
import requests
import hashlib

#defines our database
db = database ()



@app.route('/')
def home():
    title = "home"
    return render_template('index.html',title=title)

@app.route('/about')
def about():
    title= "about"
    return render_template('index.html',title=title)

@app.route('/home')
def backtohomepage():
    title= 'home'
    return redirect(url_for("home"))

@app.route('/data')
def data():
    title = "Data"
    books = db.queryDB('SELECT * FROM Book_tbl')
    return render_template('data.html', title=title, books=books)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", '')
    author = request.form.get("author",'')

    db.updateDB("INSERT INTO Book_TBL(title,author) VALUES (?,?)", [title, author])
    flash("Book Added Successfully")

    return redirect(url_for("data"))

@app.route('/delete/<int:Book_ID>', methods=['GET', 'POST'])
def delete(Book_ID):
    books = db.queryDB("SELECT * FROM Book_tbl WHERE Book_ID = ?", [Book_ID])
    if not books:
        flash('Book not found.', 'danger')
    else:
        db.updateDB("DELETE FROM Book_tbl WHERE Book_ID = ?", [Book_ID])
        flash('Book deleted successfully.', 'success')
    return redirect(url_for('data'))

@app.route('/Login')
def login():
    title = "Log In"
    found_user = ""

    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pword"]
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        found_user = db.queryDB("SELECT * FROM User_Table WHERE name = ?", [user])
    if found_user:
        stored_password = found_user[0][3]
        if stored_password == hashed_password:
            session["user"] = user
            session["email"] = found_user[0][2]
            flash("LogIn successful", 'success')
            return redirect(url_for("home"))
        else:
            flash("Incorrect password.", "danger")
    else:
        flash("User not found.", "danger")
    
    if "user" in session:
        flash("Already Logged IN!", "info")
        return redirect(url_for("users"))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    current_user = session.get('user')
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pword"]
        email = request.form["email"]

        hashed_email = hashlib.md5(str(email).encode()).hexdigest()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        result = db.queryDB("SELECT * FROM User_Table WHERE name = ? or email = ?", [user, hashed_email])
        if result:
            flash('Email or username already exists, please try a different one', 'danger')
            return redirect(url_for('register'))

            db.updateDB("INSERT INTO users (name,email,password) VALUES (?,?,?)", [user, hashed_email, hashed_password])
            return render_template('login.html', title='login')
        else:
            return render_template('register.html', title='Register')
    else:
        return render_template('register.html', title='Register')
