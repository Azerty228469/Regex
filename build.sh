#!/bin/bash

#Construction des images
docker-compose build

# Vérification
if [ $? -eq 0 ]; then
    echo -e "########################################################################################"
    echo -e "###### Construction de l'image du serveur flask et mysql réalisée avec succès ########"
    echo -e "#########################################################################################"
else
    echo -e "######################################################################################"
    echo -e "######## La construction de l'image du serveur flask et mysql a échoué #############"
    echo -e "#######################################################################################"
fi 

#Lancement des serveurs
docker-compose up -d

# Vérification
if [ $? -eq 0 ]; then
    echo -e "########################################################################################"
    echo -e "###### Lancement du serveur flask et mysql réalisée avec succès ########"
    echo -e "#########################################################################################"
else
    echo -e "######################################################################################"
    echo -e "######## Lancement du serveur flask et mysql a échoué #############"
    echo -e "#######################################################################################"
fi 