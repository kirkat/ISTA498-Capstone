import os 
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import datasets
import pickle
import pandas as pd

def loadmodel():
    with open('sentiment.pickle', 'rb') as f:
        grid_search = pickle.load(f)
    return grid_search

def loaddata(fold,week):
    week = "week"+str(week)+".csv"
    fold = "#"+fold
    path = os.path.join(fold,week)
    file = pd.read_csv(path)
    return file.iloc[:,6]

def predict(data,model):
    predict = []
    for i in range(len(data)):
        file = open("test.txt","w")
        file.write(data[i].strip())
        file.close()
        file = open("test.txt")
        result = model.predict(file)
        predict.append(result[0])
        file.close()
    return (sum(predict)/len(predict))
    
def main(argv):
    model = loadmodel()
    file = open("marvels_rate_SVM.csv","a+")
    file.write(argv[0])
    for i in range(6):
        data = loaddata(argv[0],i)
        score = predict(data,model)
        file.write(","+str(score))
    file.write("\n")
    file.close()

if __name__ == '__main__':
    main(sys.argv[1:])
