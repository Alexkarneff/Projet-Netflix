import csv
import pandas as pd

# 1 Lecture du fichier CSV

films_data = []

with open("data/dataset/movies_metadata_credits_joined.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for film in reader:
        titre = film.get("original_title", "").strip()
        langue = film.get("original_language", "").strip()
        duree = film.get("runtime", "").strip()
        genres_str = film.get("genres", "")

        genres_list =[]
        if genres_str:
        # Séparer par les virgules et nettoyer chaque genre
            genres_list = [g.strip() for g in genres_str.split(",") if g.strip()]


        # Enregistrer chaque film avec son genre
        if genres_list:
            for genre in genres_list:
                films_data.append({
                    "titre": titre,
                    "genre": genre,
                    "langue": langue,
                    "duree": duree
                })
            else:
                # Film sans genre
                films_data.append({
                    "titre": titre,
                    "genre": "Unknown",
                    "langue": langue,
                    "duree": duree
                })

df = pd.DataFrame(films_data)


# Dictionnaire des langues principales

langues = {
    "1": ("fr", "Français"),
    "2": ("en", "Anglais"),
    "3": ("es", "Espagnol"),
    "4": ("de", "Allemand"),
    "5": ("it", "Italien"),
    "6": ("ja", "Japonais"),
    "7": ("zh", "Chinois")
}

# Naviguer entre les films 5 par 5

def naviguer_films(df_films, titre_contexte="Films"):
   
    if df_films.empty:
        print("Aucun film à afficher.")
        return
    
    total_films = len(df_films)
    films_par_page = 5
    page_actuelle = 0
    total_pages = (total_films + films_par_page - 1) // films_par_page
    
    while True:
        # Calculer les indices de début et fin pour la page actuelle
        debut = page_actuelle * films_par_page
        fin = min(debut + films_par_page, total_films)
        
        # Afficher l'en-tête
        print(f"{titre_contexte} - Page {page_actuelle + 1}/{total_pages}")
        
        # Afficher les films de la page actuelle
        films_page = df_films.iloc[debut:fin]
        for idx, (_, film) in enumerate(films_page.iterrows(), start=debut + 1):
            titre = film.get("titre", "N/A")
            genre = film.get("genre", "N/A")
            langue = film.get("langue", "N/A")
            duree = film.get("duree", "N/A")
            
            print(f"\n{idx}. {titre}")
            print(f"   Genre: {genre} | Langue: {langue} | Durée: {duree} min")
        
        # Afficher les options de navigation
        print("\n" + "-"*60)
        options = []
        if page_actuelle < total_pages - 1:
            options.append("n/Entrée: Suivant")
        if page_actuelle > 0:
            options.append("p: Précédent")
        options.append("q: Quitter")
        print(" | ".join(options))
        
        # Demander l'action à l'utilisateur
        choix = input("\nVotre choix : ").strip().lower()
        
        if choix in ("q", "quit", "quitter"):
            break
        elif choix in ("n", "next", "suivant", ""):
            if page_actuelle < total_pages - 1:
                page_actuelle += 1
            else:
                print("Vous êtes déjà à la dernière page.")
        elif choix in ("p", "prev", "précédent", "precedent"):
            if page_actuelle > 0:
                page_actuelle -= 1
            else:
                print("Vous êtes déjà à la première page.")
        else:
            print("Commande non reconnue. Utilisez 'n' (suivant), 'p' (précédent) ou 'q' (quitter).")
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


        if choix_genre in ("0", "q", "Q"):
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
            # Afficher le nombre de films trouvés
            print(f"\n{len(df_filtre_genre)} films trouvés pour ce genre.")
            
            # Nouvelle option : navigation ou filtre par langue
            print("\nOptions :")
            print("1. Naviguer dans tous les films du genre sélectionné")
            print("2. Filtrer par langue")
            print("0. Retour au menu principal")
            
            reponse = input("\nVotre choix : ").strip()

            if reponse == "1":
                # Navigation dans les films du genre
                naviguer_films(df_filtre_genre, f"Films du genre sélectionné")
                input("\nAppuyez sur Entrée pour revenir au menu principal...")
            elif reponse == "2":
                # Filtre par langue
                df_filtre_langue = langue_filtre(df_filtre_genre)
                if df_filtre_langue is not None and not df_filtre_langue.empty:
                    print(f"\n{len(df_filtre_langue)} films trouvés après filtrage par langue.")
                    
                    # Proposer la navigation sur les films filtrés
                    voir_films = input("Voulez-vous naviguer dans ces films ? (o/n) : ").strip().lower()
                    if voir_films == "o":
                        naviguer_films(df_filtre_langue, "Films filtrés par genre et langue")
                    
                    input("\nAppuyez sur Entrée pour revenir au menu principal...")
            elif reponse == "0":
                continue
            else:
                print("Réponse invalide, retour au menu principal.")
