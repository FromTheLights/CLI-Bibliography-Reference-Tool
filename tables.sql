USE bozo_outil_bibliographique;

CREATE TABLE IF NOT EXISTS Reference (
    idReference int PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(50) UNIQUE NOT NULL,
    revue VARCHAR(50) NOT NULL,
    annee YEAR NOT NULL,
    hyperlien VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Auteur (
    idAuteur int PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Etiquette (
    idEtiquette int PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Reference_Etiquette (
    idReference int,
    idEtiquette int,
    PRIMARY KEY (idReference, idEtiquette),
    FOREIGN KEY (idReference) REFERENCES Reference(idReference) ON DELETE CASCADE,
    FOREIGN KEY (idEtiquette) REFERENCES Etiquette(idEtiquette) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reference_Auteur (
    idReference int,
    idAuteur int,
    PRIMARY KEY (idReference, idAuteur),
    FOREIGN KEY (idReference) REFERENCES Reference(idReference) ON DELETE CASCADE,
    FOREIGN KEY (idAuteur) REFERENCES Auteur(idAuteur) ON DELETE CASCADE
);