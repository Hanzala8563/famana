import os
import pandas as pd
import numpy as np

#MNOV:minimum number of the votes
#MV:mean vote from the report
#item:movie
#IVC:number of votes for the movie
#IAV:average vote of the movie
def weighted_rating(item, MNOV, MV):
    IVC = item['vote_count']
    IAV = item['vote_average']
   
    return (IVC/(IVC+MNOV) * IAV) + (MNOV/(MNOV+IAV) * MV)

def random_movie_recommendation():

    #path specification
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __dataset_location__=os.path.join(__location__,"dataset")
    #print(__dataset_location__)

    movie_metadata = pd.read_csv(os.path.join(__dataset_location__,"movies_metadata.csv"), low_memory=False) #reads movies

    average_vote = movie_metadata['vote_average'].mean() #calculates mean/average vote of movie_metadata list
    number_of_votes = movie_metadata['vote_count'].quantile(0.80) 

    best_movies = movie_metadata.copy().loc[movie_metadata['vote_count'] >= number_of_votes] #gets movies where vote count bigger than limit
    best_movies['score'] = weighted_rating(best_movies,number_of_votes,average_vote) #applies imdb calculation

    sub_movies = best_movies.sort_values('score', ascending=False) #sorts movie scores 
    top_movies=sub_movies[['title', 'vote_count', 'vote_average', 'score']].head(30) #get top 30 of 
    top_movies=top_movies['title']
    movies_list=np.array(top_movies) #convert pandas frame to numpy list

    import random
    rnd_indx=random.randint(0,29) #get random movie from list
    return(movies_list[rnd_indx])








