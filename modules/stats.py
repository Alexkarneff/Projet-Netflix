import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data/dataset/movies_metadata_credits_joined2.csv", sep = ",")

def stats_globales(dataset):
        nombre_total_de_films = dataset.id.count()
        durée_totale_des_films = dataset.runtime.sum()

        print (f"Le moteur de recherche comporte {nombre_total_de_films} films au total !")
        print (f"La durée totale des films est de {durée_totale_des_films} minutes, soit {durée_totale_des_films/60} heures !")
        

        for language in ("en","fr","it","de","ja"):
            pourcentage = (dataset["original_language"].value_counts(normalize=True)[language]) * 100
            print(f"les films en {language} représentent {pourcentage:.1f}% des films du moteur !")





