import fonctions_matrice as fct_mat


def fonctionnalite_1():
    with open("README.txt", "r") as fichier:
        print(fichier.read())


def fonctionnalite_2(noms_presidents):
    print("Les noms des présidents présents dans le corpus de documents sont :")
    for nom_president in noms_presidents:
        print("- " + nom_president)


def fonctionnalite_3(nom_fichier_presidents, noms_presidents):
    with open(nom_fichier_presidents, "r") as fichier:
        contenu_fichier = fichier.read()
    tous_prenoms = True
    for nom_president in noms_presidents:
        if nom_president not in contenu_fichier:
            tous_prenoms = False

    def modif_prenoms():
        contenu_fichier = ""
        for nom_president in noms_presidents:
            print("Entrez le prénom que vous souhaitez associer à", nom_president, " : ", end="")
            contenu_fichier += nom_president + ":" + input() + "\n"
        with open(nom_fichier_presidents, "w") as fichier:
            fichier.write(contenu_fichier)

    if not tous_prenoms:
        input_utilisateur = input("Certains présidents n'ont pas de prénoms associés à leur nom.\n"
                                  "Entrez \"o\" pour ajouter les prénoms : ")
        if input_utilisateur == "o":
            modif_prenoms()
    else:
        print("Les prénoms associés aux présidents sont :")
        with open(nom_fichier_presidents, "r") as fichier:
            for ligne in fichier:
                ligne_split = ligne.split(":")
                print("- " + ligne_split[0] + " : " + ligne_split[1], end="")
        print()
        input_utilisateur = input("Souhaitez vous modifier les prénoms associés aux noms des présidents ?\n"
                                  "Entrez \"o\" pour modifier les prénoms : ")
        if input_utilisateur == "o":
            modif_prenoms()


def fonctionnalite_4(return_matrice_tf_idf):
    print("Les mots les moins importants dans le corpus de documents sont :")
    for mot in fct_mat.tf_idf_nul(return_matrice_tf_idf):
        print("- " + mot)


def fonctionnalite_5(return_matrice_tf_idf):
    print("Les mots les plus importants dans le corpus de documents sont :")
    for mot in fct_mat.tf_idf_max(return_matrice_tf_idf):
        print("- " + mot)


def fonctionnalite_6(noms_presidents, nom_repertoire_nettoye):
    reponse_valide = False

    while not reponse_valide:
        input_president = input("Entrez le nom du président choisi : ")

        if input_president in noms_presidents:
            reponse_valide = True
            liste_mot_max_pres = fct_mat.mot_max_president(nom_repertoire_nettoye, input_president)
            print("\nLes mots les plus répétés par le président", input_president, "sont :")
            for mot in liste_mot_max_pres:
                print("- " + mot)
        else:
            print("\nErreur : Veuillez entrer un nom de président présent dans le corpus de documents (",
                  end="")
            for indice_nom in range(len(noms_presidents) - 1):
                print(noms_presidents[indice_nom], end=", ")
            print(noms_presidents[-1] + ")\n")


def fonctionnalite_7(nom_repertoire_nettoye):
    input_mot = input("Entrez le mot recherché : ")
    return_mot_enonce_president = fct_mat.mot_enonce_president(nom_repertoire_nettoye, input_mot)

    if not return_mot_enonce_president[0]:
        print('\nAucun président n\'a énoncé le mot "' + input_mot + '".')
    else:
        print('\nLes présidents qui ont énoncé le mot "' + input_mot + '" sont :')
        for nom_president in return_mot_enonce_president[0]:
            print("- " + nom_president)

        print("\nLes présidents qui l'ont énoncé le plus de fois sont :")
        for nom_president in return_mot_enonce_president[1]:
            print("- " + nom_president)


def fonctionnalite_8(nom_repertoire_nettoye):
    input_mot = input("Entrez le mot recherché : ")
    print('\nLe premier président à utiliser le mot "' + input_mot + '" est :',
          fct_mat.premier_president_mot(nom_repertoire_nettoye, input_mot))


def fonctionnalite_9(return_matrice_tf_idf):
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


def main():
    NOM_REPERTOIRE_DISCOURS = "speeches"
    NOM_REPERTOIRE_NETTOYE = "cleaned"

    NOM_FICHIER_PRESIDENTS = "presidents.txt"  # Noms et prénoms stockés dans ce fichier

    noms_presidents = fct_mat.recup_noms_presidents(NOM_REPERTOIRE_DISCOURS)

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
            fonctionnalite_1()

        elif reponse_utilisateur == "2":
            fonctionnalite_2(noms_presidents)

        elif reponse_utilisateur == "3":
            fonctionnalite_3(NOM_FICHIER_PRESIDENTS, noms_presidents)

        elif reponse_utilisateur == "4":
            fonctionnalite_4(return_matrice_tf_idf)

        elif reponse_utilisateur == "5":
            fonctionnalite_5(return_matrice_tf_idf)

        elif reponse_utilisateur == "6":
            fonctionnalite_6(noms_presidents, NOM_REPERTOIRE_NETTOYE)

        elif reponse_utilisateur == "7":
            fonctionnalite_7(NOM_REPERTOIRE_NETTOYE)

        elif reponse_utilisateur == "8":
            fonctionnalite_8(NOM_REPERTOIRE_NETTOYE)

        elif reponse_utilisateur == "9":
            fonctionnalite_9(return_matrice_tf_idf)

        elif reponse_utilisateur == "q":
            demander_numero = False

        print()


main()
