PINTO RIBEIRO Clément, RADOUANE Ismaël

Lien du dépôt : https://github.com/ismardn/pychatbot-pinto_ribeiro-radouane-a.git

Le dossier contient :
- Un fichier README.txt (vous êtes en train de le lire)
- Deux répertoires "speeches" et "cleaned", contenant respectivement les discours des présidents, et ces discours sans caractères spéciaux
- Un fichier "presidents.txt", contenant (ou non) les prénoms associés aux noms des présidents
- Plusieurs fichiers Python :
     ~ "main.py", chargé de l'interaction entre l'ensemble des programmes du projet avec l'utilisateur
     ~ "traitement_fichiers.py", s'occupant du traitement des fichiers
     ~ "calcul_tf_idf.py", s'occupant du calcul du TF et de l'IDF des mots, et du calcul de la matrice TF-IDF du corpus
     ~ "fonctionnalites.py", chargé de réaliser les fonctionnalités proposées dans les consignes
     ~ "generation_reponse.py", chargé de générer une réponse automatique

Notice d'utilisation :

Les fichiers nécessaires à la bonne exécution du programme sont :
- Le répertoire "speeches" contenant les discours des présidents
- Les fichiers Python "main.py", "traitement_fichiers.py", "calcul_tf_idf.py", "fonctionnalites.py" et "generation_reponse.py"

Pour lancer le programme, exécutez le fichier Python "main.py" (dans PyCharm, de préférence*), puis suivez les instructions.
Toutes les fonctionnalités demandées sont accessibles.

Si vous souhaitez ajouter un fichier contenant un discours d'un président, veuillez ajouter un fichier de nom "Nomination_[Nom du Président][Numéro du fichier**].txt" (sans les crochets), dans le dossier "speeches". L'exécution du fichier "main.py" se chargera du traitement du fichier.

*L'affichage de la matrice TF-IDF (Fonctionnalité n°10) se fait correctement dans les consoles/terminaux sur lesquels on peut se déplacer horizontalement (et qui ne dépendent donc pas de la largeur de la fenêtre). L'affichage fonctionne très bien avec la console de PyCharm.

**L'ajout du numéro du fichier contenant le discours d'un certain président peux être fait uniquement dans le cas où un même président possède plusieurs fichiers contenant ses discours, afin de bien distinguer plusieurs discours différents provenant d'un même président.
