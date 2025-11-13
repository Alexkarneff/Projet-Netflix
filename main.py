from modules import utilisateur

def afficher_menu_principal():
    # Affiche le menu principal.
    print("\n=== MOTEUR DE RECHERCHE NETFLIX ===")
    print("1. Faire une recherche (simulation)")
    # print("Utiliser les filtres")
    print("2. Noter un film")
    print("3. Voir mes statistiques")
    print("4. Supprimer mes données")
    print("5. Quitter")


def main() :
        print("Bienvenue sur le moteur de recherche Netflix !")
        # users = utilisateur.load_users()    #charge tous les utilisateurs enregistrés
        username = input("Entrez votre nom d'utilisateur : ").strip()
        print (username)
        # current_user = utilisateur.create_user(users, username)      #crée un utilisateur si inexistant, reconnaît un utilisateur existant autrement
        while True:
            afficher_menu_principal()
            choix = input("Choisissez une option : ")
            match choix:
                case "1":                       #choix 1 Rechercher un film
                        print("\n--- Nouvelle recherche ---")
                        genre = input("Entrez un genre (ex: Action, Comédie, Horreur) : ")
                        pays = input("Entrez un pays (ex: USA, France, UK) : ")
                        try:
                            duration = int(input("Durée souhaitée (en minutes) : "))
                        except ValueError:
                            duration = None
                        # utilisateur.record_search(current_user, genre=genre, country=country, duration=duration)    # enregistre la recherche de l'utilisateur
                        print(f"🔍 Recherche enregistrée : {genre}, {pays}, {duration} min")
                        # utilisateur.save_users(users)            #enregistre les changements utilisateur

                case "2":                        #choix 2 Noter un film
                        print("\n--- Noter un film ---")
                        title = input("Titre du film : ")
                        try:
                            rating = int(input("Note (1 à 5) : "))
                        except ValueError:
                            print("Veuillez entrer un nombre entre 1 et 5.")
                        continue
                        # utilisateur.rate_movie(current_user, title, rating)           #enregistre la note de l'utilisateur pour le film
                        # utilisateur.save_users(users)            #enregistre les changements utilisateur
                case "3":
                        print("MES STATS :")
                        # utilisateur.show_user_stats(current_user)   # choix 3 Montre les stats de l'utilisateur connecté
        
                case "4":
                        confirmation = input("Êtes-vous sûr de vouloir supprimer vos données ? (oui/non) : ")               # choix 4 Supprimer l'utilisateur connecté après confirmation
                        if confirmation.lower() == "oui":       
                            print("Vos données ont été supprimées. Au revoir !")
                            break
                        else:
                            print("Suppression annulée.")
                case "5":
                        print("Merci d'avoir utilisé le moteur Netflix. À bientôt !")                           # choix 5 Déconnexion de l'utilisateur
                        break
                case _:
                        print("Choix invalide. Veuillez entrer un chiffre de 1 à 5.")                   # gère les choix qui ne sont pas de 1 à 5
                        break
                  
if __name__ == "__main__":
    main()