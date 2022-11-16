# scraping-books

This is a web scraping project using following:
- Python
- requests
- BeautifulSoup
- sqlite3 database

## Process

- Here we are gathering information about the bestselling books from the [Bookdepository](https://www.bookdepository.com/bestsellers) website 
- There are 1020 books listed over 34 pages on the site
- using python libraries requests to get data from the url and beautifulsoup to parse the data
- The info gathered from the site are
  - book title
  - author
  - published date
  - publisher
  - format
  - price
  - language
  - rating
 - Then the data is saved in sqlite database.

#### To run this on local machine 

- You need to install [sqlite3](https://www.sqlite.org/download.html) on your local machine, 
and import the sqlite3 module to run the queries.

##### Create a virtual environement
```
pip install virtualenv
virtualenv <env name>
```
##### Activate the virtual environment and install the required libraries
```
env\scripts\activate
pip install -r requirements.txt
```

##### Clone the repository to local machine
```
git clone <repo url>
cd <folder name>
```

##### Create table 'books' in your database in sqlite3 terminal or you can include below lines in code
```
CREATE TABLE books (id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, author TEXT, published TEXT, publisher TEXT, format TEXT, language TEXT, price FLOAT, rating FLOAT, total_ratings INT);
```

##### Run the file and run the below line to check the data in database
```
SELECT * FROM books LIMIT 10;
```
