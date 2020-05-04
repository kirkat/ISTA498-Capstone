"""
ISTA 498
This program creates BeautifulSoup objects from the imdb Parasite user reviews and imdb Avengers Endgame user reviews.
User reviews are parsed from the BeautifulSoup objects and used to create a DataFrame with pandas.
Then the DataFrame is output to a 'parasite_imdb_review.csv' and imdb_avengers_review.csv' with 'User', 'Rating', 'Date', 'Title', 'Comment' as the columns. 
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
    df.columns = ['User', 'Rating', 'Date', 'Title', 'Comment']
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
        rating = review.find('span').text.strip()
        rating = rating.split('/')
        if rating[0].isnumeric():
            if int(rating[0]) >= 6:
                rating = "POS"
            else:
                rating = "NEG"
        else:
            rating = "NEG"
        temp.append(rating)
        
        #Date
        date = review.find('span', {'class' : 'review-date'}).string
        temp.append(date)
        
        #Title
        temp.append(review.find('a').contents[0])
       
        #Comment
        comment = review.find('div', {'class' : 'text'}).text
        temp.append(comment)
        
        reviewees_info.append(temp)
        
    save_soup(filename, reviewees_info)
    
#This function takes CSV files with the same headers and combines them to one csv.
def combine(files, new_fname):
    storage = []
    
    for file in files:
        df = pd.read_csv(file, index_col=None, header=0)
        storage.append(df)
        
    frame = pd.concat(storage, axis=0, ignore_index=True)
    frame.to_csv(new_fname, index=False)

def main():
    
    parasite_url_1 = "https://www.imdb.com/title/tt6751668/reviews/_ajax"
    parasite_url_2 = "https://www.imdb.com/title/tt6751668/reviews/_ajax?ref_=undefined&paginationKey=g4wp7cjnqa5tczyg7cxxxnrzrpsmmabhzfmxvlnomwklyczuf43o6ss6oi4vznjkd54k5v77ikp2u3tl54o5uy7zt23nzly"
    parasite_url_3 = "https://www.imdb.com/title/tt6751668/reviews/_ajax?ref_=undefined&paginationKey=g4wp7cbeq43toyyf7otxvmjwrps4sbzhzfmxvlnomwklyczuf43o6ss6oqyfzmjjdn4k43xbrogmhwqosedhcghqbjirx6a"
    
    avengers_url_1 = "https://www.imdb.com/title/tt4154796/reviews/_ajax"
    avengers_url_2 = "https://www.imdb.com/title/tt4154796/reviews/_ajax?ref_=undefined&paginationKey=g4wp7cjoryzdozyl7owxxmrzqpqm6bzhzfmxvlnomwklyczuf43o6ss7pazvlnzddv4k44uirvb5gs53wdzzuk26oybhwmq"
    avengers_url_3 = "https://www.imdb.com/title/tt4154796/reviews/_ajax?ref_=undefined&paginationKey=g4wp7cjoqe3tayab66uhfmjzrhq42hjjtzpwzouokkd2gbzgpnt6ucksoy3vzmzob4d6h7spo5fmarq4grjfbx4jxt4v2"
    
    scrape_and_save('imdb_parasite_review_pt1.csv', parasite_url_1)
    scrape_and_save('imdb_parasite_review_pt2.csv', parasite_url_2)
    scrape_and_save('imdb_parasite_review_pt3.csv', parasite_url_3)
    
    scrape_and_save('imdb_avengers_review_pt1.csv', avengers_url_1)
    scrape_and_save('imdb_avengers_review_pt2.csv', avengers_url_2)
    scrape_and_save('imdb_avengers_review_pt3.csv', parasite_url_3)
    
    combine(['imdb_parasite_review_pt1.csv', 'imdb_parasite_review_pt2.csv', 'imdb_parasite_review_pt3.csv'], 'imdb_parasite_review.csv')
    combine(['imdb_avengers_review_pt1.csv', 'imdb_avengers_review_pt2.csv', 'imdb_avengers_review_pt3.csv'], 'imdb_avengers_review.csv')

if __name__ == "__main__":
    main()
