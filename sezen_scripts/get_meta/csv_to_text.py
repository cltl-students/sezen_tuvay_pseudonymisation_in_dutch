import csv
import os
from collections import defaultdict
def csv_to_text():
    """
    This function is used to change the structure of the files in preparation for the file get_meta.py in the same directory (get_meta). 
    """
    directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/annotated-data/'
    for file in os.listdir(directory):
        with open(directory+file, encoding = 'utf-8') as csv_file_handler:
            csvreader = csv.reader(csv_file_handler)
            tokens_list = []
            sentence_list = []
            for row in csvreader:
                tokens_list.append(row[0])
            sentence_list = ' '.join(tokens_list)
        with open('/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/not_annotated_text/' + file.replace('Annotations - ', '').replace(" ", "_").strip('.csv') + '.txt', 'w') as text_file:
            text_file.write(str(sentence_list))
csv_to_text()
