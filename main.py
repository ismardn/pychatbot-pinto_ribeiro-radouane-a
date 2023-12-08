import os
import fonctions_matrice as fct_mat


# Fonction permettant d'accéder au ChatBot
def acceder_chatbot():
    pass


# Fonction permettant d'afficher le contenu du fichier "README.txt"
def fonctionnalite_1():
    with open("README.txt", "r", encoding="utf-8") as fichier:
        # Ouverture du fichier avec l'encodage "utf-8" afin de conserver les accents
        print(fichier.read())


# Afficher l'ensemble des présidents présents dans le corpus de documents sous la forme de liste
def fonctionnalite_2(noms_presidents):
    print("Les noms des présidents présents dans le corpus de documents sont :")
    for nom_president in noms_presidents:
        print("- " + nom_president)


# Afficher l'ensemble des prénoms des présidents et/ou les modifier
def fonctionnalite_3(nom_fichier_presidents, noms_presidents):
    if not os.path.isfile(nom_fichier_presidents):  # Si le fichier "presidents.txt" n'existe pas, le créer
        # Le paramètre "x" permet de créer le fichier s'il n'existe pas
        open(nom_fichier_presidents, "x", encoding="utf-8")

    with open(nom_fichier_presidents, "r", encoding="utf-8") as fichier:
        contenu_fichier = fichier.read()

    tous_prenoms = True
    for nom_president in noms_presidents:
        if nom_president not in contenu_fichier:
            # Si un le nom d'un président récupéré dans les noms des fichiers n'est pas dans le fichier "presidents.txt"
            # Alors le contenu du fichier doit être modifié donc variable "tous_prenoms" passée à False
            tous_prenoms = False

    def modif_prenoms():  # Fonction interne qui permet d'associer des prénoms aux noms des présidents
        contenu_fichier_pres = ""
        for nom_pres in noms_presidents:
            print("Entrez le prénom que vous souhaitez associer à", nom_pres, ": ", end="")
            # On stocke les prénoms des présidents sous la forme "nom1:prénom1\nnom2:prénom2\n..."
            contenu_fichier_pres += nom_pres + ":" + input() + "\n"
        with open(nom_fichier_presidents, "w", encoding="utf-8") as fichier_pres:
            fichier_pres.write(contenu_fichier_pres)

    if not tous_prenoms:
        input_utilisateur = input("Certains présidents n'ont pas de prénoms associés à leur nom.\n"
                                  "Entrez \"o\" pour ajouter les prénoms : ")
        if input_utilisateur == "o":
            modif_prenoms()
    else:  # Si tous les présidents ont un prénom associé, alors on se contente de les afficher
        print("Les prénoms associés aux présidents sont :")
        with open(nom_fichier_presidents, "r", encoding="utf-8") as fichier:
            for ligne in fichier:
                ligne_split = ligne.split(":")  # On récupère les noms/prénoms sous forme de listes
                # Afin de les afficher sous la forme - Nom : Prénom
                print("- " + ligne_split[0] + " : " + ligne_split[1], end="")  # end="" car ligne_split[1] contient "\n"

        input_utilisateur = input("\nSouhaitez vous modifier les prénoms associés aux noms des présidents ?\n"
                                  "Entrez \"o\" pour modifier les prénoms : ")
        if input_utilisateur == "o":  # On propose à l'utilisateur de modifier les prénoms s'il le souhaite
            modif_prenoms()


# Fonctionnalité n°4 (même principe que la fonctionnalité n°2)
def fonctionnalite_4(liste_mots_corpus, noms_fichiers, matrice):
    print("Les mots les moins importants dans le corpus de documents sont :")
    for mot in fct_mat.tf_idf_nul(liste_mots_corpus, noms_fichiers, matrice):
        print("- " + mot)


