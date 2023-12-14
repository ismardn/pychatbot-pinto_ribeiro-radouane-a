"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient toutes les fonctions chargées de réaliser les fonctionnalités proposées dans les consignes
(récupérer les noms des présidents, les mots les plus présents dans le corpus, ceux énoncés par tous les présidents...)
"""


import calcul_tf_idf


# Fonction pour récupérer les noms des présidents
def retirer_caracteres_nom_fichier(nom_fichier):
    # Slice de la chaîne "nom_fichier" pour enlever les premiers caractères ("Nomination_") et l'extension
    nom_president_temp = nom_fichier[len("Nomination_"):len(nom_fichier) - len(".txt")]
    nom_president = ""
    for caractere in nom_president_temp:
        if caractere not in "0123456789":  # Si le caractère n'est pas un chiffre alors on l'ajoute a la nouvelle chaine
            nom_president += caractere

    return nom_president


# Fonction pour remettre au propre la liste du nom des présidents en retirant les numéros et les doublons
def recup_noms_presidents(noms_fichiers):
    noms_presidents_temp = []
    for nom_fichier in noms_fichiers:
        # On applique la fonction retirer_caracteres_nom_fichier() sur chaque nom de fichier
        nom_president = retirer_caracteres_nom_fichier(nom_fichier)
        noms_presidents_temp.append(nom_president)

    noms_presidents = []  # Suppression des doublons
    for nom_president in noms_presidents_temp:
        # Si le nom du président n'est pas déjà dans la liste alors on l'ajoute
        if nom_president not in noms_presidents:
            noms_presidents.append(nom_president)

    return noms_presidents


def tf_idf_nul(liste_mots, noms_fichiers, matrice):  # Fonction renvoyant les mots avec un score TF-IDF nul
    moyenne_tf_idf_mots = []

    # Calcul de la moyenne des TF-IDF pour chaque mot en fonction des différents fichiers
    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    liste_valeurs_min = []

    for indice_valeur_min in range(len(moyenne_tf_idf_mots)):
        # Si la moyenne du score TF-IDF d'un mot entre tous les fichiers est nulle, alors on l'ajoute à la liste,
        # puisque ce seront forcément les mots avec le TF-IDF le plus bas
        if moyenne_tf_idf_mots[indice_valeur_min] == 0:
            liste_valeurs_min.append(liste_mots[indice_valeur_min])

    return liste_valeurs_min


def tf_idf_max(liste_mots, noms_fichiers, matrice):  # Fonction renvoyant les mots avec le score TF-IDF le plus élevé.
    moyenne_tf_idf_mots = []

    # Calcul de la moyenne des TF-IDF (même principe que la fonction précédente)
    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    valeur_max = -1
    for valeur in moyenne_tf_idf_mots:
        if valeur > valeur_max:
            valeur_max = valeur

    liste_mot_max = []
    for indice_valeur in range(len(moyenne_tf_idf_mots)):
        if moyenne_tf_idf_mots[indice_valeur] == valeur_max:
            liste_mot_max.append(liste_mots[indice_valeur])

    return liste_mot_max


# Fonction renvoyant le mot le plus utilisé par un président
def mot_max_president(liste_mots, noms_fichiers, matrice, nom_president, nom_repertoire):
    liste_mots_non_important = tf_idf_nul(liste_mots, noms_fichiers, matrice)

    contenu_fichiers = ""

    for nom_fichier in noms_fichiers:
        if nom_president in nom_fichier:
            with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
                contenu_fichiers = fichier.read() + " "

    tf_contenu_fichiers = calcul_tf_idf.calcul_tf(contenu_fichiers)

    valeur_max = -1
    for mot in tf_contenu_fichiers:
        valeur = tf_contenu_fichiers[mot]
        if valeur > valeur_max and mot not in liste_mots_non_important:
            valeur_max = valeur

    liste_mot_max = []

    for mot in tf_contenu_fichiers:
        if tf_contenu_fichiers[mot] == valeur_max:
            liste_mot_max.append(mot)

    return liste_mot_max


# Fonction renvoyant le président ayant énonce le mot recherche le plus de fois
def mot_enonce_president(noms_fichiers, nom_repertoire, mot_recherche):
    dict_pres_mot = {}

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

    for nom_president in dict_pres_mot:
        if dict_pres_mot[nom_president] >= compteur_max:
            if dict_pres_mot[nom_president] > compteur_max:
                liste_pres_max = []
                compteur_max = dict_pres_mot[nom_president]
            liste_pres_max.append(nom_president)

    return [nom_president for nom_president in dict_pres_mot], liste_pres_max


# Fonction permettrant de trouver le premier président à avoir parler d'un mot ou d'un sujet
def premier_president_mot(noms_fichiers, nom_repertoire, mot_recherche):
    dict_pres_mot = {}

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichier_split = fichier.read().split()

            nom_president = retirer_caracteres_nom_fichier(nom_fichier)

            for indice_mot in range(len(contenu_fichier_split)):
                if contenu_fichier_split[indice_mot] == mot_recherche:
                    if nom_president in dict_pres_mot:
                        if dict_pres_mot[nom_president] < indice_mot:
                            dict_pres_mot[nom_president] = indice_mot
                    else:
                        dict_pres_mot[nom_president] = indice_mot

    if dict_pres_mot != {}:
        premier_pres = list(dict_pres_mot.keys())[0]
        liste_pres = [dict_pres_mot[premier_pres], premier_pres]

        for nom_president in dict_pres_mot:
            if dict_pres_mot[nom_president] < liste_pres[0]:
                liste_pres = [dict_pres_mot[nom_president], nom_president]

        return liste_pres[1]


# Fonction permettant de renvoyer les mots que tout les président on évoqué au moins une fois.
def mots_tous_presidents(liste_mots, noms_fichiers, matrice, nom_repertoire):
    liste_mots_non_important = tf_idf_nul(liste_mots, noms_fichiers, matrice)

    liste_contenu_fichier_split = []

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_contenu_fichier_split.append(fichier.read().split())

    liste_mots_tous_president = []

    for mot in liste_mots:
        mot_in_fichiers = [mot in liste_contenu_fichier_split[indice_fichier]
                           for indice_fichier in range(len(noms_fichiers))]

        dict_pres = {}
        for nom_president in recup_noms_presidents(noms_fichiers):
            dict_pres[nom_president] = [[nom_fichier for nom_fichier in noms_fichiers if nom_president in nom_fichier],
                                        False]
            for indice_fichier in range(len(noms_fichiers)):
                if nom_president in noms_fichiers[indice_fichier] and mot_in_fichiers[indice_fichier]:
                    dict_pres[nom_president][1] = True

        tous_pres = True

        for nom_president in dict_pres:
            if not dict_pres[nom_president][1]:
                tous_pres = False

        if tous_pres and mot not in liste_mots_non_important:
            liste_mots_tous_president.append(mot)

    return liste_mots_tous_president
