import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance/finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol, shares = request.form.get("symbol"), int(request.form.get("shares"))

        # Get stock info through look up function
        symbol_data = lookup(symbol)
        unit_price, name = symbol_data['price'], symbol_data['name']

        # Query database for user cash
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        # Compare inputed shares value with user's current cash
        cash, transaction_sum = row[0]['cash'], (shares * unit_price)
        if cash >= transaction_sum:
            # Insert new buy transaction in table
            db.execute("""INSERT INTO transactions (user_id, amount, price, symbol, sold) 
                        VALUES ((SELECT id FROM users WHERE id = :id), :amount, :price, :symbol)""", id=session["user_id"], amount=shares, price=unit_price, symbol=symbol)

            cash -= transaction_sum
            # Subtract transaction value from user funds
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash, id=session["user_id"])
            
            return render_template("buy.html", status="success", message=f"Transaction succeded, you bought {shares} shares of {name}")

        else:
            return render_template("buy.html", status="danger", message=f"Transaction failed, insuficient funds for buying {shares} shares of {name}")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # Get stock info through look up function
        symbol_data = lookup(symbol)
        if symbol_data == None:
            return render_template("quote.html", quote=f"Oops... symbol not found")
        else:
            name, price = symbol_data['name'], usd(symbol_data['price'])
            return render_template("quote.html", quote=f"Current share price of {name}: {price}")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username, password, confirmation  = request.form.get("username"), request.form.get("password"), request.form.get("confirmation")
        # Check if the entered username already exists in the database
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows) != 0:
            return apology("this username already exists", 403)
            # Check if password and password confirmation match
        elif password != confirmation:
            return apology("the password and confirmation don't match") # Bad request error

        # INSERT the new user into users, storing a hash of the user’s password
        hash_value = generate_password_hash(password, method='sha256')
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash_value)
        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
