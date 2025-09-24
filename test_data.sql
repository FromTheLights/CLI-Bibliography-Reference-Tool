USE bozo_outil_bibliographique;

SET FOREIGN_KEY_CHECKS = 0;

-- REFERENCE
LOAD DATA LOCAL INFILE './data/references.txt'
INTO TABLE Reference
FIELDS TERMINATED BY ','
(@titre, @revue, @annee, @hyperlien, @description)
SET
    titre = TRIM(@titre),
    revue = TRIM(@revue),
    annee = TRIM(@annee),
    hyperlien = TRIM(@hyperlien),
    description = TRIM(@description);



-- AUTEUR
LOAD DATA LOCAL INFILE './data/auteurs.txt'
INTO TABLE Auteur
LINES TERMINATED BY '\n'
(@ligne)
SET
    nom = TRIM(REPLACE(REPLACE(@ligne, "\r", ""), "\n", ""));



-- ETIQUETTE
LOAD DATA LOCAL INFILE './data/etiquettes.txt'
INTO TABLE Etiquette
LINES TERMINATED BY '\n'
(@ligne)
SET
    nom = TRIM(REPLACE(REPLACE(@ligne, "\r", ""), "\n", ""));



-- REFERENCE_AUTEUR
CREATE TEMPORARY TABLE temp_reference_auteur (
    titre VARCHAR(50),
    nom VARCHAR(50)
);

LOAD DATA LOCAL INFILE './data/references_auteurs.txt'
INTO TABLE temp_reference_auteur
FIELDS TERMINATED BY ','
(@titre, @nom)
SET
    titre = TRIM(@titre),
    nom = TRIM(REPLACE(REPLACE(@nom, "\r", ""), "\n", ""));

INSERT INTO Reference_Auteur
SELECT Reference.idReference, Auteur.idAuteur
FROM temp_reference_auteur tmp
JOIN Reference ON tmp.titre = Reference.titre
JOIN Auteur ON tmp.nom = Auteur.nom;

DROP TEMPORARY TABLE temp_reference_auteur;



-- REFERENCE_ETIQUETTE
CREATE TEMPORARY TABLE temp_reference_etiquette (
    titre VARCHAR(50),
    nom VARCHAR(50)
);

LOAD DATA LOCAL INFILE './data/references_etiquettes.txt'
INTO TABLE temp_reference_etiquette
FIELDS TERMINATED BY ','
(@titre, @nom)
SET
    titre = TRIM(@titre),
    nom = TRIM(REPLACE(REPLACE(@nom, "\r", ""), "\n", ""));

INSERT INTO Reference_Etiquette
SELECT Reference.idReference, Etiquette.idEtiquette
FROM temp_reference_etiquette tmp
JOIN Reference ON tmp.titre = Reference.titre
JOIN Etiquette ON tmp.nom = Etiquette.nom;

DROP TEMPORARY TABLE temp_reference_etiquette;


SET FOREIGN_KEY_CHECKS = 1;