import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def select_menu(db , mak=None, mod=None, rg=None, userid=None):
    """Query the vehicles database and return the details to fill the drop down menus for the template."""
    # if argument make, model or reg is provided then refine the other select boxes. If no argument, then just return all.
    # if argument userid is provided then the function will only refine the user's own cars.
    # e.g. if you choose toyota as a make in the first select box, then when the page reloads, the model, reg and year select drop downs
    # will only show toyota models.
    if userid:
        if mak:
            make = db.execute("SELECT DISTINCT make FROM vehicles WHERE user=:user", user=userid)
            model = db.execute("SELECT DISTINCT model FROM vehicles WHERE make=:make AND user=:user", make=mak, user=userid)
            reg = db.execute("SELECT reg FROM vehicles WHERE make=:make AND user=:user", make=mak, user=userid)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE make=:make AND user=:user", make=mak, user=userid)
        elif mod:
            make = db.execute("SELECT DISTINCT make FROM vehicles WHERE user=:user", user=userid)
            model = db.execute("SELECT DISTINCT model FROM vehicles WHERE user=:user", user=userid)
            reg = db.execute("SELECT reg FROM vehicles WHERE model=:model AND user=:user", model=mod, user=userid)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE model=:model AND user=:user", model=mod, user=userid)
        elif rg:
            make = db.execute("SELECT DISTINCT make FROM vehicles WHERE user=:user", user=userid)
            model = db.execute("SELECT DISTINCT model FROM vehicles WHERE user=:user", user=userid)
            reg = db.execute("SELECT reg FROM vehicles WHERE user=:user", user=userid)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE reg=:reg AND user=:user", reg=rg, user=userid)
        else:
            make = db.execute("SELECT DISTINCT make FROM vehicles WHERE user=:user", user=userid)
            model = db.execute("SELECT DISTINCT model FROM vehicles WHERE user=:user", user=userid)
            reg = db.execute("SELECT DISTINCT reg FROM vehicles WHERE user=:user", user=userid)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE user=:user", user=userid)
    else:
        if mak:
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles WHERE make=:make", make=mak)
            reg = db.execute("SELECT reg FROM vehicles WHERE make=:make", make=mak)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE make=:make", make=mak)
        elif mod:
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles")
            reg = db.execute("SELECT reg FROM vehicles WHERE model=:model", model=mod)
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE model=:model", model=mod)
        elif rg:
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles")
            reg = db.execute("SELECT reg FROM vehicles")
            year = db.execute("SELECT DISTINCT year FROM vehicles WHERE reg=:reg", reg=rg)
        else:
            make = db.execute("SELECT DISTINCT make FROM vehicles")
            model = db.execute("SELECT DISTINCT model FROM vehicles")
            reg = db.execute("SELECT DISTINCT reg FROM vehicles")
            year = db.execute("SELECT DISTINCT year FROM vehicles")

    return make, model, reg, year