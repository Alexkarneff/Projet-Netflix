from modules import *


def afficher_menu_principal():
    """Affiche le menu principal."""
    print("\n=== MOTEUR DE RECHERCHE NETFLIX ===")
    print("1. Faire une recherche (simulation)")
    # print("Utiliser les filtres")
    print("2. Noter un film")
    print("3. Voir mes statistiques")
    print("4. Supprimer mes données")
    print("5. Quitter")



while True:
    afficher_menu_principal()
    choix = input("Choisissez une option : ")
    match choix:
        case "1":
                print("\n--- Nouvelle recherche ---")
                genre = input("Entrez un genre (ex: Action, Comédie, Horreur) : ")
                country = input("Entrez un pays (ex: USA, France, UK) : ")
                try:
                    duration = int(input("Durée souhaitée (en minutes) : "))
                except ValueError:
                    duration = None
        case "2":
                print("\n--- Noter un film ---")
                title = input("Titre du film : ")
        case "3":
                print("MES STATS :")
                # user.show_user_stats(current_user)   # Montre les stats 
   
        case "4":
                confirmation = input("Êtes-vous sûr de vouloir supprimer vos données ? (oui/non) : ")
                if confirmation.lower() == "oui":
                    #delete user       
                    print("Vos données ont été supprimées. Au revoir !")
                    break
                else:
                    print("Suppression annulée.")
        case "5":
                print("Merci d'avoir utilisé le moteur Netflix. À bientôt !")
                break
        case _:
                print("Choix invalide. Veuillez entrer un chiffre de 1 à 5.")
                break