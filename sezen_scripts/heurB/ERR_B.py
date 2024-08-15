import pandas as pd
import re
import os
import numpy as np
directory = '/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/renamed_gold_model_combined_heuristics_b/'
all_COR = []
all_PAR = []
all_INC = []
all_MIS = []
all_SPU = []
all_NON = []
all_COMPLETE_INC = []
all_B_INC = []
all_I_INC = []
files = []
pronouns = {'hem', 'haar', 'zijn', 'mijn', 'mij', 'jou', 'jouw', 'ons', 'onze', 'uw', 'zij', 'je', 'ze', 'me', 'we', 'u', 'hen', 'hun', 'hij', 'wij', 'jullie', 'ik'}
etiquette = {
    'mevrouw', 'meneer', 'mevrou', 'mijnheer','vrouw', 'Dhr.', 'mevr.', 'heer', 'mr', 'dhr', 'mr.','advocaat','advocate','ambassadeur','attaché','baron','barones',
    'commissaris', 'consul','doctorandus','gedeputeerde','gezant','gouverneur','graaf','gravin','hoogleraar','ingenieur',
    'inspecteur','jonkheer','jonkvrouw','kandidaat-notaris','kantonrechter','kardinaal','koning','koningin','korpschef',
    'gemeenteraadslid', 'meester','minister','ombudsman','notaris','officier van justitie','burgemeester'
    'president','prins','prinses','generaal','professor','raadsheer','rechter','secretaris-generaal',
    'staatssecretaris','voorzitter','wethouder'}
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
                all_lengths = []
                countertje = 0
                for i in range(len(df)):
                    if re.findall(r'\d+', str(df.loc[i, 'gold'])) != re.findall(r'\d+', str(df.loc[i, 'model'])) and len(df.loc[i, 'model']) > 3 and len(df.loc[i, 'gold']) > 4:
                        INC += 1   
                        #AttributeError: 'float' object has no attribute 'lower'
                        # if df.loc[i, 'token'].lower() == 'hij' and type(df.loc[i, 'token'].lower) != float:
                        #     countertje += 1
                        #     print(countertje)
                    elif str(df.loc[i, 'gold']).startswith("['B") and str(df.loc[i, 'model']).startswith("['I") and (re.findall(r'\d+', str(df.loc[i, 'gold'])) == re.findall(r'\d+', str(df.loc[i, 'model']))): 
                        PAR += 1

                    elif str(df.loc[i, 'gold']).startswith("['I") and str(df.loc[i, 'model']).startswith("['B") and (re.findall(r'\d+', str(df.loc[i, 'gold'])) == re.findall(r'\d+', str(df.loc[i, 'model']))):
                        PAR += 1

                    elif str(df.loc[i, 'gold']) != "['']" and df.loc[i, 'model'] == '[]':
                        MIS += 1

                    elif str(df.loc[i, 'gold']) == "['']" and  df.loc[i, 'model'] != '[]':
                        SPU += 1
                    elif df.loc[i, 'gold'] == df.loc[i, 'model'] and len(df.loc[i, 'model']) > 3 and len(df.loc[i, 'gold']) > 4:
                        COR += 1
                    elif df.loc[i, 'gold'] == "['']" and df.loc[i, 'model'] == '[]':
                        NON += 1
                all_COR.append(COR)
                all_PAR.append(PAR)
                all_INC.append(INC)
                all_MIS.append(MIS)
                all_SPU.append(SPU)
                all_NON.append(NON)
        header = ['files', 'COR', 'PAR', 'INC', 'MIS', 'SPU', 'NON']
        output_dict = {'file': files, 'COR': all_COR, 'PAR': all_PAR, 'INC': all_INC, 'MIS': all_MIS, 'SPU':all_SPU, 'NON':all_NON} 
        df = pd.DataFrame(output_dict).sort_values(by='file', key=lambda col: col.map(natural_sort_key))

        df.to_csv('/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/muc_tables/ERR_B.tsv', index=False, sep='\t', header=header)
        

        