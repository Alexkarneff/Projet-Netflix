# recherches.py
from __future__ import annotations
import ast
import re
import pandas as pd
import json

# ---------- Couleurs ANSI ----------
class C:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def _parse_list_of_dicts(val, key="name", limit=None):
    """Parse une liste de dictionnaires (genres, cast, etc.)"""
    if pd.isna(val):
        return ""
    try:
        data = ast.literal_eval(val) if isinstance(val, str) else val
        if isinstance(data, list):
            items = []
            for x in data:
                if isinstance(x, dict):
                    items.append(str(x.get(key, "")))
                else:
                    items.append(str(x))
            if limit is not None:
                items = items[:limit]
            return ", ".join(i for i in items if i)
        return str(val)
    except Exception:
        return str(val)

def _truncate(s: str, n: int = 80) -> str:
    """Tronque une chaîne à n caractères"""
    if pd.isna(s):
        return ""
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"

def _parse_duration(val) -> int | None:
    """Convertit la durée en minutes (int)"""
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except:
        return None

def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Prépare le DataFrame avec colonnes optimisées pour la recherche"""
    df_copy = df.copy()
    
    # Colonne genres lisible
    if "genres" in df_copy.columns and "_genres_str" not in df_copy.columns:
        df_copy["_genres_str"] = df_copy["genres"].apply(
            lambda v: _parse_list_of_dicts(v, "name").lower()
        )
    
    # Colonne cast lisible
    if "cast" in df_copy.columns and "_cast_str" not in df_copy.columns:
        df_copy["_cast_str"] = df_copy["cast"].apply(
            lambda v: _parse_list_of_dicts(v, "name").lower()
        )
    
    # Durée en minutes
    if "runtime" in df_copy.columns and "_duration_min" not in df_copy.columns:
        df_copy["_duration_min"] = df_copy["runtime"].apply(_parse_duration)
    
    return df_copy

def _print_fiche_film(film_row: pd.Series, title_col: str):
    """Affiche les informations d'un film de manière formatée"""
    print(f"\n{C.BOLD}{C.HEADER}{'='*60}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}FICHE DU FILM{C.RESET}")
    print(f"{C.BOLD}{C.HEADER}{'='*60}{C.RESET}\n")
    
    # Titre
    titre = film_row.get(title_col, "N/A")
    print(f"{C.BOLD}Titre :{C.RESET} {titre}")
    
    # Date de sortie
    if "release_date" in film_row.index:
        print(f"{C.BOLD}Date de sortie :{C.RESET} {film_row.get('release_date', 'N/A')}")
    
    # Genres
    if "genres" in film_row.index:
        genres = _parse_list_of_dicts(film_row.get("genres"), "name")
        print(f"{C.BOLD}Genres :{C.RESET} {genres if genres else 'N/A'}")
    
    # Langue
    if "original_language" in film_row.index:
        lang = film_row.get("original_language", "N/A")
        print(f"{C.BOLD}Langue :{C.RESET} {lang}")
    
    # Durée
    if "runtime" in film_row.index:
        runtime = film_row.get("runtime", "N/A")
        if pd.notna(runtime):
            print(f"{C.BOLD}Durée :{C.RESET} {runtime} minutes")
    
    # Casting
    if "cast" in film_row.index:
        cast = _parse_list_of_dicts(film_row.get("cast"), "name", limit=5)
        print(f"{C.BOLD}Casting (top 5) :{C.RESET} {cast if cast else 'N/A'}")
    
    # Synopsis
    if "overview" in film_row.index:
        overview = film_row.get("overview", "N/A")
        if pd.notna(overview) and overview != "N/A":
            print(f"\n{C.BOLD}Synopsis :{C.RESET}")
            print(f"{_truncate(str(overview), 300)}")
    
    # Note
    if "vote_average" in film_row.index:
        vote = film_row.get("vote_average", "N/A")
        print(f"\n{C.BOLD}Note moyenne :{C.RESET} {vote}/10")
    
    print(f"\n{C.BOLD}{C.HEADER}{'='*60}{C.RESET}\n")

def prompt(msg: str) -> str:
    """Fonction helper pour les inputs"""
    try:
        return input(msg).strip()
    except EOFError:
        return ""

