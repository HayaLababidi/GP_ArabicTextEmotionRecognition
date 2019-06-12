import gensim
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
import string
from nltk.stem.isri import ISRIStemmer
from googleapiclient.discovery import build
import pickle
import csv


class Data_operations:
    my_api_key = "AIzaSyCUKEOsT6ecC3ods862vgsVOawWyii0NDQ"
    my_cse_id = "007967891901694126580:i3iq-cjlldq"

    def __init__(self):  # , my_api_key, my_cse_id):
        self._dictionary = None
        self._test_size = 0.1
        self.out_of_vocab = 0
        self.in_vocab = 0
        self._aravec_model_name = "full_grams_sg_300_twitter"
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
                                print("added " + tokens[j])
                            except:
                                print(tokens[j] + " Sub word cant be embedded")
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
        print("uniques:", uniques)
        # uniques = (set(uniques))
        length = len(uniques)
        print(length)
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
                print("skipped row{}".format(i))
                continue

            length = len(chars)

            for indexRow in range(length):
                temp = []
                temp.append(chars[indexRow])
                data_Array2d.append(temp)
        print("max_length of sentences", max_length)

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
                print(row[0])
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
        print("encoded_dataset vector lenght", encoded_datasetLength)
        # x = np.array(encoded_dataset)
        print("dataset shape", encoded_dataset.shape)
        print("\n------------------")
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
            self._vector_size = 300
            embedded_vector, in_vocab, out_vocab = self.embed_doc_word(text)
        elif mode == 1:
            #  one hot
            pass
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

        data_df = pd.read_csv("Emotional-Tone-Dataset.csv", encoding="windows-1256")
        X = data_df[['tweet']].values
        Y = data_df[['label']].values
        # use own labels
        label_binarizer = LabelBinarizer()
        label_binarizer.fit(Y)  # need to be global or remembered to use it later
        one_hot_Y = label_binarizer.transform(Y)
        if mode == 0:
            self._number_of_inputs = 140
            self._vector_size = 300
            X_train, X_test, y_train, y_test = train_test_split(X, one_hot_Y, test_size=self._test_size,
                                                                random_state=42)
            eX_train, eX_test = self.embed_dataset_word(X_train, X_test)
        elif mode == 1:
            pass
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
            pass
        return eX_train, eX_test, y_train, y_test, label_binarizer.classes_

    # add char embedding functions  3 of them  keras one hot integer
    # label making function