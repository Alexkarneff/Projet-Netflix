import csv
import pandas as pd
import ast  # pour interpréter les listes sous forme de texte

# -----------------------------
# 1 Lecture du fichier CSV
# -----------------------------
films_data = []

with open("data/dataset/movies_metadata_credits_joined 2.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for film in reader:
        titre = film.get("original_title", "").strip()
        langue = film.get("original_language", "").strip()
        duree = film.get("runtime", "").strip()
        genres_str = film.get("genres", "")

        # Tenter de convertir le champ genres en liste Python
        try:
            genres_data = ast.literal_eval(genres_str) if genres_str else []
        except (ValueError, SyntaxError):
            genres_data = []

        genres_list = []

        # Extraire les noms de genres selon le format
        if isinstance(genres_data, list):
            for g in genres_data:
                if isinstance(g, dict) and "name" in g:
                    genres_list.append(g["name"])
                elif isinstance(g, str):
                    genres_list.append(g.strip())

        # Enregistrer chaque film avec son genre
        for genre in genres_list:
            films_data.append({
                "titre": titre,
                "genre": genre,
                "langue": langue,
                "duree": duree
            })

df = pd.DataFrame(films_data)

# -----------------------------
# Dictionnaire des langues principales
# -----------------------------
langues = {
    "1": ("fr", "Français"),
    "2": ("en", "Anglais"),
    "3": ("es", "Espagnol"),
    "4": ("de", "Allemand"),
    "5": ("it", "Italien"),
    "6": ("ja", "Japonais"),
    "7": ("zh", "Chinois")
}

# -----------------------------
# Fonction pour filtrer par genre
# -----------------------------
def genre_filtre():
    genre_valide = False
    df_genre = None

    while not genre_valide:
        print("\n=== MENU DES GENRES ===")
        print("1. Action")
        print("2. Comedy")
        print("3. Drama")
        print("4. Autre genre")
        print("0. Quitter")

        choix_genre = input("Choisissez un genre valide : ").strip()

        if choix_genre == "0":
            return None  # quitter

        if choix_genre == "1":
            genre = "Action"
        elif choix_genre == "2":
            genre = "Comedy"
        elif choix_genre == "3":
            genre = "Drama"
        elif choix_genre == "4":
            genre = input("Entrez le nom du genre valide : ").strip()
        else:
            print("Choix invalide, veuillez saisir une valeur de la liste.")
            continue

        df_genre = df[df["genre"].str.lower() == genre.lower()]
        if df_genre.empty:
            print(f"Aucun film trouvé pour le genre '{genre}'.")
        else:
            genre_valide = True

    return df_genre


# -----------------------------
# Fonction pour filtrer par langue
# -----------------------------
def langue_filtre(df_genre):
    langue_valide = False
    df_final = None

    while not langue_valide:
        print("\n=== FILTRAGE PAR LANGUE ===")
        for num, (code, nom) in langues.items():
            print(f"{num}. {nom} ({code})")
        print("8. Autre langue")
        print("0. Retour au menu des genres")

        choix_langue = input("Entrez votre choix de langue : ").strip()

        if choix_langue == "0":
            return None
        elif choix_langue in langues:
            code_langue, nom_langue = langues[choix_langue]
        elif choix_langue == "8":
            code_langue = input("Entrez le code de la langue (ex: ko, ru, pt...) : ").strip().lower()
        else:
            print("Choix invalide, veuillez saisir une valeur de la liste.")
            continue

        df_final = df_genre[df_genre["langue"].str.lower() == code_langue.lower()]
        if df_final.empty:
            print("Aucun film trouvé pour ce filtre.")
        else:
            print(f"\nFilms trouvés ({len(df_final)}) :")
            print(df_final.head(10))
            langue_valide = True

    return df_final

# -----------------------------
# Boucle principale
# -----------------------------
def programme_filtre():
    programme_actif = True
    
    while programme_actif:
        df_filtre_genre = genre_filtre()
        if df_filtre_genre is None:
            programme_actif = False
        else:
            # Nouvelle étape : demander si on veut filtrer par langue
            print(f"\nFilms trouvés pour ce genre ({len(df_filtre_genre)}) :")
            reponse = input("Voulez vous filtrer par langue ? (o/n) ")

            if reponse == "n":
                print("\n--- Résultats du filtre par genre ---")
                print(df_filtre_genre.head(10))
                input("\nAppuyez sur Entrée pour revenir au menu principal...")
            elif reponse == "o":
                df_filtre_langue = langue_filtre(df_filtre_genre)
                if df_filtre_langue is not None:
                    print("\n--- Recherche terminée ---")
                    input("Appuyez sur Entrée pour revenir au menu principal...")
            else:
                print("Réponse invalide, retour au menu principal.")
