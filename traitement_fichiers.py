"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient les fonctions s'occupant du traitement des fichiers (récupérer la liste des fichiers du corpus ainsi
que traiter le contenu de ces derniers)
"""


import os


# Création d'une liste comprenant tout les noms des fichers. txt présent dans le corpus
def liste_fichiers(repertoire, extension):
    noms_fichiers = []
    for nom_fichier in os.listdir(repertoire):  # Pour chaque fichier dans le répertoire
        if nom_fichier.endswith(extension):
            # Si le fichier est un fichier avec l'extension ".extension", alors on l'ajoute à la liste "noms_fichiers"
            noms_fichiers.append(nom_fichier)

    return noms_fichiers


# Transformation des textes des fichiers: mise en forme des textes en mettant tout en minuscule
def en_minuscule(chaine):
    nouvelle_chaine = ""

    for caractere in chaine:
        if ord("A") <= ord(caractere) <= ord('Z'):  # Si le code ASCII du caractère appartient à ceux des majuscules
            nouvelle_chaine += chr(ord(caractere) + ord("a") - ord("A"))  # On transforme le caractère en minuscule
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


# Application de la fonction précédente à tout les fichiers
def creer_fichiers_minuscule(noms_fichiers, nom_repertoire_discours, nom_repertoire_nettoye):
    for nom_fichier in noms_fichiers:
        # On ouvre tous les fichiers du programme avec l'encodage utf-8 pour bien conserver les accents, notamment ici,
        # mais également dans l'entièreté du code
        with open(nom_repertoire_discours + "/" + nom_fichier, "r", encoding="utf-8") as fichier_ancien, \
                open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier_nettoye:
            # Application de la fonction minuscule sur chaque fichier du dossier des discours
            fichier_nettoye.write(en_minuscule(fichier_ancien.read()))


# Remise en forme des textes en enlevant les caractères spéciaux ainsi que les numéros.
def suppression_caracteres_speciaux(chaine, caracteres=None):
    if caracteres is None:  # Si le paramètre "caracteres" n'est pas spécifié
        caracteres_speciaux = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                               ',', '-', "'", '.', '!', '?', '_', ':', '\n', '"', ';', '`']  # Caractères à supprimer
    else:
        caracteres_speciaux = caracteres

    nouvelle_chaine = ""

    for caractere in chaine:
        if caractere in caracteres_speciaux:
            nouvelle_chaine += " "  # Remplacement des caractères spéciaux par des espaces
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


# Nettoyer l'entièreté des fichiers contenus dans le répertoire des discours
def nettoyage_complet_fichiers(nom_repertoire_nettoye, noms_fichiers, nom_repertoire_discours):
    if not os.path.exists(nom_repertoire_nettoye):  # Création du répertoire pour fichiers nettoyés s'il n'existe pas
        os.mkdir(nom_repertoire_nettoye)

    creer_fichiers_minuscule(noms_fichiers, nom_repertoire_discours, nom_repertoire_nettoye)

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            ancien_contenu = fichier.read()  # On stocke dans un variable l'ensemble du contenu du fichier

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier:
            # Application de la fonction supprimant les caractères spéciaux sur chaque fichier du dossier nettoyé
            fichier.write(suppression_caracteres_speciaux(ancien_contenu))
