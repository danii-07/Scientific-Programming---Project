import streamlit as st
from movierec import load_data, preprocess_data, create_similarity_engine, recommend_movies
from PIL import Image

mdata = load_data()
mdata = preprocess_data(mdata)
similarity_matrix, tfidf = create_similarity_engine(mdata)

st.set_page_config(
    page_title= "Dani's Cinema"
)

def run():
    img1= Image.open('/Users/hectorchaves/Documents/GitHub/Scientific-Programming---Project/IMG_0116.PNG')
    st.image(img1, use_row_width= True)
    st.title("Dani's Cinema")

movie_title = st.text_input("Enter a movie title:")

if st.button("Get Recommendations"):
    if movie_title:
        recommendations = recommend_movies(movie_title)
        st.write("Recommendations:")
        if recommendations[0] == "Movie not found.":
            st.write(recommendations[0]) #print the error
        else:
            for movie in recommendations:
                st.write(movie)
    else:
        st.write("Please enter a movie title.")