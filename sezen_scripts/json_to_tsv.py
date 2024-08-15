import json
import csv

def json_to_tsv(json_file, tsv_file):
    with open(json_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    with open(tsv_file, 'w', newline='', encoding='utf-8') as outfile:
        tsv_writer = csv.writer(outfile, delimiter='\t')
        tsv_writer.writerow(['token'])
        for entry in data:
            tsv_writer.writerow([entry['token']])

json_file = "/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/pseudonymised-data-a/annotated_13e_raadsvergadering_15_september_2022.json"  # replace with your input JSON file path
tsv_file = '/Users/sezentuvay/Desktop/ALLES voor Thesis/e2e-Dutch-master/sezen_data/OUTPUT.tsv'   
json_to_tsv(json_file, tsv_file)
