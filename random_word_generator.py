from random_word import RandomWords
import random
import csv



def random_word_list(length):
    r = RandomWords()
    return [r.get_random_word() for i in range(length)]
        
def random_year_list(length):
    return [random.randint(1920, 2025) for i in range(length)]

def random_hyperlien_list(length):
    r = RandomWords()
    return ["www." + r.get_random_word() + ".com" for i in range(length)]
        

def produire_table_croisement(fichier_autre, fichier_titre_autre, min, max):
    with open('./data/references.txt') as f:
        titres = []
        for line in f:
            # Remove any trailing newline/whitespace
            cleaned_line = line.strip()
        
            # Only process non-empty lines
            if cleaned_line:
                # Split the line by commas and take the first element
                first_part = cleaned_line.split(',', 1)[0]
                titres.append(first_part)
    with open(fichier_autre, newline='') as f:
        reader = csv.reader(f)
        autres = list(reader)
    with  open(fichier_titre_autre, 'w') as f:
        for i in range(10000):
            nombre_association = random.randint(min,max)
            autres_choisis = random.sample(range(100), nombre_association)
            for j in range(nombre_association):
                string = titres[i] + "," + autres[autres_choisis[j]][0] + "\n"
                f.write(string)


def produire_references(quantite):
    with  open('./data/references.txt', 'w') as f:
        liste_titre_1 = random_word_list(quantite)
        print("list 1 loaded")
        liste_titre_2 = random_word_list(quantite)
        print("list 2 loaded")
        liste_revue = random_word_list(quantite) 
        print("list 3 loaded")
        liste_annee = random_year_list(quantite)
        print("list 4 loaded")
        liste_hyperlien = random_hyperlien_list(quantite) 
        print("list 5 loaded")
        liste_breve_description = random_word_list(quantite)
        print("list 6 loaded")

        for i in range(quantite):
            string1 = liste_titre_1[i] + " " + liste_titre_2[i] + "," + liste_revue[i] + ","
            string2 = str(liste_annee[i])
            string3 = "," + liste_hyperlien[i] + "," + liste_breve_description[i] + "\n"
            f.write(string1)
            f.write(string2)
            f.write(string3)

def produire_etiquette(quantite):
    with open('./data/etiquettes.txt', 'w') as f:
        liste = random_word_list(quantite)
        print("list loaded")
        for i in range(quantite):
            f.write(liste[i] + "\n")

def produire_auteur(quantite):
    with open('./data/auteurs.txt', 'w') as f:
        liste_prenom = random_word_list(quantite)
        print("list loaded")
        liste2_nom = random_word_list(quantite)
        print("list loaded")
        for i in range(quantite):
            f.write(liste_prenom[i] + " " + liste2_nom[i] + "\n")
    

def main():
    #produire_references(10000)
    #produire_auteur(100)
    #produire_etiquette(100)
    produire_table_croisement('./data/etiquettes.txt','./data/references_etiquettes.txt', 0, 4)
    produire_table_croisement('./data/auteurs.txt','./data/references_auteurs.txt', 1, 5)


    





if __name__ == "__main__":
    main()