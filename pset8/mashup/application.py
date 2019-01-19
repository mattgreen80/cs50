import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)
# pretty print for flask function jsonify must be disabled or a 500 server error occurs.
# pretty print is applying sylistic elements to the code such as spacing, indentation etc.
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))


@app.route("/articles")
def articles():
    """Look up articles for geo"""

    # get the geo tag from url get request
    geo = request.args.get("geo")
    if not geo:
        raise RuntimeError("Missing argument")

    # lookup the geo tag using the lookup function from helpers.py
    feedcache = lookup(geo)

    # Return JSON object using flask jsonify function. This fails without disabling pretty print
    return jsonify(feedcache)


@app.route("/search")
def search():
    """Search for places that match query"""

    # get the search parameter argument from the url get request
    q = request.args.get("q")
    if not q:
        raise RuntimeError("Missing argument")

    # split the search string into a list where a comma occurs
    query = q.split(',')

    # empty list to contain query result
    result = []

    # if query is has more than one item in list then it has more than just post code or place name
    if len(query) > 1:
        for item in query:
            # extract state code but ignore country code
            if item.isupper() and item != " US":
                # extract state code
                code = item
                # remove the state code from the list once found
                query.remove(code)
                # remove any spaces and add wildcard to state code
                code = re.sub(" ", "", code) + '%'
                # query database for the code and name
                result = db.execute("SELECT * FROM places WHERE place_name LIKE :query AND admin_code1 LIKE :code", query=query[0] + '%', code=code)
        # if no code was found then second list item must be state name so query for place and state name
        if not result:
            # remove any whitespace from second string
            query[1] = re.sub(" ", "", query[1])
            result = db.execute("SELECT * FROM places WHERE place_name LIKE :query AND admin_name1 LIKE :query2", query=query[0] + '%', query2=query[1] + '%')

    # if only one item in the query list check if a place name
    elif query[0].istitle():
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :q", q=query[0] + '%')
    # as above but check if a postal code
    elif query[0].isdigit():
        result = db.execute("SELECT * FROM places WHERE postal_code LIKE :q", q=query[0] + '%')
    # query must consist of place name and state code in one string so slice off the state code
    # Can improve this by using the state code instead of discarding it
    else:
        query[0] = query[0][0:-3]
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :q", q=query[0] + '%')

    # return the above dict list as array of JSON objects
    return jsonify(result)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
