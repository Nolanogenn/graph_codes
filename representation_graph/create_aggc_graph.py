import json
import spacy
import sys
import pprint
import pandas as pd

filename = sys.argv[1]

nlp = spacy.load('en_core_web_sm')

sentences = f"{filename}_clean_format.txt"
relations = f"{filename}_relations.tsv"
entities = f"{filename}_entities.tsv"


sentences_file = open(sentences).readlines()
df_entities = pd.read_csv(entities, sep='\t')
df_relations = pd.read_csv(relations,names=['label', 'e1', 'e2'], sep='\t')

final_file = []

for i, s in enumerate(sentences_file):
    sentence_id = i
    doc = nlp(s)
    tokens = []
    heads = []
    pos = []
    deprel = []


    relation_row = df_relations.iloc[i]
    relation_label = relation_row['label']

    entities = df_entities.loc[df_entities['in_sentence']==i]
   
    entities_surface_form = [x['surface_form'] for i,x in entities.iterrows()]
    if type(entities_surface_form[0]) == str and type(entities_surface_form[1]) == str:
        #we split the entities in order to account for mwes
        subj = entities_surface_form[0].split()
        obj = entities_surface_form[1].split()

        subj_start = 0
        subj_end = 0

        obj_start = 0
        obj_end = 0

        for token in doc:
            if token.text == subj[0]:
                subj_start = token.i
            elif token.text == subj[-1]:
                subj_end = token.i
            elif token.text == obj[0]:
                obj_start = token.i
            elif token.text == obj[-1]:
                obj_end = token.i

            tokens.append(token.text)
            deprel.append(token.dep_)
            heads.append(token.head.i)
            pos.append(token.pos_)
        
        jsonLine = {
                "id" : sentence_id,
                "relation" : relation_label,
                "token" : tokens,
                "pos" : pos,
                "head" : heads,
                "deprel" : deprel,
                "subjstart" : subj_start,
                "subjend" : subj_end,
                "objstart" : obj_start,
                "objend" : obj_end
                }
        final_file.append(jsonLine)

outputfile_name = f'aggcn/{filename}.json'
with open(outputfile_name, 'w+') as f:
    json.dump(final_file, f)

