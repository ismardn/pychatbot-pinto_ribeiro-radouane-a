"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient toutes les fonctions s'occupant du calcul du TF et de l'IDF de chacun des mots du corpus, ainsi que
du calcul de la matrice TF-IDF du corpus.
"""


import math


def calcul_tf(chaine):  # Fonction pour calculer le TF d'une chaîne
    """
    Cette fonction calcule le Term Frequency (TF) d'une chaîne de texte.

    :param chaine: Chaîne de texte.
    :return: Dictionnaire associant à chaque mot sa valeur TF dans la chaîne.
    """
    liste_mots = chaine.split()

    dict_tf = {}

    for mot in liste_mots:  # Mise en place d'un dictionnaire associant à chaque mot sa valeur TF
        if mot not in dict_tf:
            dict_tf[mot] = 1  # Création d'une nouvelle clé si le mot n'existe pas
        else:
            dict_tf[mot] += 1  # Incrémentation de sa valeur, sinon

    return dict_tf


def calcul_tf_total(noms_fichiers, nom_repertoire):  # Application de la fonction "calcul_tf" à tout les fichiers
    """
    Applique la fonction "calcul_tf" à tous les fichiers du corpus.

    :param noms_fichiers: Liste des noms de fichiers dans le corpus.
    :param nom_repertoire: Répertoire où se trouvent les fichiers du corpus.
    :return: Liste des valeurs TF pour chaque fichier sous la forme de N dictionnaires (N = nombre de fichiers).
    """
    liste_tf = []

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_tf.append(calcul_tf(fichier.read()))

    return liste_tf


def calcul_idf_total(noms_fichiers, nom_repertoire):  # Fonction permettant de calculer le score IDF de chaque mot
    """
    Calcul du score IDF pour chaque mot dans le corpus.

    :param noms_fichiers: Liste des noms de fichiers dans le corpus.
    :param nom_repertoire: Répertoire où se trouvent les fichiers du corpus.
    :return: Dictionnaire associant à chaque mot son score IDF.
    """
    contenu_fichiers_liste = []
    contenu_fichiers = ""

    # Lecture des fichiers pour construire le corpus et la liste de mots
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichier = fichier.read()
            contenu_fichiers_liste.append(contenu_fichier.split())
            contenu_fichiers += contenu_fichier + " "

    chaine_split = contenu_fichiers.split()
    liste_mots = []

    # Construction de la liste de mots unique dans le corpus
    for mot in chaine_split:
        if mot not in liste_mots:
            liste_mots.append(mot)

    dict_idf = {}  # Initialisation du dictionnaire pour stocker les scores IDF

    # Calcul du score IDF pour chaque mot
    for mot in liste_mots:

        nombre_fichiers_mot = 0
        for indice_fichier in range(len(noms_fichiers)):
            if mot in contenu_fichiers_liste[indice_fichier]:
                nombre_fichiers_mot += 1

        dict_idf[mot] = math.log10(len(noms_fichiers) / nombre_fichiers_mot)  # Calcul de l'IDF

    return dict_idf


def creation_matrice_corpus(noms_fichiers, nom_repertoire, idf_total):
    """
    Crée une matrice de TF-IDF pour chaque mot dans le corpus.

    :param noms_fichiers: Liste des noms de fichiers dans le corpus.
    :param nom_repertoire: Répertoire où se trouvent les fichiers du corpus.
    :param idf_total: Dictionnaire associant à chaque mot son score IDF.
    :return: Tuple composé de la liste des mots et de la matrice de TF-IDF associée.
    """
    # Calcul des valeurs TF pour chaque fichier
    valeurs_tf_fichier = calcul_tf_total(noms_fichiers, nom_repertoire)

    # On récupère tous les mots du corpus
    liste_mots = [mot for mot in idf_total]

    contenu_fichiers_liste = []

    # Lecture des fichiers pour construire une liste de listes contenant les mots de chaque fichier
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichiers_liste.append(fichier.read().split())

    matrice = []

    # Construction de la matrice de TF-IDF pour chaque mot
    for mot in liste_mots:

        tfs_idf_mot = []

        for indice_fichier in range(len(noms_fichiers)):
            valeur_tf_fichier = valeurs_tf_fichier[indice_fichier]

            if mot in contenu_fichiers_liste[indice_fichier]:
                tfs_idf_mot.append(idf_total[mot] * valeur_tf_fichier[mot])  # Calcul du produit TF-IDF
            else:
                # Si le mot n'est pas dans le fichier, alors son TF est nul donc le produit le sera aussi
                tfs_idf_mot.append(0)

        matrice.append(tfs_idf_mot)

    return liste_mots, matrice
