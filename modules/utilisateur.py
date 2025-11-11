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
        self.favorite_country = {}    # {pays: nombre de recherches}
        self.average_duration = []    # liste des durées des films recherchés


    # def to_dict(self):                  Convertit l'objet utilisateur en dictionnaire pour l'enregistrement JSON.

        return {
            "username": self.username,
            "search_history": self.search_history,
            "ratings": self.ratings,
            "connections": self.connections,
            "favorite_genres": self.favorite_genres,
            "favorite_country": self.favorite_country,
            "average_duration": self.average_duration
        }
    

# FONCTIONS GLOBALES

def load_users():
    return


def create_user(users, username):                               # Crée un nouvel utilisateur s’il n’existe pas encore. 
    if username in users:
        print(f"Bienvenue à nouveau, {username} !")
        users[username].connections += 1
    else:
        print(f"Nouvel utilisateur créé : {username}")
        users[username] = User(username)
        users[username].connections = 1
    # save_users(users)                                         # Enregistre les données utilisateur
    return users[username]


def save_users(users):                                      # Enregistre les données utilisateur
    # json.dump ...
    ""


def rate_movie(user, title, rating):                        # Permet à l'utilisateur de noter un film.
    
    if 1 <= rating <= 5:
        user.ratings[title] = rating
        print(f"Vous avez noté {title} : {rating}/5")
    else:
        print("La note doit être comprise entre 1 et 5.")


def show_user_stats(user):
     print(f"\n--- Statistiques de {user.username} ---")
     print(f"Nombre de connexions : {user.connections}")


def delete_user(users,username):                            # Supprime les données personnelles d'un utilisateur.
    ""
