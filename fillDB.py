import csv
import sys
from cs50 import SQL

db = SQL("sqlite:///networth.db")

def main():

    with open('transactions.csv', "r") as f:
        reader = csv.reader(f)

        for row in reader:
            amount = row[0]
            location = row[1]
            date = row[2]
            print(amount, location, date)
            db.execute("INSERT INTO Transactions (Amount, Location, Date) VALUES (?, ?, ?)", amount, location, date)

main()