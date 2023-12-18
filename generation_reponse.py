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
    """
    Cette fonction formate une question en la convertissant en minuscules et en supprimant les caractères spéciaux.

    :param question: La question à formater.
    :return: Une liste des mots de la question formatée.
    """

    # Appel de fonctions externes pour convertir la question en minuscules et supprimer les caractères spéciaux
    chaine_formatee = tt_fich.en_minuscule(tt_fich.suppression_caracteres_speciaux(question))

    return chaine_formatee.split()


def mot_dans_corpus(noms_fichiers, nom_repertoire, question):
    """
    Cette fonction cherche les mots de la question dans le corpus formé par l'ensemble des fichiers.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers.
    :param question: La question à analyser.
    :return: Une liste des mots de la question présents dans le corpus.
    """

    # Concaténation du contenu de tous les fichiers du corpus dans une seule chaîne de caractères
    contenus_fichiers = ""
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            contenus_fichiers += fichier.read() + " "

    # Division de la chaîne en une liste de mots
    contenus_fichiers_split = contenus_fichiers.split()

    # Liste pour stocker les mots de la question présents dans le corpus
    mot_corpus = []

    # Formatage de la question en utilisant une fonction externe
    question_formatee = formater_question(question)

    for mot in question_formatee:
        if mot in contenus_fichiers_split:
            mot_corpus.append(mot)

    return mot_corpus


def tf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus):
    """
    Cette fonction calcule le score TF-IDF pour les mots de la question par rapport au corpus spécifié.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers.
    :param question: La question pour laquelle le score TF-IDF est calculé.
    :param liste_mots_corpus: Une liste des mots du corpus.
    :return: Un dictionnaire associant chaque mot de la question à son score TF-IDF.
    """

    # Obtention des mots de la question présents dans le corpus
    mot_corpus = mot_dans_corpus(noms_fichiers, nom_repertoire, question)

    # Initialisation d'un dictionnaire avec des scores TF nuls pour chaque mot du corpus
    dict_tf = {}
    for mot in liste_mots_corpus:
        dict_tf[mot] = 0

    # Construction d'une chaîne contenant les mots de la question présents dans le corpus
    chaine_question = ""
    for mot in mot_corpus:
        chaine_question += mot + " "

    dict_tf_question = calcul_tf_idf.calcul_tf(chaine_question)

    # Mise à jour du dictionnaire de scores TF avec les scores calculés pour la question
    for mot in dict_tf_question:
        dict_tf[mot] = dict_tf_question[mot]

    return dict_tf


def tf_idf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus, idf_total):
    """
    Cette fonction calcule le vecteur TF-IDF pour les mots de la question par rapport au corpus spécifié.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire: Le répertoire où se trouvent les fichiers.
    :param question: La question pour laquelle le vecteur TF-IDF est calculé.
    :param liste_mots_corpus: Une liste des mots du corpus.
    :param idf_total: Un dictionnaire contenant les scores IDF pour tous les mots du corpus.
    :return: Un vecteur TF-IDF pour les mots de la question.
    """

    # Calcul des scores TF pour les mots de la question
    tf_total = tf_question(noms_fichiers, nom_repertoire, question, liste_mots_corpus)

    vecteur = []

    # Calcul du score TF-IDF pour chaque mot de la question en utilisant les scores TF et IDF
    for mot in liste_mots_corpus:
        vecteur.append(idf_total[mot] * tf_total[mot])

    return vecteur


def produit_scalaire(vecteur_a, vecteur_b):
    """
    Cette fonction calcule le produit scalaire entre deux vecteurs.

    :param vecteur_a: Le premier vecteur.
    :param vecteur_b: Le deuxième vecteur.
    :return: Le produit scalaire entre les deux vecteurs.
    """

    somme = 0

    # Calcul du produit scalaire en parcourant les indices des vecteurs
    for indice in range(len(vecteur_a)):
        somme += vecteur_a[indice] * vecteur_b[indice]

    return somme


