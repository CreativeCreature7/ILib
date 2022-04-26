# ----------------------------------
# Working with Database : SQLite
# ----------------------------------
from flask import Flask, redirect, render_template, request, url_for, session
from my_modules import my_data_base
from random import randint
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'my_secret'
app.permanent_session_lifetime = timedelta(minutes=30)

dbms = my_data_base.MyDatabase(my_data_base.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()

admin_name = 'admin'
admin_password = 'admin'


# Program entry point
@app.route('/', methods=['GET', 'POST'])
def login():
    app.current = 'home'
    message = ''
    if 'user' in session:
        message = "already logged in"
        if app.current == 'booksloans':
            return redirect(url_for('books_loans', message=message))
        elif app.current == 'customers':
            return redirect(url_for('customers', message=message))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_name and password == admin_password:
            session['user'] = 'admin'
            message = 'logged in successfully'
        else:
            message = 'incorrect login details. please try again'
    return render_template("login.html", message=message)




@app.route('/booksloans', methods=['GET', 'POST'])
def books_loans():
    app.current = 'booksloans'
    message = ''
    if 'user' in session:
        if request.method == 'POST':
            if 'delete_book' in request.form: 
                message = dbms.delete_book_by_id(request.form['delete_book'])
            if 'loan_book' in request.form: 
                users_ids = dbms.get_users_id()
                random_user = users_ids[randint(0, len(users_ids))-1][0]
                print(random_user)
                message = dbms.loan_book(random_user, request.form['loan_book'])
            if 'return_book' in request.form:
                message = dbms.return_book(request.form['return_book'])
            if 'name' in request.form and 'author' in request.form and 'year_published' and 'book_type' in request.form:
                message = dbms.add_book(request.form['name'], request.form['author'], request.form['year_published'], request.form['book_type'])
            if 'book_name' in request.form:
                books = dbms.find_book_by_name(request.form['book_name'])
                books_id = dbms.get_books_id_from_loans()
                return render_template("booksloans.html", books=books, books_id=books_id)  
        elif 'message' in request.args:
            message = request.args['message']
        books = dbms.get_data_db(table=my_data_base.BOOKS)
        books_id = dbms.get_books_id_from_loans()
        print(books_id)
        return render_template("booksloans.html", books=books, books_id=books_id, message=message)
    return redirect(url_for('login'))

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    app.current = 'customers'
    message = ''
    late_loans = dbms.display_late_loans()
    if 'user' in session:
        if request.method == 'POST':
            if 'name' in request.form and 'city' in request.form and 'age' in request.form:
                message = dbms.add_customer(request.form['name'], request.form['city'], request.form['age'])
            if 'remove_customer' in request.form:
                message = dbms.remove_customer(request.form['remove_customer'])
            if 'customer_name' in request.form:
                res = dbms.find_customer_by_name(request.form['customer_name'])
                return render_template("customers.html", customers=res, late_loans=late_loans)  
        res = dbms.get_data_db(table=my_data_base.CUSTOMERS)
        if 'message' in request.args:
            message = request.args['message']
        return render_template("customers.html", customers=res, message=message, late_loans=late_loans)
    return redirect(url_for('login'))

@app.route('/generate')
def generate():
    dbms.generate_fake_data()
    return redirect(url_for('login'))

# run the program
if __name__ == "__main__":
    app.run(debug=True)
