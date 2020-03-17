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

def main():

    with open('sentiment.pickle', 'rb') as f:
        grid_search = pickle.load(f)
    os.chdir('review') 
    #open the files in review
    path = os.getcwd()
    file_list=os.listdir(path)
    if '.DS_Store' in file_list:
        file_list.remove('.DS_Store')
    if 'new' in file_list:
        file_list.remove('new')
    file_list.sort()
    predict_result = []
    for fn in file_list:
        areview  = open(fn)
        #predict the result of the file
        result = grid_search.predict(areview)
        #print out result of prediction
        predict_result.append(result[0])
        if result[0]==1:
            print(fn+": pos")
        else:
            print(fn+": neg")
    print("Positive Rate = "+str(sum(predict_result)/len(predict_result)))

if __name__ == '__main__':
    main()
