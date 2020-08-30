import os
import csv 
import sys

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, text


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create table books if it doesn't exist
db.execute(text("CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year SMALLINT NOT NULL)"))
db.commit()

# Read csv file and write into books table
def main():
    books = []     
    try:
        with open("books.csv", "r") as file:
            data = csv.reader(file)
            books = list(data)
            for book in books[1:]:
                db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                               {"isbn": book[0], "title": book[1], "author": book[2], "year": book[3]})
                db.commit()
                print(book)
    except IOError:
        sys.exit(f"Could not read {books}")

if __name__ == "__main__":
    main()

