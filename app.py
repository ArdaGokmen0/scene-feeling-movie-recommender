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


df = get_data()
use_embeddings = st.sidebar.toggle("Use semantic similarity", value=False)
recommender = get_recommender(df, use_embeddings)


st.title("Scene-Based Movie Recommender")

st.write(
    "Get movie recommendations based not only on what you liked, "
    "but eventually on why you liked it."
)

if use_embeddings:
    st.caption("Semantic similarity mode is enabled.")

st.divider()

st.subheader("Your favorite movies")
st.caption("Use original movie titles in English, for example: Now You See Me.")

col1, col2, col3 = st.columns(3)

with col1:
    movie_1 = st.text_input("Favorite movie 1", placeholder="Example: Inception")

with col2:
    movie_2 = st.text_input("Favorite movie 2", placeholder="Example: Interstellar")

with col3:
    movie_3 = st.text_input("Favorite movie 3", placeholder="Example: The Dark Knight")


scene_text = st.text_area(
    "Describe one unforgettable scene from any of these movies, if you want more personalized recommendations.",
    placeholder="Example: A character reveals hidden intelligence and shocks everyone in the room...",
    height=120
)

recommend_button = st.button("Recommend movies")


if recommend_button:
    favorite_movies = [movie_1, movie_2, movie_3]
    favorite_movies = [m for m in favorite_movies if m.strip()]

    if len(favorite_movies) < 3:
        st.warning("Please enter 3 favorite movies.")
    else:
        normalized_scene_text = normalize_scene_text(scene_text) if scene_text.strip() else scene_text
        scene_analysis = analyze_scene_text(normalized_scene_text) if normalized_scene_text.strip() else None

        recommendations, matched_movies = recommender.recommend_from_favorites(
            favorite_movies,
            top_n=5,
            scene_analysis=scene_analysis,
            scene_text=normalized_scene_text
        )

        unmatched_movies = []
        for movie_title in favorite_movies:
            if recommender.find_movie_index(movie_title) is None:
                unmatched_movies.append(movie_title)

        if len(matched_movies) == 0:
            st.error("None of the movies were found in the dataset. Try more popular English movie titles.")

            for movie_title in unmatched_movies:
                suggestions = recommender.suggest_movie_titles(movie_title)
                if suggestions:
                    st.info(f"Could not find '{movie_title}'. Did you mean: {', '.join(suggestions)}?")
        else:
            st.success(f"Matched movies: {', '.join(matched_movies)}")

            for movie_title in unmatched_movies:
                suggestions = recommender.suggest_movie_titles(movie_title)
                if suggestions:
                    st.info(f"Could not find '{movie_title}'. Did you mean: {', '.join(suggestions)}?")
                else:
                    st.info(f"Could not find '{movie_title}'. Try the original English TMDB title.")

            if scene_text.strip():
                st.subheader("Scene Analysis")

                if normalized_scene_text != scene_text:
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
                    st.info("A small scene-based bonus is now included while keeping the original movie similarity system.")
                else:
                    st.info("No clear scene motifs detected yet. Try describing the scene with more detail.")

            st.subheader("Top 5 Recommendations")

            for _, row in recommendations.iterrows():
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
                            "These motifs are used as a small bonus in the recommendation score."
                        )

                    if scene_analysis and any(scene_analysis.values()):
                        st.caption(f"Scene bonus: {row['scene_bonus']:.2f}")

                    if use_embeddings and scene_text.strip():
                        st.caption(f"Scene semantic similarity: {row['scene_semantic_similarity']:.2f}")

                    st.caption(
                        f"Rating: {row['vote_average']} | Popularity: {round(row['popularity'], 2)}"
                    )
