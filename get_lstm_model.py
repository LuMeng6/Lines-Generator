# To train the LSTM model
# Created by Lu Meng
# Last update: 12/18/18
# This part takes Jason Brownlee's blog as a reference

import numpy as np
from pickle import dump
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.models import Sequential
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer

fi = open("training_data.txt", "r")
data = fi.read()
lines = data.split('\n')
fi.close()

# encode sequences of words to ingeters
tokenizer = Tokenizer(filters='\n')
tokenizer.fit_on_texts(lines)
training_data = tokenizer.texts_to_sequences(lines) # integer
vocab_size = len(tokenizer.word_index) + 1 # vocabulary size

# separate training data into input set X and output set Y
training_data = np.array(training_data)
X, Y = training_data[:,:-1], training_data[:,-1]
# one-hot encode the output word
Y = to_categorical(Y, num_classes=vocab_size)
seq_length = X.shape[1]

# define the model
model_lstm = Sequential()
# embedding layer
model_lstm.add(Embedding(vocab_size, 32, input_length=seq_length))
# 2 hidden layers
model_lstm.add(LSTM(100, return_sequences=True))
model_lstm.add(LSTM(100))
# dense layers: fully connected
model_lstm.add(Dense(100, activation='relu'))
model_lstm.add(Dense(vocab_size, activation='softmax'))
# print(model_lstm.summary())

model_lstm.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# try different values of batch sizes and epochs to find the best performance
model_lstm.fit(X, Y, batch_size=128, epochs=100)

# save the model and the tokenizer
model_lstm.save('model_lstm.h5')
dump(tokenizer, open('tokenizer.pkl', 'wb'))
