import pickle
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
import time

#load api()
load_dotenv()
API_KEY=os.getenv('api_key')

#Load data

movies= pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.RequestException as e:
        # Log warning only once for debugging; you can also remove st.warning to avoid UI clutter
        print(f"Could not load poster for movie ID {movie_id} : {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"




def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movie_path=[]

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)  #movie title
        recommended_movie_path.append(fetch_posters(movie_id))  #movie poster  
        time.sleep(0.2)
    return recommended_movies,recommended_movie_path



st.header("Movie Recommendation System")

selected_movie=st.selectbox(
    'Choose a movie to get similar recommendation',
    movies['title'].values
)

#button trigers recomendation

if st.button('Recommend'):
    with st.spinner("Fetching recommendation.."):
        names,posters =recommend(selected_movie)

        cols= st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])