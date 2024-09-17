import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=cd64fed5157a255b37ec9f42e850e6bb&language=en-US'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].id
        recommend_movies.append(movies_df.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

movies_df = pickle.load(open('movies.pkl','rb'))
movies = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender')

selected_movie = st.selectbox(
"select a movie",
(movies),
)

st.write("You selected:", selected_movie)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])  # Display the movie title in each column
            st.image(posters[i], use_column_width=True)  # Display the poster in each column