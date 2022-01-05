import os
from random import shuffle
from numpy import average
import pandas as pd
import numpy as np
from numpy.random import shuffle

#NOV number of votes AV average vote
def weighted_rating(item, NOV, AV):
    IC = item['vote_count']
    IAV = item['vote_average']
   
    return (IC/(IC+NOV) * IAV) + (NOV/(NOV+IAV) * AV)

def random_movie_recommendation():

    #path specification
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    __dataset_location__=os.path.join(__location__,"dataset")

    #print(__dataset_location__)

    movie_metadata = pd.read_csv(os.path.join(__dataset_location__,"movies_metadata.csv"), low_memory=False) #reads movies

    average_vote = movie_metadata['vote_average'].mean() #calculates mean/average vote of movie_metadata list

    number_of_votes = movie_metadata['vote_count'].quantile(0.90) #calculates number of votes in given dataset

    best_movies = movie_metadata.copy().loc[movie_metadata['vote_count'] >= number_of_votes] #gets movies where vote count bigger than limit

    best_movies['score'] = weighted_rating(best_movies,number_of_votes,average_vote) #applies imdb calculation

    sub_movies = best_movies.sort_values('score', ascending=False) #sorts movie scores 

    top_movies=sub_movies[['title', 'vote_count', 'vote_average', 'score']].head(20) #get top 20 of 

    top_movies=top_movies['title']

    movies_list=np.array(top_movies) #convert pandas frame to numpy list

    import random
    rnd_indx=random.randint(0,19) #get random movie from list


    return(movies_list[rnd_indx])



print(random_movie_recommendation())




