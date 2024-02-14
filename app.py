from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__, template_folder='/srv/templates')
app.secret_key = 'your_secret_key'  # Clé secrète pour les messages flash

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'mysql'  # Nom du service Docker MySQL
app.config['MYSQL_USER'] = 'root'   # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'password'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'users'    # Nom de la base de données MySQL

# Initialize MySQL
mysql = MySQL(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Regex pour la validation de l'identifiant
ID_REGEX = re.compile(r'^[a-z0-9]{6,10}$')

# Regex pour la validation du mot de passe
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[%#{}@])[a-zA-Z\d#%{}@]{6,15}$')

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

        # Validation de l'identifiant et du mot de passe
        if not ID_REGEX.match(identifiant):
            flash('Identifiant invalide', 'error')
            return render_template('newuser.html')
        if not PASSWORD_REGEX.match(password):
            flash('Mot de passe invalide', 'error')
            return render_template('newuser.html')

        # Vérifier si l'identifiant ou l'email est déjà utilisé
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE identifiant = %s OR email = %s", (identifiant, email))
        user = cur.fetchone()

        if user:
            flash('Identifiant ou email déjà utilisé', 'error')
            return render_template('newuser.html')

        # Hasher le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insérer le nouvel utilisateur dans la base de données
        cur.execute("INSERT INTO utilisateurs (identifiant, email, password_hash) VALUES (%s, %s, %s)", (identifiant, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Inscription réussie', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

