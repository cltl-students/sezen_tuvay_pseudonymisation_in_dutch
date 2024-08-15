#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import re
import pandas as pd
import json
import os
import jsbeautifier

pronouns = {'ik', 'hem', 'haar', 'zijn', 'mijn', 'mij', 'jou', 'jouw', 'ons', 'onze', 'uw', 'zij', 'je', 'ze', 'me', 'we', 'u', 'hen', 'hun', 'hij', 'wij', 'jullie',}
etiquette = {
    'mevrouw', 'meneer', 'mevrou', 'mijnheer','vrouw', 'Dhr.', 'mevr.', 'heer', 'mr', 'dhr', 'mr.','advocaat','advocate','ambassadeur','attaché','baron','barones',
    'commissaris', 'consul','doctorandus','gedeputeerde','gezant','gouverneur','graaf','gravin','hoogleraar','ingenieur',
    'inspecteur','jonkheer','jonkvrouw','kandidaat-notaris','kantonrechter','kardinaal','koning','koningin','korpschef',
    'gemeenteraadslid', 'meester','minister','ombudsman','notaris','officier van justitie','burgemeester',
    'president','prins','prinses','generaal','professor','raadsheer','rechter','secretaris-generaal',
    'staatssecretaris','voorzitter','wethouder'}

def heuristics(file):
    """
    This function applies Heuristics B to one file. First, the file is opened from output_combined. Then, all pronouns are found. 
    The coref-number that is attached to this pronoun is found and the persons which are referenced by with this pronoun are also found.
    Then, I-PER is assigned to all pseudovalues. Then, when an etiquette is found, the first token is changed into a 'B_PER', 
    the following tokens are kept 'I_PER'. After this, single mentions are found and 
    pseudo numbers are eventually made sequential
    """
    potential_persons_list = []
    persons_list = []
    data = []
    directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_combined/'
    with open(directory+file, "r") as infile:
        csv_reader = csv.reader(infile, delimiter='\t')
        header = next(csv_reader)
        for row in csv_reader:
            info = {'token': row[1], 'coref': row[2].split('|'), 'ner': row[3], 'pseudo': []}
            data.append(info)
    
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

    for i, line in enumerate(data):
        coref_labels = line['coref']
        if line['token'].lower() in pronouns:
            if len(line['coref']) != 0:
                for element in line['coref']:
                    if element.startswith('(') and element.endswith(')'):
                        potential_person = element.strip('()')
                        potential_persons_list.append(str(potential_person))
    for i, line in enumerate(data):
        for element in line['coref']:
            an_element = element.strip('()')
            if an_element in set(potential_persons_list):
                #print(line)# and data[i]['ner'].endswith('-PER'):
                # and len(data[i]['pseudo']) == 0:
                persons_list.append(an_element)
            if an_element in set(persons_list):
                data[i]['pseudo'].append('I_PER_'+str(an_element))
                

    #ner-people as well
    #assumption: most surnames have: I, I, E. Never, I, I, I. 
    # 
    d = 10000
    for i, line in enumerate(data):
        if line['ner'] != 'O' and line['pseudo'] == []:
            if line['ner'].startswith('B-') and len(line['coref']) == 1:
                potential_person = line['coref'][0].strip('()')
                data[i]['pseudo'].append('I_PER_'+str(potential_person))
                if data[i+1]['ner'].startswith('I-') or data[i+1]['ner'].startswith('E-'):# and len(data[i]['pseudo']) == 0 or data[i+1]['ner'].startswith('E-') and len(data[i]['pseudo']) == 0:
                    data[i+1]['pseudo'].append('I_PER_'+str(potential_person))
                #if int(i+2) <= len(data):
                if data[i+2]['ner'].startswith('E-'):
                    data[i+2]['pseudo'].append('I_PER_'+str(potential_person))
            elif line['ner'].startswith('B-') and len(line['coref']) != 1:
                data[i]['pseudo'].append('I_PER_'+str(d))
                if data[i+1]['ner'].startswith('I-') or data[i+1]['ner'].startswith('E-') and int(i+2) <= len(data):# and len(data[i]['pseudo']) == 0 or data[i+1]['ner'].startswith('E-') and len(data[i]['pseudo']) == 0:
                    data[i+1]['pseudo'].append('I_PER_'+str(d))
                elif int(i+2) <= len(data):
                    if data[i+2]['ner'].startswith('E-'): 
                        data[i+2]['pseudo'].append('I_PER_'+str(d))
                        d += 10000
            elif line['ner'].startswith('S-') and line['token'][0].isupper() == True:
                    if len(line['coref']) == 1:
                        element = line['coref'][0].strip('()')
                        data[i]['pseudo'].append('I_PER_'+str(element))
                    else:
                        data[i]['pseudo'].append('I_PER_'+str(d))
                        d += 10000
                        
    # etiquette, B_PER
    for i, line in enumerate(data):
        if line['token'].lower() in etiquette:
            if len(data[i+1]['pseudo']) != 0 :
                element = data[i+1]['pseudo'][0].strip('I_PER_')
                if len(data[i]['pseudo']) == 0:
                    data[i]['pseudo'].append('B_PER_'+str(element))   
                else:
                    data[i]['pseudo'][0]=('B_PER_'+str(element))
                    data[i]['pseudo'] = [data[i]['pseudo'][0]]

        elif 'I_PER' in str(line['pseudo']) and len(data[i-1]['pseudo']) == 0:
            data[i]['pseudo'] = [data[i]['pseudo'][0].replace('I_PER', 'B_PER')]
    
    #removing double pseudonyms and taking the first one!
    for i, line in enumerate(data):
        if len(line['pseudo']) == 2:
            line['pseudo'] = [line['pseudo'][0]]
           
    # making pseudo-numbers sequential
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
    outfile = open("/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/pseudo-b/"+file+".json", "w", encoding='utf-8')
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

