import streamlit as st
from movierec import load_data, preprocess_data, create_similarity_engine, recommend_movies, filter_movies, create_filtered_similarity_engine, separate_genres
from PIL import Image

mdata = load_data() # first we load the data
mdata = preprocess_data(mdata) # here we tell streamlit to cache the result of the preprocess_data function
similarity_matrix, tfidf = create_similarity_engine(mdata) # this basically tells streamlit to store the result of creating a TF-IDF matrix, and calculating the similarity matrix.

img1 = Image.open('/Users/hectorchaves/Documents/GitHub/Scientific-Programming---Project/images/IMG_0116.PNG')
st.image(img1, use_container_width=True)
st.title("Dani's Cinema")

mdata_separated = separate_genres(mdata) # separate genres before any filtering

unique_genres_list = ['Action', 'Adventure', 'Sci-Fi', 'Horror', 'Thriller', 'Animation', 'Comedy', 'Family', 'Fantasy', 'Drama', 'Music', 'Biography', 'History', 'Romance', 'Crime', 'Western', 'War', 'Mystery'] 
# using the mdata_separated for the unique (individual) genres

# genre selection with a drop down

selected_genre = st.selectbox("Select the genre of the movie you are looking for:", ["All"] + unique_genres_list, key="genre_selectbox")

# year selection with checkboxes

years = sorted(mdata['Year'].unique())
selected_years = st.multiselect("Select the year in which the movie you are looking for was released:", years, key="year_multiselect")

# filtering the data

filtered_mdata_app = filter_movies(mdata_separated, selected_genre, selected_years)
filtered_similarity_matrix = None
filtered_tfidf = None

if not filtered_mdata_app.empty:
    filtered_similarity_matrix, filtered_tfidf = create_filtered_similarity_engine(filtered_mdata_app)

def recommend_movies_filtered(movie_title, top_n=10):
    return recommend_movies(movie_title, filtered_similarity_matrix, filtered_mdata_app, top_n)

def recommend_movies_original(movie_title, top_n=10):
    return recommend_movies(movie_title, similarity_matrix, mdata, top_n)

movie_title = st.text_input("Enter a movie title", key="movie_title_input")
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=20, value=10, step=1, key="num_recommendations_slider")

if st.button("Get Recommendations"):
    if movie_title:
        if not filtered_mdata_app.empty:
            recommendations = recommend_movies_filtered(movie_title, top_n=num_recommendations)
        else:
            recommendations = recommend_movies_original(movie_title, top_n=num_recommendations)

        st.write("Recommendations:")
        if recommendations and recommendations[0] == "Movie not found or try with capital letter or incorrect year, if not then is definetly not in my cinema :(.":
            st.write(recommendations[0])
        elif recommendations:
            for i, movie in enumerate(recommendations):
                st.write(movie, key=f"movie_{i}")
        else:
            st.write("No recommendations found.")
    else:
        st.write("Please enter a movie title.")