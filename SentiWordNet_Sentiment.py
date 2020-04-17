import pandas as pd 
import nltk 
from nltk import word_tokenize 
from nltk.corpus import stopwords 
from nltk.corpus import sentiwordnet as swn 
import string

def text_score(text):
    #create单词表
    #nltk.pos_tag是打标签
    stop = stopwords.words("english") + list(string.punctuation)
    ttt = nltk.pos_tag([i for i in word_tokenize(str(text).lower()) if i not in stop])
    word_tag_fq = nltk.FreqDist(ttt)
    wordlist = word_tag_fq.most_common()

    #变为dataframe形式
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
            
        #计算单个评论的单词分数
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
    return sum(textdf.iloc[:,3])

def ratetext(com):
    # com = linkdel(com)
    score_list = []
    for i in range(len(com)):
        score_list.append(text_score(com[i]))
    return score_list

# def linkdel(com):
#     df = pd.DataFrame().
#     for i in com:
#         i = i[:i.find("https")]
#     return com

def readin(path):
    file = pd.read_csv(path)
    return file.iloc[:,6]

def posrate(scores):
    pos = 0;
    for i in scores:
        if i >0:
            pos+=1
    print(pos/len(scores))

def main():
    com =  readin("output_got.csv")
    scores = ratetext(com)
    posrate(scores)

if __name__ == '__main__':
    main()
