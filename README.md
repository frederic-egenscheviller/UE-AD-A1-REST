# UE-AD-A1-REST 

Projet universitaire visant à la découverte des API Rests sous forme de microservices.<br>
L'ensemble de ces microservices pourrait être assimilable à un système pouvant fonctionner dans un cinéma pour la réservation de places.<br>
Le TP réalisé est le TP Rouge (implémentation de deux routes qui font appel à OMBDAPI).<br>

L'API externe intérogée est accessible à l'url suivante : http://www.omdbapi.com/

Afin de tester l'API, un fichier Json généré pour le logiciel Insomnia contenant quelques requêtes intéressantes est disponible à la racine du projet.<br>
Pour télécharger Insomnia : https://insomnia.rest/download

## Démarrage 🚀

Pour lancer le projet, il est nécessaire d'avoir Docker d'installé sur sa machine.<br>
Il suffit de se placer dans le dossier principal du projet et lancer la commande suivante :<br>

```bash
docker-compose up
```

## Demandes ✍️

4 microservices :
- user REST
- booking REST
- movie REST
- showtime REST

Les microservices sont tous des API Rests et doivent communiquer entre eux selon un certain schéma. User peut faire appel à Movie et Booking. Booking peut appeler Showtime. Le seul point d'entrée de l'application est l'API User.<br>

Le microservice user est utilisé pour la gestion des utilisateurs. Le microservice movie contient les films et les informations à propos d'eux. Le microservice showtime contient les réservations effectuées par les utilisateurs avec leur nom, la date et les films concernés. Le microservice booking permet d'effectuer une réservation, notamment en vérifiant que le film est bien disponible à l'affiche pour le jour demandé.

Chaque microservice contient un CRUD et certains des routes supplémentaires.

## Membres du projet 🧑‍💻

EGENSCHEVILLER Frédéric</br>
LABORDE Baptiste
