# sezen_tuvay_pseudonymisation_in_dutch
A framework for pseudonymisation in Dutch
<br>
This repository belongs to the Master's Thesis Project "Towards a Dutch pseudonymisation Framework" by Sezen, supervised by Isa Maks. The project was carried out in collaboration with the company Bolesian. <br>
<br>
This project investigates the task of Pseudonymisation in Dutch and builds a framework to achieve this task. Annotation Guidelines are established to provide instructions
on consistent Pseudonymisation. A Dutch pseudonymisation dataset has been constructed. An existing Coreference Resolution model and an existing Named Entity Recognition tagger are integrated and new Heuristics are built to achieve the task. Heuristics A being a straightforward way of pseudonymisation, where persons are identified by the NER-tagger and its references are identified by the Coreference Resolution model. Heuristics B is a more advanced way, where the pronouns are used to find the persons, and the Coreference Resolution model identifies the references. These two Heuristics are tested and evaluated using the MUC evaluation metric. The findings indicate that Heuristics B is better at identifying coreference chains compared to Heuristics A. However, both Heuristics struggle to find the links between the chains. Although it is evident that personal names, pronouns and forms of address must be pseudonymised, there are still some cases where it is challenging to determine whether pseudonymisation is necessary. The findings also indicate that the end-to-end Coreference Resolution model is not well-suited for this task, since many error patterns which have been ascertained derive from the errors made by the Coreference Resolution model. 

<br>

## README
This project has been developed starting in April 2023. Therefore, some packages and installations might need some older installations. This will all be explained here. 
<br>
This repository is called sezen_tuvay_pseudonymisation_in_dutch and also includes the e2e-Dutch-master repository, as well as sezen_scripts. This latter one includes all scripts for the pseudonymisation using the Coreference Resolution Model and the Flair NER-tagger and is the repository made for this Thesis project. Only files in 'sezen_data' and 'sezen_scripts' are made by me. This README only covers the scripts and datafiles which are created for the pseudonymisation. This means that the entire e2e-Dutch-master repository is only shortly explained, since this can be found in: <br>
https://github.com/Filter-Bubble/e2e-Dutch.<br>
The README.md of the Filter-Bubble/e2e-Dutch repository is included in the e2e-Dutch repository. (in contrast to this README.md) This, since the installation and running of the e2e requires some setup which is explained in that README.md
<br>

## Environment
Install all packages in a virtual environment to ensure all packages will have the correct versions (and not overlapping with other versions in the source). I have used a source environment. <br>

## Requirements
There are three different requirements.txt files in this entire repository. The most important one for my thesis is: sezenrequirements.txt. The packages in here are the following: <br>
tensorflow>=2.0.0<br>
e2e-Dutch==0.4.1<br>
flair==0.12.2<br>
pandas==1.3.5<br>
nltk==3.8.1<br>
numpy==1.21.6<br>

These all need to be installed to be able to run the code for the pseudonymisation. <br>

The longrequirements.txt includes all the requirements within the environment, and when a package is unsuccesfully installed because of version faults, you can check here which version of the packages needs to be installed. Moreover, when the packages of sezenrequirements.txt are installed, packages in this longrequirements.txt are also installed. However, only the sezenrequirements.txt needs to be installed. The last requirements.txt file is of the e2e-Dutch-master repository (used later on as: pip install -r requirements.txt). <br>
<br>

## Project Overview
There are a few different steps taken in this project. All directories are in e2e-Dutch-master/scripta/sezen_scripts.  All datafolders are explained after each step in bold, as well as in the end. <br>
Step 0: Capturing the metadata <br>
Step 1:  Running the Coreference Resolution Model per file <br>
Step 2:  Running the NER-model per file <br>
Step 3:  Aligning the output of these models per file <br>
Step 4:  Running HeurA <br>
Step 5:  Running HeurB <br>
Step 6:  Calculating the Metrics <br>
<br>
The files and scripts that belong to these steps and how to run them are explained here. Most functions are explained in the files as comments.<br>
<br>
## Step 0: Capturing the metadata
In the directory get_meta, there are two files: csv_to_text.py, and get_meta.py. csv_to_text.py has to be called first. Then, the output of this file is used to get metadata of all the files in the directory. The information that can be gathered from this metadata is useful for the evaluation later in on the project. Information about the sentences, tokens, words, references and persons is gathered using this get_meta.py file. <br>
<br>
**not_annotated_text**: this is the folder where the not annotated text is in, and is used for metadata information <br>
**annotated-data**: this is the folder where the annotated-data is in and is in csv-format. The annotations have been performed in Google Spreadsheets and then downloaded as csv0files. In this folder these annotations exist.  <br>

