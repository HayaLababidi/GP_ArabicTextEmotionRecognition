import re
import string
from nltk.stem.isri import ISRIStemmer

#text = input("enter arabic text")

#مسح التشكيل و علامات الترقيم و الحروف المتكررة---------
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                         """, re.VERBOSE)


def normalize_arabic(text):
    text = re.sub("إ", "ا", text)
    text = re.sub("أ", "ا", text)
    text = re.sub("آ", "ا", text)
    text = re.sub("ا", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)
#----------------------------------------------------

#-------------tokenization and stop word removal
def tokens_remove_stopwords(text):

    text = text.split()
    result = list()
    ch = 0

    arabic_stop_words = ["من", "فى", "الي", "علي", "عن", "حتي", "مذ", "منذ", "و", "الا", "او", "ام", "ثم", "بل", "لكن",
                         "كل" , "متى" , "يوم"]

    for word in text:
        for stop_word in arabic_stop_words:
            if word == stop_word:
                ch = 1
                break

        if ch != 1:
            result.append(word)

        ch = 0

    return result
#_______________________________________

#تكتبوا دى فى الcmd
#****pip install nltk****
#Rooting words
def rooting(text):
    result = list()
    for word in text:
        stemmer = ISRIStemmer()
        result.append(stemmer.stem(word))
    return result

#remove english and empty strings
def remove_english(tokens):
    filtered_tokens = list()
    for word in tokens:
        if (not re.match(r'[a-zA-Z]+', word, re.I)) and word != '':
            filtered_tokens.append(word)
    return filtered_tokens


def preprocess1(text):
    text = str(text)
    text = remove_diacritics(text)
    text = remove_punctuations(text)
    text = normalize_arabic(text)
    text = remove_repeating_char(text)
    tokens = re.split(" ", text)
    tokens = remove_english(tokens)
    return tokens

def preprocess2(text):
    text = str(text)
    text = remove_diacritics(text)
    text = remove_punctuations(text)
    text = normalize_arabic(text)
    text = remove_repeating_char(text)
    text = tokens_remove_stopwords(text)
    text = remove_english(text)
    text = rooting(text)
    return text

'''
text = normalize_arabic(text)
text = remove_diacritics(text)
text = remove_punctuations(text)
text = remove_repeating_char(text)


print(text)
'''

