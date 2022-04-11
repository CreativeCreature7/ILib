import datetime
from faker import Faker
from random import randint
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime  

# Global Variables
SQLITE                  = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
BOOKS = 'Books'
CUSTOMERS = 'Customers'
LOANS = "loans"


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, db_type, username='', password='', db_name=''):
        db_type = db_type.lower()

        if db_type in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[db_type].format(DB=db_name)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        # Create Tables
        metadata = MetaData()
        books = Table(BOOKS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String),
                      Column('author', String),
                      Column('year_published', Integer),
                      Column('type', Integer)
                      )

        customers = Table(CUSTOMERS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String),
                      Column('city', String),
                      Column('age', Integer)
                      )

        loans = Table(LOANS, metadata,
                        Column('cust_id', Integer, ForeignKey('Customers.id')),
                        Column('book_id', Integer, ForeignKey('Books.id')),
                        Column('loan_date', DateTime),
                        Column('return_date', DateTime)
                        )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)


    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return

        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    # Select
    def get_data_db(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}';"
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append(row)
                result.close()
        return res

    # Examples



    def delete_by_id(self, table, id):
        # Delete Data by Id
        
        query = f"DELETE FROM {table} WHERE id={id}"
        self.execute_query(table=table)
        return f"deleted {id} successfully"


    def add_book(self, name, author, year_published, book_type):
        # Insert Data
        query = f"INSERT INTO {BOOKS}(name, author, year_published, type) " \
                f"VALUES ('{name}', '{author}', {year_published}, {book_type});"
        self.execute_query(query=query)

    def add_customer(self, name, city, age):
        # Insert Data
        query = f"INSERT INTO {CUSTOMERS}(name, city, age) " \
                f"VALUES ('{name}', '{city}', {age});"
        self.execute_query(query=query)

    def loan_book(self, cust_id, book_id):
        query = f"SELECT * FROM {LOANS} WHERE book_id={book_id}"
        res = self.get_data_db(query=query)
        if res:
            return "Book is already loaned"
        query = f"SELECT type FROM {BOOKS} WHERE id={book_id}"
        book_type = self.get_data_db(query=query)
        if book_type == 1:
            return_date = datetime.date(datetime.now()) + timedelta(days=10)
        elif book_type == 2:
            return_date = datetime.date(datetime.now()) + timedelta(days=5)
        else:
            return_date = datetime.date(datetime.now()) + timedelta(days=2)
        query = f"INSERT INTO {LOANS}(cust_id, book_id, loan_date, return_date) " \
                f"VALUES ({cust_id}, {book_id}, '{datetime.date(datetime.now())}', '{return_date}');"
        self.execute_query(query=query)
        return "Book loaned successfully"

    # when book_id is not on database it is available for loan
    def return_book(self, book_id):
        query = f"SELECT * FROM {LOANS} where book_id={book_id}"
        res = self.get_data_db(query=query)
        if res:
            query = f"DELETE FROM {LOANS} WHERE book_id={book_id}"
            self.execute_query(query=query)
        else:
            print('Book not loaned')
    def display_all_books(self):
        return self.get_data_db(table=BOOKS)

    def display_all_customers(self):
        return self.get_data_db(table=CUSTOMERS)

    def display_all_loans(self):
        return self.get_data_db(table=LOANS)

    def display_all_late_loans(self):
        late_loans = []
        res = self.get_data_db(table={LOANS})
        for loan in res:
            if datetime.datetime.now() < loan[3]:
                late_loans.append(loan)
        return late_loans

    def find_book_by_name(self, name):
        query = f"SELECT * FROM {BOOKS} WHERE name= '{name}'"
        res = self.get_data_db(query=query)
        if res:
            return res
        return 'Book Not Found'

    def find_customer_by_name(self, name):
        query = f"SELECT * FROM {CUSTOMERS} WHERE name= '{name}'"
        res = self.get_data_db(query=query)
        if res:
            return res
        return 'Customer Not Found'

    def delete_book_by_id(self, id):
        # Delete Book by Id
        query = f"DELETE FROM {BOOKS} WHERE id={id}"
        self.execute_query(query=query)
        return f"deleted {id} successfully"
    
    def remove_customer(self, id):
        # Delete Customer by Id
        query = f"DELETE FROM {CUSTOMERS} WHERE id={id}"
        self.execute_query(query=query)
        return f"deleted {id} successfully"

    # genreate 100 fake users and books
    def generate_fake_data(self):
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
            try:
                self.add_customer(name, city, age)
                self.add_book(book_name, book_author, book_year, book_type)
                if i%5 == 0:
                    self.loan_book(randint(1, 100), randint(1, 100), datetime.date(loan_date), datetime.date(return_date))  
            except Exception as e:
                print(e)