# Fonctionnalité n°5 (même principe que la fonctionnalité n°2)
def fonctionnalite_5(liste_mots_corpus, noms_fichiers, matrice):
    print("Les mots ayant le score TF-IDF le plus élevé sont :")
    for mot in fct_mat.tf_idf_max(liste_mots_corpus, noms_fichiers, matrice):
        print("- " + mot)


def fonctionnalite_6(noms_presidents, liste_mots_corpus, noms_fichiers, matrice, nom_repertoire):  # Fonctionnalité n°6
    reponse_valide = False

    while not reponse_valide:  # Tant que l'utilisateur n'entre pas un nom de président présent dans le corpus
        nom_president = input("Entrez le nom du président choisi : ")

        if nom_president in noms_presidents:  # Si le président existe, on affiche ses mots les plus répétés
            reponse_valide = True
            liste_mot_max_pres = fct_mat.mot_max_president(liste_mots_corpus, noms_fichiers, matrice, nom_president,
                                                           nom_repertoire)
            print("\nLes mots les plus répétés par le président", nom_president, "sont :")
            for mot in liste_mot_max_pres:
                print("- " + mot)
        else:
            print("\nErreur : Veuillez entrer un nom de président présent dans le corpus de documents (",
                  end="")
            # On indique à l'utilisateur les noms qu'il a le droit d'entrer
            for indice_nom in range(len(noms_presidents) - 1):
                print(noms_presidents[indice_nom], end=", ")
            print(noms_presidents[-1] + ")\n")


def fonctionnalite_7(noms_fichiers, nom_repertoire):  # Fonctionnalité n°7
    mot_recherche = input("Entrez le mot recherché : ")
    return_mot_enonce_president = fct_mat.mot_enonce_president(noms_fichiers, nom_repertoire, mot_recherche)

    if not return_mot_enonce_president[0]:  # Si la liste contenant les présidents qui ont énoncé le mot est vide :
        print('\nAucun président n\'a énoncé le mot "' + mot_recherche + '".')
    else:
        print('\nLes présidents qui ont énoncé le mot "' + mot_recherche + '" sont :')
        for nom_president in return_mot_enonce_president[0]:
            print("- " + nom_president)

        print("\nLes présidents qui l'ont énoncé le plus de fois sont :")
        for nom_president in return_mot_enonce_president[1]:
            print("- " + nom_president)


def fonctionnalite_8(noms_fichiers, nom_repertoire):  # Fonctionnalité n°8
    mot_recherche = input("Entrez le mot recherché : ")
    print('\nLe premier président à utiliser le mot "' + mot_recherche + '" est :',
          fct_mat.premier_president_mot(noms_fichiers, nom_repertoire, mot_recherche))


def fonctionnalite_9(liste_mots_corpus, noms_fichiers, matrice, nom_repertoire):  # Fonctionnalité n°9
    print("Les mots évoqués par tous les présidents (sauf les mots dits \"non importants\") sont :")
    for mot in fct_mat.mots_tous_presidents(liste_mots_corpus, noms_fichiers, matrice, nom_repertoire):
        print("- " + mot)


