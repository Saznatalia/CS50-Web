# Project 1 Books Review Website

Books review website that allows user register an account or login to the existing one, search for a book by typing title, author or isbn of the book, and review selected book. Book page has all neccesary details, including number of reviews and average score from Goodreads website for this book and reviews from other users. User is allowed to leave 1 review for the book or just rate with a star. User can also modify his/her password. 


There are 3 more python files presented for this project, additionally to application.py (main application file):
- import.py that imports the books into the database from csv file
- helper.py that has login_required function, apology (error) page
- createdb.py that creates database tables needed for this project