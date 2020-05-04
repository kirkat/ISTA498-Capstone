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
def save_soup(fname, data):
    df = pd.DataFrame(data)
    df.columns = ['User', 'Date', 'Review', 'Rating']
    df.to_csv(fname, index=False)

#This function creates a BeautifulSoup object and parses through each User review from an imdb user review.
def scrape_and_save(filename, url):
    soup = get_soup(url)
    reviews = soup.find_all('div', attrs={'class': 'row review_table_row'})
    months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
              "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    data = []
    for r in reviews:
        name = r.find('a', {'class' : 'unstyled bold articleLink'}).string
        date = r.find('div', {'class' : 'review-date subtle small'}).string.strip()
        date = date.replace(',', '')
        date = date.split()
        date = str(months[date[0]]) + "/" + date[1] + "/" + date[2]
        review = r.find('div', {'class' : 'the_review'}).string.strip()
        pos = r.find('div', {'class' : 'review_icon icon small fresh'})
        if pos == None:
            data.append([name, date, review, "NEG"])
        else:
            data.append([name, date, review, "POS"])
    save_soup(filename, data)
    
#This function takes CSV files with the same headers and combines them to one csv.
def combine(files, new_fname):
    storage = []
    
    for file in files:
        df = pd.read_csv(file, index_col=None, header=0)
        storage.append(df)
        
    frame = pd.concat(storage, axis=0, ignore_index=True)
    frame.to_csv(new_fname, index=False)

def main():
    
    parasite_url_1 = "https://www.rottentomatoes.com/m/parasite_2019/reviews?type=top_critics&sort="
    parasite_url_2 = "https://www.rottentomatoes.com/m/parasite_2019/reviews?type=top_critics&sort=&page=2"
    parasite_url_3 = "https://www.rottentomatoes.com/m/parasite_2019/reviews?type=top_critics&sort=&page=3"
    parasite_url_4 = "https://www.rottentomatoes.com/m/parasite_2019/reviews?sort=rotten"
    
    avengers_url_1 = "https://www.rottentomatoes.com/m/avengers_endgame/reviews?type=top_critics"
    avengers_url_2 = "https://www.rottentomatoes.com/m/avengers_endgame/reviews?type=top_critics&sort=&page=2"
    avengers_url_3 = "https://www.rottentomatoes.com/m/avengers_endgame/reviews?type=top_critics&sort=&page=3"
    
    scrape_and_save('rt_parasite_review_pt1.csv', parasite_url_1)
    scrape_and_save('rt_parasite_review_pt2.csv', parasite_url_2)
    scrape_and_save('rt_parasite_review_pt3.csv', parasite_url_3)
    scrape_and_save('rt_parasite_review_pt4.csv', parasite_url_4)
    
    scrape_and_save('rt_avengers_review_pt1.csv', avengers_url_1)
    scrape_and_save('rt_avengers_review_pt2.csv', avengers_url_2)
    scrape_and_save('rt_avengers_review_pt3.csv', avengers_url_3)
    
    combine(['rt_parasite_review_pt1.csv', 'rt_parasite_review_pt2.csv', 'rt_parasite_review_pt3.csv', 'rt_parasite_review_pt4.csv'], 'rt_parasite_review.csv')
    combine(['rt_avengers_review_pt1.csv', 'rt_avengers_review_pt2.csv', 'rt_avengers_review_pt3.csv'], 'rt_avengers_review.csv')

if __name__ == "__main__":
    main()
