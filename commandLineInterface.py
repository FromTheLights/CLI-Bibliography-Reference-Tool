import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="le_1root_desql",
    database="ReferencesBibliographiques"
)

mycursor = db.cursor()

#mycursor.execute("CREATE DATABASE ReferencesBibliographiques")


mycursor.execute("DROP TABLE IF EXISTS ReferenceEtiquette")
mycursor.execute("DROP TABLE IF EXISTS ReferenceAuteur")
mycursor.execute("DROP TABLE IF EXISTS Reference")
mycursor.execute("DROP TABLE IF EXISTS Auteur")
mycursor.execute("DROP TABLE IF EXISTS Etiquette")



mycursor.execute("""CREATE TABLE Reference (
                 idReference int PRIMARY KEY AUTO_INCREMENT,
                  titre VARCHAR(50),
                  revue VARCHAR(50),
                  annee smallint UNSIGNED,
                  hyperlien VARCHAR(100),
                  description VARCHAR(100)
                 )""")

mycursor.execute("""CREATE TABLE Auteur (
                 idAuteur int PRIMARY KEY AUTO_INCREMENT,
                  nom VARCHAR(50)
                 )""")

mycursor.execute("""CREATE TABLE Etiquette (
                 idEtiquette int PRIMARY KEY AUTO_INCREMENT,
                  nom VARCHAR(50) UNIQUE
                 )""")

mycursor.execute("""CREATE TABLE ReferenceEtiquette (
                 idReference int,
                  idEtiquette int,
                  PRIMARY KEY (idReference, idEtiquette),
                 FOREIGN KEY (idReference) REFERENCES Reference(idReference),
                 FOREIGN KEY (idEtiquette) REFERENCES Etiquette(idEtiquette)                  
                 )""")

mycursor.execute("""CREATE TABLE ReferenceAuteur (
                 idReference int,
                  idAuteur int,
                  PRIMARY KEY (idReference, idAuteur),
                 FOREIGN KEY (idReference) REFERENCES Reference(idReference),
                 FOREIGN KEY (idAuteur) REFERENCES Auteur(idAuteur)
                 )""")

 