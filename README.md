# Moteur de recherche en Python V2

---

## Bienvenue sur le README de notre application.

### Explication du projet

Ce projet est un projet de fin de module de la matière de Programmation de spécialité Python. Il s'agit de créer un moteur de recherche en Python avec 3 versions différentes.
Vous pouvez changer de version en changeant de tag.

Ici, vous allez trouver la version 1 de notre projet. Cette version est une version qui permet de faire des recherches sur deux sites de vente en ligne, à savoir [Reddit](https://www.reddit.com/) et [Arxiv](https://export.arxiv.org/). Cette version permet de faire des recherches sur ces deux sites en passant un mot clé et un nombre de documents à retourner. Les documents retournés seront stockés dans une fichier apart. Ensuite, on va afficher les documents retournés dans le terminal ou bien dans l'interface graphique (Jupiter Notebook), il est conseillé d'utiliser l'interface graphique pour une meilleure expérience. Pour lancer le projet, vouillez suivre les étapes dans la section [Lancement du projet](#lancement-du-projet).

### Les membres de groupe

Ce travail a été fait par un groupe de 2 personnes :

- GHIZLAN Moqim [@moqim.ghizlan](https://gitlab.com/moqim.ghizlan)
- JOMAA Akrem [@akrem_jomaa](https://gitlab.com/akrem_jomaa.ghizlan)

### Note importante

Avant de lancer le projet, la moitié des documents retournés par le moteur de recherche sont récupérés à partir de Reddit, pour cela, il faut avoir un compte Reddit et créer une application pour pouvoir utiliser l'API de Reddit. Pour faire cela, nous vous invitons à suivre ce [tutoriel](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c) pour créer une application Reddit et récupérer le client_id, le client_secret et le user agent. Une fois que vous avez ces deux informations, vous pouvez les mettre dans le fichier `.env` dans la variable `REDDIT_CLIENT_ID`, `REDDIT_SECRET_ID` et `REDDIT_USER_AGENT` respectivement. Le fichier `.env` se trouve à la racine du projet.

En tout cas, si vous n'avez pas de compte Reddit, vous pouvez toujours lancer le projet, mais vous n'allez pas avoir tous les documents retournés par le moteur de recherche. Merci de respecter les consignes 😀. Rappel :

- Sans ces informations, le projet ne va pas fonctionner.
- Il faut bien respecter les noms des variables dans le fichier `.env` sinon le projet ne va pas fonctionner.

## Lancement du projet

### Prérequis

Pour lancer le projet, vous pouvez le lancer en deux manières différentes, mais il y aura toujours une étape commune qui est l'installation des dépendances. Pour cela, veuillez suivre les étapes suivantes :

Dnas un dossier de votre choix, veuillez lancer le terminal et exécuter les commandes suivantes :

- Cloner le projet en utilisant la commande suivante :

```
$ git clone https://github.com/akremjomaa/searchEngine.git
```

- Aller dans le dossier du projet :

```
$ cd searchEngine
```

- Créer un environnement virtuel, il existe plusieurs manières de le faire, mais nous allons utiliser la méthode la plus simple qui est la suivante :

```
$ python3 -m venv venv
```

- Activer l'environnement virtuel :
  Si vous êtes sur Windows :

```
$ venv\Scripts\activate.bat
```

Si vous êtes sur Linux ou Mac :

```
$ source venv/bin/activate
```

- Installer les dépendances :

```
$ pip install -r requirements.txt
```

### Lancer le projet en ligne de commande

Pour lancer et utiliser le projet en ligne de commande, veuillez suivre les étapes suivantes :

- dans le dossier du projet, exécuter la commande suivante :

```
$ python3 main.py
```

Le programme va vous demander de saisir un mot clé et un nombre de documents à retourner. Une fois que vous avez saisi ces deux informations, le programme va vous afficher les documents retournés dans le terminal.

### Lancer le projet en interface graphique

Pour lancer et utiliser le projet en interface graphique, veuillez suivre les étapes suivantes :

- dans le dossier du projet, exécuter la commande suivante :

```
$ jupyter lab
```

Une fois que vous avez exécuté cette commande, une page web va s'ouvrir dans votre navigateur par défaut. Dans cette page, vous allez trouver le fichier `CorpusNoteBook.ipynb`, veuillez l'ouvrir. Une fois que vous avez ouvert le fichier, vous allez trouver une icône en haut à gauche qui ressemble à un bouton `play`, veuillez cliquer dessus pour exécuter le code. Une fois que vous avez cliqué sur le bouton `play`, le programme va vous demander de saisir un mot clé et un nombre de documents à retourner. Une fois que vous avez saisi ces deux informations, le programme va vous afficher les documents retournés dans le terminal.

## Gestions des erreurs

Une fois que vous avez lancé le projet, il y a plusieurs erreurs qui peuvent se produire. Les erreurs sont écrites entre les balises `[ERRER]`. Nnous allons les lister ici et vous donner les solutions pour les résoudre.

### Erreurs liées à l'API de Reddit

#### Erreur 1

- `CODE-402 [ERROR] The subreddit you entered does not exist` : Indique que le subreddit n'existe pas.
- Solution : Veuillez vérifier que le subreddit existe e.

#### Erreur 2

- `CODE-403 | CODE-404 [ERROR] You are not allowed to access this subreddit` : Indique que vous n'avez pas les droits pour y accéder.
- Solution : Veuillez vérifier que vous avez bien les droits pour y accéder.

#### Erreur 3

- `CODE-500 [ERROR] An internal server error occured.` : Indique qu'il y a une erreur interne au niveau du serveur.
- Solution : Veuillez réessayer plus tard.

### Erreurs liées à l'API d'Arxiv

#### Erreur 1

- `CODE-400 [ERROR] Bad request` : Indique que la requête est mal formée.
- Solution : Veuillez vérifier que la requête est bien formée.

#### Erreur 2

- `CODE-404 [ERROR] Bad Entry` : Indique que l'entrée est mal formée.
- Solution : Veuillez vérifier que l'entrée est bien formée.

## Conclusion

Pour conclure, nous avons pu réaliser un moteur de recherche en Python qui permet de faire des recherches sur deux sites de documents en ligne, à savoir [Reddit](https://www.reddit.com/) et [Arxiv](https://export.arxiv.org/). Cette version permet de faire des recherches sur ces les deux sites et ensuite faire quelques statstique sur les documents retournés. Et enfin, il vous permet de faire des recherches sur toutes les documents retournés par le moteur de recherche. Nous allons ajouer une nouvelle fonctionnalité qui est l'interface graphique dans la version 3 de notre projet. Pour plus d'informations.
