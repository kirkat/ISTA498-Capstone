# -*- coding: utf-8 -*-  
"""Build a sentiment analysis / polarity model
Sentiment analysis can be casted as a binary text classification problem,
that is fitting a linear classifier on features extracted from the text
of the user messages so as to guess whether the opinion of the author is
positive or negative.
In this examples we will use a movie review dataset.
"""

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

    os.chdir("review_polarity")
    movie_reviews_data_folder = os.getcwd()
    dataset = load_files(movie_reviews_data_folder, shuffle=False)
    print("n_samples: %d" % len(dataset.data))
    # split the dataset in training and test set:
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.2, random_state=None)
  
    # TASK: Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
        ('clf', LinearSVC(C=1000, max_iter = 10000)),
    ])

    # TASK: Build a grid search to find out whether unigrams or bigrams are
    # more useful.
    # Fit the pipeline on the training set using grid search for the parameters
    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
    }

    # Init the model
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
    #Train the model
    grid_search.fit(docs_train, y_train)

    # TASK: print the mean and std for each candidate along with the parameter
    # settings for all the candidates explored by grid search.
    n_candidates = len(grid_search.cv_results_['params'])
    for i in range(n_candidates):
        print(i, 'params - %s; mean - %0.2f; std - %0.2f'
                 % (grid_search.cv_results_['params'][i],
                    grid_search.cv_results_['mean_test_score'][i],
                    grid_search.cv_results_['std_test_score'][i]))

    #test the accuracy of the model
    y_predicted = grid_search.predict(docs_test)
    print(y_predicted)
    # Print the classification report
    print(metrics.classification_report(y_test, y_predicted,
                                        target_names=dataset.target_names))

    # Go to 2 level up in directory
    os.chdir('../')
    
    # Save the tarined model in a pickle file
    with open('sentiment.pickle', 'wb') as f:
        pickle.dump(grid_search, f)
    
if __name__ == '__main__':
    main()