# Fonctionnalité n°10 : Affichage de la matrice TF-IDF sous forme de tableau
def fonctionnalite_10(noms_fichiers, liste_mots_corpus, matrice):

    # Fonction interne permettant de retourner le mot le plus long d'une liste de mots
    def taille_mot_plus_long(liste_mots):
        taille_max = 0

        for mot in liste_mots:
            longueur_mot = len(mot)
            if longueur_mot > taille_max:
                taille_max = longueur_mot

        return taille_max

    # Fonction interne permettant de compléter une chaîne de caractères avec des espaces en fonction d'une taille max
    def ajuster_espaces(chaine, taille_max):
        taille_restante = taille_max + 1 - len(chaine)
        return chaine + taille_restante * " "  # Complétion de la chaîne avec des espaces en fonction de taille_restante

    # Récupération des termes les plus long pour adapter le tableau
    noms_fichiers_plus_long = taille_mot_plus_long(noms_fichiers)
    mot_plus_long = taille_mot_plus_long(liste_mots_corpus)

    # Affichage de x * " " pour correspondre à la taille du plus grand mot
    print((mot_plus_long + len("|  |")) * " ", end="")
    for _ in range(len(noms_fichiers) - 1):
        # Puis x * "_" en fonctione des bordures, espaces et tailles des noms de fichiers
        print((noms_fichiers_plus_long + len(" | ")) * "_", end="")
    print((noms_fichiers_plus_long + len("  ")) * "_")

    # Deuxième ligne; premier espace correspondant à la taille du plus grand mot
    print((mot_plus_long + len("|  ")) * " ", end="")
    for nom_fichier in noms_fichiers:  # Affichage des noms des fichiers avec bordures
        print("| " + ajuster_espaces(nom_fichier, noms_fichiers_plus_long), end="")
    print("|")

    def fermer_tableau():  # Fonction interne permettant de fermer le tableau à chaque nouvelle ligne
        print((mot_plus_long + len("  ")) * "_", end="")
        for _ in range(len(noms_fichiers)):
            print("|__" + noms_fichiers_plus_long * "_", end="")
        print("|")

    print(" ", end="")
    fermer_tableau()

    # On étend le tableau en affichant tous les mots puis en le fermant grâce à la fonction "fermer_tableau"
    for indice_mot in range(len(liste_mots_corpus)):
        print("| " + ajuster_espaces(liste_mots_corpus[indice_mot], mot_plus_long), end="")
        for indice_fichier in range(len(noms_fichiers)):
            print("| " + ajuster_espaces(str(matrice[indice_mot][indice_fichier]), noms_fichiers_plus_long), end="")
        print("|\n|", end="")
        fermer_tableau()


