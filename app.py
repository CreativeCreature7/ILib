# ----------------------------------
# Working with Database : SQLite
# ----------------------------------

from flask import Flask, redirect, render_template, request, url_for, session
from my_modules import my_data_base
from random import randint
from datetime import timedelta


app = Flask(__name__)
print(type(app))
app.secret_key = 'my_secret'
app.permanent_session_lifetime = timedelta(minutes=30)



dbms = my_data_base.MyDatabase(my_data_base.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()

admin_name = 'admin'
admin_password = 'admin'


# Program entry point
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        if app.current == 'booksloans':
            app.current = 'home'
            return redirect(url_for('books_loans'))
        elif app.current == 'customers':
            app.current = 'home'
            return redirect(url_for('customers'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_name and password == admin_password:
            session['user'] = 'admin'
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/generate')
def generate():
    dbms.generate_fake_data()
    return redirect(url_for('login'))


@app.route('/booksloans', methods=['GET', 'POST'])
def books_loans():
    app.current = 'booksloans'
    if 'user' in session:
        message = ''
        # res = dbms.get_data_db(table=my_data_base.LOANS) - gets all loans
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
                return render_template("booksloans.html", books=res)  
        res = dbms.get_data_db(table=my_data_base.BOOKS)
        return render_template("booksloans.html", books=res, message=message)
    return redirect(url_for('login'))

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    app.current = 'customers'
    if 'user' in session:
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
    return redirect(url_for('login'))


# run the program
if __name__ == "__main__":
    app.run(debug=True)
