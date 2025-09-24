import mysql.connector
from mysql.connector import Error
import time
from tabulate import tabulate





#cree une connexion avec le serveur sql et crée la base de données
def initialiser():
    try:
        connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="le_1root_desql",
        )
        connexion.cursor().execute("""CREATE DATABASE IF NOT EXISTS bozo_outil_bibliographique""")
        print("Base de données créée")
        return connexion
    except Error as error:
        print(f"Erreur avec la création de la base de données: {error}")
        return None




#cree une connexion avec le serveur sql et la base de donnees
def connecter():
    try:
        connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="le_1root_desql",
            database="bozo_outil_bibliographique",
            allow_local_infile=True
        )
        print("Connexion complete")
        return connexion
    except Error as error:
        print(f"Incapable de connecter. Erreur: {error}")
        return None




#sert a rouler un fichier sql
def executer_ficher_sql(connexion, chemin):
    try:
        with open(chemin, "r") as fichier:
            readFile = fichier.read()
    except IOError:
        print("Le fichier ne peut etre ouvert.")

    commandes = readFile.split(";")
    curseur = connexion.cursor()
    for commande in commandes:
        try:
            curseur.execute(commande)
        except Error as erreur:
            print(f"Erreur sur '{commande}': {erreur}")
    connexion.commit()
    curseur.close()





#cette fonction demande le nom d'un auteur principal afin de faire l'ajout de la reference avec un auteur principal qui est requis
def ajouter_reference(connexion, titre, revue, annee, hyperlien, description, nom):
    try:
        with connexion.cursor() as curseur:
            curseur.execute("""INSERT INTO Reference (titre, revue, annee, hyperlien, description)
                            VALUES (%s, %s, %s, %s, %s)""", (titre, revue, annee, hyperlien, description))
            ajouter_auteur(connexion, titre, nom)
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False




#supprime un reference avec son titre et va nettoyer les autres tableaux qui ont maintenant des auteurs et etiquettes orpheline
def supprimer_reference(connexion, titre):
    try:
        with connexion.cursor() as curseur:

            #recherche des auteurs
            curseur.execute("""SELECT r_a.idAuteur 
                            FROM Reference r
                            JOIN Reference_Auteur r_a ON r.idReference = r_a.idReference
                            WHERE r.titre = %s""", (titre,))
            idAuteurs = curseur.fetchall()


            #rechercher des etiquettes
            curseur.execute("""SELECT r_e.idEtiquette 
                            FROM Reference r
                            JOIN Reference_Etiquette r_e ON r.idReference = r_e.idReference
                            WHERE r.titre = %s""", (titre,))
            idEtiquettes = curseur.fetchall()


            #suppression de la reference. Les donnees dans les tables de jonction sont egalement supprimee
            curseur.execute("""DELETE FROM Reference
                            WHERE Reference.titre = %s""", (titre,))


            #suppression des etiquettes orphelines
            for idEtiquette in idEtiquettes:
                curseur.execute("""DELETE FROM Etiquette
                                WHERE idEtiquette = %s
                                AND idEtiquette NOT IN (SELECT idEtiquette FROM Reference_Etiquette)""", (idEtiquette[0],))
                
            #suppression des auteurs orphelins    
            for idAuteur in idAuteurs:
                curseur.execute("""DELETE FROM Auteur
                                WHERE idAuteur = %s
                                AND idAuteur NOT IN (SELECT idAuteur FROM Reference_Auteur)""", (idAuteur[0],))
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False



#ajoute l'etiquette et son entree dans la table de jonction en lien avec la reference
def ajouter_etiquette(connexion, titre, nom):
    try:
        with connexion.cursor() as curseur:

            #cherche l'etiquette et l'ajoute s'il n'existe pas
            curseur.execute("""SELECT idEtiquette FROM Etiquette WHERE nom = %s""", (nom,))
            temp = curseur.fetchone()
            if temp is None:
                curseur.execute("""INSERT INTO Etiquette (nom) VALUES (%s)""", (nom,))
                curseur.execute("""SELECT idEtiquette FROM Etiquette WHERE nom = %s""", (nom,))
                idEtiquette = curseur.fetchone()[0]
            else:
                idEtiquette = temp[0]

            #recherche de la reference
            curseur.execute("""SELECT idReference FROM Reference WHERE titre = %s""", (titre,))
            idReference = curseur.fetchone()[0]            


            #ajout dans la table de jonction
            curseur.execute("""INSERT INTO Reference_Etiquette (idReference, idEtiquette)
                            VALUES (%s, %s)""", (idReference, idEtiquette))
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False




