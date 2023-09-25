from __main__ import app 
from flask import url_for , render_template, redirect, request, flash

from db_connecter import database

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