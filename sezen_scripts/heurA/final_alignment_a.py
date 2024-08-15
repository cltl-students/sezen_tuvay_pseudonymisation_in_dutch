import os
import json
import pandas as pd
directory = "/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/final_tokenized/"
directory2 = "/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/pseudo-a/"
def final_alignment():
    """
    In this function, the pseudonymised data and the gold set (from the annotations) are taken and put together in one file
    This, to be able to evaluate the model output. 
    """
    for file in os.listdir(directory):
        if file != '.DS_Store':
            with open(directory+file) as f:
                text = f.read()
                gold_token_list = []
                gold_pseudo_list = []
                a_line = text.split('\n')
                for items in a_line:
                    token = items.split('\t')[0]
                    gold_token_list.append(token)
                    gold_pseudo = items.split('\t')[-1]
                    gold_pseudo = gold_pseudo.replace('-', '_')
                    gold_pseudo_list.append([gold_pseudo])
             
        if file != '.DS_Store':
            file = file.rstrip('.tsv')
            filename = file+'.json'
            with open(directory2+filename) as file2:
                a_file = json.load(file2)
                model_token_list = []
                model_pseudo_list = []
                for item in a_file:
                    model_token_list.append(item['token'])
                    model_pseudo_list.append(item['pseudo'])
        header = ['token', 'gold', 'model']
        a_dict = {'token': gold_token_list, 'gold': gold_pseudo_list, 'model': model_pseudo_list} 
        
        df = pd.DataFrame(a_dict)
        df.to_csv(f'/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/gold_model_combined_heuristics_a/{filename}.tsv', index=True, sep='\t', header=header)
      

final_alignment()
