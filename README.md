# AvalamGameIntelligence
("intelligence"...)
This repo contains a project for a course, and will be explained in French.

Réalisé par Frédéric Druppel (18053)
# Prérequis 

Les codes python trouvés dans ce repo sont conçus pour fonctionner avec [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner), et plus spécifiquement "Avalam".
Ces codes nécéssitent également les librairies suivantes :
- sys
- cherrypy
- random
- math
- pickle
- socket
- json

# Installation et lancement
Afin de pouvoir faire fonctionner ce code, il suffit de cloner le repo dans un dossier, et éxécuter le document launcher.py avec python 3 depuis un terminal, avec comme argument optionnel le port de communication vers le serveur de jeu.
Exemple : 
```
AvalamGameIntelligence-master $ python3 launcher.py <port>
```

La commande ^C arrête l'exécution.
# Explication des documents python

### launcher&#46;py <port>
Ce document sert à lancer le programme. L'argument <port> optionnel permet de spécifier un port à utiliser par  "AvalamGameIntelligence", sinon le port 8008 sera utilisé.
Les variables "subPort" ,"name", "matricules" et "supervisorHost" peuvent être modifiés et ont cet effet :
- "subPort" : le port entrant de [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner) qui gère les inscriprions (3001 par défaut)
- "name" : modifie le nom affiché sur le serveur généré par [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner)
- "matricules" : modifie le(s) matricule(s) de(s) étudiant(s), 
- "supervisorHost" : modifie l'adresse à laquelle se connecter pour accéder à [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner)

### subscribe&#46;py
Ce document gère l'inscription auprès de [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner) en envoyant un fichier JSON via un protocol TCP.

### server&#46;py
Ce document s'occupe de recevoir les données de [AIGameRunner](https://github.com/ECAM-Brussels/AIGameRunner), de les interpréter, et de renvoyer un JSON contenant le cooup à faire, préalablement décidé par l'intelligence artificielle.
### serverRandom&#46;py
Ce document fait la même chose que server&#46;py, mais se contente d'un générateur de nombres aléatoire pour générer le coup à faire (par défaut ce document n'est pas utilisé).
### ai&#46;py
Ce document contient le "coeur" de l'intelligence artificielle, notamment les fonctions d'un algorithme de type [minimax avec ɑ-β-pruning](https://en.wikipedia.org/wiki/Alpha–beta_pruning) et perception de profondeur. La fonction heuristique est déclarée comme ceci :
```
def utility(_gamestate):
...
```

# Stratégie & fonctionnement
*un schéma bloc au format JPEG se trouve également dans ce repo*
La stratégie de jeu consiste à maximiser "notre" nombre de pions visibles (en haut des piles), tout en minimisant les pions visibles de l'adversaire.
Le fonctionnement de l'algorithme minimax ne sera pas expliqué ici, car [d'autres sites](https://en.wikipedia.org/wiki/Alpha–beta_pruning) l'expliquent mieux. Néanmoins le fonctionnement de certaines fonction peut être intéressant à détailler.
##### actions(_gamestate)
Cette fonction renvoie une liste de tout les coups possibles, en fonction de l'état du jeu. C'est elle qui, en quelque sorte, contient les règles du jeu. 
Elle parcoure toutes les piles sur le tableau, regarde si leur hauteur est inférieure à 5 et si il y a un ou plusieurs voisins sur les cases à coté, dont la hauteur ne dépasse pas (5 moins la hauteur de la pile actuelle).
Ensuite elle revoie une liste contenant les déplacement sous le format
```
[fromX, fromY, toX, toY]
```
##### gameIsOver(_gamestate)
Renvoie vrai si aucun mouvement n'est possible, en regardant si ce que renvoie actions(_gamestate) est vide. Si ce que renvoie actions(_gamestate) contient quelque chose, ça veut dire qu'il y a encore moyen de faire des coups, et que le jeu n'est pas terminé.

##### result(_gamestate, _action)
Renvoie un état de tableau généré à partir de l'état actuel "_gamestate", en suivant le déplacement spécifié par _action.

##### utility(_gamestate)
Revoie une valeur d'utilité calculée à partir de plusieurs éléments :
- Nombre de piles de couleur du jouer
- Nombre de piles de couleur de l'adversaire
- Nombre de piles totales
- Nombres de piles de couleur du jouer avec comme hauteur = 4
- Nombres de piles de couleur du jouer avec comme hauteur = 5

Une formule calcule ensuite une valeur en fonction de ces paramètres.
__Ceci est la stratégie de jeu de l'IA__

#### Un autre détail
Comme au début du jeu le nombre de possibilités est élevé, ça prendrait trop de temps de calculer un choix à 3 coups ou plus à l'avance. Donc, avant de lancer l'IA, server&#46;py calcule le nombre de coups avec <ia&#46;actions(gameState)>. Si le nombre d'actions possible, le paramère de profondeur de recherche de l'IA vaudra 2, sinon il est augmenté à 5.

# Améliorations
Afin de rendre l'IA plus performante, lusieurs éléments peuvent être améliorés :
- Choisir une profondeur de recherche selon une courbe plus lisse, plutôt que de passe de 2 à 5 en un coup.
- Optimiser la vitesse lors du calcul d'actions possibles
- Utiliser une IA basée sur un système neuronal, entrainé par un algorithme d'entrainement génétique. (Ceci prend du temps à améliorer, mais est pratiquement imbattable une fois entrainé correctement)
- Commencer à bosser sur ce projet plus tôt :)


# Sources

- [Artificial Intelligence: A Modern Approach (Third Edition) -- Stuart RUSSELL, Peter NORVIG, 2010 ](http://aima.cs.berkeley.edu), (surtout le chapitre 5)
- [Alpha-Beta pruning - Wikipedia](https://en.wikipedia.org/wiki/Alpha–beta_pruning)
- Cours de dévloppement informatique 2BA à L'ECAM Brussels Engineering School, donné par monsieur [Quentin LURKIN](https://www.linkedin.com/in/qlurkin/)
- Conseils de [Sébastien d'OREYE](https://www.linkedin.com/in/sébastien-d-oreye-716283a8/), chercheur au CERDECAM

Made with ❤️, lots of ☕️, and lack of 🛌
Publié sous CreativeCommons BY-NC-SA 4.0

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