## Step 1: Running the Coreference Resolution Model per file <br>
To run the e2e-Dutch-master Coreference Resolution model per file in the repository, the e2e coref model in Dutch needs to be installed. This model can be found in the following github link (and also in this entire repository): <br>
https://github.com/Filter-Bubble/e2e-Dutch <br>
First you need to follow the instructions given in the README.md file (not the 'sezenREADME.md') <br>
run: <br>
pip install -r requirements.txt <br>
pip install tensorflow <br>
pip install e2e-Dutch <br>

To run the Coreference Resolution model on a file, the following command needs to be run: <br>

python -m e2edutch.predict -o sezen_data/output/annotated_13e_raadsvergadering_15_september_2022.conll -f conll sezen_data/not_annotated_text/annotated_13e_raadsvergadering_15_september_2022.txt

<br>
And replace sezen_data/output/ with the folder that the conll-file is in, and replace sezen_data/not_annotated_text/ with the folder you want the output to be. The filename annotated_13e_raadsvergadering_15_september_2022 needs to be replaced when you want to run the Coref-model on another file. <br>

**output copy:** this is the folder where the output of Step 1, running this in terminal (change file names): python -m e2edutch.predict -o  <br>
sezen_data/output/annotated_13e_raadsvergadering_15_september_2022.conll -f conll sezen_data/not_annotated_text/annotated_13e_raadsvergadering_15_september_2022.txt     --> needs to be. <br> 

## Step 2:  Running the NER-model per file
In sezen_scripts, a folder called 'NER' includes a file named: flair_on_conll.py. When this is called, all files are NER-tagged by Flair. It is important to mention that Flair needs Python 3.8 or higher. Therefore, to not change the versions and installments for the Coreference Model, it is easier to make a new directory and a new NER-script, and put sezen_data/output in this new directory and copy-paste the flair_on_conll.py to this new script. This, since the Coreference Model has been set up in python 3.7<br>

**output_ner_new**: this is the folder where the output of flair_on_conll.py needs to be <br>

## Step 3:  Aligning the output of these models per file
In sezen_scripts a folder called 'COREF+NER', a script called ''combine_ner_coref.py" is included. When this is called, all files with a NER-tag (output of Step 2, sezen_data/output_ner_new) and all files with a Coreference Resolution tag (output of Step 1, sezen_data/output copy) are combined. The output of this can be found in sezen_data/output_combined. <br>

**output_combined**: this is the folder where the output of combine_ner_coref.py needs to be <br>

## Step 4:  Running HeurA:
To run HeurA, first the script a_heuristics.py needs to be run. This script takes all datafiles and runs heuristics A on these files. Then, final_alignment_a.py needs to be run, which takes the output of a_heuristics.py and the annotated datafiles (the gold set) and combines these by putting both in a csv-file, where the first column is the token, the second column is the gold output (annotations) and the third column is the model output. <br>

**final_tokenized**: this is the folder where the output of the manual retokenization needs to be.This is needed for Step 4 and Step 5 (final_alignment_a.py and final_alignment_b.py). Since  the e2e model retokenizes the files in a very inconsistent way, this needed to be done manually. This has been explained in the Thesis. The old tokens are shifted to confirm the new tokenization (which is the same tokenization as the output of the e2e).   <br>
**pseudo-a**: this is the folder where the output of heurA.py needs to be <br>
**gold_model_combined_heuristics_a**: this is the folder where the output of final_alignment_a.py needs to be <br>

