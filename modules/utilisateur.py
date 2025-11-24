import json
import os

# -*- coding: utf-8 -*-

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
    
    def from_dict(data):                                # Reconstruit un objet User à partir du dictionnaire Json sauvegardé
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
        if os.path.getsize(USER_FILE)>0:
            with open(USER_FILE, "r", encoding='utf-8') as f:
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
     with open(USER_FILE, "w", encoding='utf-8') as f:
        json.dump({u: user.to_dict() for u, user in users.items()}, f, indent=4, ensure_ascii=False)

def search_record(user, genre=None, language=None, duration=None):               #Enregistre les recherches utilisateur
    user.search_history.append({"genre": genre, "language": language, "duration": duration})

    if genre:
        user.favorite_genres[genre] = user.favorite_genres.get(genre,0) +1
    if language:
        user.favorite_language[language] = user.favorite_language.get(language, 0) + 1
    if duration :
        user.average_duration.append(duration)

def rate_movie(user, title):                                                    # Permet à l'utilisateur de noter un film. 
    while True:
        try:
            rating = (input("Entrez une note de 1 à 5: "))

            if rating in ("q", "Q", "quit"):
                break

            rating = int(rating)

            if rating in (1, 2, 3, 4, 5):
                user.ratings[title] = rating
                print(f"Vous avez noté {title} : {rating}/5")
                break  # Sort de la boucle une fois la note valide

            else:
               print("La note doit être comprise entre 1 et 5.")

        except ValueError:
            print("Note invalide. Veuillez entrer un nombre entier.")

def user_statistics(user):
    if not user.search_history:
        if user.connections:
            print(f"\n Vous vous êtes connecté {user.connections} fois")
        print("\n Aucune recherche effectuée pour le moment.")
        return
    
    print(f"\n=== STATISTIQUES UTILISATEUR ===")
    print(f"Nombre total de recherches : {len(user.search_history)}")

    # Afficher les films consultés
    films_consultes = [s.get("film") for s in user.search_history if "film" in s]
    if films_consultes:
        print(f"\nFilms consultés ({len(set(films_consultes))} films uniques) :")
        for film in list(dict.fromkeys(films_consultes)):
            print(f"  • {film}")

    # Genres les plus recherchés
    if user.favorite_genres:
        print("\nGenres les plus recherchés :")
        genres_tries = sorted(user.favorite_genres.items(), key=lambda x: x[1], reverse=True)
        for genre, count in genres_tries[:5]:
            print(f"  • {genre} : {count} fois")

    # Langues les plus recherchées
    if user.favorite_language:
        print("\nLangues les plus recherchées :")
        language_tries = sorted(user.favorite_language.items(), key=lambda x: x[1], reverse=True)
        for language, count in language_tries[:5]:
            print(f"  • {language} : {count} fois")

    # Durée moyenne recherchée
    if user.average_duration:
        duree_moy = sum(user.average_duration) / len(user.average_duration)
        print(f"\nDurée moyenne recherchée : {int(duree_moy)} minutes")

    # Nombre de connexions
    if user.connections:
        print(f"\nVous vous êtes connecté {user.connections} fois")

def delete_user(users,username):                            # Supprime les données personnelles d'un utilisateur.
    if username in users :
        del users[username]
        save_users(users)
        print(f"Données de {username} supprimées avec succès.")
    else: 
        print(f"Utilisateur introuvable")