import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data\movies_metadata_credits_joined.csv", sep = ",")

# print(movies_dataset["original_title"].head())

# def recherche_genre(genre_saisi, movies_dataset = movies_dataset):
#     return movies_dataset[(genre_saisi in movies_dataset["genres"])]


# new_dataset = recherche_genre('Family')

# Fonction de recherche par durée : retourne un dataset contenant uniquement les films ayant exactement la bonne durée
# Les lignes sont triées du film le plmus populaire au moins populaire
"""
def recherche_duree(duree_saisie:float, dataset = movies_dataset):
    new_dataset = dataset[dataset["runtime"] == duree_saisie]
    new_dataset = new_dataset.sort_values("popularity", ascending=False)
    return new_dataset

new_dataset = recherche_duree(81.0)
print(new_dataset.head())"""


# Recherche par langue : fonctionne

def recherche_langue(langue_saisie:str, dataset = movies_dataset):
    langue_lettres = langue_saisie[0].lower()+langue_saisie[1].lower()
    new_dataset = dataset[movies_dataset["original_language"]==langue_lettres]
    new_dataset = new_dataset.sort_values("popularity", ascending=False)
    return new_dataset

new_dataset = recherche_langue('English')
print(new_dataset.head())


def recherche_genre(genre_saisi, movies_dataset = movies_dataset):
    films_filtres = []
    for i in movies_dataset["genres"]:
        for j in i:
            if j[1] == genre_saisi:
                films_filtres.append(movies_dataset[movies_dataset["genres"]==i]["original_title"])
    
    return films_filtres


new_dataset = recherche_genre('Family')
print(new_dataset)



