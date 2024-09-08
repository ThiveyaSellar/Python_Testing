import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


"""app = Flask(__name__)
app.secret_key = 'something_special'"""

def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            return render_template('welcome.html', club=club,
                                   competitions=competitions)
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
            return render_template('welcome.html', club=club,
                                   competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = \
        [c for c in competitions if c['name'] == request.form['competition']][
            0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        # Vérifier qu'il y a assez de places pour la compétition et assez de place
        if placesRequired <= int(club["points"]):
            if int(competition['numberOfPlaces']) - placesRequired >= 0:
                # Maj du nombre de places disponibles pour la compétition
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces']) - placesRequired
                # Maj du nombre de points pour le club
                club['points'] = int(club["points"]) - placesRequired
                flash('Great-booking complete!')
                return render_template('welcome.html', club=club,
                                       competitions=competitions)
            else:
                flash('Not enough places!')
                return render_template('welcome.html', club=club,
                                       competitions=competitions)
        else:
            flash('Not enough points!')
            return render_template('welcome.html', club=club,
                                   competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app({"TESTING": False})

if __name__ == "__main__":
    app.run()
