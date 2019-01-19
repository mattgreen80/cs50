from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter. This is adding the usd function to the filters dict in the jinja env.
# http://jinja.pocoo.org/docs/dev/api/#writing-filters
# first class functions can be treated as if they were variables. usd is a function.
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    # personal touch (add cash)
    if request.method == "POST":
        # get amount of cash to add, making sure it is a valid amount
        try:
            cashadd = float(request.form.get("add"))
        except ValueError:
            # flash a message to user when the page reloads if the input is invalid
            flash("Invalid amount!")
            return redirect("/")
        if cashadd > 0:
            # get user's current cash
            cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
            # convert query to float and add to amount given by user
            cashadd += float(cash[0]['cash'])
            # update user's cash with new amount
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cashadd, id=session["user_id"])
        else:
            flash("Invalid amount!")
            return redirect("/")

    # note: queries using db.execute return a list of dict objects containing key value pairs
    # name variable to show current users name in template
    name = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    # variable to show current cash
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    # users stock owned
    stock = db.execute("SELECT name FROM portfolio WHERE userid = :userid GROUP BY name", userid=session["user_id"])

    # users shares owned
    shares = db.execute("SELECT name, SUM(quantity) FROM portfolio WHERE userid = :userid GROUP BY name", userid=session["user_id"])

    # for every dict object in stock, retireve the name, then query the price for that name and put it into a list called price
    # the list created will match the order of the names in stock
    price = []
    for dic in stock:
        temp0 = lookup(dic["name"])
        if temp0:
            price.append(temp0["price"])
        else:
            apology("lookup failed", 400)

    # total value of shares and cash. loop over the prices in the list, and because every price in the list is in the same order as
    # every dict in the stock object, the index iterator created with enumerate will get the quantity of each share from the dict and then
    # multiply it by each value in the price list.
    total = 0.0
    for index, value in enumerate(price):
        quant = shares[index]["SUM(quantity)"]
        total += value*quant
    total = total + cash[0]["cash"]

    # return the template with the relevant objects for jinja
    return render_template("index.html", name=name, cash=cash, total=total, shares=shares, price=price, usd=usd)

    return apology("Cant display index", 400)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # get share symbol from form
        symb = request.form.get("symbol")
        # check if there is text and that it is a symbol
        if symb is None:
            return apology("Invalid symbol", 400)
        else:
            # retrieve stock price, symbol and stock name via lookup function
            quote = lookup(request.form.get("symbol"))

        # retrieve number of shares wanted as an int
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            # return apology if not int
            return apology("Invalid amount", 400)

        # if stock does not exist or is blank or if there is no quantity then apologise
        if quote is not None and shares > 0 :
            # get current user's cash. query session dict for current user logged in
            cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
            cash = cash[0]["cash"]

            # check that user has enough cash to purchase shares
            if cash > shares * quote["price"]:
                # insert transaction into portfolio table if user has enough cash
                db.execute("INSERT INTO portfolio (name, userid, price, quantity) VALUES (:name, :userid, :price, :quantity)",name=quote["symbol"],userid=session["user_id"], price=quote["price"], quantity=shares)
                # update user's cash in the users table
                db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash-shares*quote["price"], id=session["user_id"])
                # return user to index summary page after purchase
                return redirect("/")
            else:
                flash("Not enough cash!")
                return redirect("/buy")
        else:
            return apology("Stock does not exist or quantity not given", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

    return apology("Buy failed", 400)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # name variable to show current users name in template
    name = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    # user's transaction history
    hist = db.execute("SELECT transactid, name, price, quantity, date FROM portfolio WHERE userid = :userid", userid=session["user_id"])

    # return the template with the relevant objects for jinja
    return render_template("history.html", name=name, hist=hist)

    # if function fails
    return apology("Can't display history", 400)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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

        # get share symbol from form
        symb = request.form.get("symbol")
        # check if there is text and that it is a symbol
        if symb is None or symb.isalpha() == False:
            return apology("Invalid symbol", 400)
        else:
            # retrieve stock price, symbol and stock name via lookup function (returns dict object)
            quote = lookup(request.form.get("symbol"))

        # display stock quote with information passed in else if quote is blank then apologise
        if quote is not None:
            # convert price to USD with helper function first
            price = usd(quote["price"])
            return render_template("quoted.html", quote=quote, price=price)
        else:
            return apology("Stock does not exist or lookup failed", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

    return apology("Quote failed", 400)


@app.route("/register", methods=["GET", "POST"])
def register():

    # get username and password with confirmation.
    if request.method == "POST":

        # Ensure username was submitted and only allow alphabetic characters for username
        # Since database is small this shouldn't create any issues and will prevent users using only numbers or symbols
        username = request.form.get("username")
        if not username:
            return apology("Please provide a username", 400)

        # Ensure both passwords were submitted.
        elif not request.form.get("password"):
            return apology("Please provide a password", 400)

        elif not request.form.get("confirmation"):
            return apology("Please confirm password", 400)

        # make sure both password fields match else apology
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match!", 400)

        # check that username is not already present in database
        if db.execute("SELECT username FROM users WHERE username = :username", username=username):
            return apology("User already exists", 400)

        # generate password hash
        # need to fix this as the same salt is being used for every password and MD5 is not secure
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:md5', salt_length=5)

        # add user to database. execute should return the primary key for the row if successful
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username")
        ,hash=hash)
        # if query does not return a row then apology else flash a message letting them know it was successful
        if result == None:
            return apology("Unable to add user", 400)
            flash("Registration successful!")
        else:
            # Forget any current session so a new one can be created below
            session.clear()
            #log user in by storing their id number in the session user id.
            userid = db.execute("SELECT id FROM users WHERE hash = :hash", hash=hash)
            # use the [0] to specify the first dict in userid object
            # with dictionaries the key values can be accessed using the same syntax for relative position e.g. ["id"]
            session["user_id"] = userid[0]["id"]
            # flash success message to user (here because it gets cleared with session.clear() so it must be after it is called)
            flash("Registration successful!")
            # Redirect user to home page after login
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

    return apology("Registration failed", 400)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # get share symbol from form
        symb = request.form.get("symbol")

        # retrieve stock price, symbol and stock name via lookup function (returns dict object)
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Lookup failed", 400)

        # retrieve number of shares to sell as an int and convert it to a negative number
        try:
            quant = int(request.form.get("shares"))
        except ValueError:
            # apologise if not an int
            return apology("Invalid quantity", 400)
        else:
            quant = abs(quant)*-1

        # variable to show user's current cash
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = cash[0]["cash"]

        # check if user owns that particular stock and that they have the same or more quantity
        shares = db.execute("SELECT name, SUM(quantity) FROM portfolio WHERE userid = :userid GROUP BY name", userid=session["user_id"])

        for share in shares:
            # if the share is found in the list (the user owns it)
            if share["name"] == quote["name"]:
                # if the quantity of the shares owned is greater than the quantity the user wants to sell
                if share["SUM(quantity)"] > quant:
                    # insert transaction into portfolio table
                    db.execute("INSERT INTO portfolio (name, userid, price, quantity) VALUES (:name, :userid, :price, :quantity)",name=quote["symbol"],userid=session["user_id"], price=quote["price"], quantity=quant)
                    # update user's cash in the users table
                    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash+(quant*-1)*quote["price"], id=session["user_id"])
                    # return user to index summary page after sell
                    return redirect('/')
                # if the quantity of the particualr share is less than the quantity user wants to sell, then apologise
                else:
                    apology("You don't have that many to sell!", 400)
            else:
                apology("You don't own any of that name", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # get a list of share names that the user owns for the select HTML element
        select = db.execute("SELECT name FROM portfolio WHERE userid=:id GROUP BY name", id=session["user_id"])

        return render_template("sell.html", select=select)

    return apology("Buy failed", 400)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
