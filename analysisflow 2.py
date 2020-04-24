import os,sys

import pandas as pd

def readfilmlist(path):
    df = pd.read_csv(path)
    return df.iloc[:,0],df.iloc[:,1]

def getSentiWordNetposrate(filmlist):
    for i in range(len(filmlist)):
        command = "python3 SentiWordNet_Sentiment.py "+filmlist[i]
        print(command)
        os.system(command)

def getSVMposrate(filmlist):
    for i in range(len(filmlist)):
        command = "python3 SVMnew.py "+filmlist[i]
        print(command)
        os.system(command)

def main():
    filmlist,datelist = readfilmlist("process_list.csv")
    getSentiWordNetposrate(filmlist)
    # getSVMposrate(filmlist)

if __name__ == '__main__':
    main()

