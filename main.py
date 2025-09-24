import database




def reinitialisation_des_donnees(curseur):
    curseur.execute("""DELETE FROM Reference""")
    curseur.execute("""DELETE FROM Etiquette""")
    curseur.execute("""DELETE FROM Auteur""")


















def menu_principal():

    print("\nVeuillez choisir une option:")
    print("1. Ajouter une référence")
    print("2. Supprimer une référence")
    print("3. Ajouter des étiquettes a une référence")
    print("4. Retirer des étiquettes d'une référence")
    print("5. Ajouter des auteurs a une référence")
    print("6. Retirer des auteurs d'une référence")
    print("7. Rechercher par titre")
    print("8. Rechercher par auteur")
    print("9. Rechercher par étiquette")
    print("10. Modifier une référence")
    print("11. Modifier une étiquette")
    print("12. Modifier un(e) auteur(e)")
    print("-1. quitter")
    choix = input("Choix: ")
    return choix


#choix 1
def menu_ajouter_reference(connexion):
    print("\nVeuillez entrez les informations suivantes: ")

    titre = input("Titre: ")
    if titre == "":
        print("Entrée invalide, annulation de la creation de la reference")
        return

    if database.verification_element(connexion, titre, "Reference"):
        print("Le titre existe déjà, retour au menu principal")
        return
    
    revue = input("revue: ")
    if revue == "":
        print("Entrée invalide, annulation de la creation de la reference")
        return


    annee = input("Annee: ")
    if (not annee.isdigit()):
        print("l'année n'est pas du bon format, Annulation de la creation de la reference")
        return
    annee = int(annee)

    hyperlien = input("Hyperlien: ")
    if hyperlien == "":
        print("Entrée invalide, annulation de la creation de la reference")
        return

    description = input("Brève description: ")
    print("Veuillez entrez le nom de l'auteur(e) principal(e)")
    nom = input("Nom: ")

    
    if (database.ajouter_reference(connexion, titre, revue, annee, hyperlien, description, nom)):
        print("Référence ajoutée avec succès")
        #ajout des auteurs
        while True:
            print("Veuillez entrez le nom d'un auteur additionnel (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                break
            if nom == "":
               print("Entrée invalide")
            elif(database.ajouter_auteur(connexion, titre, nom)):
                print("Auteur(e) ajouté(e)")
            else:
                print("Auteur(e) déjà ajouté(e)")    

        #ajout des etiquettes
        while True:
            print("\nVeuillez entrez le nom de l'etiquette a ajouter (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                break
            if nom == "":
               print("Entrée invalide")
            elif(database.ajouter_etiquette(connexion, titre, nom)):
                print("Étiquette ajoutée")
            else:
                print("Étiquette déjà ajoutée")
    else:
        print("Probleme lors de l'ajout de la reference")
    
         
     
#choix 2
def menu_supprimer_reference(connexion):
    print("\nVeuillez entrez le titre de la reference a supprimer: ")
    titre = input("Titre: ")
    if(not database.verification_element(connexion, titre, "Reference")):
        print("Référence inexistante")
        return
    if(database.supprimer_reference(connexion, titre)):
        print("Reference supprimee")
    else:
        print("Probleme avec la suppresion de la reference")


#choix 3
def menu_ajouter_etiquette(connexion):
    print("\nVeuillez entrez le titre de l'article qui recoit une nouvelle etiquette (-1 pour terminer): ")
    titre = input("Titre: ")
    if(not database.verification_element(connexion, titre, "Reference")):
        print("Reference inexistante, retour au menu principal")
    else:
        while True:
            print("Veuillez entrez le nom de l'etiquette a ajouter (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                return
            elif nom == "":
                print("Entrée invalide")
            elif(database.ajouter_etiquette(connexion, titre, nom)):
                print("Etiquette(s) ajoutee(s)")
            else:
                print("Probleme avec l'ajout de l'etiquette")


#choix 4
def menu_supprimer_etiquette(connexion):
    print("\nVeuillez entrez le titre de l'article auquel on enleve des etiquettes (-1 pour terminer): ")
    titre = input("Titre: ")
    if(not database.verification_element(connexion, titre, "Reference")):
        print("Reference inexistante, retour au menu principal")
    else:
        while True:
            print("Veuillez entrez le nom de l'etiquette a retirer (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                return
            if(database.supprimer_etiquette(connexion, titre, nom)):
                print("Etiquette retiree")
            else:
                print("Probleme avec le retrait de l'etiquette")
     
#choix 5
def menu_ajouter_auteur(connexion):
    print("\nVeuillez entrer le titre de l'article qui recoit un(e) nouvel(le) auteur(e) (-1 pour terminer): ")
    titre = input("Titre: ")
    if(not database.verification_element(connexion, titre, "Reference")):
        print("Reference inexistante, retour au menu principal")
    else:
        while True:
            print("Veuillez entrer le nom de l'auteur(e) a ajouter (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                return
            elif nom == "":
                print("Entrée invalide")
            elif(database.ajouter_auteur(connexion, titre, nom)):
                print("auteur(e) ajoute(e)")
            else:
                print("Probleme avec l'ajout de l'auteur(e)")


#choix 6
def menu_supprimer_auteur(connexion):
    print("\nVeuillez entrer le titre de l'article auquel on enleve un(e) auteur(e) (-1 pour terminer): ")
    titre = input("Titre: ")
    if(not database.verification_element(connexion, titre, "Reference")):
        print("Reference inexistante, retour au menu principal")
    else:
        while True:
            print("Veuillez entrer le nom de l'auteur(e) a retirer (-1 pour terminer): ")
            nom = input("Nom: ")
            if (nom == "-1"):
                return
            if(database.supprimer_auteur(connexion, titre, nom)):
                print("Auteur(e) retire(e)")
            else:
                print("Probleme avec le retrait de l'auteur(e)")


#choix 7
def menu_recherche_par_titre(connexion):
    print("\nVeuillez entrer le titre de l'article a chercher: ")
    titre = input("Titre: ")
    if database.verification_element(connexion, titre, "Reference"):
        database.impression_par_titre(connexion, titre)
    else:
        print("Reference inexistante, retour au menu principal")


#choix 8
def menu_recherche_par_auteur(connexion):
    print("\nVeuillez entrer nom de l'auteur: ")
    nom = input("Auteur(e): ")
    if database.verification_element(connexion, nom, "Auteur"):
        database.impression_par_auteur(connexion, nom)
    else:
        print("Auteur(e) inexistant(e), retour au menu principal")


#choix 9
def menu_recherche_par_etiquette(connexion):
    print("\nVeuillez entrer le nom de l'etiquette a chercher: ")
    nom = input("nom: ")
    if database.verification_element(connexion, nom, "Etiquette"):        
        database.impression_par_etiquette(connexion, nom)
    else:
        print("Etiquette inexistante, retour au menu principal")


#choix 10
def menu_modifier_reference(connexion):
    print("\nVeuillez entrer le titre de l'article à modifier: ")
    ancien_titre = input("Titre: ")
    if database.verification_element(connexion, ancien_titre, "Reference"):
        database.impression_par_titre(connexion, ancien_titre)
        nouveau_titre = input("Nouveau titre: ")
        if nouveau_titre == "":
            print("Entrée invalide, annulation de la modification")
            return
        if not database.verification_element(connexion, nouveau_titre, "Reference") or ancien_titre == nouveau_titre:  
            revue = input("Nouvelle revue: ")
            if revue == "":
                print("Entrée invalide, annulation de la modification")
                return
            annee = input("Nouvelle année de publication: ")
            if(not annee.isdigit()):
                print("l'année n'est pas du bon format, Annulation de la creation de la reference")
                return
            annee = int(annee)     
            hyperlien = input("Nouvel hyperlien: ")
            if hyperlien == "":
                print("Entrée invalide, annulation de la modification")
                return
            description = input("Nouvelle description: ")
            database.modifier_reference(connexion, ancien_titre, nouveau_titre, revue, annee, hyperlien, description)
            print("Référence mise à jour")
        else:
         print("Ce titre est en conflit avec un titre déjà dans la base, retour au menu principal")           
    else:
        print("Reference inexistante, retour au menu principal")


#choix 11
def menu_modifier_etiquette(connexion):
    print("\nVeuillez entrer le nom de l'etiquette à modifier: ")
    nom = input("nom étiquette: ")
    if database.verification_element(connexion, nom, "Etiquette"):
        nouveau_nom = input("Nouveau nom: ")
        if nouveau_nom == "":
            print("Entrée invalide, annulation de la modification")
            return
        if not database.verification_element(connexion, nouveau_nom, "Etiquette") or nom == nouveau_nom:
            database.modifier_etiquette(connexion, nom, nouveau_nom)
            print("Nom d'étiquette mis à jour")
        else:
            print("Cette étiquette existe déjà")
    else:
        print("Étiquette inexistante, retour au menu principal")

#choix 12
def menu_modifier_auteur(connexion):
    print("\nVeuillez entrer nom de l'auteur(e) à modifier: ")
    nom = input("Auteur(e): ")
    if database.verification_element(connexion, nom, "Auteur"):
        nouveau_nom = input("Nouveau nom: ")
        if nouveau_nom == "":
            print("Entrée invalide, annulation de la modification")
            return
        if not database.verification_element(connexion, nouveau_nom, "Auteur") or nom == nouveau_nom:
            database.modifier_auteur(connexion, nom, nouveau_nom)
            print("Nom d'auteur(e) mis à jour")
        else:
            print("Cet(te) auteur(e) existe déjà")
    else:
        print("Étiquette inexistante, retour au menu principal")

###DEBUGGING#######


def main():
    database.initialiser() #creation de la base de donnee si elle n'existe pas
    connexion = database.connecter() #connexion a la base de donnee
    database.executer_ficher_sql(connexion, "./tables.sql") #creation des tables si elle n'existe pas

    curseur = connexion.cursor()


    #pour donnee tests seulement
    reinitialisation_des_donnees(curseur)
    database.executer_ficher_sql(connexion, "./test_data.sql") #données tests
    #fin pour donnees tests

    while True:
        choix = menu_principal()
        if choix == "1":
            menu_ajouter_reference(connexion)
        elif choix == "2":
            menu_supprimer_reference(connexion)
        elif choix == "3":
            menu_ajouter_etiquette(connexion)
        elif choix == "4":
            menu_supprimer_etiquette(connexion)
        elif choix == "5":
            menu_ajouter_auteur(connexion)
        elif choix == "6":
            menu_supprimer_auteur(connexion)
        elif choix == "7":
            menu_recherche_par_titre(connexion)
        elif choix == "8":
            menu_recherche_par_auteur(connexion)
        elif choix == "9":
            menu_recherche_par_etiquette(connexion)
        elif choix == "10":
            menu_modifier_reference(connexion)
        elif choix == "11":
            menu_modifier_etiquette(connexion)
        elif choix == "12":
            menu_modifier_auteur(connexion)
        elif choix == "-1":
            return
    
if __name__ == "__main__":
    main()