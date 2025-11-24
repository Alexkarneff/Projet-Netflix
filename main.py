# -*- coding: utf-8 -*-
import pandas as pd

movies_dataset = pd.read_csv("data/dataset/movies_metadata_credits_joined.csv", sep = ",")

from modules import utilisateur
from modules import filtres
from modules import stats
from modules import recherches
from modules import admin

def afficher_menu_principal():
    # Affiche le menu principal.
    print("\n=== MOTEUR DE RECHERCHE NETFLIX ===")
    print("1. Menu des genres")
    print("2. Faire une recherche")
    print("3. Noter un film")
    print("4. Voir mes statistiques")
    print("5. Supprimer mes données")
    print("q. Quitter")


def main() :
        print("\nBienvenue sur le moteur de recherche Netflix !")
        print("\n--- Statistiques Globales ---")
        stats.stats_globales(movies_dataset)
        users = utilisateur.load_users()    # charge tous les utilisateurs enregistrés
        username = input("\nEntrez votre nom d'utilisateur : ").strip()
        current_user = utilisateur.create_user(users, username)      # crée un utilisateur si inexistant, reconnaît un utilisateur existant autrement
        
        while True:
            afficher_menu_principal()
            choix = input("Choisissez une option : ").strip()
            match choix:              
                case "1":                                           # choix 1 Filtrer les films
                       filtres.programme_filtre()

                case "2":                                           # choix 2 Rechercher un film
                        # Définir l'utilisateur actuel dans le module recherches
                        recherches.set_current_user(current_user)
                        
                        # Lancer le module de recherche
                        recherches.main()
                        
                        # Sauvegarder les modifications utilisateur
                        utilisateur.save_users(users)

                case "3":                                           # choix 3 Noter un film
                        print(" --- Noter un film ---")
                        title = input("Titre du film : ")
                        if title in movies_dataset["original_title"].values :
                            utilisateur.rate_movie(current_user, title)                 # enregistre la note de l'utilisateur pour le film
                            utilisateur.save_users(users)                               # enregistre les changements utilisateur
                        else :
                              print("Film Introuvable")

                case "4":                                           # choix 4 Afficher les statistiques utilisateur
                        utilisateur.user_statistics(current_user)
        
                case "5":                                           # choix 5 Supprimer l'utilisateur connecté après confirmation
                        confirmation = input("Êtes-vous sûr de vouloir supprimer vos données ? (oui/non) : ")               
                        if confirmation.lower() == "oui":       
                            utilisateur.delete_user(users,username)
                            print("Vos données ont été supprimées. Au revoir !")
                            break
                        else:
                            print("Suppression annulée.")
                case "admin":                                                                       # menu admin
                        admin.programme_admin()                                               

                case "Q" | "q":                                                                   # choix 6 Déconnexion de l'utilisateur
                        print("Merci d'avoir utilisé le moteur Netflix. À bientôt !")                           
                        break
                 
                case _:
                        print("Choix invalide. Veuillez entrer un chiffre de 1 à 5 ou q pour quitter.")                   # gère les choix qui ne sont pas de 1 à 6
                        continue
                  
if __name__ == "__main__":
    main()