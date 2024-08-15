import pandas as pd
import re
import os
from collections import defaultdict
import numpy as np
directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/renamed_gold_model_combined_heuristics_a/'
all_COR = []
all_PAR = []
all_INC = []
all_MIS = []
all_SPU = []
all_NON = []
all_COMPLETE_INC = []
all_B_INC = []
all_I_INC = []
len_df = []
all_all =[]
files = []


#This code can be used to calculate the MUC-categories for the Lenient ERR. In here, COR is COR2. 


def natural_sort_key(key):
            return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', key)]


for file in os.listdir(directory):
        if file != '.DS_Store':
            files.append(file.rstrip('.json.tsv'))
            with open(directory+file) as f:
                df = pd.read_csv(f, sep='\t')
                COR = 0
                PAR = 0
                INC = 0
                MIS = 0
                SPU = 0
                NON = 0
                PART_COR = 0
                NEW_COR = 0
                all_lengths = 0
                countertje = 0
                dict_in_INC = defaultdict(int)
                for i in range(len(df)):
                    if (re.findall(r'\d+', str(df.loc[i, 'gold'])) != re.findall(r'\d+', str(df.loc[i, 'model']))) and df.loc[i, 'model'] != '[]' and df.loc[i, 'gold'] != "['']":
                        numeric_value = re.findall(r'\d+', str(df.loc[i, 'model']))
                        dict_in_INC[int(numeric_value[0])] += 1
                    elif str(df.loc[i, 'gold']).startswith("['B") and str(df.loc[i, 'model']).startswith("['I") and (re.findall(r'\d+', str(df.loc[i, 'gold'])) == re.findall(r'\d+', str(df.loc[i, 'model']))): 
                        PAR += 1
                    elif str(df.loc[i, 'gold']).startswith("['I") and str(df.loc[i, 'model']).startswith("['B") and (re.findall(r'\d+', str(df.loc[i, 'gold'])) == re.findall(r'\d+', str(df.loc[i, 'model']))):
                        PAR += 1
                    elif str(df.loc[i, 'gold']) != "['']" and df.loc[i, 'model'] == '[]':
                        MIS += 1
                    elif str(df.loc[i, 'gold']) == "['']" and  df.loc[i, 'model'] != '[]':
                        SPU += 1
                    elif df.loc[i, 'gold'] == df.loc[i, 'model'] and len(df.loc[i, 'model']) > 3:# and len(df.loc[i, 'gold']) > 4:
                        COR += 1
                    elif df.loc[i, 'gold'] == "['']" and df.loc[i, 'model'] == '[]':
                        NON += 1
                for key, value in dict_in_INC.items(): 
                    if value > 1: #when the same label is used more than once, so at least 2 times: PAR_COR is assigned +value. 
                        PART_COR += value
                    elif value == 1:
                        INC += 1  
                NEW_COR = COR + PART_COR
                all_COR.append(NEW_COR)
                all_PAR.append(PAR)
                all_INC.append(INC)
                all_MIS.append(MIS)
                all_SPU.append(SPU)
                all_NON.append(NON)
        header = ['files', 'COR', 'PAR', 'INC', 'MIS', 'SPU', 'NON']
        output_dict = {'file': files, 'COR': all_COR, 'PAR': all_PAR, 'INC': all_INC, 'MIS': all_MIS, 'SPU':all_SPU, 'NON':all_NON} 
        df = pd.DataFrame(output_dict).sort_values(by='file', key=lambda col: col.map(natural_sort_key))
        df.to_csv('/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/muc_tables/LenERR_A_2.tsv', index=False, sep='\t', header=header)

                    

                    