from flask import Flask, render_template
from cs50 import SQL
from helpers import scraper

app = Flask(__name__)

db = SQL("sqlite:///ciders.db")

@app.route("/")
def index():
    scraper() # Remove the hash symbol when I want to rerun the scrape
    rows = db.execute("SELECT name, price, description FROM ciders")
    return render_template("index.html", rows=rows)

@app.route("/about")
def about():
    return render_template("about.html")