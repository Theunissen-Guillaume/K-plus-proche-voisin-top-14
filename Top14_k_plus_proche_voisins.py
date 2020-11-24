#!/usr/bin/env python3
# coding: utf-8

try:            # Signale une erreur d'importation
    import csv                          # tableur
    import matplotlib.pyplot as plt     # graphique
    from math import sqrt               # Racine carré
    import sys                          # Exit
except ImportError:
    print("Erreur lors de l'import de bibliothèque.")


def extraction_donnee(fname, donnee):
    '''
    Extrait les données du .csv sous forme de liste de tuple.
    :param fname: Nom du fichier
    :param donnee: Liste vide
    :return: Liste pleine "donnee"
    '''

    with open(fname, 'r', encoding='utf8') as fichier_lecture:  # On ouvre fname, en utf8
        reader = csv.reader(fichier_lecture, delimiter=';')  # On cree le reader de csv, qui separent chaque ligne par ";"
        for ligne in reader:
            donnee.append(tuple(ligne))  # On stocke tout dans une liste de tuple
    return donnee


def extraire_equipe(donnee):
    '''
    Garde uniquement les données liées à une équipe qui est demandé. Si aucune n'est précisée, tout est gardé.
    :param donnee: Liste contenant les donnees des joueurs
    :return: Liste_equipe_demander
    '''

    validation = 0
    liste_equipe_demander = []
    equipe_precise = str(input("Une equipe precise ? y/n"))

    if equipe_precise == "y":   # Si l'utilisateur soouhaite une équipe précise :
        while validation != 1:
            equipe_demande = str(input("Choisissez une équipe (nom commencant par une majuscule ?"))
            for i in donnee:    # On parcours chaque lignes de donnee
                if i[0] == equipe_demande:  # Si les noms d'équipe correspond, on ajoute la ligne à liste_equipe_demander
                    liste_equipe_demander.append(i)
                    validation = 1   # On quite le while
            if validation != 1:     # Aucune équipe n'a été trouver
                print("Equipe non présente ou mal ortographiée.")
                equipe_precise = str(input("Une equipe precise ? y/n"))
                if equipe_precise == "n":               # on propose de choisir une nouvelle équipe -> nouvelle itération
                    liste_equipe_demander = donnee[:]   # Ou on prend toute les équipe
                    return liste_equipe_demander
        return liste_equipe_demander

    elif equipe_precise == "n":
        liste_equipe_demander = donnee[:]
        return liste_equipe_demander    # On retourne toute les équipes

    else:
        print("Erreur de saisie")   # Si la reponse est differente de "y" ou "n" :
        sys.exit()


def representation(liste_equipe_demander, taille, masse):
    '''
    Construit le graphique représentant les joueurs en fonction de leurs masse et taille.
    :param liste_equipe_demander: Liste contenant tout les joueurs utiles
    :param taille: Taille de l'utilisateur
    :param masse: Masse de l'utilisateur
    :return: Matrice contenant les listes de tuple de joueurs, trié par poste
    '''

    matrice = [[], [], [], [], [], []]  # Matrice contenant 6 emplacements vides pour les 6 postes
    label = ["Avant", "2ème ligne", "3ème ligne", "Demi", "Trois-Quarts", "Arrière"]    # Poste -> label légende
    color = ["blue", "red", "green", "purple", "brown", "yellow"]   # Couleurs du graphique
    marker = ["x", "+", "s", "o", "d", "^"]     # Marker du graphique

    for i in liste_equipe_demander:     # Regroupe les joueurs dans les 6 listes de la matrice en fonction de leurs poste
        for c in range(0, 6):
            if i[3] == label[c]:        # Si le poste du joueurs correspond à un label, il est ajouté à la matrice[c]
                matrice[c].append(i)    # matrice[c] : c correspond au labels
                break

    for index in range(0, 6):   # Permet de créé le graphique
        for p in matrice[index]:    # p = liste des joueurs d'un poste
            plt.plot(int(p[5]), int(p[6]), c=color[index], marker=marker[index])
        plt.plot(int(matrice[index][0][5]), int(matrice[index][0][6]), c=color[index], marker=marker[index], label=label[index])
        '''
        Tout se fait avec l'index. Dans le premier ligne, on place la point de marker index, couleur index, et joueurs[5][6]
        correspondant à la taille et masse. 
        La seconde ligne place un point, deja placé dans la première, servant à créé la légende en lui affectant un label = un poste
        Cela evite d'avoir un label à chaque joueur, et d'avoir une légende incompréhensible
        '''
    plt.plot(taille, masse, c='black', marker='o', label="Vous")  # Place le point correspondant à l'utilisateur

    if len(liste_equipe_demander) > 400:
        plt.title("Top 14")     # Si il y a beaucoup de joueurs = plusieurs équipe -> titre = TOP 14
    else:
        plt.title("Equipe de " + matrice[0][0][0])      # Titre = Nom de l'équipe
    plt.xlabel("Taille en cm")      # Légende des axes
    plt.ylabel("Masse en kg")
    plt.legend()    # Affiche la légende
    plt.show()      # Affiche le graphique
    return matrice


def distance(matrice, taille, masse):
    '''
    Calcule la distance sur le graphique de l'utilisateur avec tout les autres joueurs.
    :param matrice: [[(j1, avant),(j2, avant)], [(j1, demi), j2, demi)]]...
    :param taille: Taille de l'utilisateur
    :param masse: Masse de l'utilisateur
    :return: Liste tout_racine, contenant une 6 listes pour les distances des joueurs des 6 postes
    '''

    racine = []
    toute_racine = []
    for c in matrice:  # [[(j1, avant),(j2, avant)], [(j1, demi), j2, demi)]]
        for a in c:
            liste = sqrt((int(a[5]) - taille) ** 2 + (int(a[6]) - masse) ** 2)  # Formule de la distance entre 2 points
            racine.append(liste)    # Ajoute à racine, liste qui sert de tampon
        trie = sorted(racine)
        toute_racine.append(trie[:])    # on l'ajoute à tout_racine de manière indépendante
        racine.clear()
    return toute_racine


def clasification(tout_racine):
    '''
    Calcule la moyenne des distances grace à l'algorythme des k plus proche voisinn
    :param tout_racine: Liste des racines
    :return: Nothing
    '''
    moyenne = {}
    poste_fini = ""
    poste = ["Avant", "2ème ligne", "3ème ligne", "Demi", "Trois-Quart", "Arrière"]
    test = 0
    index = 0
    k = int(input("K des K plus proche voisin ? \n"))

    for i in tout_racine:
        for a in range(0, k):
            try:
                test += i[a]    # On additione les k premières valeurs
            except IndexError:
                break
        test = test / k     # On divise par k -> moyenne
        moyenne[poste[index]] = test    # On l'ajoute au dictionnaire moyenne, avec comme nom, le poste, et valeur, test
        test = 0
        index += 1
    index = 0
    for key in sorted(moyenne, key=moyenne.get):    # On trie les valeurs dans l'ordre croissant
        print(key + " : moyenne des distances -> " + str(moyenne[key]))    # On les affiches
        if index == 0:  # On prend le plus petit, ce sera la poste_fini, celui qui correspond le mieux à l'utilisateur
            poste_fini = key
        index += 1
    print("\n" + "Le poste : " + poste_fini + " , est celui qui vous correspond le plus.")
    return


masse = float(input("Votre masse ?"))
taille = float(input("Votre taille ?"))
donnee = []
fname = "JoueursTop14.csv"

clasification(distance(representation(extraire_equipe(extraction_donnee(fname, donnee)), taille, masse), taille, masse))


