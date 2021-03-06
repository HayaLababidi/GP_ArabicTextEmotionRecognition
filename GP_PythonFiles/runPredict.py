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
import gensim
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
import string
from nltk.stem.isri import ISRIStemmer
from googleapiclient.discovery import build
import pickle
from matplotlib import pyplot as plt
import itertools
import sys

class Data_operations:
    my_api_key = "AIzaSyCUKEOsT6ecC3ods862vgsVOawWyii0NDQ"
    my_cse_id = "007967891901694126580:i3iq-cjlldq"

    def __init__(self):  # , my_api_key, my_cse_id):
        self._dictionary = None
        self._test_size = 0.1
        self.out_of_vocab = 0
        self.in_vocab = 0
        self._aravec_model_name = r"C:\GP_PythonFiles\models\full_grams_sg_100_twitter"
        self.arabic_punctuations = '''`÷×؛<>_()*&^%][،/:"؟.,'{}~¦+|!”…“–»«•'''
        self.english_punctuations = string.punctuation
        self.english_numbers = "0123456789"
        self.punctuations_list = self.arabic_punctuations + self.english_punctuations + self.english_numbers
        self.t_model = None
        self._number_of_inputs = 140
        self._vector_size = 100
        self.arabic_diacritics = re.compile("""
                                        ـ    | # empty line in between letters (longation) 
                                         ّ    | # Tashdid
                                         َ    | # Fatha
                                         ً    | # Tanwin Fath
                                         ُ    | # Damma
                                         ٌ    | # Tanwin Damm
                                         ِ    | # Kasra
                                         ٍ    | # Tanwin Kasr
                                         ْ    | # Sukun
                                     """, re.VERBOSE)
        self.google_api_key = "AIzaSyCUKEOsT6ecC3ods862vgsVOawWyii0NDQ"
        self.cse_id = "007967891901694126580:i3iq-cjlldq"

    # mode 0 functions
    def google_search(self, search_term):
        service = build("customsearch", "v1", developerKey=self.google_api_key)
        res = service.cse().list(q=search_term, cx=self.cse_id).execute()
        return res['spelling']['correctedQuery']

    def normalize_arabic(self, text):
        text = re.sub("إ", "ا", text)
        text = re.sub("أ", "ا", text)
        text = re.sub("آ", "ا", text)
        text = re.sub("ا", "ا", text)
        # text = re.sub("ى", "ي", text)
        # text = re.sub("ؤ", "ء", text)
        # text = re.sub("ئ", "ء", text)
        # text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        return text

    def remove_diacritics(self, text):
        text = re.sub(self.arabic_diacritics, '', text)
        return text

    def remove_punctuations(self, text):
        for c in self.punctuations_list:
            text = text.replace(c, " ")
        return text

    def remove_repeating_char(self, text):
        return re.sub(r'(.)\1+', r'\1', text)

    def tokens_remove_stopwords(self, text):
        text = text.split()
        result = list()
        ch = 0

        arabic_stop_words = ["من", "فى", "الي", "علي", "عن", "حتي", "مذ", "منذ", "و", "الا", "او", "ام", "ثم", "بل",
                             "لكن",
                             "كل", "متى", "يوم"]

        for word in text:
            for stop_word in arabic_stop_words:
                if word == stop_word:
                    ch = 1
                    break

            if ch != 1:
                result.append(word)

            ch = 0

        return result

    def rooting(self, text):
        result = list()
        for word in text:
            stemmer = ISRIStemmer()
            result.append(stemmer.stem(word))
        return result

    def remove_english(self, tokens):
        filtered_tokens = list()
        for word in tokens:
            if (not re.match(r'[a-zA-Z]+', word, re.I)) and word != '':
                filtered_tokens.append(word)
        return filtered_tokens

    def preprocess_doc(self, text):
        text = str(text)
        text = self.remove_diacritics(text)
        text = self.remove_punctuations(text)
        text = self.normalize_arabic(text)
        text = self.remove_repeating_char(text)
        tokens = re.split(" ", text)
        tokens = self.remove_english(tokens)
        return tokens

    def embed_doc_word(self, text):
        if self.t_model is None:
            self.t_model = gensim.models.Word2Vec.load(self._aravec_model_name + '.mdl')

        preprocessed_text = self.preprocess_doc(text)
        # print(preprocessed_text)

        embedded_vectors = np.zeros(
            shape=(
            self._number_of_inputs, self._vector_size))  # np array of arrays (array of 100/300 float number per word)
        embedded_vectors_index = 0
        for i in range(len(preprocessed_text)):
            if embedded_vectors_index > self._number_of_inputs:
                break
            try:
                embedded_vectors[embedded_vectors_index] = self.t_model.wv[preprocessed_text[i]]
                embedded_vectors_index = embedded_vectors_index + 1
            except:
                try:
                    result = self.rooting([preprocessed_text[i]])[0]
                    embedded_vectors[embedded_vectors_index] = self.t_model.wv[result]
                    embedded_vectors_index = embedded_vectors_index + 1
                except:
                    try:
                        # print(self,"in google search " + preprocessed_text[i])
                        search_output = self.google_search(preprocessed_text[i])
                        # print("search_output " + search_output)
                        tokens = re.split(" ", search_output)
                        for j in range(len(tokens)):
                            try:
                                embedded_vectors[embedded_vectors_index] = self.t_model.wv[tokens[j]]
                                embedded_vectors_index = embedded_vectors_index + 1
                                #print("added " + tokens[j])
                            except:
                                pass
                                #print(tokens[j] + " Sub word cant be embedded")
                    except:
                        # print(preprocessed_text[i] + "word cant be embedded") #currently emojis can't be embedded and for any extreme case (skip wrongly written words)
                        self.out_of_vocab = self.out_of_vocab + 1
        self.in_vocab = self.in_vocab + embedded_vectors_index
        return embedded_vectors, self.out_of_vocab, self.in_vocab

    def embed_dataset_word(self, X_train, X_test):
        eX_train = np.zeros(shape=(len(X_train), self._number_of_inputs, self._vector_size),
                            dtype=np.float16)  # number of tweets*max number of words per tweet*vector size per word
        eX_test = np.zeros(shape=(len(X_test), self._number_of_inputs, self._vector_size), dtype=np.float16)

        self.out_of_vocab = 0
        self.out_of_vocab = 0
        for i in range(len(X_train)):
            eX_train[i], self.out_of_vocab, self.out_of_vocab = self.embed_doc_word(X_train[i])

        for i in range(len(X_test)):
            eX_test[i], self.out_of_vocab, self.out_of_vocab = self.embed_doc_word(X_test[i])
        # print("out emo", self.out_of_vocab)
        # print("in emo", self.in_vocab)
        return eX_train, eX_test

    # mode 2 functions
    def get_dictonary(self, dataset):
        uniques = ''
        row = ''
        for text in dataset:
            # row = ''
            try:
                row = row + ''.join(set(text[0]))
            except:
                pass
            # uniques = uniques.join(set(row)) #append(row)

            # print("row:", row)
        uniques = uniques.join(set(row))
        #print("uniques:", uniques)
        # uniques = (set(uniques))
        length = len(uniques)
        #
        #print(length)
        indexes = list(range(length))

        di = dict(zip(uniques, indexes))
        return di

    def convert_to_int_doc(self, text, dictionary):

        row_length = 288
        padding = len(dictionary)
        row = []
        try:
            for char in text[0]:
                number = dictionary[char]
                row.append(number)
            length = len(row)
            for i in range(length, row_length):
                row.append(padding)
        except:
            length = len(row)
            for i in range(length, row_length):
                row.append(padding)
        return np.array(row)

    def one_hot_encode_doc(self, dictionary, text):
        onehot_text = []
        row_length = 288
        padding = np.zeros(len(dictionary))
        if text[0] is not None:
            try:
                for character in text[0]:
                    vector = np.zeros(len(dictionary))
                    index = dictionary[character]
                    vector[index] = 1
                    onehot_text.append(vector)
            except :
                pass
        length = len(onehot_text)
        for i in range(length, row_length):
            onehot_text.append(padding)
        return onehot_text

    def one_hot_encode_dataset(self, dictionary,dataset):
        data_array2d = []
        for row in dataset:
            temp = []
            temp = self.one_hot_encode_doc(dictionary, row)
            data_array2d.append(temp)

        return data_array2d




    def one_hot_encode(dataset):
        max_length = 0
        data_Array2d = []

        for i in range(len(dataset)):
            try:
                chars = list(dataset[i][0])
                cur_length = len(dataset[i][0])
                if cur_length > max_length:
                    max_length = cur_length
            except:
                #print("skipped row{}".format(i))
                continue

            length = len(chars)

            for indexRow in range(length):
                temp = []
                temp.append(chars[indexRow])
                data_Array2d.append(temp)
        #print("max_length of sentences", max_length)

        hot = OneHotEncoder(handle_unknown='ignore')
        # print("dataset array length",len(data_Array2d))
        hot.fit(data_Array2d)
        # print("categorys",hot.categories)

        encoded_dataset = np.zeros(shape=(len(dataset), max_length, 155))  # list of encoded rows
        encoded_row = np.zeros(shape=(max_length, 155))  # vectors for each char in dataset row

        # for each row get 2darray of char
        # encode each char ,append encoded_row
        # append encoded dataset

        for i in range(len(dataset)):
            row = dataset[i]
            try:
                chars = list(row[0])
            except:
                pass
                #print(row[0])
            length = len(chars)
            char_2d = []
            for indexRow in range(max_length):
                temp = []
                try:
                    temp.append(chars[indexRow])
                except:
                    temp.append(" ")
                char_2d.append(temp)
            encoded_row = hot.transform(char_2d).toarray()


            encoded_dataset[i] = encoded_row

        encoded_datasetLength = len(encoded_dataset[0])
        #print("encoded_dataset vector lenght", encoded_datasetLength)
        # x = np.array(encoded_dataset)
        #print("dataset shape", encoded_dataset.shape)
        #print("\n------------------")
        return encoded_dataset, max_length, encoded_datasetLength

    def convert_to_int_dataset(self, dataset, dictionary):

        row_length = 288
        data_length = len(dataset)
        int_dataset = np.zeros((data_length, row_length))
        padding = len(dictionary)

        for index in range(data_length):
            text = dataset[index]
            row = self.convert_to_int_doc(text, dictionary)
            int_dataset[index] = row

        return int_dataset

    def embedd_doc(self, text, mode):

        # mode 0 word embedding , mode 1 one hot , mode 2 integer embedding,3 keras
        embedded_vector = []
        if mode == 0:
            self._number_of_inputs = 140
            self._vector_size = 100
            embedded_vector, in_vocab, out_vocab = self.embed_doc_word(text)
        elif mode == 1:
            if self._dictionary is None:
                # load dictionary if it's not loaded
                try:
                    pickle_in = open("dict.pickle", "rb")
                    self._dictionary = pickle.load(pickle_in)
                except:
                    #  indicate some error and quit
                    return "no dictionary was found "
            embedded_vector = self.one_hot_encode_doc(self._dictionary,text)
        elif mode == 2:
            #  integer representation
            if self._dictionary is None:
                # load dictionary if it's not loaded
                try:
                    pickle_in = open("dict.pickle", "rb")
                    self._dictionary = pickle.load(pickle_in)
                except:
                    #  indicate some error and quit
                    return "no dictionary was found "
            # convert each character to integer number
            embedded_vector = self.convert_to_int_doc(text, self._dictionary)
        '''elif mode == 3:
        #experemental mode , future work
            return X, label_binarizer.classes_, one_hot_Y'''
        return embedded_vector

    def read_dataset(self, mode):
        # mode 0 word embedding , mode 1 one hot , mode 2 integer embedding,3 keras

        data_df = pd.read_csv("C:\GP_PythonFiles\models\Emotional-Tone-Dataset.csv", encoding="windows-1256")
        X = data_df[['tweet']].values
        Y = data_df[['label']].values
        # use own labels
        label_binarizer = LabelBinarizer()
        label_binarizer.fit(Y)  # need to be global or remembered to use it later
        one_hot_Y = label_binarizer.transform(Y)
        if mode == 0:
            self._number_of_inputs = 140
            self._vector_size = 100
            X_train, X_test, y_train, y_test = train_test_split(X, one_hot_Y, test_size=self._test_size,
                                                                random_state=42)
            eX_train, eX_test = self.embed_dataset_word(X_train, X_test)
        elif mode == 1:
            if self._dictionary is None:
                try:
                    pickle_in = open("dict.pickle", "rb")
                    self._dictionary = pickle.load(pickle_in)
                except:
                    self._dictionary = self.get_dictonary(X)
                    pickle_out = open("dict.pickle", "wb")
                    pickle.dump(self._dictionary, pickle_out)
                    pickle_out.close()
            X = self.one_hot_encode_dataset(self._dictionary, X)
            eX_train, eX_test, y_train, y_test = train_test_split(X, one_hot_Y, test_size=self._test_size,
                                                                random_state=42)
        elif mode == 2:
            if self._dictionary is None:
                try:
                    pickle_in = open("dict.pickle", "rb")
                    self._dictionary = pickle.load(pickle_in)
                except:
                    self._dictionary = self.get_dictonary(X)
                    pickle_out = open("dict.pickle", "wb")
                    pickle.dump(self._dictionary, pickle_out)
                    pickle_out.close()

            # convert each character to integer number
            int_dataset = self.convert_to_int_doc(X, self._dictionary)
            eX_train, eX_test, y_train, y_test = train_test_split(int_dataset, one_hot_Y, test_size=self._test_size,
                                                                  random_state=42)
        elif mode == 3:
            # experimental
            pass
        return eX_train, eX_test, y_train, y_test, label_binarizer.classes_

    # add char embedding functions  3 of them  keras one hot integer
    # label making function

