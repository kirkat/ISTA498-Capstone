import pandas as pd 
import nltk 
from nltk import word_tokenize 
from nltk.corpus import stopwords 
from nltk.corpus import sentiwordnet as swn 
import string
import os
import sys

def text_score(text):
    stop = stopwords.words("english") + list(string.punctuation)
    ttt = nltk.pos_tag([i for i in word_tokenize(str(text).lower()) if i not in stop])
    word_tag_fq = nltk.FreqDist(ttt)
    wordlist = word_tag_fq.most_common()

    key = []
    part = []
    frequency = []
    for i in range(len(wordlist)):
        key.append(wordlist[i][0][0])
        part.append(wordlist[i][0][1])
        frequency.append(wordlist[i][1])
    textdf = pd.DataFrame({'key':key,
                      'part':part,
                      'frequency':frequency},
                      columns=['key','part','frequency'])

    #编码
    n = ['NN','NNP','NNPS','NNS','UH']
    v = ['VB','VBD','VBG','VBN','VBP','VBZ']
    a = ['JJ','JJR','JJS']
    r = ['RB','RBR','RBS','RP','WRB']

    for i in range(len(textdf['key'])):
        z = textdf.iloc[i,1]

        if z in n:
            textdf.iloc[i,1]='n'
        elif z in v:
            textdf.iloc[i,1]='v'
        elif z in a:
            textdf.iloc[i,1]='a'
        elif z in r:
            textdf.iloc[i,1]='r'
        else:
            textdf.iloc[i,1]=''
            

    score = []
    for i in range(len(textdf['key'])):
        m = list(swn.senti_synsets(textdf.iloc[i,0],textdf.iloc[i,1]))
        s = 0
        ra = 0
        if len(m) > 0:
            for j in range(len(m)):
                s += (m[j].pos_score()-m[j].neg_score())/(j+1)
                ra += 1/(j+1)
            score.append(s/ra)
        else:
            score.append(0)
    # print(textdf)  
    textdf = pd.concat([textdf,pd.DataFrame({'score':score})],axis=1)
    return sum(textdf.iloc[:,3]) # return text score

def ratetext(com):
    # com = linkdel(com)
    score_list = []
    for i in range(len(com)):
        score_list.append(text_score(com[i]))
    return score_list

def readin(path):
    file = pd.read_csv(path)
    return file.iloc[:,6]

def posrate(scores):
    pos = 0;
    for i in scores:
        if i >0.2:
            pos+=1
    return (pos/len(scores))

def main(argv):
    posratebyweek = []
    for i in range(6):
        fold = "#"+argv[0]
        file = "week"+str(i)+".csv"
        path = os.path.join(fold,file)
        com =  readin(path)
        scores = ratetext(com)
        posratebyweek.append(posrate(scores))
    file = open("marvels_rate_sentiwordnet.csv","a+")
    file.write(argv[0])
    for i in posratebyweek:
        file.write(","+str(i))
    file.write("\n")
    file.close()

if __name__ == '__main__':
    main(sys.argv[1:])
