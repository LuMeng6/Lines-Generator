# To get the training data for the LSTM model
# Created by Lu Meng
# Last update: 12/16/18

import string

fi = open("TS_lines.txt", "r")
data = fi.read()
fi.close()

# to get clean data
data = data.replace('--', ' ')
data = data.split()
data = [word for word in data if not '[' in word and not ']' in word]

# make words in the window as inputs and the first word after window 
# as the result of LSTM
window_size = 20
length = window_size + 1
lines = list()
for i in range(length, len(data)):
    line = ' '.join(data[i-length:i])
    lines.append(line)

# save the training data
data = '\n'.join(lines)
fo = open("training_data.txt", 'w')
fo.write(data)
fo.close()