# --------------------------------------------- Fonction principale --------------------------------------------- #
def main():
    # Initialisations des constantes : noms de répertoires qui peuvent potentiellement changer et noms de fichiers
    NOM_REPERTOIRE_DISCOURS = "speeches"
    NOM_REPERTOIRE_NETTOYE = "cleaned"
    NOM_FICHIER_PRESIDENTS = "presidents.txt"  # Les prénoms à partir des noms seront stockés dans ce fichier

    noms_fichiers = fct_mat.liste_fichiers(NOM_REPERTOIRE_DISCOURS, "txt")

    noms_presidents = fct_mat.recup_noms_presidents(noms_fichiers)

    # Nettoyage des fichiers (suppression des caractères spéciaux, etc.)
    fct_mat.nettoyage_complet_fichiers(NOM_REPERTOIRE_NETTOYE, noms_fichiers, NOM_REPERTOIRE_DISCOURS)

    # On récupère l'IDF de tous les mots ici puisqu'il est commun à tous les fichiers
    idf_total = fct_mat.calcul_idf_total(noms_fichiers, NOM_REPERTOIRE_NETTOYE)

    # On récupère le tuple retourné par la fct "creation_matrice_corpus" (Liste des fichiers, liste des mots, matrice)
    liste_mots_corpus, matrice_corpus = fct_mat.creation_matrice_corpus(noms_fichiers, NOM_REPERTOIRE_NETTOYE,
                                                                        idf_total)

    print("\nBienvenue sur le ChatBot de Clément PINTO RIBEIRO et de Ismaël RADOUANE.\n")

    demander_premier_numero = True

    while demander_premier_numero:

        print("\nVeuillez entrer \"1\" pour accéder au ChatBot "
              "ou entrer \"2\" pour accéder aux différentes fonctionnalités du programme.\n")

        reponse_utilisateur = input("Entrez le numéro choisi : ")
        # Tant que l'utilisateur ne répond pas '1' ou '2', ou 'q'
        while reponse_utilisateur not in ["1", "2", "q"]:
            print("\nErreur : Veuillez entrer les nombres \"1\" ou \"2\", ou \"q\" pour quitter.\n")
            reponse_utilisateur = input("Entrez le numéro choisi : ")

        if reponse_utilisateur == "1":
            acceder_chatbot()

        elif reponse_utilisateur == "2":
            demander_deuxieme_numero = True

            while demander_deuxieme_numero:
                print("\nPour accéder aux différentes fonctionnalités, veuillez entrer le numéro associé à celles-ci :"
                      "\n\n"
                      "1. Lire la notice d'utilisation\n"
                      "2. Accéder aux noms des présidents\n"
                      "3. Changer/Accéder aux prénoms des présidents\n"
                      "4. Afficher les mots les moins importants dans le corpus de documents\n"
                      "5. Afficher les mots ayant le score TF-IDF le plus élevé\n"
                      "6. Afficher les mots les plus répétés par le président choisi\n"
                      "7. Afficher les noms des présidents qui ont parlé du mot choisi\n"
                      "8. Afficher le premier président à utiliser le mot choisi\n"
                      "9. Afficher les mots évoqués par tous les présidents (sauf les mots dits \"non importants\")\n"
                      "10. Accéder à la matrice TF-IDF\n"
                      "Ou entrez \"q\" pour quitter\n")

                reponse_utilisateur = input("Entrez le numéro choisi : ")
                # Tant que l'utilisateur ne répond pas '1', '2', '3', '4', '5', '6', '7', '8', '9', '10' ou 'q'
                while reponse_utilisateur not in [str(nombre) for nombre in range(1, 11)] + ["q"]:
                    print("\nErreur : Veuillez entrer un nombre entier entre 1 et 10, ou \"q\" pour quitter.\n")
                    reponse_utilisateur = input("Entrez le numéro choisi : ")

                print()

                # En fonction de la réponse de l'utilisateur, on exécute la fonctionnalité associée
                if reponse_utilisateur == "1":
                    fonctionnalite_1()

                elif reponse_utilisateur == "2":
                    fonctionnalite_2(noms_presidents)

                elif reponse_utilisateur == "3":
                    fonctionnalite_3(NOM_FICHIER_PRESIDENTS, noms_presidents)

                elif reponse_utilisateur == "4":
                    fonctionnalite_4(liste_mots_corpus, noms_fichiers, matrice_corpus)

                elif reponse_utilisateur == "5":
                    fonctionnalite_5(liste_mots_corpus, noms_fichiers, matrice_corpus)

                elif reponse_utilisateur == "6":
                    fonctionnalite_6(noms_presidents, liste_mots_corpus, noms_fichiers, matrice_corpus,
                                     NOM_REPERTOIRE_NETTOYE)

                elif reponse_utilisateur == "7":
                    fonctionnalite_7(noms_fichiers, NOM_REPERTOIRE_NETTOYE)

                elif reponse_utilisateur == "8":
                    fonctionnalite_8(noms_fichiers, NOM_REPERTOIRE_NETTOYE)

                elif reponse_utilisateur == "9":
                    fonctionnalite_9(liste_mots_corpus, noms_fichiers, matrice_corpus, NOM_REPERTOIRE_NETTOYE)

                elif reponse_utilisateur == "10":
                    fonctionnalite_10(noms_fichiers, liste_mots_corpus, matrice_corpus)

                elif reponse_utilisateur == "q":
                    demander_deuxieme_numero = False  # La deuxième boucle "while" s'arrête

                print()

                if demander_deuxieme_numero:  # Si l'utilisateur n'a pas entré "q"
                    continuer = input("\nEntrez \"o\" pour accéder à une autre fonctionnalité : ")
                    if continuer != "o":  # Si l'utilisateur n'entre pas "o"
                        demander_deuxieme_numero = False

        elif reponse_utilisateur == "q":
            demander_premier_numero = False

        if demander_premier_numero:
            continuer = input("\nEntrez \"o\" pour retourner au menu principal : ")
            if continuer != "o":
                demander_premier_numero = False


if __name__ == "__main__":  # Exécution du programme principal (fonction "main()")
    main()
