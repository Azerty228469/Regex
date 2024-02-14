FROM mysql:8

# Copie le fichier de configuration personnalisé
COPY mysql/my.cnf /etc/mysql/conf.d/my.cnf

# Définir les utilisateurs et les privilèges MySQL
ENV MYSQL_ROOT_PASSWORD=root

# Copier le script SQL d'initialisation dans le conteneur
COPY mysql/init.sql /docker-entrypoint-initdb.d/
RUN chown 1000:1000 /var/lib/mysql

# Expose le port
EXPOSE 3306

CMD ["mysqld"]