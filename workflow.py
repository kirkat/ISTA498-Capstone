import os
import pandas as pd

def readfilmlist(path):
    df = pd.read_csv(path)
    return df.iloc[:,0],df.iloc[:,1]

def pulldata(filmlist,datelist):
    for i in range(len(filmlist)):
        command = "python3 pullTweets.py --querysearch \"#"+filmlist[i]+"\" --since "+datelist[i]+ " --maxtweets 1000"
        print(command)
        os.system(command)


def main():
    filmlist,datelist = readfilmlist("marvel_films_list.csv")
    pulldata(filmlist,datelist)

if __name__ == '__main__':
    main()
