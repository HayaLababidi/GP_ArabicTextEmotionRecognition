import pandas as pd
from sklearn.model_selection import train_test_split
import embedding
def read_dataset():
    data_df = pd.read_csv("Emotional-Tone-Dataset - Copy.csv", encoding="windows-1256")
    X = data_df[['tweet']].values
    Y = data_df[['label']].values

    X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.33, random_state=42)
    eX_train = list()
    eX_test = list()

    for tweet in X_train:
        eX_train.append(embedding.embed_doc(tweet))

    for tweet in X_test:
        eX_test.append(embedding.embed_doc(tweet))
    return eX_train, eX_test, y_train, y_test

read_dataset()