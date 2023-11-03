from flask import Blueprint, render_template, flash, request, redirect, session
from . import db
from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint('auth', __name__)

def is_user_admin():
    """Returns True if the current user is an admin, False otherwise"""
    is_admin = db.execute("SELECT is_admin FROM users WHERE id = ?", session["user_id"])
    return is_admin[0]['is_admin'] == 1


@auth.route("/register_user", methods=["GET", "POST"])
def register_user():
    """Register user"""

    if request.method == "POST":
        print("POST")
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", category="error")
            return render_template("register_user.html")
        else:
            username = request.form.get("username")
            check_duplicate = db.execute("SELECT id FROM users where username = ?", username)
            if check_duplicate:
                flash("username already exists", category="error")
                return render_template("register_user.html")

        if not request.form.get("password"):
            flash("must provide password", category="error")
            return render_template("register_user.html")
        elif not request.form.get("confirmation"):
            flash("must provide password confirmation", category="error")
            return render_template("register_user.html")
        else:
            if not request.form.get("password") == request.form.get("confirmation"):
                flash("password does not match", category="error")
                return render_template("register_user.html")
            else:
                password = request.form.get("password")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password, method='pbkdf2:sha1', salt_length=8))
        return redirect("/")

    else:
        return render_template("register_user.html")
    

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("You must provide an username", category="error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("You must provide a password", category="error")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password", category="error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["is_admin"] = rows[0]["is_admin"]
        print(session)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")