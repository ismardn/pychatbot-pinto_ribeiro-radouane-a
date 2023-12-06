import os
import math


# Création d'une liste comprenant tout les noms des fichers. txt présent dans le corpus
def liste_fichiers(repertoire, extension):
    noms_fichiers = []
    for nom_fichier in os.listdir(repertoire):  # Pour chaque fichier dans le répertoire
        if nom_fichier.endswith(extension):
            # Si le fichier est un fichier avec l'extension ".extension", alors on l'ajoute à la liste "noms_fichiers"
            noms_fichiers.append(nom_fichier)

    return noms_fichiers


def retirer_caracteres_nom_fichier(nom_fichier):
    # Slice de la chaîne "nom_fichier" pour enlever les premiers caractères ("Nomination_") et l'extension
    nom_president_temp = nom_fichier[len("Nomination_"):len(nom_fichier) - len(".txt")]
    nom_president = ""
    for caractere in nom_president_temp:
        if caractere not in "0123456789":  # Si le caractère n'est pas un chiffre alors on l'ajoute a la nouvelle chaine
            nom_president += caractere

    return nom_president


# Fonction pour remettre au propre la liste du nom des présidents en retirant les numéruos et les doublons
def recup_noms_presidents(nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    noms_presidents_temp = []
    for nom_fichier in noms_fichiers:
        # On applique la fonction suppressions caractères sur chaque nom de fichier
        nom_president = retirer_caracteres_nom_fichier(nom_fichier)
        noms_presidents_temp.append(nom_president)

    noms_presidents = []  # Suppression des doublons
    for nom_president in noms_presidents_temp:
        # Si le nom du président n'est pas déjà dans la liste alors on l'ajoute
        if nom_president not in noms_presidents:
            noms_presidents.append(nom_president)

    return noms_presidents


# Transformation des textes des fichiers: mise en forme des textes en mettant tout en minuscule
def en_minuscule(chaine):
    nouvelle_chaine = ""

    for caractere in chaine:
        if ord("A") <= ord(caractere) <= ord('Z'):  # Si le code ASCII du caractère appartient aux majuscules
            nouvelle_chaine += chr(ord(caractere) + ord("a") - ord("A"))  # On le transforme en minuscule
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


# Application de la fonction précédente à tout les fichiers
def creer_fichiers_minuscule(nom_repertoire_discours, nom_repertoire_nettoye):
    noms_fichiers = liste_fichiers(nom_repertoire_discours, "txt")

    for nom_fichier in noms_fichiers:
        # On ouvre tous les fichiers du programme avec l'encodage utf-8 pour bien conserver les accents, notamment ici
        with open(nom_repertoire_discours + "/" + nom_fichier, "r", encoding="utf-8") as fichier_ancien, \
                open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier_nettoye:
            # Application de la fonction minuscule sur chaque fichier du dossier des discours
            fichier_nettoye.write(en_minuscule(fichier_ancien.read()))


# Remise en forme des textes en enlevant les caractères spéciaux ainsi que les numéros.
def suppression_caracteres_speciaux(chaine):
    caracteres_speciaux = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                           ',', '-', "'", '.', '!', '?', '_', ':', '\n', '"', ';', '`']  # Caractères supprimés

    nouvelle_chaine = ""

    for caractere in chaine:
        if caractere in caracteres_speciaux:  # Remplacement des caractères spéciaux par des espaces
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

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            ancien_contenu = fichier.read()  # On stocke dans un variable l'ensemble du contenu du fichier

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier:
            # Application de la fonction supprimant les caractères spéciaux sur chaque fichier du dossier des discours
            fichier.write(suppression_caracteres_speciaux(ancien_contenu))


def calcul_tf(chaine):  # Fonction pour calculer le TF
    liste_mots = chaine.split()
    dictionnaire = {}

    for mot in liste_mots:  # Mise en place d'un dictionnaire associant à chaque mot son score
        if mot not in dictionnaire:
            dictionnaire[mot] = 1  # Création d'une nouvelle clé si le mot n'existe pas
        else:
            dictionnaire[mot] += 1  # Incrémentation de sa valeur sinon

    return dictionnaire


def calcul_tf_total(nom_repertoire):  # Application de la fonction "calcul_tf" à tout les fichiers
    liste_tf = []

    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_tf.append(calcul_tf(fichier.read()))

    return liste_tf


