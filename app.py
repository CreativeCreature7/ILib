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
from flask import Flask, render_template
from my_modules import init_db

api = Flask(__name__)
dbms = init_db.MyDatabase(init_db.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()
dbms.add_book('How to kill a dragon', 'Guy Ben Hemo', 2021, 2)
dbms.add_book('How to kill a dragon - 2', 'Guy Ben Hemo', 2022, 3)

@api.route('/')
def home():
    return render_template("index.html")

@api.route('/books')
def books():
    res= dbms.get_data_db(table=init_db.BOOKS)
    return render_template("books.html",books=res)




# Program entry point
def main():
    api.run(debug=True)

    # # Create Tables
    # dbms.create_db_tables()
    # # dbms.insert_single_data()
    # # dbms.db_query(init_db.USERS)
    # # dbms.db_query(init_db.ADDRESSES)
    # dbms.insert_cars("green",2034)
    # dbms.db_query(table= init_db.CARS)

    # dbms.db_query(query= f"select color from '{init_db.CARS}'")
    # dbms.delete_by_id(init_db.CARS,2 )
    # res= dbms.db_query(table= init_db.CARS)
    # print(res[1])
    # # dbms.sample_query() # simple query
    # # dbms.sample_delete() # delete data
    # # dbms.sample_insert() # insert data
    # # dbms.sample_update() # update data


# run the program
if __name__ == "__main__": main()
