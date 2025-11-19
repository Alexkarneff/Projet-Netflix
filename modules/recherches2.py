# recherches.py
from __future__ import annotations
import argparse
import ast
import sys
import re
import math
import pandas as pd
from pathlib import Path

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

BASE = Path(__file__).parent
DEFAULT_DATA = BASE / "../data/dataset/movies_metadata_credits_joined 2.csv"

# ---------- Utils CSV ----------
def load_dataframe(path_str: str | Path) -> pd.DataFrame:
    p = Path(path_str).expanduser().resolve()
    if not p.exists():
        print(f"{C.RED}[ERREUR]{C.RESET} Fichier introuvable : {p}", flush=True)
        sys.exit(1)
    return pd.read_csv(p, low_memory=False, dtype=str)

def _parse_list_of_dicts(val, key="name", limit=None):
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
    if pd.isna(s):
        return ""
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"

# ---------- Durées ----------
_DURATION_COL_CANDIDATES = ["runtime", "duration", "length", "running_time", "time"]

def _parse_duration_to_minutes(raw) -> int | None:
    if raw is None or (isinstance(raw, float) and math.isnan(raw)):
        return None
    s = str(raw).strip().lower()
    if not s:
        return None
    # nombre simple => minutes (si très grand → secondes)
    try:
        f = float(s)
        return int(round(f / 60)) if f > 10000 else int(round(f))
    except Exception:
        pass
    # HH:MM
    m = re.fullmatch(r"(\d{1,2}):(\d{1,2})", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    # XhYY / X h YY
    m = re.fullmatch(r"(\d+)\s*h\s*(\d+)", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    # Xh
    m = re.fullmatch(r"(\d+)\s*h", s)
    if m:
        return int(m.group(1)) * 60
    # YYm / min / minutes
    m = re.fullmatch(r"(\d+)\s*(m|min|mins|minute|minutes)", s)
    if m:
        return int(m.group(1))
    # secondes → minutes
    m = re.fullmatch(r"(\d+)\s*(s|sec|secs|seconde|secondes)", s)
    if m:
        return int(round(int(m.group(1)) / 60))
    return None

def _ensure_duration_minutes(df: pd.DataFrame) -> pd.DataFrame:
    if "_duration_min" in df.columns:
        return df
    minutes = None
    for col in _DURATION_COL_CANDIDATES:
        if col in df.columns:
            minutes = df[col].apply(_parse_duration_to_minutes)
            break
    if minutes is None:
        minutes = pd.Series([None] * len(df), index=df.index)
    df["_duration_min"] = minutes
    return df

def _ensure_year_column(df: pd.DataFrame) -> pd.DataFrame:
    """Crée une colonne _year (int) à partir de release_year/year/release_date si possible."""
    if "_year" in df.columns:
        return df
    year_col = None
    for c in ["release_year", "year", "release_date"]:
        if c in df.columns:
            year_col = c
            break
    if year_col is None:
        df["_year"] = pd.Series([None] * len(df), index=df.index)
        return df

    if year_col == "release_date":
        years = pd.to_numeric(df[year_col].str.slice(0, 4), errors="coerce")
    else:
        years = pd.to_numeric(df[year_col], errors="coerce")
    df["_year"] = years
    return df

def _ensure_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    if "_genres" not in df.columns and "genres" in df.columns:
        df["_genres"] = df["genres"].apply(
            lambda v: _truncate(_parse_list_of_dicts(v, "name"), 80)
        )
    if "_cast" not in df.columns and "cast" in df.columns:
        df["_cast"] = df["cast"].apply(
            lambda v: _truncate(_parse_list_of_dicts(v, "name", limit=8), 120)
        )
    df = _ensure_duration_minutes(df)
    df = _ensure_year_column(df)
    return df

def make_readable(df: pd.DataFrame, limit: int | None = None) -> pd.DataFrame:
    res = _ensure_display_columns(df.copy())
    title_col = next((c for c in ["title", "original_title", "movie_title"] if c in res.columns), None)
    date_col  = next((c for c in ["release_date", "year", "release_year"] if c in res.columns), None)
    cols = [c for c in [title_col, date_col, "_genres", "_cast", "_duration_min"] if c]
    if not cols:
        cols = list(res.columns[:5])
    out = res.loc[:, cols]
    if limit is not None:
        out = out.head(limit)
    pd.set_option("display.max_colwidth", 140)
    return out

# ---------- Helpers affichage ciblé ----------
def _print_only_column(df: pd.DataFrame, column: str, label: str | None = None, limit: int = 20):
    """Affiche uniquement la colonne demandée (sortie la plus précise possible)."""
    if column not in df.columns:
        print(f"{C.YELLOW}[INFO]{C.RESET} Colonne '{column}' indisponible.", flush=True)
        return
    ser = df[column].dropna()
    if ser.empty:
        print("Aucun résultat.", flush=True)
        return
    to_show = pd.DataFrame({label or column: ser.head(limit)})
    print(to_show.to_string(index=False), flush=True)

def _print_fiche_complete(film_row: pd.Series):
    """Affichage complet des infos d'un film."""
    print(f"\n{C.BOLD}{C.HEADER}=== Fiche complète du film ==={C.RESET}", flush=True)
    champs_cles = [
        "title", "original_title", "movie_title",
        "overview",
        "release_date", "year", "release_year", "_year",
        "original_language",
        "runtime", "_duration_min",
        "genres", "_genres",
        "cast", "_cast",
        "vote_average", "vote_count",
        "budget", "revenue",
        "id", "imdb_id"
    ]
    for champ in champs_cles:
        if champ in film_row.index:
            val = film_row.get(champ)
            label = champ
            if champ in ("genres", "cast"):
                val = _parse_list_of_dicts(val, "name")
            if champ == "_duration_min":
                label = "duration_min"
            if champ == "_genres":
                label = "genres_lisibles"
            if champ == "_cast":
                label = "cast_lisible"
            print(f"{C.BOLD}{label}{C.RESET} : {val}", flush=True)

# ---------- Menus ----------
def prompt(msg: str) -> str:
    try:
        return input(msg).strip()
    except EOFError:
        return ""

def menu_principal(df: pd.DataFrame):
    while True:
        print(f"\n{C.CYAN}{C.BOLD}=== Moteur de recherche de films (CSV) ==={C.RESET}", flush=True)
        print(f"{C.DIM}Tapez un titre ou une partie de titre, ou 'q' pour quitter.{C.RESET}", flush=True)
        titre = prompt(f"{C.GREEN}> Nom (ou partie du nom) : {C.RESET}")
        if titre.lower() in {"q", "quit", "exit"}:
            print("Au revoir 👋", flush=True)
            return

        title_col = next((c for c in ["original_title", "title", "movie_title"] if c in df.columns), None)
        if not title_col:
            print(f"{C.RED}[ERREUR]{C.RESET} Aucune colonne titre trouvée dans le CSV.", flush=True)
            return

        mask = df[title_col].fillna("").str.contains(re.escape(titre), case=False, na=False)
        results = df[mask]

        if results.empty:
            print(f"{C.YELLOW}Le titre recherché n'est pas dans la base de donnée.{C.RESET}", flush=True)
            choix = prompt('> Saisir "revenir au menu précédent" pour revenir, ou Entrée pour réessayer : ')
            if choix.lower() == "revenir au menu précédent" | "q":
                continue
            else:
                continue

        readable = make_readable(results, limit=5)
        print(f"\n{C.BOLD}Résultats trouvés (max 5) :{C.RESET}\n", flush=True)
        for i, (_, row) in enumerate(readable.iterrows(), start=1):
            t = str(row.get(title_col, ""))
            d = str(row.get("release_date", "")) if "release_date" in readable.columns else ""
            print(f"{C.BLUE}[{i}]{C.RESET} {t}  {C.DIM}{d}{C.RESET}", flush=True)

        while True:
            sel = prompt(f'\n{C.GREEN}> Choisis un numéro (ou tape "revenir au menu précédent") : {C.RESET}')
            if sel.lower() == "revenir au menu précédent":
                break
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(readable):
                    # Récupérer l’index réel dans le DataFrame d’origine
                    chosen_index = results.iloc[idx:idx+1].index[0]
                    film_row = results.loc[chosen_index]

                    # Afficher la fiche détaillée du film avant le sous-menu filtres
                    print(f"\n{C.BOLD}{C.CYAN}=== Informations sur le film sélectionné ==={C.RESET}", flush=True)
                    detail_df = make_readable(results.loc[[chosen_index]], limit=1)
                    print(detail_df.to_string(index=False), flush=True)

                    # Puis lancer le sous-menu filtres
                    submenu_filtres(df, film_row, title_col)
                    break
            print(f"{C.YELLOW}Sélection invalide.{C.RESET}", flush=True)

def _afficher_filtre_colonly(df: pd.DataFrame, colonne_filtre: str, valeur: str,
                             col_reelle: str | None = None,
                             only_print_col: str | None = None,
                             label: str | None = None):
    """
    Filtre sur `colonne_filtre` (ou `col_reelle` si colonne absente) avec sous-chaîne `valeur`,
    puis n'imprime QUE la colonne `only_print_col` (ou la colonne effective si None).
    """
    col = colonne_filtre if colonne_filtre in df.columns else (
        col_reelle if col_reelle and col_reelle in df.columns else None
    )
    if not col:
        print(f"{C.YELLOW}[INFO]{C.RESET} Colonne '{colonne_filtre}' indisponible.", flush=True)
        return
    if not valeur:
        print(f"{C.YELLOW}[INFO]{C.RESET} Pas de valeur à filtrer.", flush=True)
        return

    mask = df[col].fillna("").str.contains(re.escape(valeur), case=False, na=False)
    subset = df[mask]
    if subset.empty:
        print("Aucun résultat.", flush=True)
        return

    col_affichee = only_print_col or col
    _print_only_column(subset, col_affichee, label=label or col_affichee, limit=10)

def _filtrer_par_duree(df: pd.DataFrame, min_min: int | None, max_min: int | None, title_col: str):
    """
    Filtre les films par durée (en minutes) sur toute la base, puis affiche
    titre + date + durée (en minutes).
    """
    df = _ensure_duration_minutes(df.copy())
    durees = pd.to_numeric(df["_duration_min"], errors="coerce")
    mask = pd.Series(True, index=df.index)

    if min_min is not None:
        mask &= durees >= min_min
    if max_min is not None:
        mask &= durees <= max_min

    subset = df[mask]
    if subset.empty:
        print("Aucun film ne correspond à cette plage de durée.", flush=True)
        return

    cols = []
    if title_col and title_col in subset.columns:
        cols.append(title_col)
    else:
        cols.append(subset.columns[0])

    if "release_date" in subset.columns:
        cols.append("release_date")
    cols.append("_duration_min")

    to_show = subset.loc[:, cols].head(5)
    to_show = to_show.rename(columns={"_duration_min": "duration_min"})
    print(f"\n{C.BOLD}Films trouvés :{C.RESET}", flush=True)
    print(to_show.to_string(index=False), flush=True)

def _filtrer_par_annee(df: pd.DataFrame, year_str: str, title_col: str):
    df_local = _ensure_year_column(df.copy())
    try:
        year = int(year_str)
    except ValueError:
        print(f"{C.YELLOW}Année invalide (entrez un entier comme 1995).{C.RESET}", flush=True)
        return

    mask = df_local["_year"] == year
    subset = df_local[mask]
    if subset.empty:
        print("Aucun film trouvé pour cette année.", flush=True)
        return

    cols = []
    if title_col in subset.columns:
        cols.append(title_col)
    if "release_date" in subset.columns:
        cols.append("release_date")
    cols.append("_year")

    to_show = subset.loc[:, cols].head(5).rename(columns={"_year": "year"})
    print(f"\n{C.BOLD}Films sortis en {year} :{C.RESET}", flush=True)
    print(to_show.to_string(index=False), flush=True)

def submenu_filtres(df: pd.DataFrame, film_row: pd.Series, title_col: str):
    """
    Sous-menu qui permet de lancer des recherches par filtres,
    en n'affichant que certaines colonnes (par exemple uniquement 'original_title').
    """
    while True:
        print(f"\n{C.CYAN}{C.BOLD}=== Sous-menu filtres ==={C.RESET}", flush=True)
        print(f"{C.DIM}Film sélectionné :{C.RESET} {film_row.get(title_col, '')}", flush=True)
        print("0) Afficher la fiche complète de ce film", flush=True)
        print("1) Filtrer par original_title ", flush=True)
        print("2) Filtrer par genre ", flush=True)
        print("3) Acteur/actrice (casting + recherche dans toute la base)", flush=True)
        print("4) Filtrer par durée (en minutes, sur toute la base)", flush=True)
        print("5) Filtrer par année de sortie", flush=True)
        print("q) Revenir au menu précédent", flush=True)

        choix = prompt(f"{C.GREEN}> Votre choix : {C.RESET}")

        if choix == "0":
            _print_fiche_complete(film_row)

        elif choix == "1":
            crit = prompt("> Partie de titre (original_title) : ")
            _afficher_filtre_colonly(
                df,
                colonne_filtre="original_title",
                valeur=crit,
                only_print_col="original_title",
                label="original_title",
            )

        elif choix == "2":
            crit = prompt("> Genre (ex: Action, Drama...) : ")

            df_local = _ensure_display_columns(df.copy())
            if "_genres" not in df_local.columns:
                print(f"{C.YELLOW}[INFO]{C.RESET} Colonne '_genres' indisponible.", flush=True)
            else:
                mask = df_local["_genres"].fillna("").str.contains(re.escape(crit), case=False, na=False)
                subset = df_local[mask]

                if subset.empty:
                    print("Aucun résultat.", flush=True)
                else:
                    cols = []
                    if title_col in subset.columns:
                        cols.append(title_col)
                    if "_genres" in subset.columns:
                        cols.append("_genres")

                    to_show = subset.loc[:, cols].head(5).rename(
                        columns={title_col: "Titre", "_genres": "Genres"}
                    )
                    print(f"\n{C.BOLD}Films trouvés pour ce genre :{C.RESET}", flush=True)
                    print(to_show.to_string(index=False), flush=True)

        elif choix == "3":
            # Sous-menu spécifique pour les acteurs / actrices
            while True:
                print(f"\n{C.CYAN}--- Sous-menu acteur/actrice ---{C.RESET}", flush=True)
                print("1) Afficher le casting complet de ce film", flush=True)
                print("2) Chercher tous les films avec un acteur/actrice donné", flush=True)
                print("q) Retour au sous-menu filtres", flush=True)

                sub = prompt(f"{C.GREEN}> Votre choix (acteur) : {C.RESET}")

                if sub == "1":
                    raw_cast = film_row.get("cast", "")
                    if pd.isna(raw_cast) or not str(raw_cast).strip():
                        print("Aucune information de casting pour ce film.", flush=True)
                    else:
                        cast_str = _parse_list_of_dicts(raw_cast, key="name")
                        noms = [n.strip() for n in cast_str.split(",") if n.strip()]
                        if not noms:
                            print("Aucune information de casting pour ce film.", flush=True)
                        else:
                            print(f"\n{C.BOLD}Acteurs / actrices :{C.RESET}", flush=True)
                            for nom in noms:
                                print(f"- {nom}", flush=True)

                elif sub == "2":
                    crit = prompt("> Nom (ou partie du nom) de l'acteur/actrice : ")
                    _afficher_filtre_colonly(
                        df,
                        colonne_filtre="cast",
                        valeur=crit,
                        only_print_col=title_col,
                        label="Titre",
                    )

                elif sub.lower() in {"q", "quit", "exit"}:
                    break

                else:
                    print("Choix invalide.", flush=True)

        elif choix == "4":
            # Sous-menu spécifique pour la durée
            while True:
                print(f"\n{C.CYAN}--- Sous-menu durée (minutes) ---{C.RESET}", flush=True)
                print("Entrez une plage de durée en minutes (laisser vide pour pas de borne).", flush=True)
                print("q) Retour au sous-menu filtres", flush=True)

                min_str = prompt("> Durée minimale (en minutes) ou q pour revenir : ")
                if min_str.lower() in {"q", "quit", "exit"}:
                    break

                max_str = prompt("> Durée maximale (en minutes) (laisser vide si aucune borne haute) : ")

                def _to_int_or_none(s: str) -> int | None:
                    s = s.strip()
                    if not s:
                        return None
                    try:
                        return int(s)
                    except ValueError:
                        return None

                min_min = _to_int_or_none(min_str)
                max_min = _to_int_or_none(max_str)

                if min_min is None and min_str.strip():
                    print("Valeur minimale invalide, veuillez entrer un entier ou laisser vide.", flush=True)
                    continue
                if max_min is None and max_str.strip():
                    print("Valeur maximale invalide, veuillez entrer un entier ou laisser vide.", flush=True)
                    continue

                _filtrer_par_duree(df, min_min, max_min, title_col)

        elif choix == "5":
            year_str = prompt("> Année (ex: 1995) : ")
            _filtrer_par_annee(df, year_str, title_col)

        elif choix.lower() in {"q", "quit", "exit"}:
            break

        else:
            print("Choix invalide.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Moteur de recherche de films sur CSV.")
    parser.add_argument(
        "--data",
        type=str,
        default=str(DEFAULT_DATA),
        help="Chemin vers le fichier CSV fusionné (movies_metadata_credits_joined.csv).",
    )
    args = parser.parse_args()

    df = load_dataframe(args.data)
    df = _ensure_display_columns(df)

    print(f"{C.DIM}[INFO] Fichier chargé : {args.data}{C.RESET}", flush=True)
    print(f"{C.DIM}[INFO] Nombre de lignes : {len(df)}{C.RESET}", flush=True)

    menu_principal(df)

if __name__ == "__main__":
    main()
