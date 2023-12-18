"""
"My first ChatBot"
Réalisé par Clément PINTO RIBEIRO & Ismaël RADOUANE

Ce fichier contient les fonctions s'occupant du traitement des fichiers (récupérer la liste des fichiers du corpus ainsi
que traiter le contenu de ces derniers)
"""


import os


def liste_fichiers(repertoire, extension):
    """
    Renvoie une liste des noms de fichiers avec l'extension spécifiée dans le répertoire donné.

    :param repertoire: Le chemin du répertoire contenant les fichiers.
    :param extension: L'extension des fichiers à rechercher.
    :return: Liste des noms de fichiers avec l'extension spécifiée.
    """
    noms_fichiers = []

    for nom_fichier in os.listdir(repertoire):
        if nom_fichier.endswith(extension):
            # Si le fichier a l'extension spécifiée, on l'ajoute à la liste "noms_fichiers"
            noms_fichiers.append(nom_fichier)

    return noms_fichiers


def en_minuscule(chaine):
    """
    Convertit tous les caractères majuscules d'une chaîne en minuscules.

    :param chaine: La chaîne à convertir.
    :return: Une nouvelle chaîne avec tous les caractères en minuscules.
    """
    nouvelle_chaine = ""

    for caractere in chaine:
        if ord("A") <= ord(caractere) <= ord('Z'):
            nouvelle_chaine += chr(ord(caractere) + ord("a") - ord("A"))
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def creer_fichiers_minuscule(noms_fichiers, nom_repertoire_discours, nom_repertoire_nettoye):
    """
    Crée des fichiers en version minuscule à partir des fichiers existants dans un répertoire de discours.

    :param noms_fichiers: Liste des noms de fichiers à traiter.
    :param nom_repertoire_discours: Le répertoire contenant les fichiers originaux.
    :param nom_repertoire_nettoye: Le répertoire où seront sauvegardés les fichiers en version minuscule.
    La fonction ne retourne rien puisqu'il s'agit ici d'un traitement de fichiers.
    """
    for nom_fichier in noms_fichiers:
        with open(nom_repertoire_discours + "/" + nom_fichier, "r", encoding="utf-8") as fichier_ancien, \
                open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier_nettoye:
            # On applique la fonction en_minuscule sur chaque fichier du dossier des discours
            fichier_nettoye.write(en_minuscule(fichier_ancien.read()))


def suppression_caracteres_speciaux(chaine, caracteres=None):
    """
    Supprime les caractères spécifiés ou une liste prédéfinie de la chaîne donnée.

    :param chaine: La chaîne de caractères à nettoyer.
    :param caracteres: Liste des caractères à supprimer. Si non spécifié, une liste prédéfinie est utilisée.
    :return: La chaîne nettoyée.
    """
    if caracteres is None:
        # Liste des caractères à supprimer par défaut
        caracteres_speciaux = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                               ',', '-', "'", '.', '!', '?', '_', ':', '\n', '"', ';', '`']
    else:
        caracteres_speciaux = caracteres

    nouvelle_chaine = ""

    for caractere in chaine:
        if caractere in caracteres_speciaux:
            nouvelle_chaine += " "  # Remplacement des caractères spéciaux par des espaces
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def nettoyage_complet_fichiers(nom_repertoire_nettoye, noms_fichiers, nom_repertoire_discours):
    """
    Effectue un nettoyage complet des fichiers du répertoire de discours.

    :param nom_repertoire_nettoye: Le nom du répertoire où les fichiers nettoyés seront enregistrés.
    :param noms_fichiers: La liste des noms de fichiers à nettoyer.
    :param nom_repertoire_discours: Le répertoire des discours originaux.
    La fonction ne retourne rien puisqu'il s'agit ici d'un traitement de fichiers.
    """
    if not os.path.exists(nom_repertoire_nettoye):
        os.mkdir(nom_repertoire_nettoye)  # Création du répertoire pour fichiers nettoyés s'il n'existe pas

    creer_fichiers_minuscule(noms_fichiers, nom_repertoire_discours, nom_repertoire_nettoye)

    for nom_fichier in noms_fichiers:
        with open(nom_repertoire_nettoye + "/" + nom_fichier, "r", encoding="utf-8") as fichier:
            ancien_contenu = fichier.read()  # On stocke dans une variable l'ensemble du contenu du fichier

        with open(nom_repertoire_nettoye + "/" + nom_fichier, "w", encoding="utf-8") as fichier:
            # Application de la fonction supprimant les caractères spéciaux sur chaque fichier du dossier nettoyé
            fichier.write(suppression_caracteres_speciaux(ancien_contenu))
