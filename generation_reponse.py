"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient toutes les fonctions chargées de générer une réponse automatique, allant du formatage de la question
récupérée de l'utilisateur à l'affinage de la réponse finale du ChatBot.
"""


import traitement_fichiers as tt_fich
import calcul_tf_idf

import math


def formater_question(question):
    chaine_formatee = tt_fich.en_minuscule(tt_fich.suppression_caracteres_speciaux(question))  # Formatage de la chaîne
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

    dict_tf_question = calcul_tf_idf.calcul_tf(chaine_question)

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
        contenu_fichier = tt_fich.suppression_caracteres_speciaux(fichier.read(), ["\n"])

    phrase_contenu_fichier = contenu_fichier.split(".")

    trouve = False
    indice_phrase = 0
    phrase = phrase_contenu_fichier[0]

    while not trouve and indice_phrase < len(phrase_contenu_fichier):
        phrase = phrase_contenu_fichier[indice_phrase]
        phrase_minuscule = tt_fich.en_minuscule(phrase)
        if mot_tf_idf_max in phrase_minuscule:
            trouve = True
        indice_phrase += 1

    return phrase


def affiner_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total, matrice_corpus,
                    nom_repertoire_discours):

    debut_question = {
        "comment": ("Après analyse, ", False),  # False = minuscule, True = majuscule
        "pourquoi": ("C'est parce que ", False),
        "peux": ("Bien sûr ! ", True),
        "sais": ("Bien sûr ! ", True),
        "que": ("Selon moi, ", False)
    }

    reponse = generation_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total,
                                 matrice_corpus, nom_repertoire_discours)

    if reponse is None:
        reponse = "Je ne suis pas encore capable de répondre à votre message... Essayez de le reformuler !"
    else:
        while reponse[0] == " " or reponse[0] == "-":
            reponse = reponse[1:]
        while reponse[-1] == " ":
            reponse = reponse[:-1]

        question_formatee = formater_question(question)

        if question_formatee[0] in debut_question:
            for debut in debut_question:
                reponse_debut = debut_question[debut]
                if question_formatee[0] == debut:
                    if reponse_debut[1]:
                        ascii_caractere = ord(reponse[0])
                        if ord("a") <= ascii_caractere <= ord('z'):
                            reponse = reponse_debut[0] + chr(ascii_caractere - (ord("a") - ord("A"))) + reponse[1:]
                        else:
                            reponse = reponse_debut[0] + reponse
                    else:
                        ascii_caractere = ord(reponse[0])
                        if ord("A") <= ascii_caractere <= ord('Z'):
                            reponse = reponse_debut[0] + chr(ascii_caractere + (ord("a") - ord("A"))) + reponse[1:]
                        else:
                            reponse = reponse_debut[0] + reponse
        else:
            ascii_caractere = ord(reponse[0])
            if ord("a") <= ascii_caractere <= ord('z'):
                reponse = chr(ascii_caractere - (ord("a") - ord("A"))) + reponse[1:]

        ascii_caractere = ord(reponse[-1])
        if not (ascii_caractere == ord("?") or ascii_caractere == ord("!")):
            reponse += "."

    return reponse
