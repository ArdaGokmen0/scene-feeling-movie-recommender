import streamlit as st

from src.data_loader import load_movies
from src.language_utils import normalize_scene_text
from src.recommender import MovieRecommender
from src.text_utils import analyze_scene_text


st.set_page_config(
    page_title="Scene-Based Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


@st.cache_data
def get_data():
    return load_movies()


@st.cache_resource
def get_recommender(df, use_embeddings):
    return MovieRecommender(df, use_embeddings=use_embeddings)


@st.cache_data
def get_movie_options(_df):
    option_df = _df.copy()

    if "vote_count" in option_df.columns:
        option_df["is_reliable"] = option_df["vote_count"].fillna(0) >= 100
        option_df = option_df.sort_values(
            ["is_reliable", "vote_average", "popularity"],
            ascending=[False, False, False]
        )
    else:
        option_df = option_df.sort_values(
            ["vote_average", "popularity"],
            ascending=[False, False]
        )

    option_df = option_df.drop_duplicates(subset=["title"], keep="first")

    movie_options = {}
    for _, row in option_df.iterrows():
        year = f" ({row['year']})" if row["year"] else ""
        rating = row["vote_average"] if row["vote_average"] else 0
        label = f"{row['title']}{year} - {rating:.1f}"
        movie_options[label] = row["title"]

    return movie_options


def get_movie_suggestions(recommender, movie_title):
    try:
        if hasattr(recommender, "suggest_movie_titles"):
            return recommender.suggest_movie_titles(movie_title)
    except Exception:
        return []

    return []


def get_resolved_movie_title(recommender, movie_title):
    try:
        movie_index = recommender.find_movie_index(movie_title)
        if movie_index is not None:
            return recommender.df.iloc[movie_index]["title"]
    except Exception:
        return None

    return None


def clear_recommendation_state():
    for key in [
        "recommendations",
        "visible_indices",
        "dismissed_indices",
        "next_replacement_index",
        "matched_movies",
        "scene_analysis",
        "normalized_scene_text",
        "original_scene_text",
        "result_use_embeddings",
        "end_of_recommendations",
    ]:
        st.session_state.pop(key, None)


def dismiss_recommendation(candidate_index, slot_index):
    st.session_state.dismissed_indices.append(candidate_index)

    next_index = st.session_state.next_replacement_index
    recommendations = st.session_state.recommendations

    while next_index < len(recommendations) and next_index in st.session_state.dismissed_indices:
        next_index += 1

    if next_index < len(recommendations):
        st.session_state.visible_indices[slot_index] = next_index
        st.session_state.next_replacement_index = next_index + 1
    else:
        st.session_state.visible_indices.pop(slot_index)
        st.session_state.next_replacement_index = next_index
        st.session_state.end_of_recommendations = True


def show_scene_analysis(scene_analysis, normalized_scene_text, original_scene_text):
    if not original_scene_text.strip():
        return

    st.subheader("Scene Analysis")

    if normalized_scene_text != original_scene_text:
        st.caption("Normalized scene meaning:")
        st.write(normalized_scene_text)

    has_scene_tags = any(scene_analysis.values())

    if has_scene_tags:
        motifs = ", ".join(scene_analysis["motifs"]) or "None detected"
        tone = ", ".join(scene_analysis["tone"]) or "None detected"
        character_dynamics = ", ".join(scene_analysis["character_dynamics"]) or "None detected"

        st.write(f"**Motifs:** {motifs}")
        st.write(f"**Tone:** {tone}")
        st.write(f"**Character dynamics:** {character_dynamics}")
        st.write(
            "These signals help the recommender look for movies with a similar emotional or motif-based appeal, "
            "not just similar genres."
        )
        st.info("Your scene description adds a small supporting signal; your favorite movies still guide the main recommendations.")
    else:
        st.info("No clear scene motifs detected yet. Try describing the scene with more detail.")


def show_recommendations(recommender):
    if "recommendations" not in st.session_state:
        return

    recommendations = st.session_state.recommendations
    visible_indices = st.session_state.visible_indices
    scene_analysis = st.session_state.scene_analysis
    matched_movies = st.session_state.matched_movies
    original_scene_text = st.session_state.original_scene_text
    result_use_embeddings = st.session_state.result_use_embeddings

    st.subheader("Recommendations")

    for slot_index, candidate_index in enumerate(list(visible_indices)):
        row = recommendations.iloc[candidate_index]

        with st.container(border=True):
            title_line = row["title"]

            if row["year"]:
                title_line += f" ({row['year']})"

            st.markdown(f"### {title_line}")

            genres = ", ".join(row["genre_list"])
            if genres:
                st.caption(genres)

            st.write(row["overview"])

            st.markdown("**Why recommended:**")

            reasons = recommender.generate_baseline_reason(row, matched_movies)

            for reason in reasons:
                st.markdown(f"- {reason}")

            if scene_analysis and scene_analysis["motifs"]:
                scene_motifs = ", ".join(scene_analysis["motifs"])
                st.caption(
                    f"Scene motifs detected: {scene_motifs}. "
                    "They gently support the recommendation, but do not override your favorite movies."
                )

            if scene_analysis and any(scene_analysis.values()):
                st.caption(f"Scene feeling match: {row['scene_bonus']:.2f}")

            if result_use_embeddings and original_scene_text.strip():
                st.caption(f"Meaning-based scene match: {row['scene_semantic_similarity']:.2f}")

            st.caption(
                f"Rating: {row['vote_average']} | Popularity: {round(row['popularity'], 2)}"
            )

            if st.button("I've watched this film", key=f"watched_{candidate_index}_{row['title']}"):
                dismiss_recommendation(candidate_index, slot_index)
                st.rerun()

    if st.session_state.end_of_recommendations:
        st.info("We've reached the end of the recommendation list for this search.")


df = get_data()
movie_options = get_movie_options(df)
use_embeddings = st.sidebar.toggle("Use semantic similarity", value=False)
recommender = get_recommender(df, use_embeddings)


st.title("Scene-Based Movie Recommender")

st.write(
    "Get movie recommendations based not only on what you liked, "
    "but eventually on why you liked it."
)

if use_embeddings:
    st.caption("Semantic mode is on, so recommendations can use meaning-based similarity.")

st.divider()

st.subheader("Your favorite movies")
st.caption("Search and choose movies that exist in the dataset.")

selected_movie_labels = st.multiselect(
    "Choose exactly 3 favorite movies from the dataset",
    options=list(movie_options.keys()),
    placeholder="Search movies..."
)


scene_text = st.text_area(
    "Describe one unforgettable scene from any of these movies, if you want more personalized recommendations.",
    placeholder="Example: A character reveals hidden intelligence and shocks everyone in the room...",
    height=120
)

recommend_button = st.button("Recommend movies")
favorite_movies = [movie_options[label] for label in selected_movie_labels]
search_signature = (
    tuple(favorite_movies),
    scene_text,
    use_embeddings,
)

if (
    "search_signature" in st.session_state and
    st.session_state.search_signature != search_signature
):
    clear_recommendation_state()
    st.session_state.pop("search_signature", None)


if recommend_button:
    if len(favorite_movies) < 3:
        st.warning("Choose exactly 3 favorite movies to get recommendations.")
    elif len(favorite_movies) > 3:
        st.warning("Choose only 3 favorite movies so the recommender has a focused taste profile.")
    else:
        normalized_scene_text = normalize_scene_text(scene_text) if scene_text.strip() else scene_text
        scene_analysis = analyze_scene_text(normalized_scene_text) if normalized_scene_text.strip() else None

        recommendations, matched_movies = recommender.recommend_from_favorites(
            favorite_movies,
            top_n=15,
            scene_analysis=scene_analysis,
            scene_text=normalized_scene_text
        )

        if len(matched_movies) == 0:
            st.error("I could not find any of those movies. Try original English movie titles.")
        else:
            clear_recommendation_state()
            recommendations = recommendations.reset_index(drop=True)
            st.session_state.recommendations = recommendations
            st.session_state.visible_indices = list(range(min(5, len(recommendations))))
            st.session_state.dismissed_indices = []
            st.session_state.next_replacement_index = min(5, len(recommendations))
            st.session_state.matched_movies = matched_movies
            st.session_state.scene_analysis = scene_analysis
            st.session_state.normalized_scene_text = normalized_scene_text
            st.session_state.original_scene_text = scene_text
            st.session_state.result_use_embeddings = use_embeddings
            st.session_state.end_of_recommendations = False
            st.session_state.search_signature = search_signature

            st.success(f"Using these movies: {', '.join(matched_movies)}")

if "recommendations" in st.session_state:
    show_scene_analysis(
        st.session_state.scene_analysis,
        st.session_state.normalized_scene_text,
        st.session_state.original_scene_text
    )
    show_recommendations(recommender)
