import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data\movies_metadata_credits_joined.csv", sep = ",")

# print(movies_dataset["original_title"].head())

# def recherche_genre(genre_saisi, movies_dataset = movies_dataset):
#     return movies_dataset[(genre_saisi in movies_dataset["genres"])]


# new_dataset = recherche_genre('Family')

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
            print("Saisie incorecte.")

    return new_dataset

new_dataset = recherche_duree()
print(new_dataset["original_title"].head())


# Recherche par langue : fonctionne
def recherche_langue(dataset = movies_dataset):
    while True: 
        try:
            langue_saisie = input("Quelle langue ? ")
            langue_lettres = langue_saisie[0].lower()+langue_saisie[1].lower()
            new_dataset = dataset[movies_dataset["original_language"]==langue_lettres]
            new_dataset = new_dataset.sort_values("popularity", ascending=False)
            break
        except IndexError:
            print("Saisie incorecte.")

    return new_dataset

new_dataset = recherche_langue()
print(new_dataset["original_title"].head())


# def recherche_genre(genre_saisi, dataset = movies_dataset):
#     films_filtres = []
#     for i in dataset["genres"]:
#         for j in i:
#             if j[1] == genre_saisi:
#                 films_filtres.append(dataset[dataset["genres"]==i]["original_title"])
    
#     return films_filtres


# new_dataset = recherche_genre('Family')
# print(new_dataset)



