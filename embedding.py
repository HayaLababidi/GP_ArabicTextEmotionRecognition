import gensim
import re
import numpy as np
import normalization
def embed_doc(text):
    t_model = gensim.models.Word2Vec.load('../models/full_grams_cbow_100_wiki.mdl')
    preprocessed_text = normalization.preprocess1(text)
    #print(preprocessed_text)

    embedded_vectors = list()#list of arrays (array of 100/300 float number per word)
    for tok in preprocessed_text:
        try:
            embedded_vectors.append(t_model.wv[tok])
        except:
            try:
                tok = normalization.rooting([tok])[0]
                embedded_vectors.append(t_model.wv[tok])
            except:
                print(tok + "word cant be embedded") #currently emojis can't be embedded and for any extreme case
        #print(tok)
    return embedded_vectors