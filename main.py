import fonctions_matrice as fct_mat


def afficher_notice_utilisation():
    with open("README.txt", "r") as fichier:
        contenu_fichier = ""
        for ligne in fichier:
            contenu_fichier += ligne
    print(contenu_fichier)


def afficher_noms_presidents(noms_presidents):
    print("Les noms des présidents présents dans le corpus de documents sont :")
    for nom_president in noms_presidents:
        print("- " + nom_president)


def acceder_prenoms_presidents(NOM_FICHIER_PRESIDENTS, noms_presidents):
    with open(NOM_FICHIER_PRESIDENTS, "r") as fichier:
        contenu_fichier = ""
        for ligne in fichier:
            contenu_fichier += ligne
    tous_prenoms = True
    for nom_president in noms_presidents:
        if nom_president not in contenu_fichier:
            tous_prenoms = False
    if not tous_prenoms:
        input_utilisateur = input("Certains présidents n'ont pas de prénoms associés à leur nom.\n"
                                  "Entrez \"o\" pour ajouter les prénoms : ")
        if input_utilisateur == "o":
            contenu_fichier = ""
            for nom_president in noms_presidents:
                print("Entrez le prénom que vous souhaitez associer à", nom_president, " : ", end="")
                contenu_fichier += nom_president + ":" + input() + "\n"
            with open(NOM_FICHIER_PRESIDENTS, "w") as fichier:
                fichier.write(contenu_fichier)
    else:
        print("Les prénoms associés aux présidents sont :")
        with open(NOM_FICHIER_PRESIDENTS, "r") as fichier:
            for ligne in fichier:
                ligne_split = ligne.split(":")
                print("- " + ligne_split[0] + " : " + ligne_split[1], end="")


def afficher_mot_moins_important(return_matrice_tf_idf):
    print("Les mots les moins importants dans le corpus de documents sont :")
    for mot in fct_mat.tf_idf_nul(return_matrice_tf_idf):
        print("- " + mot)