def norme_vecteur(vecteur):
    """
    Cette fonction calcule la norme euclidienne d'un vecteur.

    :param vecteur: Le vecteur pour lequel la norme est calculée.
    :return: La norme euclidienne du vecteur.
    """

    # Initialisation d'une somme pour stocker le résultat de la norme euclidienne
    somme = 0

    for indice in range(len(vecteur)):
        somme += vecteur[indice] ** 2

    norme = math.sqrt(somme)

    return norme


def calcul_similarite(vecteur_a, vecteur_b):
    """
    Cette fonction calcule la similarité cosinus entre deux vecteurs.

    :param vecteur_a: Le premier vecteur.
    :param vecteur_b: Le deuxième vecteur.
    :return: La similarité cosinus entre les deux vecteurs.
    """

    # Calcul des normes euclidiennes des deux vecteurs
    norme_vect_a = norme_vecteur(vecteur_a)
    norme_vect_b = norme_vecteur(vecteur_b)

    # Vérification pour éviter la division par zéro
    if norme_vect_a == 0 or norme_vect_b == 0:
        return None

    # Calcul de la similarité cosinus en utilisant le produit scalaire et les normes
    similarite_cosinus = produit_scalaire(vecteur_a, vecteur_b) / (norme_vect_a * norme_vect_b)

    return similarite_cosinus


def transposee_matrice(matrice):
    """
    Cette fonction calcule la transposée d'une matrice.

    :param matrice: La matrice d'origine.
    :return: La transposée de la matrice.
    """

    # Initialisation d'une nouvelle matrice pour stocker la transposée
    nouvelle_matrice = []

    # Parcours de la matrice initiale avec inversion des lignes et colonnes
    for indice_colonne in range(len(matrice[0])):

        ligne_nouvelle_matrice = []

        for indice_ligne in range(len(matrice)):
            # Changement des lignes/colonnes réalisé ici pour obtenir la transposée
            ligne_nouvelle_matrice.append(matrice[indice_ligne][indice_colonne])

        nouvelle_matrice.append(ligne_nouvelle_matrice)

    return nouvelle_matrice


def doc_pertinent(noms_fichiers, vecteur_question, matrice_corpus):
    """
    Cette fonction détermine le document le plus pertinent par rapport à une question.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param vecteur_question: Le vecteur TF-IDF de la question.
    :param matrice_corpus: La matrice TF-IDF du corpus.
    :return: Le nom du document le plus pertinent.
    """

    similarite_max = [None, -1]

    # Calcul de la transposée de la matrice du corpus
    matrice_corpus_transposee = transposee_matrice(matrice_corpus)

    for indice_fichier in range(len(noms_fichiers)):

        similarite = calcul_similarite(vecteur_question, matrice_corpus_transposee[indice_fichier])

        if similarite is None:
            return None

        # Mise à jour du document le plus pertinent si la similarité actuelle est supérieure à la maximale enregistrée
        if similarite > similarite_max[1]:
            similarite_max = [noms_fichiers[indice_fichier], similarite]

    return similarite_max[0]


def tf_idf_question_max(vecteur_question, liste_mots_corpus):
    """
    Cette fonction détermine le mot avec le score TF-IDF le plus élevé dans le vecteur de la question.

    :param vecteur_question: Le vecteur TF-IDF de la question.
    :param liste_mots_corpus: Une liste des mots du corpus.
    :return: Le mot avec le score TF-IDF le plus élevé dans le vecteur de la question.
    """

    valeurs_max = [None, -1]

    for indice_valeur in range(len(vecteur_question)):
        valeur = vecteur_question[indice_valeur]
        # Mise à jour des valeurs maximales si la valeur actuelle est supérieure à la maximale enregistrée
        if valeur > valeurs_max[1]:
            valeurs_max = [indice_valeur, valeur]

    return liste_mots_corpus[valeurs_max[0]]


