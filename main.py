import os
import math


def liste_fichiers(repertoire, extension):

    noms_fichiers = []
    for nom_fichier in os.listdir(repertoire):
        if nom_fichier.endswith(extension):
            noms_fichiers.append(nom_fichier)

    return noms_fichiers


def recup_noms_presidents(nom_fichier_presidents, nom_repertoire_discours):
    noms_fichiers = liste_fichiers(nom_repertoire_discours, "txt")

    noms_presidents_temp = []
    for nom_fichier in noms_fichiers:
        # Slice de la chaîne "nom_fichier" pour enlever les premiers caractères ("Nomination_") et l'extension
        nom_president_temp = nom_fichier[len("Nomination_"):len(nom_fichier) - len(".txt")]
        nom_president = ""
        for caractere in nom_president_temp:
            if caractere not in "0123456789":
                nom_president += caractere
        noms_presidents_temp.append(nom_president)

    noms_presidents = []  # Suppression des doublons
    for nom_president in noms_presidents_temp:
        if nom_president not in noms_presidents:
            noms_presidents.append(nom_president)

    with open(nom_fichier_presidents, "r") as fichier:
        contenu_fichier = ""
        for ligne in fichier:
            contenu_fichier += ligne

    with open(nom_fichier_presidents, "a") as fichier:  # Ajout des noms des présidents dans un fichier
        for nom_president in noms_presidents:
            if nom_president not in contenu_fichier:
                fichier.write(nom_president + " : \n")

    return noms_presidents


def recup_prenoms_presidents(nom_fichier_presidents):
    prenoms_presidents = []

    with open(nom_fichier_presidents, "r") as fichier:
        for ligne in fichier:
            ligne_split = ligne.split()
            prenoms_presidents.append(ligne_split[-1])

    return prenoms_presidents


def en_minuscule(chaine):
    nouvelle_chaine = ""

    for caractere in chaine:
        if 60 <= ord(caractere) <= 95:
            nouvelle_chaine += chr(ord(caractere) + 32)
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def creer_fichiers_minuscule(nom_repertoire_discours, nom_repertoire_nettoye):
    noms_fichiers = liste_fichiers(nom_repertoire_discours, "txt")

    if not os.path.exists(nom_repertoire_nettoye):  # Création du répertoire pour fichiers nettoyés s'il n'existe pas
        os.mkdir(nom_repertoire_nettoye)

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire_discours + "/" + nom_fichier, "r") as fichier_ancien, \
                open(nom_repertoire_nettoye + "/" + nom_fichier, "w") as fichier_nettoye:
            for ligne_ancien in fichier_ancien:
                fichier_nettoye.write(en_minuscule(ligne_ancien))


def suppression_caracteres_speciaux(chaine):
    caracteres_speciaux = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                           ',', '-', "'", '.', '!', '?', '_', ':', '\n', '"', ';', '`']

    nouvelle_chaine = ""

    for caractere in chaine:
        if caractere in caracteres_speciaux:
            nouvelle_chaine += " "
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def suppression_double_espaces(chaine):
    nouvelle_chaine = ""

    for indice_caractere in range(len(chaine) - 1):
        if chaine[indice_caractere] == " " and chaine[indice_caractere + 1] == " ":
            nouvelle_chaine += ""
        else:
            nouvelle_chaine += chaine[indice_caractere]
    nouvelle_chaine += " "

    return nouvelle_chaine


def nettoyage_complet_fichiers(nom_repertoire_discours, nom_repertoire_nettoye):
    creer_fichiers_minuscule(nom_repertoire_discours, nom_repertoire_nettoye)
    
    noms_fichiers = liste_fichiers(nom_repertoire_nettoye, "txt")

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r") as fichier:
            ancien_contenu = ""
            for ligne_ancien in fichier:
                ancien_contenu += ligne_ancien

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "w") as fichier:
            contenu_sans_caracteres_speciaux = suppression_caracteres_speciaux(ancien_contenu)
            nouveau_contenu = suppression_double_espaces(contenu_sans_caracteres_speciaux)

            fichier.write(nouveau_contenu)


