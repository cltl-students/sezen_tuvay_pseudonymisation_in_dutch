import pandas as pd
import os

directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output copy/' 
directory2 = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_ner_new/'
filenames_list = []


def align_tokens():
    """
    This function aligns the tokens of the output of the end-to-end Coreference Resolution model, as well as the output
    of the Flair NER-tagger. This, in order to finally make the pseudonymisation taga which is done in the following step: 
    see README.md   
    """
    for file in os.listdir(directory):
        if file.endswith('.conll'): 
            with open(directory+file, encoding='utf-8') as f:
                text = f.readlines()
            a_token_list = []
            coref_list = []
            for l in text:
                a_line = l.split('\n')
                if a_line != ['', '']:
                    for items in a_line:
                        new_items = items.split('\t')
                        if new_items != [''] and new_items != ['#begin document (example);'] and new_items != ['#end document']:
                            a_token_list.append(new_items[2])
                            coref_list.append(new_items[3].replace('-', 'O'))
        if file != '.DS_Store':
            file2 = file.rstrip('conll')
            file2 = file2 + 'csv'
            filename = file2.rstrip('.csv')
            with open(directory2+file2, encoding='utf-8') as file:
                ner_list = []
                b_token_list = []
                text = file.readlines()
                for line in text:
                    b_line = line.rsplit('\t',1)
                    ner_list.append(b_line[-1].strip('\n'))
                    b_token_list.append(b_line[0])
            header = ['token', 'coref', 'ner']
            a_dict = {'token': a_token_list, 'coref': coref_list, 'ner': ner_list} 
            df = pd.DataFrame(a_dict)
            df.to_csv(f'/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/output_combined/{filename}.tsv', index=True, sep='\t', header=header)
            
align_tokens()


