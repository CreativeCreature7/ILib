# ----------------------------------
# Working with Database : SQLite
# ----------------------------------
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


@app.route('/books', methods=['GET', 'POST'])
def books():
    message = ''
    if request.method == 'POST':
        if 'delete_book' in request.form: 
            message = dbms.delete_book_by_id(request.form['delete_book'])
        if 'loan_book' in request.form: 
            message = dbms.loan_book(randint(1,100), request.form['loan_book'])
        if 'return_book' in request.form:
            message = dbms.return_book(request.form['return_book'])
        if 'name' in request.form and 'author' in request.form and 'year_published' and 'book_type' in request.form:
            message = dbms.add_book(request.form['name'], request.form['author'], request.form['year_published'], request.form['book_type'])
        if 'book_name' in request.form:
            res = dbms.find_book_by_name(request.form['book_name'])
            return render_template("books.html", books=res)  
    res = dbms.get_data_db(table=my_data_base.BOOKS)
    return render_template("books.html", books=res, message=message)


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    message = ''
    print(request.form)
    if request.method == 'POST':
        if 'name' in request.form and 'city' in request.form and 'age' in request.form:
            message = dbms.add_customer(request.form['name'], request.form['city'], request.form['age'])
        if 'remove_customer' in request.form:
            message = dbms.remove_customer(request.form['remove_customer'])
        if 'customer_name' in request.form:
            res = dbms.find_customer_by_name(request.form['customer_name'])
            return render_template("customers.html", customers=res)  
    res = dbms.get_data_db(table=my_data_base.CUSTOMERS)
    return render_template("customers.html", customers=res, message=message)

@app.route('/loans')
def loans():
    res = dbms.get_data_db(table=my_data_base.LOANS)
    return render_template("loans.html", loans=res)

@app.route('/late_loans')
def late_loans():
    res = dbms.display_all_late_loans()
    return render_template("late_loans.html", late_loans=res)


# run the program
if __name__ == "__main__":
    app.run(debug=True)