def _appliquer_filtres_progressifs(df: pd.DataFrame, genre: str, duree_min: int | None, 
                                   duree_max: int | None, acteur: str, langue: str) -> pd.DataFrame:
    """
    Applique les filtres de manière progressive et intelligente.
    Si aucun résultat avec tous les critères, relâche progressivement les contraintes.
    """
    df_filtered = df.copy()
    criteres_appliques = []
    
    # Filtre 1: Genre (le plus restrictif en général)
    if genre:
        mask_genre = df_filtered["_genres_str"].fillna("").str.contains(genre.lower(), case=False, na=False)
        if mask_genre.any():
            df_filtered = df_filtered[mask_genre]
            criteres_appliques.append(f"genre '{genre}'")
    
    # Filtre 2: Acteur
    if acteur and "_cast_str" in df_filtered.columns:
        mask_acteur = df_filtered["_cast_str"].fillna("").str.contains(acteur.lower(), case=False, na=False)
        if mask_acteur.any():
            df_filtered = df_filtered[mask_acteur]
            criteres_appliques.append(f"acteur '{acteur}'")
        elif not criteres_appliques:  # Si c'est le seul critère, on garde quand même
            df_filtered = df_filtered[mask_acteur]
            criteres_appliques.append(f"acteur '{acteur}'")
    
    # Filtre 3: Langue
    if langue and "original_language" in df_filtered.columns:
        mask_langue = df_filtered["original_language"].fillna("").str.contains(langue, case=False, na=False)
        if mask_langue.any():
            df_filtered = df_filtered[mask_langue]
            criteres_appliques.append(f"langue '{langue}'")
    
    # Filtre 4: Durée (appliqué en dernier, plus flexible)
    if (duree_min is not None or duree_max is not None) and "_duration_min" in df_filtered.columns:
        mask_duree = pd.Series(True, index=df_filtered.index)
        
        if duree_min is not None:
            mask_duree &= df_filtered["_duration_min"] >= duree_min
        if duree_max is not None:
            mask_duree &= df_filtered["_duration_min"] <= duree_max
        
        # Si on a des résultats avec la durée exacte, on les prend
        if mask_duree.any():
            df_filtered = df_filtered[mask_duree]
            if duree_min and duree_max:
                criteres_appliques.append(f"durée {duree_min}-{duree_max} min")
            elif duree_min:
                criteres_appliques.append(f"durée >= {duree_min} min")
            else:
                criteres_appliques.append(f"durée <= {duree_max} min")
        else:
            # Sinon, on relâche la contrainte de durée et on cherche "au plus près"
            if duree_min and duree_max:
                duree_cible = (duree_min + duree_max) / 2
                df_filtered["_duree_diff"] = abs(df_filtered["_duration_min"] - duree_cible)
                df_filtered = df_filtered.sort_values("_duree_diff")
                criteres_appliques.append(f"durée proche de {int(duree_cible)} min")
    
    return df_filtered, criteres_appliques



