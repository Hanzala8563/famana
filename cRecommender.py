import os
import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_director(item):
    for obj in item:
        if obj['job'] == 'Director':
            return obj['name']
    return np.nan

def get_list(item):
    if isinstance(item, list):
        names = [i['name'] for i in item]

        if len(names) > 3:
            names = names[:3]
        return names
    return []

def clean_data(item):
    if isinstance(item, list):
        return [str.lower(i.replace(" ", "")) for i in item]
    else:
        if isinstance(item, str):
            return str.lower(item.replace(" ", ""))
        else:
            return ''

def create_soup(item):
    return ' '.join(item['keywords']) + ' ' + ' '.join(item['cast']) + ' ' + item['director'] + ' ' + ' '.join(item['genres'])

def referenced_recommendation(title):
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __dataset_location__=os.path.join(__location__,"dataset")

    movie_metadata = pd.read_csv(os.path.join(__dataset_location__,"movies_metadata.csv"), low_memory=False)

    credits = pd.read_csv(os.path.join(__dataset_location__,'credits.csv'))
    keywords = pd.read_csv(os.path.join(__dataset_location__,'keywords.csv'))

    movie_metadata = movie_metadata.drop([19730, 29503, 35587])

    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')
    movie_metadata['id'] = movie_metadata['id'].astype('int')

    movie_metadata = movie_metadata.merge(credits, on='id')
    movie_metadata = movie_metadata.merge(keywords, on='id')

    meta_features = ['cast', 'crew', 'keywords', 'genres']

    for feature in meta_features:
        movie_metadata[feature] = movie_metadata[feature].apply(literal_eval)


    movie_metadata['director'] = movie_metadata['crew'].apply(get_director)

    meta_features = ['cast', 'keywords', 'genres']

    for feature in meta_features:
        movie_metadata[feature] = movie_metadata[feature].apply(get_list)

    meta_features = ['cast', 'keywords', 'director', 'genres']

    for feature in meta_features:
        movie_metadata[feature] = movie_metadata[feature].apply(clean_data)

        
    movie_metadata['soup'] = movie_metadata.apply(create_soup,axis=1)

    number_of_count = CountVectorizer(stop_words='english')
    matrix_of_count = number_of_count.fit_transform(movie_metadata['soup'])

    cosine_sim = cosine_similarity(matrix_of_count, matrix_of_count)

    movie_metadata = movie_metadata.reset_index()

    indices = pd.Series(movie_metadata.index, index=movie_metadata['title'])

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    movie=movie_metadata['title'].iloc[movie_indices]
    movie=movie.head(3)
    movie_list=np.array(movie)

    return movie_list