import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# first we load the data
# the @ represents a decorator in the streamlit library, decorators modify the behavior of a function.

@st.cache_data 

# if a function is called again with the same inputs,
# the cached (stored) result is returned instead of recomputing the function.

def load_data():
    mdata = pd.read_csv("/Users/hectorchaves/Documents/GitHub/Scientific-Programming---Project/IMDB-Movie-Data.csv")
    return mdata

mdata = load_data()

# here we tell streamlit to cache the result of the preprocess_data function,
# so that the function is only executed once when the Streamlit app starts, making it faster.

@st.cache_resource
def preprocess_data(mdata):

    # here we combine some features, so that the similarity calculations are more accurate,
    # thanks to creating a better representation of each movie's content by uniting all the important characteristics.

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

# core of the recommendation system :)

def recommend_movies(movie_title, top_n=10): # here we take the title of the movie for the recommendation and the number of how many i want.
    try: # i use try and except for error handling, just in case ;)
        movie_index = mdata[mdata['Title'] == movie_title].index[0] # here i find the index of the movie in the df that matches the input title, through a boolean series, where True means that the movie titles match.
        similar_movies = list(enumerate(similarity_matrix[movie_index])) # here i get back the similarity scores for the movie at movie_index, then finally create a list with them.
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True) # now it sorts the similar_movies list in descending (True) order with the similarity score.
        
        # the key lambda allows you to define a function in a single line of code,
        # easy example above i tell the sorted function to use the 2nd element of each item in a collection as the basis for sorting or comparison ;)

        similar_movies = similar_movies[1:top_n+1]  # here we get the top most similar movies, excluding the input itself.
        recommended_movies = [mdata.iloc[i[0]]['Title'] for i in similar_movies] # here a list is created of the titles of the recommended movies.
        
        # with the i use the index to get the title of the movie from the mdata DataFrame, used in class.

        return recommended_movies
    except IndexError:
        return ["Movie not found or try with capital letter, if not then is definetly not in my cinema :(."]
