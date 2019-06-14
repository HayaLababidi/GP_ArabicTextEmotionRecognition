from model import model
from Data_operations import Data_operations
import csv
import numpy as np
from matplotlib import pyplot as plt
import itertools


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    # print(cm)
    plt.figure(figsize=(15, 15))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title,fontsize=20)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, fontsize=20, rotation=45)
    plt.yticks(tick_marks, classes, fontsize=20)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 fontsize=20,
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label',fontsize=20)
    plt.xlabel('Predicted label',fontsize=20)
    plt.savefig('cm')


class system:
    dir_ = "./models/"

    def __init__(self):
        self.m = model()
        self.data = Data_operations()

    def predict_doc(self, text, modelname='trial', mode=0):  # add default model name
        embedded_vector = self.data.embedd_doc(text, mode)
        classes = np.load(self.dir_ + "classes.npy")
        if mode == 0:
            arr = np.zeros(shape=(1, embedded_vector.shape[0], embedded_vector.shape[1]))
            arr[0] = np.array(embedded_vector)
            softmax_prediction = self.m.predict(arr, modelname)
        return np.argmax(softmax_prediction)

    def add_sample(self, text, lable, filename="new_EmotionalTone_dataset.csv"):  # make sure to add an empty one
        row = [text, lable]
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

    def embedd_dataset(self, modelname='trial', mode=0):
        X_train, X_test, y_train, y_test, classes_ = self.data.read_dataset(mode)
        np.save(self.dir_+'X_train_mode_' + str(mode) + '.npy', X_train)
        np.save(self.dir_+'X_test_mode_' + str(mode) + '.npy', X_test)
        np.save(self.dir_+'y_train_mode_' + str(mode) + '.npy', y_train)
        np.save(self.dir_+'y_test_mode_' + str(mode) + '.npy', y_test)
        np.save(self.dir_+"classes.npy", classes_)
        return X_train, X_test, y_train, y_test, classes_

    def train_model(self, modelname='trial', mode=0):
        try:
            print(self.dir_+'X_train_mode_' + str(mode) + '.npy')
            X_train = np.load(self.dir_+'X_train_mode_' + str(mode) + '.npy')
            X_test = np.load(self.dir_+'X_test_mode_' + str(mode) + '.npy')
            y_train = np.load(self.dir_+'y_train_mode_' + str(mode) + '.npy')
            y_test = np.load(self.dir_+'y_test_mode_' + str(mode) + '.npy')
            classes_ = np.load(self.dir_+"classes.npy")
        except:
            X_train, X_test, y_train, y_test, classes_ = self.embedd_dataset(modelname, mode)
        if self.m.model is None:
            self.m.train(X_train, y_train, modelname)
        else:
            self.m.retrain(X_train, y_train, modelname)

    def test_model(self, modelname='trial', mode=0):
        try:
            X_test = np.load(self.dir_+'X_test_mode_' + str(mode) + '.npy')
            y_test = np.load(self.dir_+'y_test_mode_' + str(mode) + '.npy')
            classes_ = np.load(self.dir_+"classes.npy")
        except:
            X_train, X_test, y_train, y_test, classes_ = self.embedd_dataset(modelname, mode)
        cm, acc, report = self.m.test(X_test, y_test, modelname)
        print("Test Accurcy: " + str(acc))
        print(report)
        plot_confusion_matrix(cm, classes_, True)

#s = system()

def console_Demo():
    s = system()
    s.predict_doc('', modelname='3_100')
    doc = input("اكتب جملة: لمعرفة حالتها\n")
    while True:
        if doc == 'break':
            print("الى اللقاء")
            break
        else:
            textlabel =s.predict_doc(doc, modelname='3_100')
            print ("الحالة:", str(textlabel))
            doc = input("")
#console_Demo()