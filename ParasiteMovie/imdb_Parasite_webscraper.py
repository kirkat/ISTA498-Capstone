"""
ISTA 498
This program creates a BeautifulSoup object from "https://www.imdb.com/title/tt6751668/reviews?ref_=tt_urv".
User reviews are parsed from the BeautifulSoup object and used to create a DataFrame with pandas. Then the DataFrame is output to a 'parasite.csv'
with 'User', 'Rating', 'Date', 'Title', 'Helpful', 'Comment' as the columns.
"""
import requests
import os.path
from bs4 import BeautifulSoup
import pandas as pd, numpy as np

#This function creates a soup object with the parasite imdb url.
def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')

#This function creates a pandas dataframe and outputs the dataframe to a csv.
def save_soup(fname, reviewees_info):
    df = pd.DataFrame(reviewees_info)
    df.columns = ['User', 'Rating', 'Date', 'Title', 'Helpful', 'Comment']
    df.to_csv(fname, index=False)

#This function creates a BeautifulSoup object and parses through each User review from imdb.
def scrape_and_save():    
    url = "https://www.imdb.com/title/tt6751668/reviews?ref_=tt_urv"
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
        
    save_soup('parasite.csv', reviewees_info)

def main():
    scrape_and_save()

if __name__ == "__main__":
    main()