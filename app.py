from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>SAE/TP Regex</h1><br> Aller au <a href="/user/">formulaire de test</a>'

@app.route('/user/', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        user = request.form.get('user')

        # Regex
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', user):
            message = 'Règles respectées, utilisateur valide.'
        else:
            message = 'Pour ajouter un utilisateur, suivez ces règles :<br> - 6 caractères minimum<br> - Au moins 1 minuscule<br> - Au moins 1 majuscule<br> - Au moins 1 chiffre'

        return render_template('user.html', message=message)

    return render_template('user.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
