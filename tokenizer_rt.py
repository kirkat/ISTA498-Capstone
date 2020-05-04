import csv
import os
import random
import matplotlib.pyplot as plt
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics

from collections import Counter

def tokenizeCSV(path=""):
    os.chdir(path)
    path = os.getcwd()
    for filename in os.listdir(path):
        reviews = []
        if ".csv" in filename:
            if not any(char.isdigit() for char in filename):
                print(filename)
                with open(filename, newline='', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        text = row[2]
                        rating = row[3]
                        reviews.append((text, rating))

                data = [i[0] for i in reviews if i[0] != "Review"]
                labels = [i[1] for i in reviews if i[1] != "Rating"]
                
                X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
                label_counts = dict(Counter(labels))
                vectorizer = CountVectorizer(ngram_range=(1, 2),
                                             token_pattern=r'\b\w+\b', min_df=1)
##                X_train_count = vectorizer.fit_transform(X_train)
                tfidf_transformer = TfidfTransformer()
##                X_train_tfidf = tfidf_transformer.fit_transform(X_train_count)
##                print(X_train_tfidf.shape)
##
##                clf = MultinomialNB().fit(X_train_tfidf, y_train)
                clf = LinearSVC()
##                text_clf = Pipeline([('vect', CountVectorizer()),
##                                     ('tfidf', TfidfTransformer()),
##                                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
##                                                           alpha=1e-3, random_state=42,
##                                                           max_iter=5, tol=None)),])

                text_clf = Pipeline([('vect', vectorizer),
                                     ('tfidf', tfidf_transformer),
                                     ('clf', clf),])
                text_clf.fit(X_train, y_train)
                #text_clf.steps[2].feature_count_
                predicted = text_clf.predict(X_test)
                print("Accuracy: {:.2f}".format(metrics.accuracy_score(y_test, predicted) * 100))
                print(metrics.classification_report(y_test, predicted))
                show_most_informative_features(vectorizer, clf)

                keys = label_counts.keys()
                values = label_counts.values()

                plt.bar(keys, values)
                plt.savefig(filename[:-4] + ".png")
                plt.show()

def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print ("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))

##                neg_class_prob_sorted = SGDClassifier.feature_log_prob_[0, :].argsort()
##                pos_class_prob_sorted = SGDClassifier.feature_log_prob_[1, :].argsort()
##
##                print(np.take(vect.get_feature_names(), neg_class_prob_sorted[:10]))
##                print(np.take(vect.get_feature_names(), pos_class_prob_sorted[:10]))
    
                
##                    random.shuffle(reviews)
##                    size = int(len(reviews) * 0.8)
##                    training = reviews[:size]
##                    test = reviews[size:]
##                    
##                    train_data = [i[0] for i in training]
##                    y_train = [i[1] for i in training]
##                    test_data = [i[0] for i in test]
##                    y_test = [i[1] for i in test]
                    
                
                #final_counts = vectorizer.fit_transform(sorted_data['Text'].values)
##                    features = vectorizer.get_feature_names()
##                    features = [w for w in features if not any(c.isdigit() for c in w)]
##
##                    #docs_train, docs_test, y_train, y_test = train_test_split(movie.data, movie.target, 
##                                                          #test_size = 0.20, random_state = 12)
    
def main():
    tokenizeCSV("rotten tomatos")

if __name__ == '__main__':
    main()
