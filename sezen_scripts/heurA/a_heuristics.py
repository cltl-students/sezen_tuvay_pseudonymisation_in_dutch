#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import re
import pandas as pd
import json
import os
import jsbeautifier

def heuristics(file):
    """
    This function applies Heuristics A to one file. First, the file is opened from output_combined. Then, all possible persons are found.
    Then, it finds the instances which are in the person list and the references to this. Then, I-PER is assigned to all pseudovalues
    Then, when an etiquette is found, the first token is changed into a 'B_PER', the following tokens are kept 'I_PER'.
    After this, single mentions are found and pseudo numbers are eventually made sequential
    """
    data = []
    directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_combined/'
    with open(directory+file, "r") as infile:
        csv_reader = csv.reader(infile, delimiter='\t')
        header = next(csv_reader)
        for row in csv_reader:
            info = {'token': row[1], 'coref': row[2].split('|'), 'ner': row[3], 'pseudo': []}
            data.append(info)

    #in all coref-keys, all coref-numbers are given. 
    for i, labeled_token in enumerate(data):
        coref_labels = labeled_token['coref']
        if 'O' in coref_labels:
            coref_labels.remove('O')
        for label in coref_labels:
            if '(' in label and not ')' in label:
                person_number = label.strip('(')
                j = i
                while f"{person_number})" not in data[j+1]['coref']:
                    data[j+1]['coref'].append(person_number)
                    j += 1
        
    etiquette = {
    'mevrouw', 'meneer', 'mevrou', 'mijnheer','vrouw', 'Dhr.', 'mevr.', 'heer', 'mr', 'dhr', 'mr.','advocaat','advocate','ambassadeur','attaché','baron','barones',
    'commissaris', 'consul','doctorandus','gedeputeerde','gezant','gouverneur','graaf','gravin','hoogleraar','ingenieur',
    'inspecteur','jonkheer','jonkvrouw','kandidaat-notaris','kantonrechter','kardinaal','koning','koningin','korpschef',
    'gemeenteraadslid', 'meester','minister','ombudsman','notaris','officier van justitie','burgemeester'
    'president','prins','prinses','generaal','professor','raadsheer','rechter','secretaris-generaal',
    'staatssecretaris','voorzitter','wethouder', 'burgemeester'}
    persons = set()
    random_nr = 10000
    # a list of persons is made here; when the NER tags a PER, the coref number is added to the list. 
    for i, line in enumerate(data):
        if 'PER' in line['ner']:
            if line['ner'] == 'S-PER':
                #print(i, line)
                for label in line['coref']:
                    extracted_label = re.findall(r'\((.*?)\)', label) 
                    if extracted_label != []:
                        persons.update(extracted_label)
            elif line['ner'] == 'B-PER':
                if any('(' in label for label in line['coref']):
                    labeled_items = [label for label in line['coref'] if '(' in label]
                    if len(labeled_items) == 1:
                        extracted_label = labeled_items[0].strip('(')
                        persons.update([extracted_label])
                    else:
                        extracted_label = labeled_items[-1].strip('(')
                        persons.update([extracted_label])
    #step 2
    all_corefs = []
    for i, line in enumerate(data):
        if len(line['coref']) == 1:
            coref_str = str(line['coref']).strip("[('')]")
            all_corefs.append(coref_str)
        elif len(line['coref']) > 1:
            #last element in coref-list is chosen here by using [-1]
            coref_str = str(line['coref'][-1]).strip("()")
            all_corefs.append(coref_str)
        else:
            all_corefs.append('[]')

    #giving I-PER
    all_coref_persons = set()
    for i, line in enumerate(data):
        j = i
        if 'PER' in line['ner'] and all_corefs[i] in persons:
            line['pseudo'].append('I_PER_'+all_corefs[i])
            all_coref_persons.add(all_corefs[i])
        elif 'PER' in line['ner'] and all_corefs[i] not in persons:
            line['pseudo'].append('I_PER_'+str(random_nr))
            if j + 1 < len(data) and 'PER' in data[j+1]['ner']:
                data[j+1]['pseudo'].append('I_PER_'+str(random_nr))
                j += 1
            else:
                random_nr += 10000
                j = 0
        elif 'PER' not in line['ner'] and all_corefs[i] in persons:
            line['pseudo'].append('I_PER_'+all_corefs[i])
           

    #checking etiquette
    for i, line in enumerate(data):
        if line['token'].lower() in etiquette:
            if len(data[i+1]['pseudo']) != 0:
                if len(data[i+1]['coref']) == 0:
                    line['pseudo'].append('B_PER_'+str(random_nr))
                    random_nr += 1
                else: 
                    number = re.findall(r'\d+', str(data[i+1]['pseudo']))
                    number = number[0]
                    line['pseudo'].append('B_PER_'+number)
                    data[i+1]['pseudo'].append('I_PER_'+number)
                    
    #for 2 pseudos in 1 line:
    for i, line in enumerate(data):
        new_line = []
        if len(line['pseudo']) > 1:
            line['pseudo'] = line['pseudo'][-1].split()
        
    #single mentions
    for i, line in enumerate(data):
        if 'I_PER' in str(line['pseudo']) and len(data[i-1]['pseudo']) == 0:
            line['pseudo'] = str(line['pseudo']).replace('I_PER', 'B_PER')
    
    #making pseudo-numbers sequential
    current_tags = ['0',]
    for i, line in enumerate(data):
        if len(line['pseudo']) != 0:
            current_tag = re.findall(r'\d+', str(line['pseudo']))
            current_tag_stripped = str(current_tag).strip("['']")
            current_tags.append(current_tag_stripped)
            current_tags = list(dict.fromkeys(current_tags))
    for i, line in enumerate(data):
        if "PER" in str(line['pseudo']):
            tag = re.findall(r'\d+', str(line['pseudo']))
            tag_stripped = str(tag).strip("['']")
            if str(tag_stripped) in current_tags:
                line['pseudo'] = str(line['pseudo']).replace(str(tag_stripped), str(current_tags.index(tag_stripped)))
            if line['token'] == '(':
                line['pseudo'] = []

    file = file.rstrip(".tsv")
    directory2 = "/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/annotated-data/Annotations - "
    with open(directory2+file+".csv", "r") as gold_file:
        gold_pseudo_list = []
        second_token_list = []
        csv_reader = csv.reader(gold_file, delimiter=',')
        for row in csv_reader:
            second_token_list.append(row[0])
            gold_pseudo_list.append(row[2])
    token_list = []
    predicted_pseudo_list = []
    for i, line in enumerate(data):
        token_list.append(line['token'])
        predicted_pseudo_list.append(line['pseudo'])
    outfile = open("/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/pseudo-a/"+file+".json", "w", encoding='utf-8')
    big_dict = []
    for a_dic in data:
        big_dict.append(a_dic)
    json.dump(big_dict, outfile, indent=1)


def heuristics_all_files():
    """
    This file applies the heuristics-function on all files in 'output_combined'.
    """
    directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_combined/'
    for my_file in os.listdir(directory):
        if my_file != '.DS_Store':
           heuristics(my_file)
heuristics_all_files()

