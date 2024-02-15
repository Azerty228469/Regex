from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clé secrète pour les messages flash

# Initialize MySQL
mysql = MySQL(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

def validate_username(username):
    messages = []
    
    # Regex pour vérifier les critères du nom d'utilisateur
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$'

    # Vérification de la longueur minimale du nom d'utilisateur
    if len(username) < 6:
        messages.append("Le nom d'utilisateur doit contenir au moins 6 caractères.")
    
    # Vérification de la présence de caractères minuscules dans le nom d'utilisateur
    if not any(char.islower() for char in username):
        messages.append("Le nom d'utilisateur doit contenir au moins une lettre minuscule.")
    
    # Vérification de la présence de caractères majuscules dans le nom d'utilisateur
    if not any(char.isupper() for char in username):
        messages.append("Le nom d'utilisateur doit contenir au moins une lettre majuscule.")
    
    # Vérification de la présence de chiffres dans le nom d'utilisateur
    if not any(char.isdigit() for char in username):
        messages.append("Le nom d'utilisateur doit contenir au moins un chiffre.")

    # Vérification du nom d'utilisateur avec la regex
    if not re.match(regex, username):
        messages.append("Le nom d'utilisateur ne respecte pas tous les critères.")
    else:
        messages.append("Rempli avec succès.")
    
    return messages

def validate_password(password):
    messages = []
    
    # Regex pour vérifier les critères du mot de passe
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#%{}])[A-Za-z\d@#%{}]{6,15}$'

    # Vérification de la longueur du mot de passe
    if len(password) < 6 or len(password) > 15:
        messages.append("Le mot de passe doit contenir entre 6 et 15 caractères.")
    
    # Vérification de la présence de chiffres dans le mot de passe
    if not any(char.isdigit() for char in password):
        messages.append("Le mot de passe doit contenir au moins un chiffre.")
    
    # Vérification de la présence de caractères minuscules dans le mot de passe
    if not any(char.islower() for char in password):
        messages.append("Le mot de passe doit contenir au moins une lettre minuscule.")
    
    # Vérification de la présence de caractères majuscules dans le mot de passe
    if not any(char.isupper() for char in password):
        messages.append("Le mot de passe doit contenir au moins une lettre majuscule.")
    
    # Vérification de la présence de caractères spéciaux dans le mot de passe
    if not any(char in '@#%{}' for char in password):
        messages.append("Le mot de passe doit contenir au moins un des caractères suivants : @#%{}")
    
    # Vérification du mot de passe avec la regex
    if not re.match(regex, password):
        messages.append("Le mot de passe ne respecte pas tous les critères.")
    else:
        messages.append("Rempli avec succès.")
    
    return messages

def validate_email(email):
    messages = []
    
    # Regex pour vérifier les critères de l'adresse e-mail
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Vérification de l'adresse e-mail avec la regex
    if not re.match(regex, email):
        messages.append("L'adresse e-mail n'est pas valide.")
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

        # Valider l'identifiant
        validation_messages = validate_username(identifiant)
        if validation_messages:
            flash(validation_messages[0], 'error')
            return redirect(url_for('new_user'))

        # Valider le mot de passe
        validation_messages = validate_password(password)
        if validation_messages:
            flash(validation_messages[0], 'error')
            return redirect(url_for('new_user'))

        # Valider l'adresse e-mail
        validation_messages = validate_email(email)
        if validation_messages:
            flash(validation_messages[0], 'error')
            return redirect(url_for('new_user'))

        # Vérifier si l'identifiant ou l'email est déjà utilisé
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE identifiant = %s OR email = %s", (identifiant, email))
        user = cur.fetchone()

        if user:
            flash('Identifiant ou email déjà utilisé', 'error')
            return redirect(url_for('new_user'))

        # Hasher le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insérer le nouvel utilisateur dans la base de données
        cur.execute("INSERT INTO utilisateurs (identifiant, email, password_hash) VALUES (%s, %s, %s)", (identifiant, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Utilisateur enregistré avec succès', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
