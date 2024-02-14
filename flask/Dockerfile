# Utiliser l'image de base Debian 11
FROM debian:11

# Mise à jour
RUN apt-get update && apt-get upgrade -y

# Installer pkg-config
RUN apt-get install -y pkg-config

# Installation des paquets
RUN apt-get install -y python-dev python3-pip default-libmysqlclient-dev

# Mettre à jour pip
RUN pip3 install --upgrade pip

# Installer les paquets Python via pip
RUN pip3 install flask flask-mysqldb mysql-connector-python flask_bcrypt

# Créer le dossier /srv/templates
RUN mkdir -p /srv
RUN mkdir -p /srv/templates

# Copier les fichiers HTML dans /srv/templates/
COPY html/accueil.html /srv/templates/
COPY html/newuser.html /srv/templates/

# Copier le fichier app1.py dans /srv/
COPY app.py /srv/

CMD ["python3", "/srv/app.py"]