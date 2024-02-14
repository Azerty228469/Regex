from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='/srv/templates')
app.secret_key = 'your_secret_key'  # Clé secrète pour les messages flash

# Initialize MySQL
mysql = MySQL(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

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
