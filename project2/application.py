import os
import requests
import sqlalchemy

from flask import Flask, session, flash, jsonify, redirect, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, User
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret'
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
def index():

    # Check if you are already logged in 
    if 'username' in session:
        return render_template("search.html")
    
    # Get data from user
    username = request.form.get("username")
    password = request.form.get("password")

    # User reached route via POST 
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE user_name = :user_name",
                          {"user_name": username}).fetchall()
 
        # Ensure user was registered
        if users == []:
            return apology("User doesn't exist, please register a new user", 403)

        hashed_password = users[0]['password']
        
        # Ensure username exists and password is correct
        if len(users) != 1:
            return apology("Invalid username", 403)

        elif check_password_hash(hashed_password, password) == False:
            return apology ("Invalid password", 403)

        # Remember which user has logged in
        session['username'] = request.form['username']
        session['user_id'] = users[0]['user_id']

        # Redirect user to search page
        return redirect(url_for('search'))
    
    # User reached route via GET
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Make sure all fields are filled and password and conifrmation are same
        if not username:
            flash("Missing username!")
            return apology("Missing username!", 403)
        elif not password:
            flash("Missing password!")
            return apology("Missing password!", 403)
        elif not confirmation:
            flash("Missing password confirmation!")
            return apology("Missing password confirmation!", 403)
        elif password != confirmation:
            flash("Your password and confirmation do not match!")
            return apology("Your password and confirmation do not match!", 403)
       
       # Make sure username is not registered
        elif db.execute("SELECT * FROM users WHERE user_name = :user_name", 
                       {"user_name": username}).rowcount == 1:
            flash("Username is already taken!")
            return apology("Username is already taken!", 403)

        # Hash password
        hash_password = generate_password_hash(password)

        # Insert a new user into database
        db.execute("INSERT INTO users (user_name, password) VALUES (:user_name, :password)",
                  {"user_name": username, "password": hash_password})
        db.commit()

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE user_name = :user_name",
                          {"user_name": username}).fetchall()

        # Remember which user has logged in
        session['username'] = request.form['username']
        session['user_id'] = users[0]['user_id']

        flash("You were successfully registered!")

        # Redirect user to registered page
        return redirect(url_for('search'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html')

#Search page
@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")

#Result page
@app.route("/result", methods=["GET", "POST"])
def result():
    search_input = request.form.get("search_input")
    if search_input == None:
        return render_template("search.html")

    # No book was found
    books = db.execute("SELECT * FROM books WHERE title ILIKE :pattern OR isbn ILIKE :pattern OR author ILIKE :pattern LIMIT 100", 
                      {"pattern": "%" + search_input + "%"}).fetchall()
    if books == []:
        return apology("Sorry, nothing was found", 403)

    # Print out results
    return render_template("result.html", books=books)

# Book page
@app.route("/result/<isbn>", methods=["GET", "POST"])
def book_page(isbn):

    # User wants to submit his review
    if request.method == "POST":
        
        # Check if user is logged in
        if session.get("user_id") is None:
            return redirect(url_for('index'))
        
        # Check that rate and review is not empty
        if not request.form.get("review") and not request.form.get("rating-value") or not request.form.get("rating-value"):
            return apology("You should rate the book and, optionally, write a review", 403)

        # Add review to the reviews table, make sure only review submitted from user
        try:
            # Add review into reviews table
            db.execute("INSERT INTO reviews (review, isbn, rate, user_id) VALUES (:review, :isbn, :rate, :user_id)",
                  {"review": request.form.get("review"), "isbn": isbn, "rate": request.form.get("rating-value"), "user_id": session["user_id"]})
            db.commit()

        except sqlalchemy.exc.IntegrityError:
            return apology("Sorry, you have already submitted the review for this book", 403)

    # Make sure the book exists
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return apology("No such book was found")

    # Reviews from other users
    reviews = db.execute("SELECT * FROM reviews INNER JOIN users ON users.user_id = reviews.user_id WHERE isbn = :isbn", 
                    {"isbn": book['isbn']}).fetchall()
    
    # Reviews from Goodreads users
    goodreads_reviews = request_review(book['isbn'])

    return render_template("book_page.html", book=book, reviews=reviews, goodreads_reviews=goodreads_reviews)

# Log out page
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for('index'))

# Change password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    # User reaches route vis POST (submitting the form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("Missing new password")
        elif not confirmation:
            return apology("Missing new password confirmation!")
        elif password != confirmation:
            return apology("Your new password and confirmation password do not match!")
    # Update password in database
        db.execute("UPDATE users SET password = :password WHERE user_id = :user_id",
                   {"password": generate_password_hash(password), "user_id": session["user_id"]})
        db.commit()

        flash("Password has been updated!")

        # Redirect user back to original page
        return redirect(url_for('search'))

    # User reaches route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_pwd.html")

# API from Goodreads to present on review page of the book
def request_review(isbn):

    # Contact API
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "6ReDH1q9Bnw9IgGfKzTwOQ", "isbns": isbn})
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        review = response.json()
        return {
            "ratings_count": int(review['books'][0]['ratings_count']),
            "reviews_count": int(review['books'][0]["reviews_count"]),
            "text_reviews_count": int(review['books'][0]["text_reviews_count"]),
            "work_ratings_count": int(review['books'][0]["work_ratings_count"]),
            "work_reviews_count": int(review['books'][0]["work_reviews_count"]),
            "work_text_reviews_count": int(review['books'][0]["work_text_reviews_count"]),
            "average_rating": float(review['books'][0]["average_rating"])       
        }
    except (KeyError, TypeError, ValueError):
        return None

# Create my API for others
@app.route("/api/<isbn>", methods=["GET"])
def book_api(isbn):
    """ Return the details of the book """

    # Make sure the book in the database
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid book isbn"}), 404
    
    # Count how many reviews on the book
    review_count_list = db.execute("SELECT COUNT(*) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()

    if len(review_count_list) == 0:
        review_count = 0
    else:
        review_count = review_count_list[0][0]
    
    # Calculate average rate
    rates = db.execute("SELECT rate FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    rate_list = []
    for i in range(len(rates)):
        rate_list.append(rates[i][0])
    average_score = float(sum(rate_list) / len(rate_list))

    return jsonify({
        "title": book["title"],
        "author": book["author"],
        "year": book["year"],
        "isbn": book["isbn"],
        "review_count": review_count,
        "average_score": average_score
    })

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.debug=True
    app.run()