## Step 5:  Running HeurB:
To run HeurB, first the script b_heuristics.py needs to be run. This script takes all datafiles and runs heuristics B on these files. Then, final_alignment_b.py needs to be run, which takes the output of b_heuristics.py and the annotated datafiles (the gold set) and combines these by putting both in a csv-file, where the first column is the token, the second column is the gold output (annotations) and the third column is the model output. <br>

**final_tokenized**: this is the folder where the output of the manual retokenization needs to be.This is needed for Step 4 and Step 5 (final_alignment_a.py and final_alignment_b.py). Since  the e2e model retokenizes the files in a very inconsistent way, this needed to be done manually. This has been explained in the Thesis. The old tokens are shifted to confirm the new tokenization (which is the same tokenization as the output of the e2e).  <br>
**pseudo-b**: this is the folder where the output of heurB.py needs to be <br>
**gold_model_combined_heuristics_b**: this is the folder where the output of final_alignment_b.py needs to be <br>


## Step 6:  Calculating the Metrics:
rename_files_A.py and rename_files_B.py can be used to rename the files to File1, File2, etc. for readability purposes. ERR_A.py and LenERR_A.py are the python files which give the MUC-categories per file for HeurA. ERR_B.py and LenERR_B.py are the python files which give the MUC-categories per file for HeurB. <br>
ERR_A and ERR_B are used to calculate the ERR scores, and LenERR_A and LenERR_B are used to calculate the lenient ERR-scores. <br>

**renamed_gold_model_combined_heuristics_a**: this is the folder where the output of rename_files_a.py needs to be<br>
**renamed_gold_model_combined_heuristics_b**: this is the folder where the output of rename_files_b.py needs to be<br>
**muc_tables**: this is the folder where the output of LenERR_A.py ERR_A.py, LenERR_B.py and ERR_B.py needs to be<br>


**DATAFOLDER: all data is in these kinds of folders: "/Users/sezentuvay/Desktop/ALLES_voor_Thesis/e2e-Dutch-master/sezen_data/". however, when you want to reproduce this project, put all data folders where you want them.** <br>
**not_annotated_text**: this is the folder where the not annotated text is in, and is used for metadata information
**annotated-data**: this is the folder where the annotated-data is in and is in csv-format. The annotations have been performed in Google Spreadsheets and then downloaded as csv0files. In this folder these annotations exist. <br>
**output copy:** this is the folder where the output of Step 1, running this in terminal (change file names): python -m e2edutch.predict -o sezen_data/output/annotated_13e_raadsvergadering_15_september_2022.conll -f conll sezen_data/not_annotated_text/annotated_13e_raadsvergadering_15_september_2022.txt     --> needs to be. <br>
**output_ner_new**: this is the folder where the output of flair_on_conll.py needs to be <br>
**output_combined**: this is the folder where the output of combine_ner_coref.py needs to be <br>
**final_tokenized**: this is the folder where the output of the manual retokenization needs to be.This is needed for Step 4 and Step 5 (final_alignment_a.py and final_alignment_b.py). <br>Since  the e2e model retokenizes the files in a very inconsistent way, this needed to be done manually. This has been explained in the Thesis. The old tokens are shifted to confirm the new tokenization (which is the same tokenization as the output of the e2e).  <br>
**pseudo-a**: this is the folder where the output of heurA.py needs to be <br>
**pseudo-b**: this is the folder where the output of heurB.py needs to be <br>
**gold_model_combined_heuristics_a**: this is the folder where the output of final_alignment_a.py needs to be  <br>
**gold_model_combined_heuristics_b**: this is the folder where the output of final_alignment_b.py needs to be  <br>
**renamed_gold_model_combined_heuristics_a**: this is the folder where the output of rename_files_a.py needs to be <br>
**renamed_gold_model_combined_heuristics_b**: this is the folder where the output of rename_files_b.py needs to be <br>
**muc_tables**: this is the folder where the output of LenERR_A.py ERR_A.py, LenERR_B.py and ERR_B.py needs to be <br>