#la foonction ci-dessous verifie tout d'abord que la reference et l'etiquette sont lies par la table de jonction, elle supprime le lien et supprimera l'etiquette si elle devient orpheline
def supprimer_etiquette(connexion, titre, nom):
    try:
        with connexion.cursor() as curseur:
            curseur.execute("""SELECT idEtiquette FROM Etiquette WHERE nom = %s""", (nom,))
            temp = curseur.fetchone()
            if temp is None:
                return False
            idEtiquette = temp[0]

            curseur.execute("""SELECT idReference FROM Reference WHERE titre = %s""", (titre,))
            temp = curseur.fetchone()
            if temp is None:
                return False
            idReference = temp[0]

            #verifie l'existance du lien entre la reference et l'etiquette en question
            curseur.execute("""SELECT * FROM Reference_Etiquette WHERE idReference = %s AND idEtiquette = %s""", (idReference,idEtiquette))
            resultat = curseur.fetchone()
            if resultat is None:
                return False
            #supprime le lien
            curseur.execute("""DELETE FROM Reference_Etiquette r_e 
                            WHERE r_e.idReference = %s AND r_e.idEtiquette = %s""", (idReference, idEtiquette))
            
            #supprime l'etiquette n'ayant plus aucune reference
            curseur.execute("""DELETE FROM Etiquette
                            WHERE idEtiquette = %s
                            AND NOT EXISTS (
                            SELECT 1 FROM Reference_Etiquette
                            WHERE idEtiquette = %s)""", (idEtiquette, idEtiquette))
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False




#ajoute l'auteur et son entree dans la table de jonction en lien avec la reference
def ajouter_auteur(connexion, titre, nom):
    try:
        with connexion.cursor() as curseur:

            #cherche l'auteur et l'ajoute s'il n'existe pas
            curseur.execute("""SELECT idAuteur FROM Auteur WHERE nom = %s""", (nom,))
            temp = curseur.fetchone()
            if temp is None:
                curseur.execute("""INSERT INTO Auteur (nom) VALUES (%s)""", (nom,))
                curseur.execute("""SELECT idAuteur FROM Auteur WHERE nom = %s""", (nom,))
                idAuteur = curseur.fetchone()[0]
            else:
                idAuteur = temp[0]

            #recherche de la reference
            curseur.execute("""SELECT idReference FROM Reference WHERE titre = %s""", (titre,))
            idReference = curseur.fetchone()[0]            


            #ajout dans la table de jonction
            curseur.execute("""INSERT INTO Reference_Auteur (idReference, idAuteur)
                            VALUES (%s, %s)""", (idReference, idAuteur))
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False




def supprimer_auteur(connexion, titre, nom):
    try:
        with connexion.cursor() as curseur:
            curseur.execute("""SELECT idAuteur FROM Auteur WHERE nom = %s""", (nom,))
            temp = curseur.fetchone()
            if temp is None:
                return False
            idAuteur = temp[0]

            curseur.execute("""SELECT idReference FROM Reference WHERE titre = %s""", (titre,))
            temp = curseur.fetchone()
            if temp is None:
                return False
            idReference = temp[0]

            #verifie l'existance du lien entre la reference et l'Auteur en question
            curseur.execute("""SELECT * FROM Reference_Auteur WHERE idReference = %s AND idAuteur = %s""", (idReference,idAuteur))
            resultat = curseur.fetchone()
            if resultat is None:
                return False

            #regarder si la reference a un autre auteur
            curseur.execute("""SELECT * FROM Reference_Auteur WHERE idReference = %s""", (idReference,))
            resultat = curseur.fetchall()
            if len(resultat) < 2:
                return False

            #supprime le lien
            curseur.execute("""DELETE FROM Reference_Auteur r_e 
                            WHERE r_e.idReference = %s AND r_e.idAuteur = %s""", (idReference, idAuteur))
            

            #supprime l'Auteur n'ayant plus aucune reference
            curseur.execute("""DELETE FROM Auteur
                            WHERE idAuteur = %s
                            AND NOT EXISTS (
                            SELECT 1 FROM Reference_Auteur
                            WHERE idAuteur = %s)""", (idAuteur, idAuteur))
            connexion.commit()
            return True
    except mysql.connector.Error:
        connexion.rollback()
        return False