def calcul_idf_total(nom_repertoire):  # Fonction permettant de calculer le score IDF de chaque mot
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    contenu_fichiers_liste = []
    contenu_fichiers = ""

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenu_fichier = fichier.read()
            contenu_fichiers_liste.append(contenu_fichier.split())
            contenu_fichiers += contenu_fichier + " "

    chaine_split = contenu_fichiers.split()
    liste_mots = []

    for mot in chaine_split:
        if mot not in liste_mots:
            liste_mots.append(mot)

    dictionnaire = {}  # Réutilisation d'un dictionnaire ici aussi pour associer à chaque mot son score

    for mot in liste_mots:

        nombre_fichiers_mot = 0
        for indice_fichier in range(len(noms_fichiers)):
            if mot in contenu_fichiers_liste[indice_fichier]:
                nombre_fichiers_mot += 1

        dictionnaire[mot] = math.log10(len(noms_fichiers) / nombre_fichiers_mot)  # Calcul de l'IDF

    return dictionnaire


# Fonction pour réaliser la transposée d'une matrice qui consiste à inverse les lignes et les colonnes de celle ci
def transposee_matrice(matrice):
    nouvelle_matrice = []

    for indice_colonne in range(len(matrice[0])):

        ligne_nouvelle_matrice = []

        for indice_ligne in range(len(matrice)):
            # Changement des lignes/colonnes réalisé ici
            ligne_nouvelle_matrice.append(matrice[indice_ligne][indice_colonne])

        nouvelle_matrice.append(ligne_nouvelle_matrice)

    return nouvelle_matrice


# Création de notre matrcice associant un score TF-IDF pour chaque noms de fichiers en fonctions des mots
def creation_matrice(nom_repertoire):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    valeur_idf_fichier = calcul_idf_total(nom_repertoire)

    liste_mots = [mot for mot in valeur_idf_fichier]

    matrice = []

    for indice_fichier in range(len(noms_fichiers)):

        tf_idf_mot = []

        with open(nom_repertoire + "/" + noms_fichiers[indice_fichier], "r", encoding="utf-8") as fichier:
            contenu_fichier_split = fichier.read().split()

            valeur_tf_fichier = calcul_tf_total(nom_repertoire)[indice_fichier]  # Utilisation de la fonction TF

            for mot in liste_mots:
                if mot in contenu_fichier_split:
                    tf_idf_mot.append(valeur_idf_fichier[mot] * valeur_tf_fichier[mot])
                else:
                    tf_idf_mot.append(0.)

        matrice.append(tf_idf_mot)

    return noms_fichiers, liste_mots, transposee_matrice(matrice)


def tf_idf_nul(return_matrice):  # Fonction renvoyant les mots avec un score TF-IDF nul
    noms_fichiers, liste_mots, matrice = return_matrice

    moyenne_tf_idf_mots = []

    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    liste_valeurs_min = []

    for indice_valeur_min in range(len(moyenne_tf_idf_mots)):
        # Si la moyenne du score TF-IDF d'un mot entre tous les fichiers est nulle, alors on l'ajoute à la liste
        if moyenne_tf_idf_mots[indice_valeur_min] == 0.:
            liste_valeurs_min.append(liste_mots[indice_valeur_min])

    return liste_valeurs_min


def tf_idf_max(return_matrice):  # Fonction renvoyant les mots avec le score TF-IDF le plus élevé.
    noms_fichiers, liste_mots, matrice = return_matrice

    moyenne_tf_idf_mots = []

    for indice_mot in range(len(liste_mots)):
        somme_tf_idf = 0
        for indice_fichier in range(len(noms_fichiers)):
            somme_tf_idf += matrice[indice_mot][indice_fichier]
        moyenne_tf_idf_mots.append(somme_tf_idf / len(noms_fichiers))

    # Initialisation de la valeur max à -1, et [] correspond à l'ensemble des mots de même TF-IDF max
    liste_valeurs_max = [-1, []]

    for valeur in moyenne_tf_idf_mots:
        if valeur > liste_valeurs_max[0]:
            liste_valeurs_max = [valeur, []]
            for indice_valeur_max in range(len(moyenne_tf_idf_mots)):
                if moyenne_tf_idf_mots[indice_valeur_max] == valeur:
                    liste_valeurs_max[1].append(liste_mots[indice_valeur_max])

    return liste_valeurs_max[1]


