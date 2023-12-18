"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient toutes les fonctions chargées de réaliser les fonctionnalités proposées dans les consignes
(récupérer les noms des présidents, les mots les plus présents dans le corpus, ceux énoncés par tous les présidents...)
"""


import calcul_tf_idf


def retirer_caracteres_nom_fichier(nom_fichier):
    """
    Cette fonction retire les caractères indésirables du nom de fichier.

    :param nom_fichier: Le nom complet du fichier.
    :return: Le nom du président extrait du nom de fichier.
    """

    # Extraction du nom du président en éliminant les premiers caractères ("Nomination_") et l'extension
    nom_president_temp = nom_fichier[len("Nomination_"):len(nom_fichier) - len(".txt")]

    # Initialisation d'une nouvelle chaîne pour stocker le nom du président
    nom_president = ""

    # Boucle pour sélectionner uniquement les caractères non numériques
    for caractere in nom_president_temp:
        if caractere not in "0123456789":
            nom_president += caractere

    return nom_president


def recup_noms_presidents(noms_fichiers):
    """
    Cette fonction récupère les noms des présidents à partir des noms de fichiers.

    :param noms_fichiers: Une liste de noms de fichiers.
    :return: Une liste de noms de présidents sans doublons.
    """

    noms_presidents_temp = []

    # Application de la fonction retirer_caracteres_nom_fichier() sur chaque nom de fichier
    for nom_fichier in noms_fichiers:
        nom_president = retirer_caracteres_nom_fichier(nom_fichier)
        noms_presidents_temp.append(nom_president)

    noms_presidents = []  # Suppression des doublons

    # Ajout des noms de présidents à la liste sans doublons
    for nom_president in noms_presidents_temp:
        if nom_president not in noms_presidents:
            noms_presidents.append(nom_president)

    return noms_presidents


def tf_idf_nul(liste_mots, noms_fichiers, matrice):
    """
    Cette fonction renvoie les mots avec un score TF-IDF nul dans le corpus.

    :param liste_mots: Une liste de tous les mots du corpus.
    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param matrice: La matrice TF-IDF du corpus.
    :return: Une liste de mots avec un score TF-IDF nul.
    """

    moyenne_tf_idf_mots = []

    # Calcul de la moyenne des TF-IDF pour chaque mot en fonction des différents fichiers
    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    liste_valeurs_min = []

    # Ajout des mots avec un score TF-IDF nul à la liste
    for indice_valeur_min in range(len(moyenne_tf_idf_mots)):
        if moyenne_tf_idf_mots[indice_valeur_min] == 0:
            liste_valeurs_min.append(liste_mots[indice_valeur_min])

    return liste_valeurs_min


def tf_idf_max(liste_mots, noms_fichiers, matrice):
    """
    Cette fonction renvoie les mots avec le score TF-IDF le plus élevé dans le corpus.

    :param liste_mots: Une liste de tous les mots du corpus.
    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param matrice: La matrice TF-IDF du corpus.
    :return: Une liste de mots avec le score TF-IDF le plus élevé.
    """

    moyenne_tf_idf_mots = []

    # Calcul de la moyenne des TF-IDF pour chaque mot en fonction des différents fichiers
    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    valeur_max = -1

    # Recherche de la valeur maximale dans la liste des moyennes TF-IDF
    for valeur in moyenne_tf_idf_mots:
        if valeur > valeur_max:
            valeur_max = valeur

    liste_mot_max = []

    # Ajout des mots avec le score TF-IDF le plus élevé à la liste
    for indice_valeur in range(len(moyenne_tf_idf_mots)):
        if moyenne_tf_idf_mots[indice_valeur] == valeur_max:
            liste_mot_max.append(liste_mots[indice_valeur])

    return liste_mot_max


def mot_max_president(liste_mots, noms_fichiers, matrice, nom_president, nom_repertoire):
    """
    Cette fonction renvoie les mots les plus fréquemment utilisés par un président dans le corpus.

    :param liste_mots: Une liste de tous les mots du corpus.
    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param matrice: La matrice TF-IDF du corpus.
    :param nom_president: Le nom du président dont on souhaite extraire les mots les plus fréquemment utilisés.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers du corpus.
    :return: Une liste de mots les plus fréquemment utilisés par le président donné.
    """

    # Récupération des mots avec un score TF-IDF nul
    liste_mots_non_important = tf_idf_nul(liste_mots, noms_fichiers, matrice)

    contenu_fichiers = ""

    # Concaténation du contenu de tous les fichiers associés au président
    for nom_fichier in noms_fichiers:
        if nom_president in nom_fichier:
            with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
                contenu_fichiers = fichier.read() + " "

    # Calcul du TF-IDF pour le contenu associé au président
    tf_contenu_fichiers = calcul_tf_idf.calcul_tf(contenu_fichiers)

    valeur_max = -1

    # Recherche de la valeur maximale dans les scores TF-IDF
    for mot in tf_contenu_fichiers:
        valeur = tf_contenu_fichiers[mot]
        if valeur > valeur_max and mot not in liste_mots_non_important:
            valeur_max = valeur

    liste_mot_max = []

    # Ajout des mots avec le score TF-IDF le plus élevé à la liste
    for mot in tf_contenu_fichiers:
        if tf_contenu_fichiers[mot] == valeur_max:
            liste_mot_max.append(mot)

    return liste_mot_max


def mot_enonce_president(noms_fichiers, nom_repertoire, mot_recherche):
    """
    Cette fonction renvoie les présidents qui ont énoncé un mot spécifique dans le corpus.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers du corpus.
    :param mot_recherche: Le mot dont on souhaite trouver les présidents qui l'ont énoncé.
    :return: Une liste de tous les présidents et une liste des présidents qui ont énoncé le mot spécifique.
    """

    dict_pres_mot = {}

    # Parcours de tous les fichiers pour compter le nombre d'occurrences du mot spécifique par président
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichier_split = fichier.read().split()

            nom_president = retirer_caracteres_nom_fichier(nom_fichier)

            for mot in contenu_fichier_split:
                if mot == mot_recherche:
                    if nom_president in dict_pres_mot:
                        dict_pres_mot[nom_president] += 1
                    else:
                        dict_pres_mot[nom_president] = 1

    compteur_max = 1
    liste_pres_max = []

    # Recherche des présidents qui ont énoncé le mot le plus fréquemment
    for nom_president in dict_pres_mot:
        if dict_pres_mot[nom_president] >= compteur_max:
            if dict_pres_mot[nom_president] > compteur_max:
                liste_pres_max = []
                compteur_max = dict_pres_mot[nom_president]
            liste_pres_max.append(nom_president)

    return [nom_president for nom_president in dict_pres_mot], liste_pres_max


def premier_president_mot(noms_fichiers, nom_repertoire, mot_recherche):
    """
    Cette fonction renvoie le premier président qui a énoncé un mot spécifique dans le corpus.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers du corpus.
    :param mot_recherche: Le mot dont on souhaite trouver le premier président qui l'a énoncé.
    :return: Le nom du premier président qui a énoncé le mot spécifique.
    """

    dict_pres_mot = {}

    # Parcours de tous les fichiers pour enregistrer l'indice du premier mot spécifique énoncé par président
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichier_split = fichier.read().split()

            nom_president = retirer_caracteres_nom_fichier(nom_fichier)

            for indice_mot in range(len(contenu_fichier_split)):
                if contenu_fichier_split[indice_mot] == mot_recherche:
                    if nom_president in dict_pres_mot:
                        # Si le mot spécifique a déjà été énoncé par ce président, on conserve l'indice le plus petit
                        if dict_pres_mot[nom_president] > indice_mot:
                            dict_pres_mot[nom_president] = indice_mot
                    else:
                        # Si c'est la première occurrence du mot pour ce président, on l'enregistre
                        dict_pres_mot[nom_president] = indice_mot

    if dict_pres_mot != {}:
        premier_pres = list(dict_pres_mot.keys())[0]
        liste_pres = [dict_pres_mot[premier_pres], premier_pres]

        # Recherche du premier président qui a énoncé le mot spécifique
        for nom_president in dict_pres_mot:
            if dict_pres_mot[nom_president] < liste_pres[0]:
                liste_pres = [dict_pres_mot[nom_president], nom_president]

        return liste_pres[1]


def mots_tous_presidents(liste_mots, noms_fichiers, matrice, nom_repertoire):
    """
    Cette fonction renvoie les mots évoqués par tous les présidents au moins une fois dans le corpus.

    :param liste_mots: Liste des mots du corpus.
    :param noms_fichiers: Liste des noms de fichiers dans le corpus.
    :param matrice: Matrice TF-IDF du corpus.
    :param nom_repertoire: Répertoire où se trouvent les fichiers du corpus.
    :return: Liste des mots évoqués par tous les présidents au moins une fois.
    """

    # Obtient les mots avec un score TF-IDF nul
    liste_mots_non_important = tf_idf_nul(liste_mots, noms_fichiers, matrice)

    # Liste pour stocker le contenu des fichiers séparé en mots
    liste_contenu_fichier_split = []

    # Parcours de tous les fichiers pour extraire le contenu en mots
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_contenu_fichier_split.append(fichier.read().split())

    # Liste pour stocker les mots évoqués par tous les présidents au moins une fois
    liste_mots_tous_president = []

    # Parcours de la liste des mots
    for mot in liste_mots:
        # Vérifie si le mot est présent dans tous les fichiers
        mot_in_fichiers = [mot in liste_contenu_fichier_split[indice_fichier]
                           for indice_fichier in range(len(noms_fichiers))]

        # Dictionnaire pour stocker les présidents et leurs fichiers associés
        dict_pres = {}

        # Parcours des noms des présidents
        for nom_president in recup_noms_presidents(noms_fichiers):
            dict_pres[nom_president] = [[nom_fichier for nom_fichier in noms_fichiers if nom_president in nom_fichier],
                                        False]
            # Vérifie si le président a évoqué le mot dans au moins un fichier
            for indice_fichier in range(len(noms_fichiers)):
                if nom_president in noms_fichiers[indice_fichier] and mot_in_fichiers[indice_fichier]:
                    dict_pres[nom_president][1] = True

        # Vérifie si le mot est évoqué par tous les présidents au moins une fois
        tous_pres = True
        for nom_president in dict_pres:
            if not dict_pres[nom_president][1]:
                tous_pres = False

        # Ajoute le mot à la liste s'il est évoqué par tous les présidents au moins une fois
        if tous_pres and mot not in liste_mots_non_important:
            liste_mots_tous_president.append(mot)

    return liste_mots_tous_president
