import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data\movies_metadata_credits_joined2.csv", sep = ",")



# Fonction de recherche par durée : retourne un dataset contenant uniquement les films ayant exactement la bonne durée
# Les lignes sont triées du film le plmus populaire au moins populaire
def recherche_duree(dataset = movies_dataset):
    while True:
        try:
            duree_saisie = float(input("Saisir une durée (en min.) : "))
            new_dataset = dataset[dataset["runtime"] == duree_saisie]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except ValueError:
            print("Saisie incorrecte.")

    return new_dataset

# new_dataset = recherche_duree()
# print(new_dataset["original_title"].head())


# Recherche par langue : fonctionne
def recherche_langue(dataset = movies_dataset):
    while True: 
        try:
            langue_saisie = input("Quelle langue ? ")
            langue_lettres = langue_saisie[0].lower()+langue_saisie[1].lower()
            new_dataset = dataset[dataset["original_language"]==langue_lettres]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except IndexError:
            print("Saisie incorrecte.")

    return new_dataset

# new_dataset = recherche_langue()
# print(new_dataset["original_title"].head())


# Recherche par genres
def recherche_genre(dataset = movies_dataset):
    while True:
        try:
            genre_saisi = input("Saisir un genre : ")
            genre_saisi = genre_saisi[0].upper() + genre_saisi[1:].lower()
            new_dataset = dataset[dataset['genres'].str.contains(genre_saisi, na=False)]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except ValueError:
            print("Saisie incorrecte.")

    return new_dataset

# new_dataset = recherche_genre()
# print(new_dataset["original_title"].head())


# Recherche par acteur (obliger d'écrire le nom avec les bonnes majuscules et minuscules)
def recherche_acteur(dataset = movies_dataset):
    while True:
        try:
            acteur_saisi = input("Nom de l'acteur : ")
            new_dataset = dataset[dataset['cast'].str.contains(acteur_saisi, na=False)]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except ValueError:
            print("Saisie incorretce.")

    return new_dataset

# new_dataset = recherche_acteur()
# print(new_dataset["original_title"].head())


# Recherche par pays (comme pour les actteurs, obliger de mettre les maj et min où il faut)
def recherche_pays(dataset = movies_dataset):
    while True:
        try:
            pays_saisi = input("Nom du pays : ")
            new_dataset = dataset[dataset['original_countries'].str.contains(pays_saisi, na=False)]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except ValueError:
            print("Saisie incorretce.")

    return new_dataset

new_dataset = recherche_pays()
print(new_dataset["original_title"].head())