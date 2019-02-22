# to generate Twilight Sparkle's lines by LSTM using Keras
# Created by Lu Meng
# Last update: 12/18/18
# Some part in this file takes Jason Brownlee's blog as a reference

import re
import random
import string
import get_analogies
from pickle import load
from nltk.corpus import wordnet
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

print("Preparing the generator...")

# load the model and the tokenizer
lstm = load_model('model_lstm.h5')
tokenizer = load(open('tokenizer.pkl', 'rb'))

fi = open("training_data.txt", "r")
data = fi.read()
lines = data.split('\n')
fi.close()
seq_length = len(lines[0].split()) - 1 # the expected length of input

print("...the generator is ready.")

# generate a sentence from the language model
def generate_sent(seed_text, n_words):
    result = list()
    sent_input = seed_text

    # limit the length of the generated sentence
    for n in range(n_words):
        finish = False
        # encode the text as integer
        encoded_text = tokenizer.texts_to_sequences([sent_input])[0]
        # extend sequences to a fixed length
        encoded_text = pad_sequences([encoded_text], maxlen=seq_length, truncating='pre')
        # predict the output word
        y_hat = lstm.predict_classes(encoded_text, verbose=0)

        # find the specific word according to y_hat
        word_output = ''
        for word, index in tokenizer.word_index.items():
            if index == y_hat:
                word_output = word
                # if the last character of the word is .|?|!, finish generating
                # make sure that the sentence isn't too short
                if re.search(r"\?|\!|\.", word) and n >= 5:
                    finish = True
                break
        sent_input += ' ' + word_output
        result.append(word_output)
        if finish:
            break
    return ' '.join(result)

# get synonyms of the word
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            if not re.search(r"_", l.name()):
                synonyms.append(l.name()) 
    return synonyms

def run(topic):
    # topic = input("Let's talk about: ")
    words_limit = 50 # limit the length of the generated sentence
    generated_line = generate_sent(topic, words_limit)

    # the interesting thing is: the line will be "i need to encourage cloudsdale mind."  
    # if Twilight has never talked about this topic before
    error_line = "i need to encourage cloudsdale mind."
    if generated_line == error_line:
        error = True
        # if topic doesn't exist, check its synonyms first
        synonyms = get_synonyms(topic)
        for syn in synonyms:
            generated_line = generate_sent(syn, words_limit)
            if generated_line != error_line:
                topic = syn
                error = False
                break
        # check its analogies if synonyms doesn't work
        if error:
            analogies = get_analogies.get_analogies(topic)
            for ana in analogies:
                generated_line = generate_sent(ana, words_limit)
                if generated_line != error_line:
                    topic = ana
                    error = False
                    break
            if error:
                return "Hm... let's talk about other things."
    return string.capwords(topic[0]) + topic[1:] + ' ' + generated_line