def modifier_reference(connexion, ancien_titre, titre, revue, annee, hyperlien, description):
    try:
        with connexion.cursor() as curseur:
            curseur.execute("""UPDATE Reference
                            SET titre = %s, revue = %s, annee = %s, hyperlien = %s, description = %s
                            WHERE titre = %s""", (titre, revue, annee, hyperlien, description, ancien_titre))
        connexion.commit()
        return True
    except mysql.connector.Error:
        connexion.rollback()
        return False


def modifier_etiquette(connexion, ancien_nom, nouveau_nom):
    with connexion.cursor() as curseur:
        curseur.execute("""UPDATE Etiquette
                        SET nom = %s
                        WHERE nom = %s""", (nouveau_nom, ancien_nom))


def modifier_auteur(connexion, ancien_nom, nouveau_nom):
    with connexion.cursor() as curseur:
        curseur.execute("""UPDATE Auteur
                        SET nom = %s
                        WHERE nom = %s""", (nouveau_nom, ancien_nom))



#impression de la table de reference qui ont le meme auteur passe en argument
def impression_par_auteur(connexion, nom):
    with connexion.cursor() as curseur:
        temps1 = time.time()
        print("\nRéférences")
        curseur.execute("""SELECT titre, revue, annee, hyperlien, description 
                        FROM Reference r, Reference_Auteur r_a, Auteur a 
                        WHERE r.idReference = r_a.idReference AND r_a.idAuteur = a.idAuteur AND a.nom = %s""", (nom,))
        imprimer_avec_curseur(curseur)
        temps2 = time.time()
        tempsReponse = round(temps2-temps1, 4)
        print(f"Temps de réponse: {tempsReponse} secondes")




#impression de la table de reference qui ont la meme etiquette passe en argument
def impression_par_etiquette(connexion, nom):
    with connexion.cursor() as curseur:
        temps1 = time.time()
        print("\nRéférences")        
        curseur.execute("""SELECT titre, revue, annee, hyperlien, description 
                        FROM Reference r, Reference_Etiquette r_e, Etiquette e 
                        WHERE r.idReference = r_e.idReference AND r_e.idEtiquette = e.idEtiquette AND e.nom = %s""", (nom,))
        imprimer_avec_curseur(curseur)
        temps2 = time.time()
        tempsReponse = round(temps2-temps1, 4)
        print(f"Temps de réponse: {tempsReponse} secondes")




#impression des informations d'une reference incluant ses etiquettes et auteurs
def impression_par_titre(connexion, titre):
    with connexion.cursor() as curseur:
        print("\nRéférences")
        curseur.execute("""SELECT titre, revue, annee, hyperlien, description 
                        FROM Reference
                        WHERE Reference.titre = %s""", (titre,))
        imprimer_avec_curseur(curseur)
        print("\nAuteurs: ")
        curseur.execute("""SELECT nom 
                        FROM Reference r, Reference_Auteur r_a, Auteur a 
                        WHERE r.idReference = r_a.idReference AND r_a.idAuteur = a.idAuteur AND r.titre = %s""", (titre,))
        imprimer_avec_curseur(curseur)
        print("\nEtiquettes (s'il y a lieu): ")
        curseur.execute("""SELECT nom 
                        FROM Reference r, Reference_Etiquette r_e, Etiquette e 
                        WHERE r.idReference = r_e.idReference AND r_e.idEtiquette = e.idEtiquette AND r.titre = %s""", (titre,))
        imprimer_avec_curseur(curseur)




#verifie la presence d'un element dans la table correspondante
def verification_element(connexion, valeur, table):
    try:
        with connexion.cursor() as curseur:
            if(table == "Auteur"):
                curseur.execute("""SELECT * FROM Auteur WHERE nom = %s""", (valeur,))
            elif(table == "Etiquette"):
                curseur.execute("""SELECT * FROM Etiquette WHERE nom = %s""", (valeur,))
            else:
                curseur.execute("""SELECT * FROM Reference WHERE titre = %s""", (valeur,))
            return curseur.fetchone() is not None
    except Error:
        print("erreur avec la verification")
        return False




#fait une belle impression de l'information contenu par le curseur
def imprimer_avec_curseur(curseur):
    print("\n")
    resultats = curseur.fetchall()
    print(tabulate(resultats, headers=[i[0] for i in curseur.description]))


