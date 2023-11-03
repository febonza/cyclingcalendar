from flask import Blueprint, render_template, request, flash, redirect, session
from . import db
import csv
import datetime
import os
from .helpers import login_required
from .auth import is_user_admin

views = Blueprint('views', __name__)

UPLOAD_FOLDER = './website/static/race_images/'

def get_races(race_category, race_month, *args, **kwargs):
    """
        This is the function that will retrieve the races from the database so it can be displayed in the front-end
        It will first understand the filters and format a query based on that, then execute
    """

    # Getting user_id from kwargs in case it's called from my_races
    # User_ID Filter
    user_id = kwargs.get("user_id")
    print(f"user_id = {user_id}")
    if user_id:
        user_id_filter = f"AND id IN (SELECT race_id FROM user_races WHERE user_id = {user_id})"
    else:
        user_id_filter = "AND 1=1"

    # Race Category Filter
    if race_category == "all":
        category_filter = "AND 1=1"
    else:
        category_filter = f"AND category = '{race_category}'"

    # Race Month Filter
    if race_month == '0':
        month_filter = "AND 1=1"
    else:
        month_filter = f"AND strftime('%m', race_date) = '{race_month}'"
    
    # Formatting query
    query = f"SELECT * FROM amateur_races WHERE 1=1 {category_filter} {month_filter} {user_id_filter} AND is_approved is true ORDER BY race_date DESC;"
    # print(query)

    # Running query in the db
    try:
        races = db.execute(query)
    except:
        flash("Could not return races from the database", category="error")
    else:
        return races


@views.route('/', methods=["GET", "POST"])
def home():
    race_category = "all"
    races_from_user_list = []
    is_admin = 0

    if session:
        if is_user_admin():
            is_admin = 1
    
    # List all races if the user is not using the filters
    if request.method == 'GET':
        all_races = db.execute("SELECT * FROM amateur_races WHERE is_approved is true ORDER BY race_date DESC;")
        if session:
            races_from_user = db.execute("SELECT race_id FROM user_races WHERE user_id = ?", session["user_id"])
            races_from_user_list = []
            for _ in races_from_user:
                races_from_user_list.append(_['race_id'])
        return render_template("home.html", races=all_races, races_from_user=races_from_user_list, is_admin=is_admin)
    else:
        race_category = request.form.get("filterCategory")
        race_month = request.form.get("filterMonth")
        return render_template("home.html", races=get_races(race_category, race_month))


@views.route('/register_race', methods=["GET", "POST"])
def register_race():
    if request.method == "GET":
        flash("All races must be approved by the admin to show up", category="warning")
        return render_template("register_race.html")
    else:
        race_name = request.form.get("registerRaceName")
        race_organizer = request.form.get("registerRaceOrganizer")
        race_local = request.form.get("registerRaceLocal")
        race_date = request.form.get("registerRaceDate")
        race_website = request.form.get("registerRaceWebsite")
        race_category = (request.form.get("registerCategory"))

        if not race_name:
            flash("Please enter a race name", category="error")
        elif not race_organizer:
            flash("Please enter the name of the organizer", category="error")
        elif not race_local:
            flash("Please enter the local of the race", category="error")
        elif not race_date:
            flash("Please enter a date", category="error")
        elif not race_website:
            flash("Please type a race name", category="error")
        elif not race_category:
            flash("Please select a category (MTB/Road Cycling)", category="error")
        elif 'registerRaceImage' not in request.files:
            flash("Please enter a race logo/image", category="error")
        else:
            if not race_website.startswith("http"):
                race_website = "http://" + race_website
            if race_category == "mtb":
                race_category = "Mountain Bike"
            elif race_category == "road":
                race_category = "Road Cycling"

            race_check = db.execute("SELECT race_name FROM amateur_races WHERE race_name = ?", race_name)
            if race_check:
                flash("Race already registered.", category="error")
                return render_template("register_race.html") 
            
            # Save image
            race_image = request.files["registerRaceImage"]
            path = os.path.join(UPLOAD_FOLDER, race_image.filename)
            race_image.save(path)

            # Transforming image name to unique name
            race_id = db.execute("select seq from sqlite_sequence WHERE name = 'amateur_races'")
            race_id = race_id[0]['seq'] + 1
            race_id = str(race_id) + "_" + race_image.filename
            
            try: 
                db.execute("INSERT INTO amateur_races (race_name,\
                                                    organizer,\
                                                    race_local,\
                                                    race_date,\
                                                    website,\
                                                    category,\
                                                    picture_race,\
                                                    is_approved\
                                                    ) VALUES(?, ?, ?, ?, ?, ?, ?, false)", race_name, race_organizer, race_local, race_date, race_website, race_category, race_image.filename)
            except:
                flash("Could not register race due a database error", category="error")
            else:
                flash("Race successfully registered", category="success")

        return render_template("register_race.html") 
    

