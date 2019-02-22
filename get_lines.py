# To get Twilight Sparkle's lines from transcripts
# Created by Lu Meng
# Last update: 12/12/18

import os
import re

files= os.listdir("Transcripts")
fo1 = open("TS_lines.txt", "w")
# fo2 = open("TS_lines_separate.txt", "w") # this is for n-gram

regex_sentence = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s(?!\.|.\?|\!|[a-z])"

for file in files:
    fi = open("Transcripts/"+file, "r")
    if re.search(r"\.txt", file):
        letter = False
        for line in fi:
            # TS_lines = False
            if letter:
                fo1.write(line)
                letter = False
                # TS_lines = True
            else:
                # to distinguish what TS says from someone calling her name
                line = "TS" + line
                if re.search(r"TSTwilight Sparkle", line) and re.search(":", line):
                    if re.search(r"Dear Princess Celestia", line):
                        letter = True
                    # print(file, line)
                    line = line.split(": ", 1)[1]
                    if len(line) > 11: # ignore lines which are too short
                        fo1.write(line)
                        # TS_lines = True
            '''
            # this part is for n-gram
            if TS_lines:
                separate_lines = re.split(regex_sentence, line)
                for i in range(len(separate_lines)):
                    fo2.write(separate_lines[i])
                    if i < len(separate_lines)-1:
                        fo2.write("\n")
            '''
        fi.close()

fo1.close()
# fo2.close()
