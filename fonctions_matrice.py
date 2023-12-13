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


def calcul_tf(chaine):  # Fonction pour calculer le TF d'une chaîne
    liste_mots = chaine.split()

    dict_tf = {}

    for mot in liste_mots:  # Mise en place d'un dictionnaire associant à chaque mot sa valeur TF
        if mot not in dict_tf:
            dict_tf[mot] = 1  # Création d'une nouvelle clé si le mot n'existe pas
        else:
            dict_tf[mot] += 1  # Incrémentation de sa valeur, sinon

    return dict_tf


def calcul_tf_total(noms_fichiers, nom_repertoire):  # Application de la fonction "calcul_tf" à tout les fichiers
    # Les valeurs TF sont stockées sous la forme de N dictionnaires avec N = nombre de fichiers
    liste_tf = []

    for nom_fichier in noms_fichiers:

        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            liste_tf.append(calcul_tf(fichier.read()))

    return liste_tf


def calcul_idf_total(noms_fichiers, nom_repertoire):  # Fonction permettant de calculer le score IDF de chaque mot
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

    dict_idf = {}  # Réutilisation d'un dictionnaire ici aussi pour associer à chaque mot son score

    for mot in liste_mots:

        nombre_fichiers_mot = 0
        for indice_fichier in range(len(noms_fichiers)):
            if mot in contenu_fichiers_liste[indice_fichier]:
                nombre_fichiers_mot += 1

        dict_idf[mot] = math.log10(len(noms_fichiers) / nombre_fichiers_mot)  # Calcul de l'IDF

    return dict_idf  # IDF est le même pour tous les fichiers; donc retour d'un unique dictionnaire


# Fonction pour réaliser la transposée d'une matrice qui consiste à inverse les lignes et les colonnes de celle ci
def transposee_matrice(matrice):
    nouvelle_matrice = []

    # On parcours la matrice initiale avec les colonnes en fonction des lignes et non l'inverse pour inverse la matrice
    for indice_colonne in range(len(matrice[0])):

        ligne_nouvelle_matrice = []

        for indice_ligne in range(len(matrice)):
            # Changement des lignes/colonnes réalisé ici
            ligne_nouvelle_matrice.append(matrice[indice_ligne][indice_colonne])

        nouvelle_matrice.append(ligne_nouvelle_matrice)

    return nouvelle_matrice


# Création de notre matrcice associant un score TF-IDF pour chaque mots en fonction des fichiers
def creation_matrice_corpus(noms_fichiers, nom_repertoire, idf_total):
    valeurs_tf_fichier = calcul_tf_total(noms_fichiers, nom_repertoire)

    liste_mots = [mot for mot in idf_total]  # On récupère tous les mots du corpus

    matrice = []

    # On réalise premièrement la matrice pour chaque fichiers en fonction des mots pour une meilleure optimisation
    for indice_fichier in range(len(noms_fichiers)):

        tf_idf_mot = []

        with open(nom_repertoire + "/" + noms_fichiers[indice_fichier], "r", encoding="utf-8") as fichier:
            contenu_fichier_split = fichier.read().split()

            valeur_tf_fichier = valeurs_tf_fichier[indice_fichier]

            for mot in liste_mots:
                if mot in contenu_fichier_split:
                    tf_idf_mot.append(idf_total[mot] * valeur_tf_fichier[mot])  # Calcul du produit TF-IDF
                else:
                    # Si le mot n'est pas dans le fichier, alors son TF est nul donc le produit le sera aussi
                    tf_idf_mot.append(0)

        matrice.append(tf_idf_mot)

    # On retourne la liste des mots du corpus (afin qu'on puisse la réutiliser), ainsi que la transposée de la matrice
    return liste_mots, transposee_matrice(matrice)


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

    tf_contenu_fichiers = calcul_tf(contenu_fichiers)

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


def formater_question(question):
    chaine_formatee = en_minuscule(suppression_caracteres_speciaux(question))  # Formatage de la chaîne
    return chaine_formatee.split()


def mot_dans_corpus(noms_fichiers, nom_repertoire, question):
    contenus_fichiers = ""
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenus_fichiers += fichier.read() + " "

    contenus_fichiers_split = contenus_fichiers.split()

    mot_corpus = []

    question_formatee = formater_question(question)

    for mot in question_formatee:
        if mot in contenus_fichiers_split:
            mot_corpus.append(mot)

    return mot_corpus


def tf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus):
    mot_corpus = mot_dans_corpus(noms_fichiers, nom_repertoire, question)

    dict_tf = {}
    for mot in liste_mots_corpus:
        dict_tf[mot] = 0

    chaine_question = ""
    for mot in mot_corpus:
        chaine_question += mot + " "

    dict_tf_question = calcul_tf(chaine_question)

    for mot in dict_tf_question:
        dict_tf[mot] = dict_tf_question[mot]

    return dict_tf


def tf_idf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus, idf_total):
    tf_total = tf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus)

    vecteur = []
    for mot in liste_mots_corpus:
        vecteur.append(idf_total[mot] * tf_total[mot])

    return vecteur


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
    norme_vect_a = norme_vecteur(vecteur_a)
    norme_vect_b = norme_vecteur(vecteur_b)

    if norme_vect_a == 0 or norme_vect_b == 0:
        return None

    return produit_scalaire(vecteur_a, vecteur_b) / (norme_vect_a * norme_vect_b)


def doc_pertinent(noms_fichiers, vecteur_question, matrice_corpus):
    similarite_max = [None, -1]

    matrice_corpus_transposee = transposee_matrice(matrice_corpus)

    for indice_fichier in range(len(noms_fichiers)):

        similarite = calcul_similarite(vecteur_question, matrice_corpus_transposee[indice_fichier])

        if similarite is None:
            return None

        if similarite > similarite_max[1]:
            similarite_max = [noms_fichiers[indice_fichier], similarite]

    return similarite_max[0]


def tf_idf_question_max(vecteur_question, liste_mots_corpus):
    valeurs_max = [None, -1]

    for indice_valeur in range(len(vecteur_question)):
        valeur = vecteur_question[indice_valeur]
        if valeur > valeurs_max[1]:
            valeurs_max = [indice_valeur, valeur]

    return liste_mots_corpus[valeurs_max[0]]


def generation_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total, matrice_corpus,
                       nom_repertoire_discours):
    vecteur_question = tf_idf_question(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total)

    document_question = doc_pertinent(noms_fichiers, vecteur_question, matrice_corpus)

    if document_question is None:
        return None

    mot_tf_idf_max = tf_idf_question_max(vecteur_question, liste_mots_corpus)

    with open(nom_repertoire_discours + "/" + document_question, "r", encoding="utf-8") as fichier:
        contenu_fichier = suppression_caracteres_speciaux(en_minuscule(fichier.read()), ["\n"])

    phrase_contenu_fichier = contenu_fichier.split(".")

    trouve = False
    indice_phrase = 0
    phrase = phrase_contenu_fichier[0]

    while not trouve and indice_phrase < len(phrase_contenu_fichier):
        phrase = phrase_contenu_fichier[indice_phrase]
        if mot_tf_idf_max in phrase:
            trouve = True
        indice_phrase += 1

    return phrase



