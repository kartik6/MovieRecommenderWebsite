import streamlit as st
import json
from Classifier import KNearestNeighbours
from operator import itemgetter
#added
from PIL import Image
from bs4 import BeautifulSoup
import PIL.Image
import requests, io
from urllib.request import urlopen
from scraper_api import ScraperAPIClient
#end of added

# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
movie_posters = []
rec_movies = []
#added
client = ScraperAPIClient('a381cfe9890b9976dc24ce04a8cf0755')
def movie_poster_fetcher(imdb_link):
    ## Display Movie Poster
    url_data = client.get(imdb_link)
    s_data = BeautifulSoup(url_data.text, "html.parser")
    imdb_dp = s_data.find("meta", property="og:image")
    if imdb_dp is not None:
        movie_poster_link = imdb_dp.attrs['content']
        u = urlopen(movie_poster_link)
        if u is not None:
            raw_data = u.read()
            image = PIL.Image.open(io.BytesIO(raw_data))
            image = image.resize((158, 301), )
            #st.image(image, use_column_width=False)
            movie_posters.append(image)
#end of added

def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    st.header('Movie Recommender')
    apps = ['--Select--', 'Movie based', 'Genre based']
    app_options = st.selectbox('Select application:', apps)
    if app_options == 'Movie based':
        movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Select a movie')
        else:
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            cols = st.columns(n)
            i = 0
            for movie, link in table:
                # Displays movie title with link to imdb
                with cols[i]:
                    st.write(f"[{movie}]({link})")
                    movie_poster_fetcher(link)
                    if i< len(movie_posters):
                        st.image(movie_posters[i])
                    i=i+1
            
    elif app_options == apps[2]:
        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            cols = st.columns(n)
            i = 0
            for movie, link in table:
                # Displays movie title with link to imdb
                with cols[i]:
                    st.write(f"[{movie}]({link})")
                    movie_poster_fetcher(link)
                    if i< len(movie_posters):
                        st.image(movie_posters[i])
                    i=i+1

        else:
            st.write("This is a simple Movie Recommender application. "
                     "You can select the genres and change the IMDb score.")
    else:
        st.write('Select option')
