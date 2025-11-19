import json
import os

USER_FILE = "data/users.json"

class User:                             # La Classe qui représente un utilisateur avec ses infos

    def __init__(self, username):
        self.username = username
        self.search_history = []      # liste des recherches effectuées
        self.ratings = {}             # {titre_film: note}
        self.connections = 0          # nombre de connexions
        self.favorite_genres = {}     # {genre: nombre de recherches}
        self.favorite_language = {}    # {pays: nombre de recherches}
        self.average_duration = []    # liste des durées des films recherchés


    def to_dict(self):                  # Convertit l'objet utilisateur en dictionnaire pour l'enregistrement JSON.

        return {
            "username": self.username,
            "search_history": self.search_history,
            "ratings": self.ratings,
            "connections": self.connections,
            "favorite_genres": self.favorite_genres,
            "favorite_language": self.favorite_language,
            "average_duration": self.average_duration
        }
    
    def from_dict(data):                                #Reconstruit un objet User à partir du dictionnaire Json sauvegardé
        user = User(data["username"])
        user.search_history = data.get("search_history", [])
        user.ratings = data.get("ratings", {})
        user.connections = data.get("connections", 0)
        user.favorite_genres = data.get("favorite_genres", {})
        user.favorite_language = data.get("favorite_language", {})
        user.average_duration = data.get("average_duration", [])
        return user                             



# FONCTIONS GLOBALES

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            data = json.load(f)
            return {name: User.from_dict(info) for name, info in data.items()}
    else:
        return {}
    


def create_user(users, username):                               # Crée un nouvel utilisateur s’il n’existe pas encore. 
    if username in users:
        print(f"Bienvenue à nouveau, {username} !")
        users[username].connections += 1
    else:
        print(f"Nouvel utilisateur créé : {username}")
        users[username] = User(username)
        users[username].connections = 1
    save_users(users)                                         # Enregistre les données utilisateur
    return users[username]


def save_users(users):                                      # Enregistre les données utilisateur
     with open(USER_FILE, "w") as f:
        json.dump({u: user.to_dict() for u, user in users.items()}, f, indent=4)

def search_record(user, genre=None, language=None, duration=None):               #Enregistre les recherches utilisateur
    user.search_history.append({"genre": genre, "language": language, "duration": duration})

    if genre:
        user.favorite_genres[genre] = user.favorite_genres.get(genre,0) +1
    if language:
        user.favorite_language[language] = user.favorite_language.get(language, 0) + 1
    if duration :
        user.average_duration.append(duration)

def rate_movie(user, title, rating):                        # Permet à l'utilisateur de noter un film.
    if 1 <= rating <= 5:
        user.ratings[title] = rating
        print(f"Vous avez noté {title} : {rating}/5")
    else:
        print("La note doit être comprise entre 1 et 5.")


def user_statistics(user):                      # Affiche les statistiques de l'utilisateur
  
    if not user.search_history:
        if user.connections :
            print(f"\n Vous vous êtes connecté {user.connections} fois")

        print("\n Aucune recherche effectuée pour le moment.")
        return
    
    print(f"\n Nombre total de recherches : {len(user.search_history)}\n")
    

    if user.favorite_genres:
        print("\n Genre les plus recherchés :")
        genres_tries = sorted(user.favorite_genres.items(), key=lambda x: x[1], reverse=True)
        for genre, count in genres_tries[:5]:
            print(f"  • {genre}: {count} fois")
   
    if user.favorite_language:
        print("\n Langues les plus recherchées :")
        language_tries = sorted(user.favorite_language.items(), key=lambda x: x[1], reverse=True)
        for language, count in language_tries[:5]:
            print(f"  • {language}: {count} fois")
    
    if user.average_duration:
        duree_moy = sum(user.average_duration) / len(user.average_duration)
        print(f"\n Duréee moyenne recherchée :")
        print(f"  {int(duree_moy)} minutes")


    if user.connections :
        print(f"\n Vous vous êtes connecté {user.connections} fois")

def delete_user(users,username):                            # Supprime les données personnelles d'un utilisateur.
    if username in users :
        del users[username]
        save_users(users)
        print(f"Données de {username} supprimées avec succès.")
    else: 
        print(f"Utilisateur introuvable")
