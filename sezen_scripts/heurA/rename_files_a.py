file_tuples = [('File8','tokenized_tb_NL.IMRO.0439.BPWMW2011-on01_3_1_1'),
('File13','tokenized_Bijlage-204-3A-20Besluit-20afwijzing-20handhavingsverzoek'),
('File10','Beantwoording_Brandbrief_Stichting_Varkens_in_Nood'),
('File12','tokenized_2018-02-06-20Brief-20college2006-02-2018-20betr'),
('File1','annotated_bijlage-4'),
('File9','tokenized_b_NL.IMRO.9926.IP1411-0001_tb11'),
('File2','annotated_PDO-1048429'),
('File7','tokenized_Verslag_openbare_commissie_Mens_en_Samenleving,_2021-09-30'),
('File6','tokenized_tb_NL.IMRO.0294.BP1001KOgroenlos63-OW01_2'),
('File3', 'annotated_afschrift-van-brief-aan-de-veteranenombudsman-over-noodopvang-veteranen'),
('File15','tokenized_ah-tk-20212022-2930'),
('File14','tokenized_tb_NL.IMRO.0294.BP1001KOgroenlos63-OW01_2_1'),
('File11',"tokenized_Brief20aan20ministers20Ollongren20en20Van20't20Wout20inz20wetsvoorstel2020Wijziging20Tijdelijke20Wet20Groningen"),
('File5','tokenized_tb_NL.IMRO.0439.BPWMW2011-on01_3_1'),
('File4', 'annotated_13e_raadsvergadering_15_september_2022')]

import os
import shutil

# this file can be used to change the names of the files, in order to make the MUC-tables more readable. 

old_directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/gold_model_combined_heuristics_a/'
new_directory = '/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/renamed_gold_model_combined_heuristics_a/'
for new_name, current_name in file_tuples:
    old_file = os.path.join(old_directory, current_name+'.json.tsv')
    new_file = os.path.join(new_directory, new_name+ '.json.tsv')
    if os.path.exists(old_file):
        shutil.copyfile(old_file, new_file)
    else:
        print(old_file, new_file)





