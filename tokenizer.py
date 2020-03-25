from sklearn.feature_extraction.text import CountVectorizer
import csv
import os

def tokenizeCSV(path=""):
    os.chdir(path)
    path = os.getcwd()
    tweets = []
    for filename in os.listdir(path):
        with open(filename, newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                date = row[0]
                user = row[1]
                text = row[6]
                tweets.append(text)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(tweets)
    features = vectorizer.get_feature_names()
    features = [w for w in features if not any(c.isdigit() for c in w)]
    print(features)
    
def main():
    tokenizeCSV("ParasiteMovie")

if __name__ == '__main__':
    main()
