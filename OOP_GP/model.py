import keras
import random
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.models import load_model
from sklearn.metrics import accuracy_score, classification_report , confusion_matrix
import csv
import numpy as np
import matplotlib as plt
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

#     print(cm)
    plt.figure(figsize=(15,15))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('cm')


class model :
    #import read_data
    def __init__(self):
        _dropout_rate = 0.2
        _dropout_rate_softmax = 0.5
        _number_of_inputs = 140 #max number of words /characters per doc(tweet)
        _vector_size = 300 #vector for each word
        _batch_size = 10
        _kernal_size= 3 #An integer or tuple/list of a single integer
        _pool_size = 2
        _noise_shape = (_batch_size,1,_number_of_inputs)
        _epochs = 100
        _test_size = 0.1 # percentage of test from the dataset
        _Learning_rate = 0.0001
        #_feature_maps = [300,400,500,600,700,800,900,1000,1100,1200]
        _feature_maps=300
        _num_conv = 8
        model= None

    def train(self,train_x, train_y,modelname= "trial0"):
        print("done input embedding")
        model = Sequential()

        # input
        # self.model.add(keras.layers.Input(shape=(_number_of_inputs,_vector_size)))

        # Dropout
        self.model.add(keras.layers.Dropout(rate=self._dropout_rate, input_shape=(
            self._number_of_inputs, self._vector_size)))  # ,noise_shape,random.randint(0,number_of_inputs)))

        # Convolution
        # self.model.add(keras.layers.Conv1D(filters=_vector_size, kernel_size=_kernal_size, strides=1,  activation="relu",input_shape=(_number_of_inputs,_vector_size)))
        # self.model.add(keras.layers.MaxPooling1D(pool_size = _pool_size, padding='same'))

        for i in range(self._num_conv):
            print(i)
            self.model.add(
                keras.layers.Conv1D(filters=self._feature_maps, kernel_size=self._kernal_size, strides=1, activation="relu"))
            if i % 2 == 0:
                print("pool", i)
                self.model.add(keras.layers.BatchNormalization())
                self.model.add(keras.layers.MaxPooling1D(pool_size=self._pool_size, padding='same'))

        # Dropout
        self.model.add(keras.layers.Dropout(self._dropout_rate_softmax))  # ,noise_shape,random.randint(0,number_of_inputs)))

        # output
        self.model.add(keras.layers.Flatten())
        # self.model.add(keras.layers.Dense(500, activation="relu"))
        self.model.add(keras.layers.Dense(8, activation="softmax"))

        opt = keras.optimizers.Adam(lr=self._Learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                    amsgrad=False);

        self.model.compile(
            loss='categorical_crossentropy',
            optimizer=opt,
            metrics=['accuracy']
        )

        tensorboard = TensorBoard(log_dir='./log', histogram_freq=1,
                                  write_graph=True,
                                  write_grads=True,
                                  batch_size=self._batch_size,
                                  write_images=True)

        self.model.summary()

        # Train the model
        self.model.fit(
            train_x,
            train_y,
            batch_size=self._batch_size,
            epochs=self._epochs,
            validation_split =0.1,
            shuffle=True,
            callbacks=[tensorboard]
        )
        self.model.save(modelname+".h5")

    def test(self,test_x,test_y,modelname,classes):
        if self.model is None:
            self.model = load_model(modelname)
        predicted_y = self.model.predict(test_x)
        acc = accuracy_score(test_y, predicted_y)
        report = classification_report(test_y, predicted_y)
        cm = confusion_matrix(test_y, predicted_y)
        return cm, acc, report

    def predict(self, sentence, modelname=""):
        if self.model is None:
            try:
                self.model = load_model(modelname)
            except:
                print("model not found")
                predicted_y = self.model.predict(sentence)
        else:
            predicted_y = self.model.predict(sentence)
        return predicted_y