@views.route('/add_my_races', methods=["POST"])
def add_my_races():
    race_id = request.form.get("raceId")
    print(race_id)
    user_registered_in_race = db.execute("SELECT 1 FROM user_races WHERE user_id = ? AND race_id = ?", session["user_id"], race_id)
    if not user_registered_in_race:
        db.execute("INSERT INTO user_races (user_id, race_id, date_added) VALUES (?, ?, ?)", session["user_id"], race_id, datetime.datetime.now())
        flash("Race added to your races", category="success")
    else:
        flash("Race alredy registered", category="warning")
    return redirect("/")


@views.route('/my_races', methods=["GET", "POST"])
@login_required
def my_races():
    race_category = "all"
    # List all races if the user is not using the filters
    if request.method == 'GET':
        all_races = db.execute("SELECT ar.* from amateur_races ar JOIN user_races ur ON ar.id = ur.race_id WHERE ur.user_id = ? ORDER BY ar.race_date DESC", session["user_id"])
        return render_template("my_races.html", races=all_races)
    else:
        race_category = request.form.get("filterCategory")
        race_month = request.form.get("filterMonth")
        return render_template("my_races.html", races=get_races(race_category, race_month, user_id = session["user_id"]))


@views.route('/remove_my_races', methods=["POST"])
def remove_my_races():
    race_id = request.form.get("raceId")
    
    db.execute("DELETE FROM user_races WHERE user_id = ? AND race_id = ?", session["user_id"], race_id)
    
    flash("Race removed from your races", category="success")
    if request.form.get("removingFromAllRaces"):
        return redirect("/")    
    else:
        return redirect("/my_races")


@views.route('/delete_race', methods=["POST"])
@login_required
def delete_race():
    race_id = request.form.get("raceId")
    
    # Check if the user is an admin by calling the is_user_admin function
    if is_user_admin():
        db.execute("DELETE FROM amateur_races WHERE id = ?", race_id)
        flash("Race deleted", category="warning")
    
    if request.form.get("removingFromAllRaces"):
        return redirect("/")    
    else:
        return redirect("/my_races")
    

@views.route('/pending_races', methods=["GET", "POST"])
@login_required
def pending_races():
    pending_races = db.execute("SELECT * FROM amateur_races WHERE is_approved is false and is_rejected is false")
    return render_template("pending_races.html", races=pending_races)


@views.route('/approve_race', methods=["POST"])
@login_required
def approve_race():
    race_id = request.form.get("raceId")
    print(race_id)
    db.execute("UPDATE amateur_races SET is_approved = true WHERE id = ?", race_id)
    flash("Race approved", category="success")
    return redirect("/pending_races")

@views.route('/reject_race', methods=["POST"])
@login_required
def reject_race():
    race_id = request.form.get("raceId")
    print(race_id)
    db.execute("UPDATE amateur_races SET is_rejected = true WHERE id = ?", race_id)
    flash("Race rejected", category="warning")
    return redirect("/pending_races")
