import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json', encoding='utf-8') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json', encoding='utf-8') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def check_booking_conditions(club, competition, placesRequired):
    # Vérifier que le club a assez de points
    if placesRequired > 12 or placesRequired <= 0:
        print(placesRequired)
        flash("Booking number should be between 1 and 12!")
    # Vérifier qu'il reste assez de places pour la compétition
    elif not int(competition['numberOfPlaces']) - placesRequired >= 0:
        flash('Not enough places!')
    elif not placesRequired <= int(club["points"]):
        flash('Not enough points!')
    else:
        return True
    return False

app = Flask(__name__)
app.secret_key = 'something_special'
competitions = loadCompetitions()
clubs = loadClubs()

"""def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)

    competitions = loadCompetitions()
    clubs = loadClubs()

    return app"""


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        current_date = datetime.now()
        return render_template('welcome.html', club=club,
                               competitions=competitions, current_date=str(current_date))
    except IndexError:
        message = "Sorry, that email was not found."
        return render_template('index.html', message=message)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = \
    [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        current_date = datetime.now()
        return render_template('welcome.html', club=club,
                               competitions=competitions, current_date=str(current_date))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    # Date actuelle
    current_date = str(datetime.now())
    try:
        # Chercher les données de la compétition sélectionnée
        competition = \
        [c for c in competitions if c['name'] == request.form['competition']][
            0]
        # Chercher les données du club de la secrétaire identifiée
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        # Date de la compéition choisie
        if competition['date'] < str(current_date):
            flash("Can't book a past competition!")
            return render_template('welcome.html', club=club,
                                   competitions=competitions,
                                   current_date=current_date)
    except IndexError:
        print("-------- Index Error --------")
        print("request.form['competition'] =", request.form['competition'])
        print("request.form['club'] = ", request.form['club'])

    # Récupérer le nombre de places sélectionné pour la réservation
    placesRequired = int(request.form['places'])

    # Vérifier les conditions de réservation
    if not check_booking_conditions(
        club,
        competition,
        placesRequired
    ):
        return render_template('welcome.html', club=club,
                           competitions=competitions,current_date=current_date)
    # Maj du nombre de places disponibles pour la compétition
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces']) - placesRequired
    # Maj du nombre de points pour le club
    club['points'] = int(club["points"]) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions,current_date=current_date)

# TODO: Add route for points display
@app.route('/points-display')
def show_club_points():
    return render_template('clubs.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))




"""app = create_app({"TESTING": False})

if __name__ == "__main__":
    app.run()"""
