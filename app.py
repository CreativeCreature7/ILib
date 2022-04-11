# author: Mahmud Ahsan
# code: https://github.com/mahmudahsan/thinkdiff
# blog: http://thinkdiff.net
# http://pythonbangla.com
# MIT License

# ----------------------------------
# Working with Database : SQLite
# ----------------------------------
from my_modules.book import Book
from my_modules.customer import Customer
from my_modules.loan import Loan
from flask import Flask, redirect, render_template, url_for
from my_modules import init_db


app = Flask(__name__)
dbms = init_db.MyDatabase(init_db.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()




# Program entry point
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate')
def generate():
    dbms.generate_fake_data()
    return redirect('/')

@app.route('/books')
def books():
    res = dbms.get_data_db(table=init_db.BOOKS)
    return render_template("books.html", books=res)

@app.route('/customers')
def customers():
    res = dbms.get_data_db(table=init_db.CUSTOMERS)
    return render_template("customers.html", customers=res)

@app.route('/loans')
def loans():
    res = dbms.get_data_db(table=init_db.LOANS)
    return render_template("loans.html", loans=res)


# run the program
if __name__ == "__main__":
    app.run(debug=True)
