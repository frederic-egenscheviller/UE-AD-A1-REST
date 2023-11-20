# UE-AD-A1-REST 

Projet universitaire visant à la découverte des API Rests sous forme de microservices.<br>
Le TP réalisé est le TP Rouge (implémentation de deux routes qui font appel à OMBDAPI).<br>

L'API externe intérogée est accessible à l'url suivante : http://www.omdbapi.com/

## Démarrage 🚀

Pour lancer le projet, il est nécessaire d'avoir Docker d'installé sur sa machine.<br>
Il suffit de se placer dans le dossier principal du projet et lancer la commande suivante :<br>

```bash
docker-compose up
```

## Demandes ✍️

4 microservices :
- user
- booking
- movie
- showtime

Les microservices sont tous des API Rests et doivent communiquer entre eux selon un certain schéma. User peut faire appel à Movie et Booking. Booking peut appeler Showtime. Le seul point d'entrée de l'application est l'API User.

## Membres du projet 🧑‍💻

EGENSCHEVILLER Frédéric</br>
LABORDE Baptiste
