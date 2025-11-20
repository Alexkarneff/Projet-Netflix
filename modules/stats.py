import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data/dataset/movies_metadata_credits_joined.csv", sep = ",")

def stats_globales(dataset):
        nombre_total_de_films = dataset.id.count()
        durée_totale_des_films = dataset.runtime.sum()

        print (f"Le moteur de recherche comporte {nombre_total_de_films} films au total !")
        print (f"La durée totale des films est de {durée_totale_des_films} minutes, soit {round(durée_totale_des_films/60)} heures !")
        

        for language in ("en","fr","it","ja"):
            pourcentage = (dataset["original_language"].value_counts(normalize=True)[language]) * 100
            print(f"les films en {language} représentent {pourcentage:.1f}% des films du moteur !")

        for genre in ("Action", "Comedy", "Drama","Animation") :
            films_par_genre = dataset[dataset['genres'].str.contains(genre, na=False)].shape[0]
            pourcentage_films_par_genre = (films_par_genre/nombre_total_de_films) *100
            print(f"Il y a {films_par_genre} films du genre {genre} dans le moteur, soit {pourcentage_films_par_genre:.1f} % des films !")

            








