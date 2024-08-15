import os
import nltk
from nltk.probability import FreqDist
from collections import defaultdict
import csv
import io
# to do: add to dataframe!
directory = '/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/annotated-data/'
directory2 = '/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/not_annotated_text/'

def meta_data(file):
    """
    This function takes as input a file, and information about the sentences is given. The number of sentences per file,
    the number of tokens in longest and shortest sentence, longest sentence, as well as average number of tokens in a sentence
    """
    with open(directory2+file, encoding = 'windows-1252', errors='ignore') as f:
        text = f.read()
        sentences = nltk.sent_tokenize(text) #the number of sentences is counted
        sum = 0
        lengths_list = [] 
        for a_sentence in sentences:
            words = nltk.word_tokenize(a_sentence) #the number of tokens in the longest sentence is counted
            length = len(words) #the longest sentence 
            lengths_list.append(length)
            sum += length 
        average_words_in_sentence = sum / len(sentences) #the average number of tokens in a sentence is given
    print(file.replace('.txt', ''), '\t', len(sentences), '\t', max(lengths_list), '\t', min(lengths_list), '\t', round(average_words_in_sentence, 2))

def get_nr_persons(file):
    """
    This function takes as input a file and information about the persons is given. The number of person references
    according to the NER gold set, the number of references according to the annotated set, the number of different persons,
    the number of words is given. 
    """
    with open(directory+file, encoding = 'utf-8') as csv_file_handler:
        csvreader = csv.reader(csv_file_handler)
        nr_of_person_references = 0
        nr_of_references = 0
        count = 0
        words_no_punc = []
        nr_of_people = []
        more_than_3_ref = 0
        for row in csvreader:
            count += 1 
            if row[1] == 'B-PER':
                nr_of_person_references += 1 #gives the number of person references according to the NER gold set. 
            if row[2].startswith('B_PER_'): 
                nr_of_references += 1 #gives the number of person references according to the annotated set
                nr_of_people.append(int(row[2].strip('B_PER_'))) ##gives the number of different persons according to the annotated set
            if row[0].isalpha():
                words_no_punc.append(row[0].lower()) #gives number of words, excluding punctuation. 

        print(file, '\t', count, '\t', len(words_no_punc),'\t', nr_of_person_references, '\t', nr_of_references, '\t', max(nr_of_people))

def main():
    for file in os.listdir(directory):
        print(get_nr_persons(file))
    for file in os.listdir(directory2):
        print(meta_data(file))
main()