def menu_recherches(df: pd.DataFrame, current_user=None):
    """Menu principal de recherche avec filtres multiples"""
    
    # Préparation du DataFrame (une seule fois)
    print(f"{C.DIM}Préparation des données pour la recherche...{C.RESET}")
    df_prepared = _prepare_dataframe(df)

    
    # Trouver la colonne titre
    title_col = next((c for c in ["original_title", "title", "movie_title"] if c in df_prepared.columns), None)
    if not title_col:
        print(f"{C.RED}[ERREUR]{C.RESET} Aucune colonne titre trouvée dans le dataset.")
        return
    
    while True:
        print(f"\n{C.CYAN}{C.BOLD}{'='*60}{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}RECHERCHE DE FILMS{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}{'='*60}{C.RESET}\n")
        print(f"{C.DIM}Entrez vos critères de recherche (laissez vide pour ignorer un critère){C.RESET}")
        print(f"{C.DIM}Tapez 'q' à tout moment pour revenir au menu principal{C.RESET}\n")
        
        # Collecte des critères
        genre = prompt(f"{C.GREEN}Genre (ex: Action, Comedy, Drama) : {C.RESET}")
        if genre.lower() in {"q", "quit", "exit", "quitter"}:
            return
        
        duree_input = prompt(f"{C.GREEN}Durée (ex: 90, 90-120) : {C.RESET}")
        if duree_input.lower() in {"q", "quit", "exit", "quitter"}:
            return
        
        acteur = prompt(f"{C.GREEN}Acteur/Actrice (nom ou partie du nom) : {C.RESET}")
        if acteur.lower() in {"q", "quit", "exit", "quitter"}:
            return
        
        langue = prompt(f"{C.GREEN}Langue (ex: en, fr, es) : {C.RESET}")
        if langue.lower() in {"q", "quit", "exit", "quitter"}:
            return
        
        # Parse durée
        duree_min, duree_max = None, None
        if duree_input:
            if "-" in duree_input:
                parts = duree_input.split("-")
                try:
                    duree_min = int(parts[0].strip()) if parts[0].strip() else None
                    duree_max = int(parts[1].strip()) if parts[1].strip() else None
                except:
                    print(f"{C.YELLOW}Format de durée invalide, critère ignoré{C.RESET}")
            else:
                try:
                    duree_cible = int(duree_input)
                    duree_min = duree_cible - 15  # ± 15 minutes
                    duree_max = duree_cible + 15
                except:
                    print(f"{C.YELLOW}Format de durée invalide, critère ignoré{C.RESET}")
        
        # Vérifier qu'au moins un critère est fourni
        if not any([genre, duree_input, acteur, langue]):
            print(f"\n{C.YELLOW}Veuillez entrer au moins un critère de recherche.{C.RESET}")
            continue
        
        # Recherche
        print(f"\n{C.DIM}Recherche en cours...{C.RESET}")
        
        results, criteres = _appliquer_filtres_progressifs(
            df_prepared, genre, duree_min, duree_max, acteur, langue
        )
        
        # Enregistrement de la recherche utilisateur
        
        if current_user is not None:
            recherche_info = {
                "genre": genre if genre else None,
                "acteur": acteur if acteur else None,
                "langue": langue if langue else None,
                "duree": duree_input if duree_input else None,
            }
            current_user.search_history.append(recherche_info)
            
            # Mettre à jour les statistiques de genres favoris
            if genre:
                current_user.favorite_genres[genre] = current_user.favorite_genres.get(genre, 0) + 1
            
            # Mettre à jour les statistiques de langue/pays
            if langue:
                current_user.favorite_language[langue] = current_user.favorite_language.get(langue, 0) + 1
            
            # Enregistrer la durée moyenne recherchée
            if duree_min and duree_max:
                duree_moyenne = (duree_min + duree_max) // 2
                current_user.average_duration.append(duree_moyenne)
        
        # Limiter à 5 résultats
        results_limit = results.head(5)
        
        # Affichage des résultats
        
        if criteres:
            print(f"{C.DIM}Critères appliqués : {', '.join(criteres)}{C.RESET}")
        
        if results.empty:
            print(f"\n{C.YELLOW}❌ Aucun film ne correspond à vos critères.{C.RESET}")
            print(f"{C.DIM}Essayez avec des critères moins restrictifs.{C.RESET}")
            
            choix = prompt(f"\n{C.GREEN}Nouvelle recherche ? (Entrée=oui, q=quitter) : {C.RESET}")
            if choix.lower() in {"q", "quit", "exit", "quitter"}:
                return
            continue
        
        print(f"\n{C.BOLD}{C.GREEN}✓ {len(results)} film(s) trouvé(s) (affichage limité à 5){C.RESET}\n")
        
        # Affichage des 5 premiers résultats
        for i, (idx, row) in enumerate(results_limit.iterrows(), 1):
            titre = str(row.get(title_col, ""))
            date = str(row.get("release_date", "")) if "release_date" in row.index else ""
            runtime = row.get("runtime", "")
            runtime_str = f" - {runtime}min" if pd.notna(runtime) else ""
            
            print(f"{C.BLUE}{C.BOLD}[{i}]{C.RESET} {titre}  {C.DIM}{date}{runtime_str}{C.RESET}")
        
        if len(results) > 5:
            print(f"\n{C.DIM}+ {len(results) - 5} autres résultats non affichés{C.RESET}")
        
        # Sélection d'un film ou nouvelle recherche
        print(f"\n{C.DIM}Entrez un numéro (1-5) pour voir les détails, ou Entrée pour nouvelle recherche{C.RESET}")
        sel = prompt(f"{C.GREEN}> Votre choix : {C.RESET}")
        
        if sel.lower() in {"q", "quit", "exit", "quitter"}:
            return
        
        if not sel:
            continue
        
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(results_limit):
                film_row = results_limit.iloc[idx]
                _print_fiche_film(film_row, title_col)
                prompt(f"{C.DIM}Appuyez sur Entrée pour continuer...{C.RESET}")
            else:
                print(f"{C.YELLOW}Numéro invalide (1-5 uniquement).{C.RESET}")
        else:
            print(f"{C.YELLOW}Sélection invalide.{C.RESET}")