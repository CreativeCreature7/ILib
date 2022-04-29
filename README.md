# ILib - Comprehensive library management system

<h2>this project is not secure!</h2>

<h2>Log-in credentials</h2>

<h3>username: admin</h3>

<h3>password: admin</h3>

<h2>available on <a href="https://i-lib.herokuapp.com/">Heroku</a></h2>

<br />

<h2>to run on local machine:</h2>

<ul>
  <li>git clone https://github.com/CreativeCreature7/ILib</li>

  <li>open app.py and run</li>
</ul>

<h1>index</h1>

<img src="https://i.ibb.co/TrLQ6D5/ilib-index.png" alt="screenshot of index page" />

<p>
  Log-in info at the top of the readme. <br />
  button - "add dummy data" adds 100 customers 100 books and some loans to
  database
</p>

<h1>Books & Loans</h1>

<img
  src="https://i.ibb.co/jHXWsZY/ilib-booksloans.png"
  alt=" screenshot of booksloans page"
/>

<p>
  search book by name - top right <br />

  cards(books) - top of the cars is the book name and at the bottom there is
  author's name with year of publishing.
  <br />
  in addition there is "loan" - button for books that can be loaned and return
  button for books that are already loaned.<br />
  you can also delete the book by pressing delete.<br />

  at the bottom left of the page there is add new book button that allows to add
  new book
</p>

<h1>Customers</h1>

<img src="https://i.ibb.co/LvxYvSn/ilib-customers.png" alt=" screenshot of customers page" />

<p>each customer is a row in the table and has these properties:</p>

<ul>
  <li>id- from database</li>

  <li>name</li>

  <li>city</li>

  <li>age</li>

  <li>
    late loans - <b>NOTE!</b> late loan is defined as about to be late in 5
    days, so the late loans table won't be empty. for real life application in
    my_modules/my_data_base.py in line 159 delete + timedelta(days=5)
  </li>

  <li>
    remove - deletes user and related loans and returns late loans and all books
  </li>
</ul>

