import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# first we load the data
@st.cache_data
def load_data():
    mdata = pd.read_csv("/Users/hectorchaves/Documents/GitHub/Scientific-Programming---Project/IMDB-Movie-Data.csv")
    return mdata

mdata = load_data()

# here we tell streamlit to cache the result of the preprocess_data function
@st.cache_resource
def preprocess_data(mdata):
    # here we combine some features
    mdata['combined_features'] = mdata['Title'] + ' ' + mdata['Genre'] + ' ' + mdata['Description'] + ' ' + mdata['Actors'] + ' ' + mdata['Director']
    return mdata

mdata = preprocess_data(mdata)

# this basically tells streamlit to store the result of creating a TF-IDF matrix,
# and calculating the similarity matrix.
@st.cache_resource
def create_similarity_engine(mdata): # here we take our new mdata as input and 
    tfidf = TfidfVectorizer(stop_words='english')  # here i convert text data into numerical vectors using the TF-IDF method, and also ignore some stop words in english.
    tfidf_matrix = tfidf.fit_transform(mdata['combined_features']) # here the TfidfVectorizer gets the unique words present in the movie descriptions and transforms the combined_features column into a TF-IDF matrix.
    similarity_matrix = cosine_similarity(tfidf_matrix) # here we calculate the c_s between movies.
    return similarity_matrix, tfidf

similarity_matrix, tfidf = create_similarity_engine(mdata) # this line just passes the movie data to the variables.

# separate genres before any filtering
def separate_genres(df):
    new_data = []
    for index, row in df.iterrows():
        movie = row['Title']
        genres_str = row['Genre']
        combined_features = row['combined_features'] # getting the combined_features from the current row
        if isinstance(genres_str, str):
            for genre in genres_str.split(', '):
                new_data.append({
                    'Title': movie,
                    'Genre': genre,
                    'Description': row['Description'],
                    'Actors': row['Actors'],
                    'Director': row['Director'],
                    'Year': row['Year'],
                    'combined_features': combined_features  # including the combined_features in the new row
                })
    return pd.DataFrame(new_data)

# new function for this two new filters
def filter_movies(mdata, selected_genre, selected_years):
    filtered_data = mdata.copy()

    if selected_genre != "All":
        filtered_data = filtered_data[filtered_data['Genre'] == selected_genre] # Exact match now

    if selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]

    return filtered_data

# another function for filtering the new genre and year categories
@st.cache_resource
def create_filtered_similarity_engine(filtered_mdata):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_mdata['combined_features'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix, tfidf

# core of the recommendation system
def recommend_movies_filtered(movie_title, filtered_similarity_matrix, filtered_mdata, top_n=10):
    return recommend_movies(movie_title, filtered_similarity_matrix, filtered_mdata, top_n)

def recommend_movies_original(movie_title, similarity_matrix, mdata, top_n=10): 
    return recommend_movies(movie_title, similarity_matrix, mdata, top_n)

def recommend_movies(movie_title, similarity_matrix, mdata, top_n=10):  # Correct definition
    try: # i use try and except for error handling, just in case ;)
        movie_index = mdata[mdata['Title'] == movie_title].index[0] # here i find the index of the movie in the df that matches the input title, through a boolean series, where True means that the movie titles match.
        similar_movies = list(enumerate(similarity_matrix[movie_index])) # here i get back the similarity scores for the movie at movie_index, then finally create a list with them.
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True) # now it sorts the similar_movies list in descending (True) order with the similarity score.
        
        # the key lambda allows you to define a function in a single line of code,
        # easy example above i tell the sorted function to use the 2nd element of each item in a collection as the basis for sorting or comparison ;)

        similar_movies = similar_movies[1:top_n + 1]  # here we get the top most similar movies, excluding the input itself.
        recommended_movies = [mdata.iloc[i[0]]['Title'] for i in similar_movies] # here a list is created of the titles of the recommended movies.
        
        # with the iloc use the index to get the title of the movie from the mdata DataFrame, like we used in class.

        return recommended_movies
    except IndexError:
        return ["Movie not found or try with capital letter, if not then is definetly not in my cinema :(."]
