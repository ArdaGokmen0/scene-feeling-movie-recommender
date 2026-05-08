import ast
import pandas as pd


def parse_name_list(value):
    """
    TMDB columns like genres/keywords are stored as stringified lists of dictionaries.
    Example:
    "[{'id': 28, 'name': 'Action'}, {'id': 12, 'name': 'Adventure'}]"
    This function extracts only the names.
    """
    try:
        items = ast.literal_eval(value)
        return [item["name"] for item in items]
    except Exception:
        return []


def load_movies(movies_path="data/tmdb_5000_movies.csv", credits_path="data/tmdb_5000_credits.csv"):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # Merge movies with credits
    df = movies.merge(credits, on="title", how="left")

    # Keep useful columns
    useful_columns = [
        "id",
        "title",
        "overview",
        "genres",
        "keywords",
        "popularity",
        "vote_average",
        "vote_count",
        "release_date",
        "cast",
        "crew",
    ]

    df = df[[col for col in useful_columns if col in df.columns]].copy()

    # Clean missing values
    df["overview"] = df["overview"].fillna("")
    df["release_date"] = df["release_date"].fillna("")
    df["popularity"] = df["popularity"].fillna(0)
    df["vote_average"] = df["vote_average"].fillna(0)
    df["vote_count"] = df["vote_count"].fillna(0)

    # Parse genres and keywords
    df["genre_list"] = df["genres"].apply(parse_name_list)
    df["keyword_list"] = df["keywords"].apply(parse_name_list)

    # Text versions
    df["genres_text"] = df["genre_list"].apply(lambda x: " ".join(x))
    df["keywords_text"] = df["keyword_list"].apply(lambda x: " ".join(x))

    # Search-friendly title
    df["title_clean"] = df["title"].str.lower().str.strip()

    # Year
    df["year"] = df["release_date"].apply(lambda x: str(x)[:4] if isinstance(x, str) and len(x) >= 4 else "")

    # Main text used for similarity
    df["content"] = (
        df["overview"] + " " +
        df["genres_text"] + " " +
        df["keywords_text"]
    )

    return df