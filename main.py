import pandas as pd
import numpy as np

movies_dataset = pd.read_csv("data/dataset/movies_metadata_credits_joined2.csv", sep = ",")

from modules import utilisateur
from modules import filtres
from modules import stats

def afficher_menu_principal():
    # Affiche le menu principal.
    print("\n=== MOTEUR DE RECHERCHE NETFLIX ===")
    print("1. Menu des genres")
    print("2. Faire une recherche (simulation)")
    print("3. Noter un film")
    # print("4. Voir mes statistiques")
    print("4. Supprimer mes données")
    print("5. Quitter")


def main() :
        print("Bienvenue sur le moteur de recherche Netflix !")
        stats.stats_globales(movies_dataset)
        users = utilisateur.load_users()    #charge tous les utilisateurs enregistrés
        username = input("Entrez votre nom d'utilisateur : ").strip()
        print (username)
        current_user = utilisateur.create_user(users, username)      #crée un utilisateur si inexistant, reconnaît un utilisateur existant autrement
        while True:
            afficher_menu_principal()
            choix = input("Choisissez une option : ").strip()
            match choix:              
                case "1":                                           #choix 2 Filtrer les films
                       filtres.programme_filtre()

                case "2":                                           #choix 1 Rechercher un film
                        print("\n--- Nouvelle recherche ---")
                        genre = input("Entrez un genre (ex: Action, Comédie, Horreur) : ")
                        country = input("Entrez un pays (ex: USA, France, UK) : ")
                        try:
                            duration = int(input("Durée souhaitée (en minutes) : "))
                        except ValueError:
                            duration = None
                        utilisateur.search_record(current_user, genre=genre, country=country, duration=duration)    # enregistre la recherche de l'utilisateur
                        print(f"🔍 Recherche enregistrée : {genre}, {country}, {duration} min")
                        utilisateur.save_users(users)            #enregistre les changements utilisateur
                case "3":                                           #choix 3 Noter un film
                        print("\n--- Noter un film ---")
                        title = input("Titre du film : ")
                        try:
                            rating = int(input("Note (1 à 5) : "))
                        except ValueError:
                            print("Veuillez entrer un nombre entre 1 et 5.")
                            continue
                        utilisateur.rate_movie(current_user, title, rating)           #enregistre la note de l'utilisateur pour le film
                        utilisateur.save_users(users)            #enregistre les changements utilisateur

                # case "4":                                           # choix 4 Montre les stats de l'utilisateur connecté
                #         print("MES STATS :")
                #         utilisateur.show_user_stats(current_user)   
        
                case "4":                                           # choix 5 Supprimer l'utilisateur connecté après confirmation
                        confirmation = input("Êtes-vous sûr de vouloir supprimer vos données ? (oui/non) : ")               
                        if confirmation.lower() == "oui":       
                            utilisateur.delete_user(users,username)
                            print("Vos données ont été supprimées. Au revoir !")
                            break
                        else:
                            print("Suppression annulée.")

                case "5":                                                                   # choix 6 Déconnexion de l'utilisateur
                        print("Merci d'avoir utilisé le moteur Netflix. À bientôt !")                           
                        break
                 
                case _:
                        print("Choix invalide. Veuillez entrer un chiffre de 1 à 5.")                   # gère les choix qui ne sont pas de 1 à 5
                        continue
                  
if __name__ == "__main__":
    main()