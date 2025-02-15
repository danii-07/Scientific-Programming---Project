import streamlit as st
from movierec import load_data, preprocess_data, create_similarity_engine, recommend_movies
from PIL import Image

mdata = load_data()
mdata = preprocess_data(mdata)
similarity_matrix, tfidf = create_similarity_engine(mdata)

img1 = Image.open('/Users/hectorchaves/Documents/GitHub/Scientific-Programming---Project/images/IMG_0116.PNG')
st.image(img1, use_container_width=True)
st.title("Dani's Cinema")

movie_title = st.text_input("Enter a movie title:")

# adding a slider for the number of recommendations that the user wants
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=20, value=10, step=1)  # Default 10

if st.button("Get Recommendations"):
    if movie_title:
        recommendations = recommend_movies(movie_title, top_n=num_recommendations)  # Pass num_recommendations to the function
        st.write("Recommendations:")
        if recommendations[0] == "Movie not found.":
            st.write(recommendations[0])
        else:
            for movie in recommendations:
                st.write(movie)
    else:
        st.write("Please enter a movie title.")