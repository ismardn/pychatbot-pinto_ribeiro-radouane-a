import tkinter
import tkinter.messagebox
import os
import math


def liste_fichiers(repertoire, extension):
    noms_fichiers = []
    for nom_fichier in os.listdir(repertoire):
        if nom_fichier.endswith(extension):
            noms_fichiers.append(nom_fichier)

    return noms_fichiers


def retirer_caracteres_nom_fichier(nom_fichier):
    # Slice de la chaîne "nom_fichier" pour enlever les premiers caractères ("Nomination_") et l'extension
    nom_president_temp = nom_fichier[len("Nomination_"):len(nom_fichier) - len(".txt")]
    nom_president = ""
    for caractere in nom_president_temp:
        if caractere not in "0123456789":
            nom_president += caractere

    return nom_president


def recup_noms_presidents(nom_fichier_presidents, nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    noms_presidents_temp = []
    for nom_fichier in noms_fichiers:
        nom_president = retirer_caracteres_nom_fichier(nom_fichier)
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
                fichier.write(nom_president + ":\n")

    return noms_presidents


def recup_prenoms_presidents(nom_fichier_presidents):
    prenoms_presidents = []

    with open(nom_fichier_presidents, "r") as fichier:
        for ligne in fichier:
            ligne_split = ligne.split(":")
            prenoms_presidents.append(ligne_split[1])

    return prenoms_presidents


def en_minuscule(chaine):
    nouvelle_chaine = ""

    for caractere in chaine:
        if ord("A") <= ord(caractere) <= ord('Z'):
            nouvelle_chaine += chr(ord(caractere) + ord("a") - ord("A"))
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def creer_fichiers_minuscule(nom_repertoire_discours, nom_repertoire_nettoye):
    noms_fichiers = liste_fichiers(nom_repertoire_discours, "txt")

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire_discours + "/" + nom_fichier, "r") as fichier_ancien, \
                open(nom_repertoire_nettoye + "/" + nom_fichier, "w") as fichier_nettoye:
            for ligne in fichier_ancien:
                fichier_nettoye.write(en_minuscule(ligne))


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


def nettoyage_complet_fichiers(nom_repertoire_discours, nom_repertoire_nettoye):
    if not os.path.exists(nom_repertoire_nettoye):  # Création du répertoire pour fichiers nettoyés s'il n'existe pas
        os.mkdir(nom_repertoire_nettoye)

    creer_fichiers_minuscule(nom_repertoire_discours, nom_repertoire_nettoye)

    noms_fichiers = liste_fichiers(nom_repertoire_nettoye, "txt")

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r") as fichier:
            ancien_contenu = ""
            for ligne in fichier:
                ancien_contenu += ligne

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "w") as fichier:
            fichier.write(suppression_caracteres_speciaux(ancien_contenu))


def calcul_tf(chaine):
    liste_mots = chaine.split()
    dictionnaire = {}

    for mot in liste_mots:
        if mot not in dictionnaire:
            dictionnaire[mot] = 1
        else:
            dictionnaire[mot] += 1

    return dictionnaire


def calcul_tf_total(nom_repertoire):
    liste_tf = []

    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    for nom_fichier in noms_fichiers:

        contenu_fichier = ""
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            for ligne in fichier:
                contenu_fichier += ligne
        liste_tf.append(calcul_tf(contenu_fichier))

    return liste_tf


def calcul_idf_total(nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    contenu_fichiers_liste = []
    contenu_fichiers_integral = ""

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            contenu_fichier = ""
            for ligne in fichier:
                contenu_fichier += ligne
            contenu_fichiers_liste.append(contenu_fichier.split())
            contenu_fichiers_integral += contenu_fichier + " "

    chaine_split = contenu_fichiers_integral.split()
    liste_mots = []

    for mot in chaine_split:
        if mot not in liste_mots:
            liste_mots.append(mot)

    dictionnaire = {}

    for mot in liste_mots:

        nombre_fichiers_mot = 0
        for indice_fichier in range(len(noms_fichiers)):
            if mot in contenu_fichiers_liste[indice_fichier]:
                nombre_fichiers_mot += 1

        dictionnaire[mot] = math.log(len(noms_fichiers) / nombre_fichiers_mot)

    return dictionnaire


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
                    tf_idf_mot.append(0.)

        matrice.append(tf_idf_mot)

    return noms_fichiers, liste_mots, transposee_matrice(matrice)


def tf_idf_nul(return_matrice):
    noms_fichiers, liste_mots, matrice = return_matrice

    moyenne_tf_idf_mots = []

    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf)

    liste_valeurs_min = []

    for indice_valeur_min in range(len(moyenne_tf_idf_mots)):
        if moyenne_tf_idf_mots[indice_valeur_min] == 0.:
            liste_valeurs_min.append(liste_mots[indice_valeur_min])

    return liste_valeurs_min