def generation_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total, matrice_corpus,
                       nom_repertoire_discours):
    """
    Cette fonction génère une réponse à une question en utilisant le document le plus pertinent.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire_nettoye: Le répertoire où se trouvent les fichiers nettoyés.
    :param question: La question à laquelle générer une réponse.
    :param liste_mots_corpus: Une liste des mots du corpus.
    :param idf_total: Un dictionnaire contenant les scores IDF pour tous les mots du corpus.
    :param matrice_corpus: La matrice TF-IDF du corpus.
    :param nom_repertoire_discours: Le répertoire où se trouvent les discours.
    :return: Une phrase en réponse à la question.
    """

    # Calcul du vecteur TF-IDF pour la question
    vecteur_question = tf_idf_question(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total)

    document_question = doc_pertinent(noms_fichiers, vecteur_question, matrice_corpus)

    # Si le document le plus pertinent n'est pas trouvé, retourne None
    if document_question is None:
        return None

    # Détermination du mot avec le score TF-IDF le plus élevé dans le vecteur de la question
    mot_tf_idf_max = tf_idf_question_max(vecteur_question, liste_mots_corpus)

    with open(nom_repertoire_discours + "/" + document_question, "r", encoding="utf-8") as fichier:
        contenu_fichier = tt_fich.suppression_caracteres_speciaux(fichier.read(), ["\n"])

    # Division du contenu du document en phrases
    phrase_contenu_fichier = contenu_fichier.split(".")

    trouve = False
    indice_phrase = 0
    phrase = phrase_contenu_fichier[0]

    # Recherche de la première phrase contenant le mot avec le score TF-IDF le plus élevé
    while not trouve and indice_phrase < len(phrase_contenu_fichier):
        phrase = phrase_contenu_fichier[indice_phrase]
        phrase_minuscule = tt_fich.en_minuscule(phrase)
        if mot_tf_idf_max in phrase_minuscule:
            trouve = True
        indice_phrase += 1

    return phrase


def affiner_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total, matrice_corpus,
                    nom_repertoire_discours):
    """
    Cette fonction affine la réponse générée en fonction du type de question.

    :param noms_fichiers: Une liste de noms de fichiers dans le corpus.
    :param nom_repertoire_nettoye: Le répertoire où se trouvent les fichiers nettoyés.
    :param question: La question à laquelle générer une réponse.
    :param liste_mots_corpus: Une liste des mots du corpus.
    :param idf_total: Un dictionnaire contenant les scores IDF pour tous les mots du corpus.
    :param matrice_corpus: La matrice TF-IDF du corpus.
    :param nom_repertoire_discours: Le répertoire où se trouvent les discours.
    :return: Une réponse affinée en fonction du type de question.
    """

    # Dictionnaire contenant des débuts de réponses en fonction du type de question
    debut_question = {
        "comment": ("Après analyse, ", False),  # False = minuscule, True = majuscule
        "pourquoi": ("C'est parce que ", False),
        "peux": ("Bien sûr ! ", True),
        "sais": ("Bien sûr ! ", True),
        "que": ("Selon moi, ", False)
    }

    # Génération de la réponse initiale
    reponse = generation_reponse(noms_fichiers, nom_repertoire_nettoye, question, liste_mots_corpus, idf_total,
                                 matrice_corpus, nom_repertoire_discours)

    # Si la réponse initiale est None, retourne un message d'indisponibilité
    if reponse is None:
        reponse = "Je ne suis pas encore capable de répondre à votre message... Essayez de le reformuler !"
    else:
        while reponse[0] == " " or reponse[0] == "-":
            reponse = reponse[1:]
        while reponse[-1] == " ":
            reponse = reponse[:-1]

        # Formatage de la question
        question_formatee = formater_question(question)

        # Affinage de la réponse en fonction du type de question
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

        # Ajout d'un point à la fin de la réponse si nécessaire
        ascii_caractere = ord(reponse[-1])
        if not (ascii_caractere == ord("?") or ascii_caractere == ord("!")):
            reponse += "."

    return reponse
