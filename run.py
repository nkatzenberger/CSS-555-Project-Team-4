# Run this in order to generate the brain images using data

from BaseExample import data_preprocessing, main

if __name__ == "__main__":
    exec(open("data_preprocessing.py").read())
    exec(open("main.py").read())