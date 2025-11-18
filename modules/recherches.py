# recherches.py
from __future__ import annotations
from pathlib import Path
import argparse
import ast
import sys
import pandas as pd

# === Chemin par défaut : CSV dans le même dossier que ce script ===
BASE = Path(__file__).parent
DEFAULT_DATA = BASE / "..\data\dataset\movies_metadata_credits_joined 2.csv"

def load_dataframe(path_str: str | Path) -> pd.DataFrame:
    p = Path(path_str).expanduser().resolve()
    if not p.exists():
        print(f"[ERREUR] Fichier introuvable : {p}")
        sys.exit(1)
    # dtype=str pour garder les colonnes en texte et éviter les surprises
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

def make_readable(df: pd.DataFrame, limit: int) -> pd.DataFrame:
    res = df.copy()

    # Colonnes “propres”
    if "genres" in res.columns:
        res["_genres"] = res["genres"].apply(lambda v: _truncate(_parse_list_of_dicts(v, "name"), 80))
    if "cast" in res.columns:
        res["_cast"] = res["cast"].apply(lambda v: _truncate(_parse_list_of_dicts(v, "name", limit=8), 120))

    # Colonnes de titre/date utilisées si présentes
    title_col = next((c for c in ["title", "original_title", "movie_title"] if c in res.columns), None)
    date_col  = next((c for c in ["release_date", "year", "release_year"] if c in res.columns), None)

    cols = [c for c in [title_col, date_col, "_genres", "_cast"] if c]
    if not cols:
        # secours : affiche les 5 premières colonnes existantes
        cols = list(res.columns[:5])

    out = res.loc[:, [c for c in cols if c in res.columns]].head(limit)
    pd.set_option("display.max_colwidth", 140)
    return out

def main():
    ap = argparse.ArgumentParser(description="Recherche lisible dans movies_metadata_credits_joined.csv")
    ap.add_argument("--data", default=str(DEFAULT_DATA), help="Chemin du CSV (défaut: fichier à côté du script)")
    ap.add_argument("--limit", type=int, default=5, help="Nombre max de lignes à afficher")
    ap.add_argument("--genre", help="Filtrer sur un genre (texte contient)")
    ap.add_argument("--actor", help="Filtrer sur un acteur (texte contient)")
    args = ap.parse_args()

    df = load_dataframe(args.data)

    # filtres simples si demandés
    mask = pd.Series([True] * len(df))
    if args.genre and "genres" in df.columns:
        mask &= df["genres"].fillna("").str.contains(args.genre, case=False, na=False)
    if args.actor and "cast" in df.columns:
        mask &= df["cast"].fillna("").str.contains(args.actor, case=False, na=False)

    df_filtered = df[mask]
    pretty = make_readable(df_filtered, args.limit)
    if pretty.empty:
        print("Aucun résultat.")
    else:
        print(pretty.to_string(index=False))

if __name__ == "__main__":
    main()