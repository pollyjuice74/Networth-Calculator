from flask import Flask, flash, redirect, render_template, request, session, json
from cs50 import SQL
from helpers import usd, is_valid_date

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

#Setting up database
db = SQL("sqlite:///networth.db")


@app.route("/", methods=["GET","POST"])
def index():
    #Selecting database
    transactions = db.execute("SELECT * FROM Transactions")

    #Calculating all time assets
    result0 = db.execute("SELECT SUM(Amount) FROM transactions WHERE Amount > 0")
    allTimeAssets = float(result0[0]['SUM(Amount)'])

    #Calculating expenses
    result1 = db.execute("SELECT SUM(Amount) FROM transactions WHERE Amount < 0")
    expenses = float(result1[0]['SUM(Amount)'])

    #Calculating networth
    networth = allTimeAssets + expenses

    #If POST method
    if request.method == "POST":
        return redirect("/entry")
    #If GET method
    else:
        return render_template("index.html", transactions=transactions, expenses=expenses, networth=networth, allTimeAssets=allTimeAssets)


@app.route("/entry", methods=["POST"])
def entry():
    #Get inputs
    amount = request.form.get("amount")
    location = request.form.get("location")
    date = request.form.get("date")

    #Input validation
    if not (amount or location or date):
        return render_template("failure.html")
    elif not is_valid_date(date):
        return render_template("failure.html")
    else:
        #Execute input and return success
        db.execute("INSERT INTO Transactions (Amount, Location, Date) VALUES (?, ?, ?)", amount, location, date)
        return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/failure")
def failure():
    return render_template("failure.html")

