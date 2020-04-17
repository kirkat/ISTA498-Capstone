import pandas as pd
import numpy as np
import os
def readin():
    dataframe = pd.read_csv("output_got.csv")
    text_line = dataframe.loc[:,"text"]
    return text_line
def main():
    files = readin()
    os.chdir("review")
    for i in range(len(files)):
        new_file = open("comment"+str(i).zfill(3)+".txt","w")
        new_file.write(files[i])
        new_file.close()
if __name__ == '__main__':
    main()