def calcul_tf(chaine):
    liste_mots = chaine.split()
    dictionnaire = {}

    for mot in liste_mots:
        if mot not in dictionnaire:
            dictionnaire[mot] = 1
        else:
            dictionnaire[mot] += 1

    return dictionnaire


def calcul_idf(chaine, nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    chaine_split = chaine.split()

    dictionnaire = {}

    for mot in chaine_split:

        nombre_fichiers_mot = 0

        for nom_fichier in noms_fichiers:

            with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
                contenu_fichier = ""
                for ligne in fichier:
                    contenu_fichier += ligne
                contenu_fichier_split = contenu_fichier.split()

                if mot in contenu_fichier_split:
                    nombre_fichiers_mot += 1

        dictionnaire[mot] = math.log(1 / (nombre_fichiers_mot / len(noms_fichiers)))

    return dictionnaire


def calcul_idf_total(nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    contenu_integral = ""

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            for ligne in fichier:
                contenu_integral += ligne
        contenu_integral += " "

    return calcul_idf(suppression_double_espaces(contenu_integral), nom_repertoire)


def calcul_tf_total(nom_repertoire):
    liste_tf = []

    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    for nom_fichier in noms_fichiers:

        contenu_fichier = ""
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            for ligne in fichier:
                contenu_fichier += ligne
        liste_tf.append(calcul_tf(suppression_double_espaces(contenu_fichier)))

    return liste_tf


def transposee_matrice(matrice):
    nouvelle_matrice = []

    for indice_colonne in range(len(matrice[0])):

        ligne_nouvelle_matrice = []

        for indice_ligne in range(len(matrice)):
            ligne_nouvelle_matrice.append(matrice[indice_ligne][indice_colonne])

        nouvelle_matrice.append(ligne_nouvelle_matrice)

    return nouvelle_matrice


def creation_matrice(nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    valeur_idf_fichier = calcul_idf_total(nom_repertoire)

    liste_mots = [mot for mot in valeur_idf_fichier]

    matrice = []

    for indice_fichier in range(len(noms_fichiers)):

        tf_idf_mot = []

        with open(nom_repertoire + "/" + noms_fichiers[indice_fichier], "r") as fichier:
            contenu_fichier = ""
            for ligne in fichier:
                contenu_fichier += ligne
            contenu_fichier_split = contenu_fichier.split()

            valeur_tf_fichier = calcul_tf_total(nom_repertoire)[indice_fichier]

            for mot in liste_mots:
                if mot in contenu_fichier_split:
                    tf_idf_mot.append(valeur_idf_fichier[mot] * valeur_tf_fichier[mot])
                else:
                    tf_idf_mot.append(0.0)

        matrice.append(tf_idf_mot)

    return noms_fichiers, liste_mots, transposee_matrice(matrice)


def tf_idf_nul(nom_repertoire):
    noms_fichiers, liste_mots, matrice = creation_matrice(nom_repertoire)

    moyenne_tf_idf_mots = []

    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf)

    print(moyenne_tf_idf_mots)



















def main():
    nom_repertoire_discours = "speeches"
    nom_repertoire_nettoye = "cleaned"

    nom_fichier_presidents = "presidents.txt"  # Noms et prénoms stockés dans ce fichier

    noms_presidents = recup_noms_presidents(nom_fichier_presidents, nom_repertoire_discours)

    print(recup_noms_presidents(nom_fichier_presidents, nom_repertoire_discours))

    # Ajout des prénoms des présidents manuellement dans le fichier "presidents.txt"

    prenoms_presidents = recup_prenoms_presidents(nom_fichier_presidents)

    nettoyage_complet_fichiers(nom_repertoire_discours, nom_repertoire_nettoye)

    print(creation_matrice(nom_repertoire_nettoye))

    print(tf_idf_nul(nom_repertoire_nettoye))






main()
