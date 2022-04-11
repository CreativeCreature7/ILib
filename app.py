# ----------------------------------
# Working with Database : SQLite
# ----------------------------------
from email import message
from flask import Flask, redirect, render_template, request, url_for
from my_modules import my_data_base
from random import randint


app = Flask(__name__)
dbms = my_data_base.MyDatabase(my_data_base.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()




# Program entry point
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate')
def generate():
    dbms.generate_fake_data()
    return redirect(url_for('home'))

# @app.route('/delete_book', methods=['GET', 'POST'])
# def delete_book():
#     return redirect(url_for('books'))

@app.route('/books', methods=['GET', 'POST'])
def books():
    message = ''
    if request.method == 'POST':
        if 'delete_book' in request.form: 
            message = dbms.delete_book_by_id(request.form['delete_book'])
        if 'loan_book' in request.form: 
            message = dbms.loan_book(randint(1,100), request.form['loan_book'])
        # dbms.delete_book(book_id)
        # return redirect(url_for('home'))
    # if request.method == 'POST':
    #     if request.form['submit'] == 'Add':
    #         dbms.add_book(request.form['name'], request.form['author'], request.form['year_published'], request.form['type'])
    #         res = dbms.get_data_db(table=my_data_base.BOOKS)
    #         return redirect(url_for('books'), books=res)
    res = dbms.get_data_db(table=my_data_base.BOOKS)
    return render_template("books.html", books=res, message=message)

@app.route('/customers')
def customers():
    res = dbms.get_data_db(table=my_data_base.CUSTOMERS)
    return render_template("customers.html", customers=res)

@app.route('/loans')
def loans():
    res = dbms.get_data_db(table=my_data_base.LOANS)
    return render_template("loans.html", loans=res)


# run the program
if __name__ == "__main__":
    app.run(debug=True)
