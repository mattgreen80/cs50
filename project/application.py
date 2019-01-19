from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
# imports for sending emails
import smtplib
from email.mime import multipart, text
# additional local helpers file
from helpers import apology, login_required, select_menu

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///site.db")

@app.route("/", methods=["GET", "POST"])
def index():
    """Show current vehicles in db"""

    if request.method == "POST":
        # using javascript, if a selection in a HTML select drop down is made, the form will submit. This allows a rudimentary way
        # to refine vehicle results in the table on the HTML page.

        make = request.form.get("make")
        if make != '...':
            # query database and refine by the make selected
            result = db.execute("SELECT * FROM vehicles WHERE make=:make", make=make)
            # function to carry out distinct queries on all columns in databse to prevent duplicates in
            # drop down menus (see helpers.py).
            sel = select_menu(db, mak=make)
            # return template with select boxes and result of above query
            return render_template("index.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        model = request.form.get("model")
        if model != '...':
            # Query database and refine by the model selected
            result = db.execute("SELECT * FROM vehicles WHERE model=:model", model=model)
            sel = select_menu(db, mod=model)
            return render_template("index.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        year = request.form.get("year")
        if year != '...':
            #Query database and refine by the year selected
            result = db.execute("SELECT * FROM vehicles WHERE year=:year", year=year)
            sel = select_menu(db)
            return render_template("index.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        reg = request.form.get("reg")
        if reg != '...':
            #Query database and refine by the registration selected
            result = db.execute("SELECT * FROM vehicles WHERE reg=:reg", reg=reg)
            sel = select_menu(db, rg=reg)
            return render_template("index.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

    else:
        # function to carry out distinct queries on all columns in databse to prevent duplicates in
        # drop down menus and support search refinement (see helpers.py).
        sel = select_menu(db)
        # query all vehicles to show in results table on initial page landing
        result = db.execute("SELECT * FROM vehicles")
        # show all vehicles in template
        return render_template("index.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

    return apology("Cant display index", 400)

@app.route("/finance", methods=["GET", "POST"])
def finance():
    """Finance application for user"""

    if request.method == "POST":
        # determine vehicle id by getting select drop down results and querying database for the vehicle id
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        reg = request.form.get("reg")
        vehicleid = db.execute("SELECT id FROM vehicles WHERE model=:model AND make=:make AND year=:year AND reg=:reg", model=model, make=make, year=year, reg=reg)
        # try to convert id to int, if there is an index error then user did not choose a vehicle so render template again.
        try:
            vehicleid = int(vehicleid[0]["id"])
        except IndexError:
            flash("Please choose a vehicle!")
            # query database for all vehicles
            # distinct query for all columns so there are no duplicates in the select boxes.
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles")
            reg = db.execute("SELECT DISTINCT reg FROM vehicles")
            year = db.execute("SELECT DISTINCT year FROM vehicles")
            return render_template("finance.html", make=make, model=model, reg=reg, year=year)

        # add the application to database when user submits information
        # list to hold form input
        add = []
        # get input (if any)
        add.append(request.form.get("first_name"))
        add.append(request.form.get("email"))
        add.append(request.form.get("last_name"))
        add.append(request.form.get("dob"))
        add.append(request.form.get("licence"))
        add.append(request.form.get("city"))
        add.append(request.form.get("occupation"))
        add.append(request.form.get("phone"))

        # remove empty elements from list (i.e. if user did not fill out all fields)
        add = list(filter(None, add))

        # if user filled in correctly, then add vehicle to database
        if len(add) == 8:
            # add application to database
            db.execute("""INSERT INTO Applications (vehicleid, first_name, email, last_name, dob, licence, city, occupation, phone)
                    VALUES (:vehicleid, :first_name, :email, :last_name, :dob, :licence, :city, :occupation, :phone
                    )""", vehicleid=vehicleid, first_name=add[0], email=add[1], last_name=add[2], dob=add[3], licence=add[4], city=add[5], occupation=add[6], phone=add[7])
            # flash success to user
            flash("Application success!")
        else:
            # query database for all vehicles
            # distinct query for all columns so there are no duplicates in the select boxes.
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles")
            reg = db.execute("SELECT DISTINCT reg FROM vehicles")
            year = db.execute("SELECT DISTINCT year FROM vehicles")
            # if user does not fill out all fields then flash and render page again.
            flash("Please fill out all details!")
            return render_template("finance.html", make=make, model=model, reg=reg, year=year)

        # on success, email copy of application to user
        # message content
        msg = multipart.MIMEMultipart()
        msg['From'] = "mattgrnwl@gmail.com"
        msg['To'] = add[1]
        msg['Subject'] = "Your CreditCar application"
        body = f"""Congratulations {add[0]}, your recent finance application for the {year} {make} {model} has been received by the team
                at CreditCar. We will contact you via {add[1]} or {add[7]} shortly."""

        # create message
        msg.attach(text.MIMEText(body, 'plain'))
        emailmsg = msg.as_string()

        # login to server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("mattgrnwl@gmail.com", "PASSWORD HERE")

        # send email to address found in form input
        try:
            server.sendmail("mattgrnwl@gmail.com", add[1], emailmsg)
            server.quit()
        except:
            flash("Email failed to send!")

        # return user to index after application
        return redirect("/")

    else:
        # query database for all vehicles
        # distinct query for all columns so there are no duplicates in the select boxes.
        make = db.execute("SELECT DISTINCT make FROM vehicles")
        model = db.execute("SELECT DISTINCT model FROM vehicles")
        reg = db.execute("SELECT DISTINCT reg FROM vehicles")
        year = db.execute("SELECT DISTINCT year FROM vehicles")
        return render_template("finance.html", make=make, model=model, reg=reg, year=year)

    return apology("Cant display application", 400)

@app.route("/vehicles", methods=["GET", "POST"])
@login_required
def vehicles():
    """Manage dealer vehicles"""

    # using javascript, if a selection in a HTML select drop down is made, the form will submit. This allows a rudimentary way
    # to refine vehicle results in the table on the HTML page.
    if request.method == "POST":
        # temporarily store user id
        userid = session["user_id"]
        # same method as index page, but userid is passed to the select_menu function (defined in helpers.py)
        make = request.form.get("make")
        if make and make != '...':
            # query database and refine by the make selected
            result = db.execute("SELECT * FROM vehicles WHERE make=:make AND user=:user", make=make, user=userid)
            # function to carry out distinct queries on all columns in databse to prevent duplicates in
            # drop down menus (see helpers.py).
            sel = select_menu(db, mak=make, userid=userid)
            # return template with select boxes and result of above query
            return render_template("vehicles.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        model = request.form.get("model")
        if model and model != '...':
            # Query database and refine by the model selected
            result = db.execute("SELECT * FROM vehicles WHERE model=:model AND user=:user", model=model, user=userid)
            sel = select_menu(db, mod=model, userid=userid)
            return render_template("vehicles.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        year = request.form.get("year")
        if year and year != '...':
            #Query database and refine by the year selected
            result = db.execute("SELECT * FROM vehicles WHERE year=:year AND user=:user", year=year, user=userid)
            sel = select_menu(db, userid=userid)
            return render_template("vehicles.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        reg = request.form.get("reg")
        if reg and reg != '...':
            #Query database and refine by the registration selected
            result = db.execute("SELECT * FROM vehicles WHERE reg=:reg AND user=:user", reg=reg, user=userid)
            sel = select_menu(db, rg=reg)
            return render_template("vehicles.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

        # allow dealer to remove vehicles
        # get rowid from user
        rowid = request.form.get("row")
        # if it was provided then remove id from database and reload page
        if rowid and rowid != '...':
            apps = db.execute("DELETE FROM vehicles WHERE id=:rowid", rowid=rowid)
            flash("Vehicle successfully removed")
            return redirect("/vehicles")

        # add new vehicle to database if user submits information
        # list to hold form input
        add = []
        # get input (if any)
        add.append(request.form.get("make0"))
        add.append(request.form.get("model0"))
        add.append(request.form.get("reg0"))
        add.append(request.form.get("year0"))
        add.append(request.form.get("kms0"))
        add.append(request.form.get("price0"))

        # remove empty elements from list (i.e. if user did not fill out all fields)
        add = list(filter(None, add))

        # if user filled in correctly, then add vehicle to database
        if len(add) == 6:
            db.execute("""INSERT INTO vehicles (make, model, reg, year, kms, price, user)
                        VALUES (:make, :model, :reg, :year, :kms, :price, :user
                        )""", make=add[0], model=add[1], reg=add[2], year=add[3], kms=add[4], price=add[5], user=session["user_id"])
            # user feedback
            flash("Vehicle added!")
            # redirect user
            return redirect("/vehicles")
        else:
            # if user made no selections but clicked a submit button, just load page as if GET was used.
            return redirect("/vehicles")

    else:
        # function to carry out distinct queries on all columns in databse to prevent duplicates in
        # drop down menus and support search refinement (see helpers.py). In this case menus only contain user's cars.
        sel = select_menu(db, userid=session["user_id"])
        # query database for all vehicles that belong to the current user logged in
        result = db.execute("SELECT * FROM vehicles WHERE user=:user", user=session["user_id"])
        # show all user's vehicles in template
        return render_template("vehicles.html", make=sel[0], model=sel[1], reg=sel[2], year=sel[3], result=result)

    # if we get to here then the user must have submitted a form without all the required input
    return apology("Invalid input or all fields not present", 400)


@app.route("/applications", methods=["GET", "POST"])
@login_required
def applications():
    """Manage dealer finance applications"""

    if request.method == "POST":
        # allow dealer to remove applications
        # get rowid from user
        rowid = request.form.get("row")
        # remove rowid from the database
        apps = db.execute("DELETE FROM Applications WHERE rowid=:rowid", rowid=rowid)
        if apps > 0:
            flash("Application successfully removed")
            return redirect("/applications")
        else:
            flash("Unable to delete application")
            return redirect("/applications")

    else:
        # get id of the vehicles the user owns
        usrveh = db.execute("SELECT id FROM vehicles WHERE user=:user", user=session["user_id"])
        # get id from each key and put in list
        usrvehids = []
        for key in usrveh:
            usrvehids.append(key["id"])
        print(usrvehids)

        # query for all applications
        allapp = db.execute("SELECT * FROM Applications")
        # make a new list with only the applications that specify vehicles the user owns.
        result = [d for d in allapp for i in usrvehids if d.get('vehicleid') == i]
        # return the apps that correspond to the vehicles the user owns.
        return render_template("applications.html", result=result)

    return apology("Cant display applications", 400)

@app.route("/about")
def about():
    """Show about page"""

    return render_template("about.html")

    return apology("Cant display about page", 400)

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