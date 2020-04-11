"""
ISTA 498
This program creates two BeautifulSoup objects from the imdb Parasite user review "https://www.imdb.com/title/tt6751668/reviews?ref_=tt_urv"
and imdb Avengers Endgame user review "https://www.imdb.com/title/tt4154796/reviews?ref_=tt_ov_rt".
User reviews are parsed from the BeautifulSoup objects and used to create a DataFrame with pandas. The first 26 reviews are captured.
Then the DataFrame is output to a 'parasite_imdb_review.csv' and imdb_avengers_review.csv' with 'User', 'Rating', 'Date', 'Title', 'Helpful', 'Comment' as the columns. 
"""
import requests
import os.path
from bs4 import BeautifulSoup
import pandas as pd, numpy as np

#This function creates a soup object with an imdb user review url.
def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')

#This function creates a pandas dataframe and outputs the dataframe to a csv.
def save_soup(fname, reviewees_info):
    df = pd.DataFrame(reviewees_info)
    df.columns = ['User', 'Rating', 'Date', 'Title', 'Helpful', 'Comment']
    df.to_csv(fname, index=False)

#This function creates a BeautifulSoup object and parses through each User review from an imdb user review.
def scrape_and_save(filename, url):
    soup = get_soup(url)
    reviews = soup.find_all('div', attrs={'class': 'lister-item-content'})
    reviewees_info = []
    
    for review in reviews:
        temp = []
        
        #User Name
        name = review.find('span', {'class' : 'display-name-link'}).string
        temp.append(name)
        
        #Rating
        rating = review.find('span').text
        temp.append(rating.strip('\n'))
        
        #Date
        date = review.find('span', {'class' : 'review-date'}).string
        temp.append(date)
        
        #Title
        temp.append(review.find('a').contents[0])
        
        #Helpful
        helpful = review.find('div', {'class' : 'actions text-muted'}).contents[0].strip('\n ')
        temp.append(helpful)
        
        #Comment
        comment = review.find('div', {'class' : 'text'}).text
        temp.append(comment)
        
        reviewees_info.append(temp)
        
    save_soup(filename, reviewees_info)

def main():
    parasite_url = "https://www.imdb.com/title/tt6751668/reviews?ref_=tt_urv"
    avengers_url = "https://www.imdb.com/title/tt4154796/reviews?ref_=tt_ov_rt"
    
    #scrape_and_save('imdb_parasite_review.csv', parasite_url)
    scrape_and_save('imdb_avengers_review.csv', avengers_url)

if __name__ == "__main__":
    main()