# Fonction renvoyant le mot le plus utilisé par un président
def mot_max_president(nom_repertoire, return_matrice, nom_president):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    liste_mots_non_important = tf_idf_nul(return_matrice)

    contenu_fichiers = ""

    for nom_fichier in noms_fichiers:
        if nom_president in nom_fichier:
            with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
                contenu_fichiers = fichier.read() + " "

    liste_valeurs_max = [-1, []]

    tf_contenu_fichiers = calcul_tf(contenu_fichiers)

    for mot in tf_contenu_fichiers:  # Reprise de la même base de code que pour la fonction TF-IDF max.
        if tf_contenu_fichiers[mot] > liste_valeurs_max[0] and mot not in liste_mots_non_important:
            liste_valeurs_max = [tf_contenu_fichiers[mot], []]
            for mot_max in tf_contenu_fichiers:
                if tf_contenu_fichiers[mot_max] == liste_valeurs_max[0]:
                    liste_valeurs_max[1].append(mot_max)

    return liste_valeurs_max[1]


# Fonction renvoyant le président ayant énonce le mot recherche le plus de fois
def mot_enonce_president(nom_repertoire, mot_recherche):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

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
def premier_president_mot(nom_repertoire, mot_recherche):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

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
def mots_tous_presidents(return_matrice, nom_repertoire_nettoye):
    noms_fichiers, liste_mots, matrice = return_matrice

    liste_mots_non_important = tf_idf_nul(return_matrice)

    liste_contenu_fichier_split = []

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_contenu_fichier_split.append(fichier.read().split())

    liste_mots_tous_president = []

    for mot in liste_mots:
        mot_in_fichiers = [mot in liste_contenu_fichier_split[indice_fichier]
                           for indice_fichier in range(len(noms_fichiers))]

        dict_pres = {}
        for nom_president in recup_noms_presidents(nom_repertoire_nettoye):
            dict_pres[nom_president] = [[nom_fichier for nom_fichier in noms_fichiers if nom_president in nom_fichier],
                                        False
                                        ]
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


def formater_question(question):
    chaine_formatee = en_minuscule(suppression_caracteres_speciaux(question))  # Formatage de la chaîne
    return chaine_formatee.split()


def mot_dans_corpus(nom_repertoire, question):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    contenus_fichiers = ""
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r") as fichier:
            contenus_fichiers += fichier.read() + " "

    contenus_fichiers_split = contenus_fichiers.split()

    mot_corpus = []

    question_formatee = formater_question(question)

    for mot in question_formatee:
        if mot in contenus_fichiers_split:
            mot_corpus.append(mot)

    return mot_corpus


def tf_question(nom_repertoire, question, liste_mots_corpus):
    question_formatee = formater_question(question)

    question_chaine = ""
    for mot in question_formatee:
        question_chaine += mot + " "

    mot_corpus = mot_dans_corpus(nom_repertoire, question_formatee)

    dictionnaire = calcul_tf(question_chaine)

    for mot in question_formatee:
        if mot not in mot_corpus:
            dictionnaire[mot] = 0
        # else:
        #     dictionnaire[mot] /= len(question_formatee)

    return dictionnaire


def tf_idf_question(nom_repertoire, question):
    noms_fichiers = liste_fichiers(nom_repertoire, "txt")

    question_formatee = formater_question(question)

    idf_corpus = calcul_idf_total(nom_repertoire)

    mot_corpus = mot_dans_corpus(nom_repertoire, question)

    matrice = []

    for _ in range(len(noms_fichiers)):
        mots = []
        for mot in question_formatee:
            if mot in mot_corpus:
                mots.append(idf_corpus[mot])
        matrice.append(mots)

    return mot_corpus, noms_fichiers, matrice


def produit_scalaire(vecteur_a, vecteur_b):
    somme = 0
    for indice in range(len(vecteur_a)):
        somme += vecteur_a[indice] * vecteur_b[indice]
    return somme


def norme_vecteur(vecteur):
    somme = 0
    for indice in range(len(vecteur)):
        somme += vecteur[indice] ** 2
    return math.sqrt(somme)


def calcul_similarite(vecteur_a, vecteur_b):
    return produit_scalaire(vecteur_a, vecteur_b) / (norme_vecteur(vecteur_a) * norme_vecteur(vecteur_b))


def doc_pertinent(return_matrice_corpus, return_matrice_question):


    noms_fichiers, liste_mots_corpus, matrice_corpus = return_matrice_corpus
    noms_fichiers, liste_mots_question, matrice_question = return_matrice_question

    similarite_max = [0, None]

    matrice_corpus_transposee = transposee_matrice(matrice_corpus)

    for indice_fichier in range(len(noms_fichiers)):
        similarite = calcul_similarite(matrice_question, )




print(tf_idf_question("cleaned", "Bonjour comment allez vous, climat histoire"))