class model:
    # import read_data
    dir_ = "C:\GP_PythonFiles\models"
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
        self.filename = "C:\GP_PythonFiles\models\weights.{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}.hdf5"
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
        #print(np.argmax(predicted_y, axis=1).shape)
        acc = accuracy_score(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        report = classification_report(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        cm = confusion_matrix(np.argmax(test_y, axis=1), np.argmax(predicted_y, axis=1))
        return cm, acc, report

    def predict(self, sentence, modelname):
        if self.model is None:
            try:
                self.model = load_model("C:\GP_PythonFiles\models\c3_100.h5")
            except:
                self.model = load_model("C:\GP_PythonFiles\models\c3_100")
            predicted_y = self.model.predict(sentence)
            # except:
            #   print(modelname+" model not found")
        else:
            predicted_y = self.model.predict(sentence)
        return predicted_y

class system:
    dir_ = 'C:\GP_PythonFiles\models'

    def __init__(self):
        self.m = model()
        self.data = Data_operations()

    def predict_doc(self, text, modelname='3_100', mode=0):  # add default model name
        embedded_vector = self.data.embedd_doc(text, mode)
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
            #print(self.dir_+'X_train_mode_' + str(mode) + '.npy')
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
        #print("Test Accurcy: " + str(acc))
        #print(report)
        plot_confusion_matrix(cm, classes_, True)

text = sys.argv[1]
s = system()
lable = s.predict_doc(text)
print (lable)