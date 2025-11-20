import json
from modules import utilisateur

USER_FILE = "data/users.json"

def affichage_admin():
        # Affiche le menu principaladmin.
    print("\n=== MENU ADMIN ===")
    print("1. Supprimer les données de tous les utilisateurs")
    print("2. Afficher le nombre d'utilisateurs inscrits")
    print("q. Quitter le menu Admin")




def programme_admin():
    programme_admin = True
    
    while programme_admin:
        affichage_admin()
        choix = input("Choisissez une option : ").strip()
        match choix :
            case "1" :
                    confirmation = input("Êtes-vous sûr de vouloir supprimer TOUTES les données ? (oui/non) : ")               
                    if confirmation.lower() == "oui":    
                        with open(USER_FILE, "w") as file:
                            json.dump({}, file)
                        print("Toutes les données ont été supprimées")
            case "2" :
                    with open(USER_FILE, "r") as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            print("Fichier JSON vide ou invalide.")
                        continue
                    if isinstance(data, dict):
                        users_list = data.get("users", [])
                    elif isinstance(data, list):
                        users_list = data
                    else:
                        users_list = []
                    
                    unique_users = {user["username"] for user in users_list if "username" in user}
                    print(f"Nombre d'utilisateurs différents : {len(unique_users)}")

            case "q" | "quit" | "quitter":
                programme_admin= False