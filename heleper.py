from faker import Faker
from random import randint
from datetime import datetime, timedelta
from my_modules import init_db

dbms = init_db.MyDatabase(init_db.SQLITE, db_name='mydb.sqlite')
dbms.create_db_tables()

# genreate 100 fake users and books
def generate_fake_data():
    fake = Faker()
    for i in range(100):
        # generate fake user
        name = fake.name()
        city = fake.city()
        age = randint(18, 60)
        # generate fake book
        book_name = fake.text(max_nb_chars=20)
        book_author = fake.name()
        book_year = randint(2000, 2020)
        book_type = randint(1, 3)
        # generate fake loan
        loan_date = datetime.now()
        if book_type == 1:
            return_date = loan_date + timedelta(days=10)
        elif book_type == 2:
            return_date = loan_date + timedelta(days=5)
        else:
            return_date = loan_date + timedelta(days=2)    
        # insert fake data
        dbms.add_customer(name, city, age)
        dbms.add_book(book_name, book_author, book_year, book_type)
        if i%5 == 0:
            dbms.loan_book(randint(1, 100), randint(1, 100), loan_date, return_date)

def main():
    generate_fake_data()
    print(dbms.get_data_db(table=init_db.BOOKS))
    print(dbms.get_data_db(table=init_db.CUSTOMERS))
    print(dbms.get_data_db(table=init_db.LOANS))

if __name__ == "__main__":
    main()