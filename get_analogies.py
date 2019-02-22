# To get analogies of the word
# Created by Lu Meng
# Last update: 12/18/18

import gensim
import pickle
from nltk.corpus import brown

'''
# get traning data
data = brown.sents(categories = brown.categories())
data = [[word.lower() for word in sent] for sent in data]
data = [[word for word in sent if word.isalpha()] for sent in data]
pickle.dump(data, open('corpus.txt', 'wb'))

# train the model
model = gensim.models.Word2Vec(data, size=100, window=7, min_count=2, workers=10)
model.save('word2vec.model')
'''

data = pickle.load(open('corpus.txt', 'rb'))
corpus = set()
for sent in data:
    for word in sent:
        corpus.add(word)

def get_analogies(word):
    if not word in corpus:
        return []
    model = gensim.models.Word2Vec.load('word2vec.model')
    similar_words = model.most_similar(positive=word)[5:]
    analogies = [word[0] for word in similar_words]
    return analogies

