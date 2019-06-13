import keras
import random
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.models import load_model
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import csv
import numpy as np
import matplotlib as plt
import itertools


class model:
    # import read_data
    dir_ = "./models/"
    def __init__(self):
        self._dropout_rate = 0.2
        self._dropout_rate_softmax = 0.5
        self._number_of_inputs = 140  # max number of words /characters per doc(tweet)
        self._vector_size = 100  # vector for each word
        self._batch_size = 10
        self._kernal_size = 3  # An integer or tuple/list of a single integer
        self._pool_size = 2
        self._epochs = 50
        self._test_size = 0.1  # percentage of test from the dataset
        self._Learning_rate = 0.0001
        # _feature_maps = [100,400,500,600,700,800,900,1000,1100,1200]
        self._feature_maps = 100
        self._num_conv = 2
        self.filename = "models/weights.{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}.hdf5"
        self.model = None

    def train(self, train_x, train_y, modelname="trial"):
        self.model = Sequential()

        # input
        # self.model.add(keras.layers.Input(shape=(_number_of_inputs,_vector_size)))

        # Dropout
        self.model.add(keras.layers.Dropout(rate=self._dropout_rate, input_shape=(
            self._number_of_inputs, self._vector_size)))  # ,noise_shape,random.randint(0,number_of_inputs)))

        # Convolution
        self.model.add(
            keras.layers.Conv1D(filters=self._vector_size, kernel_size=self._kernal_size, strides=1, activation="relu"))
        # self.model.add(keras.layers.MaxPooling1D(pool_size = _pool_size, padding='same'))

        for i in range(self._num_conv):
            # print(i)
            self.model.add(
                keras.layers.Conv1D(filters=self._feature_maps, kernel_size=self._kernal_size, strides=1,
                                    activation="relu"))
            if i % 2 == 0:
                # print("pool", i)
                #if i % 4 == 0:
                    #self.model.add(keras.layers.BatchNormalization())
                self.model.add(keras.layers.MaxPooling1D(pool_size=self._pool_size, padding='same'))

        # Dropout
        self.model.add(
            keras.layers.Dropout(self._dropout_rate_softmax))  # ,noise_shape,random.randint(0,number_of_inputs)))

        # output
        self.model.add(keras.layers.Flatten())
        # self.model.add(keras.layers.Dense(500, activation="relu"))
        self.model.add(keras.layers.Dense(8, activation="softmax"))

        opt = keras.optimizers.Adam(lr=self._Learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                    amsgrad=False);

        self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        self.model.summary()

        tensorboard = TensorBoard(log_dir='./log', histogram_freq=1, write_graph=True, write_grads=True,
                                  batch_size=self._batch_size, write_images=True)
        Checkpoint = keras.callbacks.ModelCheckpoint(self.filename, monitor='val_acc', verbose=0, save_best_only=True,
                                                     save_weights_only=False, mode='auto', period=1)
        ReduceLR = keras.callbacks.ReduceLROnPlateau()

        # Train the model
        self.model.fit(train_x, train_y, batch_size=self._batch_size, epochs=self._epochs, validation_split=0.1,
                       shuffle=True, callbacks=[tensorboard, Checkpoint, ReduceLR])
        self.model.save(self.dir_ + modelname + ".h5")

    def retrain(self, train_x, train_y, modelname="trial"):
        tensorboard = TensorBoard(log_dir='./log', histogram_freq=1, write_graph=True, write_grads=True,
                                  batch_size=self._batch_size, write_images=True)
        Checkpoint = keras.callbacks.ModelCheckpoint(self.filename, monitor='val_acc', verbose=0, save_best_only=True,
                                                     save_weights_only=False, mode='auto', period=1)
        ReduceLR = keras.callbacks.ReduceLROnPlateau()

        # Train the model
        self.model.fit(train_x, train_y, batch_size=self._batch_size, epochs=self._epochs, validation_split=0.1,
                       shuffle=True, callbacks=[tensorboard, Checkpoint, ReduceLR])
        self.model.save(modelname + ".h5")

    def test(self, test_x, test_y, modelname):
        if self.model is None:
            try:
                self.model = load_model(self.dir_+modelname + ".h5")
            except:
                self.model = load_model(self.dir_ + modelname)
        self.model.summary()
        predicted_y = self.model.predict(test_x)
        print(np.argmax(predicted_y, axis=1).shape)
        acc = accuracy_score(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        report = classification_report(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        cm = confusion_matrix(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        return cm, acc, report

    def predict(self, sentence, modelname):
        if self.model is None:
            try:
                self.model = load_model(self.dir_ + modelname + ".h5")
            except:
                self.model = load_model(self.dir_ + modelname)
            predicted_y = self.model.predict(sentence)
            # except:
            #   print(modelname+" model not found")
        else:
            predicted_y = self.model.predict(sentence)
        return predicted_y