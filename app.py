from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clé secrète pour les messages flash

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'regex_mysql_1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sae61db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Fonction pour valider le nom d'utilisateur
def validate_username(username):
    messages = []
    regex = r'^[a-zA-Z0-9]{6,10}$'  # Contraintes sur le nom d'utilisateur
    if not re.match(regex, username):
        messages.append("Le nom d'utilisateur doit contenir entre 6 et 10 caractères alphanumériques ASCII.")
    else:
        messages.append("Rempli avec succès.")
    return messages

# Fonction pour valider le mot de passe
def validate_password(password):
    messages = []
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[%#@{}])[A-Za-z\d%@#{}]{6,15}$'  # Contraintes sur le mot de passe
    if not re.match(regex, password):
        messages.append("Le mot de passe doit contenir entre 6 et 15 caractères, avec au moins une minuscule, une majuscule, un chiffre et un caractère spécial parmi #%{}@.")
    else:
        messages.append("Rempli avec succès.")
    return messages

# Fonction pour valider l'adresse email
def validate_email(email):
    messages = []
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Contraintes sur l'adresse email
    if not re.match(regex, email):
        messages.append("Adresse email invalide.")
    else:
        messages.append("Rempli avec succès.")
    return messages

@app.route('/')
def index():
    return render_template('accueil.html')

@app.route('/newuser')
def new_user():
    return render_template('newuser.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        password = request.form['password']
        email = request.form['email']

        # Connexion à la base de données
        cur = mysql.connection.cursor()

        # Vérification si l'identifiant ou l'email est déjà utilisé
        cur.execute("SELECT * FROM utilisateur WHERE identifiant = %s OR email = %s", (identifiant, email))
        user = cur.fetchone()

        if user:
            flash('Identifiant ou email déjà utilisé', 'error')
            return redirect(url_for('new_user'))

        # Vérification des critères du nom d'utilisateur
        username_messages = validate_username(identifiant)

        # Vérification des critères du mot de passe
        password_messages = validate_password(password)

        # Vérification des critères de l'adresse email
        email_messages = validate_email(email)

        # Si toutes les conditions sont respectées
        if all(messages == ["Rempli avec succès."] for messages in [username_messages, password_messages, email_messages]):
            # Hashage du mot de passe
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Insertion du nouvel utilisateur dans la base de données
            cur.execute("INSERT INTO utilisateur (identifiant, email, password_hash) VALUES (%s, %s, %s)", (identifiant, email, hashed_password))
            mysql.connection.commit()
            cur.close()

            flash('Inscription réussie', 'success')
            return redirect(url_for('index'))

        # Si au moins une condition n'est pas respectée, réafficher la page avec les messages d'erreur
        else:
            for messages in [username_messages, password_messages, email_messages]:
                for message in messages:
                    flash(message, 'error')
            return redirect(url_for('new_user'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
