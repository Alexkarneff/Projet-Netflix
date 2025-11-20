import json
from modules import utilisateur

USER_FILE = "data/users.json"

def affichage_admin():
        # Affiche le menu principaladmin.
    print("\n=== MENU ADMIN ===")
    print("1. Afficher le nombre d'utilisateurs inscrits")
    print("2. Supprimer les données de tous les utilisateurs")

    print("q. Quitter le menu Admin")


def programme_admin():
    programme_admin = True
    
    while programme_admin:
        affichage_admin()
        choix = input("Choisissez une option : ").strip()
        match choix :
            case "1":
                users = utilisateur.load_users()
                print(f"Nombre d'utilisateurs différents : {len(users)}")
            case "2":
                confirmation = input("Êtes-vous sûr de vouloir supprimer TOUTES les données ? (oui/non) : ")
                if confirmation.lower() == "oui":
                    utilisateur.save_users({})  # sauvegarde un dictionnaire vide
                    print("Toutes les données ont été supprimées")


            case "q" | "quit" | "quitter":              # quitter le menu admin
                programme_admin= False