from flair.data import Sentence as FlairSentence
from flair.models import SequenceTagger
import csv
import os

flair_model = SequenceTagger.load("flair/ner-dutch-large")
directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output copy/'
def ner_tagging_a_file(file):
    """
    param: 
    This function takes as input one file and uses Flair to NER-tag the tokens in this file. 
    """
    a_file = open(directory+file, "r", encoding='utf-8')
    text = a_file.readlines()
    a_list = []
    tokenized_text = []
    for l in text:
        new_line = l.split('\t')
        if len(new_line) > 1:
            tokenized_text.append(new_line[2])
    flair_sentence = FlairSentence(tokenized_text)
    flair_model.predict(flair_sentence)
    for token in flair_sentence:
        token_text = token.text
        if token.labels[0].value.endswith('-PER'):
            token_label = token.labels[0].value
        else:
            token_label = 'O'
        a_list.append(token_text)
        a_list.append(token_label)
    with open('/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_ner_2/'+file.strip('.conll') +'.csv', 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter='\t')
        writer.writerows(zip(a_list[::2], a_list[1::2]))

def ner_tagging_all_files():
    """
    This function takes as input the directory (sezen_data/output_copy/) and loads the function 'ner_tagging_a_file'
    on every file in this directory. 
    """
    #file = open('/Users/sezentuvay/Desktop/e2e-Dutch-master/sezen_data/not_annotated_text/'+file, "r")
    directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output copy/'
    for my_file in os.listdir(directory):
        print(my_file)
        if my_file != '.DS_Store':
            ner_tagging_a_file(my_file)

ner_tagging_all_files()