def tf_idf_max(return_matrice):
    noms_fichiers, liste_mots, matrice = return_matrice

    moyenne_tf_idf_mots = []

    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf)

    liste_valeurs_max = [-1, []]

    for valeur in moyenne_tf_idf_mots:
        if valeur > liste_valeurs_max[0]:
            liste_valeurs_max = [valeur, []]
            for indice_valeur_max in range(len(moyenne_tf_idf_mots)):
                if moyenne_tf_idf_mots[indice_valeur_max] == valeur:
                    liste_valeurs_max[1].append(liste_mots[indice_valeur_max])

    return liste_valeurs_max[1]


def mot_max_president(nom_repertoire, nom_president):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    contenu_fichiers = ""

    for nom_fichier in noms_fichiers:
        if nom_president in nom_fichier:
            with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
                for ligne in fichier:
                    contenu_fichiers += ligne
            contenu_fichiers += " "

    liste_valeurs_max = [-1, []]

    tf_contenu_fichiers = calcul_tf(contenu_fichiers)

    for mot in tf_contenu_fichiers:
        if tf_contenu_fichiers[mot] > liste_valeurs_max[0]:
            liste_valeurs_max = [tf_contenu_fichiers[mot], []]
            for mot_max in tf_contenu_fichiers:
                if tf_contenu_fichiers[mot_max] == liste_valeurs_max[0]:
                    liste_valeurs_max[1].append(mot_max)

    return liste_valeurs_max[1]


def mot_enonce_president(nom_repertoire, mot_recherche):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    dict_pres_mot = {}

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            contenu_fichier = ""
            for ligne in fichier:
                contenu_fichier += ligne

            contenu_fichier_split = contenu_fichier.split()

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


def premier_president_mot(nom_repertoire, liste_mot_recherche):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    dict_pres_mot = {}

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            contenu_fichier = ""
            for ligne in fichier:
                contenu_fichier += ligne

            contenu_fichier_split = contenu_fichier.split()

            nom_president = retirer_caracteres_nom_fichier(nom_fichier)

            for indice_mot in range(len(contenu_fichier_split)):
                if contenu_fichier_split[indice_mot] in liste_mot_recherche:
                    if nom_president in dict_pres_mot:
                        if dict_pres_mot[nom_president] < indice_mot:
                            dict_pres_mot[nom_president] = indice_mot
                    else:
                        dict_pres_mot[nom_president] = indice_mot

    premier_pres = list(dict_pres_mot.keys())[0]
    liste_pres = [dict_pres_mot[premier_pres], premier_pres]

    for nom_president in dict_pres_mot:
        if dict_pres_mot[nom_president] < liste_pres[0]:
            liste_pres = [dict_pres_mot[nom_president], nom_president]

    return liste_pres[1]


########################################################################################################################
# Question 6 impossible ################################################################################################
########################################################################################################################


def fenetre_aide():
    with open("README.txt", "r") as fichier:
        contenu_fichier = ""
        for ligne in fichier:
            contenu_fichier += ligne
    tkinter.messagebox.showinfo(title="Aide", message=contenu_fichier.encode())


# test

def main():
    NOM_REPERTOIRE_DISCOURS = "speeches"
    NOM_REPERTOIRE_NETTOYE = "cleaned"

    NOM_FICHIER_PRESIDENTS = "presidents.txt"  # Noms et prénoms stockés dans ce fichier

    fenetre = tkinter.Tk()

    fenetre.geometry("600x400")
    fenetre.configure(background="white")
    fenetre.resizable(width=False, height=False)

    aide = tkinter.Menu(fenetre)
    aide.add_command(label="Aide", command=fenetre_aide)
    fenetre.config(menu=aide)

    # noms_presidents = recup_noms_presidents(nom_fichier_presidents, nom_repertoire_discours)
    #
    # print(recup_noms_presidents(nom_fichier_presidents, nom_repertoire_discours))
    #
    # # Ajout des prénoms des présidents manuellement dans le fichier "presidents.txt"
    #
    # prenoms_presidents = recup_prenoms_presidents(nom_fichier_presidents)
    #
    # nettoyage_complet_fichiers(nom_repertoire_discours, nom_repertoire_nettoye)
    #
    # print(creation_matrice(nom_repertoire_nettoye))

    fenetre.mainloop()


main()