def main():
    NOM_REPERTOIRE_DISCOURS = "speeches"
    NOM_REPERTOIRE_NETTOYE = "cleaned"

    NOM_FICHIER_PRESIDENTS = "presidents.txt"  # Noms et prénoms stockés dans ce fichier

    noms_presidents = fct_mat.recup_noms_presidents(NOM_FICHIER_PRESIDENTS, NOM_REPERTOIRE_DISCOURS)

    fct_mat.nettoyage_complet_fichiers(NOM_REPERTOIRE_DISCOURS, NOM_REPERTOIRE_NETTOYE)

    return_matrice_tf_idf = fct_mat.creation_matrice(NOM_REPERTOIRE_NETTOYE)

    print("\nBienvenue sur le ChatBot de Clément PINTO RIBEIRO et de Ismaël RADOUANE.\n")

    demander_numero = True

    while demander_numero:
        print("\nPour accéder aux différents menus, veuillez entrer le numéro associé :\n\n"
              "1. Lire la notice d'utilisation\n"
              "2. Accéder aux noms des présidents\n"
              "3. Changer/Accéder aux prénoms des présidents\n"
              "4. Afficher la liste des mots les moins importants dans le corpus de documents\n"
              "5. Afficher la liste de mot ayant le score TF-IDF le plus élevé\n"
              "6. Afficher la liste de mot les plus répétés par le président choisi\n"
              "7. Afficher les noms des présidents qui ont parlé du mot choisi\n"
              "8. Afficher le premier président à utiliser le mot choisi\n"
              "9. Accéder à la matrice TF-IDF\n"
              "Ou entrez \"q\" pour quitter\n")

        reponse_accepte = False
        while not reponse_accepte:
            reponse_utilisateur = input("Entrez le numéro choisi : ")
            if reponse_utilisateur in [str(nombre) for nombre in range(1, 10)] + ["q"]:
                reponse_accepte = True
            else:
                print("\nErreur : Veuillez entrer un nombre entier entre 1 et 9\n")

        print()
        if reponse_utilisateur == "1":
            afficher_notice_utilisation()

        elif reponse_utilisateur == "2":
            afficher_noms_presidents(noms_presidents)

        elif reponse_utilisateur == "3":
            acceder_prenoms_presidents(NOM_FICHIER_PRESIDENTS, noms_presidents)

        elif reponse_utilisateur == "4":
            afficher_mot_moins_important(return_matrice_tf_idf)

        elif reponse_utilisateur == "5":
            afficher_mot_moins_important(return_matrice_tf_idf)

        elif reponse_utilisateur == "6":
            reponse_valide = False

            while not reponse_valide:
                input_president = input("Entrez le nom du président choisi : ")

                if input_president in noms_presidents:
                    reponse_valide = True
                    liste_mot_max_pres = fct_mat.mot_max_president(NOM_REPERTOIRE_NETTOYE, input_president)
                    print("\nLes mots les plus répétés par le président", input_president, "sont :")
                    for mot in liste_mot_max_pres:
                        print("- " + mot)
                else:
                    print("\nErreur : Veuillez entrer un nom de président présent dans le corpus de documents (",
                          end="")
                    for indice_nom in range(len(noms_presidents) - 1):
                        print(noms_presidents[indice_nom], end=", ")
                    print(noms_presidents[-1] + ")\n")

        elif reponse_utilisateur == "7":
            input_mot = input("Entrez le mot recherché : ")
            return_mot_enonce_president = fct_mat.mot_enonce_president(NOM_REPERTOIRE_NETTOYE, input_mot)

            print('\nLes présidents qui ont énoncé le mot "' + input_mot + '" sont :')
            for nom_president in return_mot_enonce_president[0]:
                print("- " + nom_president)

            print("\nLes présidents qui l'ont énoncé le plus de fois sont :")
            for nom_president in return_mot_enonce_president[1]:
                print("- " + nom_president)

        elif reponse_utilisateur == "8":
            input_mot = input("Entrez le mot recherché : ")
            print('\nLe premier président à utiliser le mot "' + input_mot + '" est :',
                  fct_mat.premier_president_mot(NOM_REPERTOIRE_NETTOYE, input_mot))

        elif reponse_utilisateur == "9":
            # FONCTION MAX TAILLE CHAINE DANS LISTE
            noms_fichiers, liste_mots, matrice = return_matrice_tf_idf

            def taille_mot_plus_long(liste_mots):
                taille_max = 0
                for mot in liste_mots:
                    longueur_mot = len(mot)
                    if longueur_mot > taille_max:
                        taille_max = longueur_mot

                return taille_max

            def ajuster_espaces(chaine, taille_max):
                taille_restante = taille_max + 1 - len(chaine)
                return chaine + taille_restante * " "

            noms_fichiers_plus_long = taille_mot_plus_long(noms_fichiers)
            mot_plus_long = taille_mot_plus_long(liste_mots)

            print((mot_plus_long + len("|  |")) * " ", end="")
            for _ in range(len(noms_fichiers) - 1):
                print((noms_fichiers_plus_long + len("  | ")) * "_", end="")
            print((noms_fichiers_plus_long + len("  |")) * "_")
            print((mot_plus_long + len("|  ")) * " ", end="")
            for nom_fichier in noms_fichiers:
                print("|  " + ajuster_espaces(nom_fichier, noms_fichiers_plus_long), end="")
            print("|")

            def fermer_tableau():
                print((mot_plus_long + len("  ")) * "_", end="")
                for _ in range(len(noms_fichiers)):
                    print("|___" + noms_fichiers_plus_long * "_", end="")
                print("|")

            print("_", end="")
            fermer_tableau()

            for indice_mot in range(len(liste_mots)):
                print("| " + ajuster_espaces(liste_mots[indice_mot], mot_plus_long), end="")
                for indice_fichier in range(len(noms_fichiers)):
                    print("| " + ajuster_espaces(str(matrice[indice_mot][indice_fichier]), noms_fichiers_plus_long) +
                          " ", end="")
                print("|\n|", end="")
                fermer_tableau()

        elif reponse_utilisateur == "q":
            demander_numero = False

        print()


main()
