import spacy
import sys
import argparse
import networkx as nx
from spacy import lang
import pandas as pd

possible_formats = ['pickle', 'graphml']

spacy_models = {
    "en" : "en_core_web_sm",
    "ca" : "ca_core_news_sm",
    "zh" : "zh_core_web_sm",
    "da" : "da_core_news_sm",
    "nl" : "nl_core_news_sm",
    "fr" : "fr_core_news_sm",
    "de" : "de_core_news_sm",
    "el" : "el_core_news_sm",
    "it" : "it_core_news_sm",
    "ja" : "ja_core_news_sm",
    "lt" : "lt_core_news_sm",
    "mk" : "mk_core_news_sm",
    "pl" : "pl_core_news_sm",
    "pt" : "pt_core_news_sm",
    "ro" : "ro_core_news_sm",
    "ru" : "ru_core_news_sm",
    "es" : "es_core_news_sm"
        }

possible_langs = [k for k in spacy_models]

class DNetwork(object):
    def __init__(self, text, spacy_model):
        self.text = text
        self.spacy_model = spacy_model
        self.G = nx.Graph()

    def create_nlp_model(self, text):
        return self.spacy_model(self.text)

    def tokenize(self):
        doc = self.create_nlp_model(self.text)
        return doc

    def getGraph(self):
        doc = self.tokenize()
        
        for t in doc:
            source_text = t.text
            source_index = t.i

            target_index = t.head.i
            dep_label = t.dep_
            
            self.G.add_edge(source_index, target_index, label=dep_label)
            self.G.add_edge(source_index, source_text, label="has_surface_form")
        
        return self.G, doc



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", help="The input file from which the graph will be created")
    parser.add_argument("--lan", choices=possible_langs, help="The language tag for the input file")
    parser.add_argument("--output", help="The output file for the final graph", default="output")
    parser.add_argument("--format", choices=possible_formats, help="The format for the output file", default="graphml")
    parser.add_argument("--entities", help="A file containing the entities extracted from the input file. While the first column has to be the entity's surface form (how it appears in the text), the following columns can be wathever kind of information you want. The important thing is that the header defines what kind of information it is", default="None")

    args = parser.parse_args()

    language = args.lan
    text = open(args.input).read()
    output_filename = args.output
    format_output = args.format

    nlp_name = spacy_models[language]
    
    nlp= spacy.load(nlp_name)

    network = DNetwork(text, nlp)
    graph, doc = network.getGraph()

    if args.entities != "None":
        df = pd.read_csv(args.entities, delimiter='\t',header=0, index_col=0)
        
        column_surface_form = df.columns[0]
        edges = df.columns[1:]

        for i, r in df.iterrows():
            surface_form = r[column_surface_form]
            tokens_surface_form = surface_form.split()
            
            if len(tokens_surface_form) == 1:
                for token in doc:
                    if token == tokens_surface_form[0]:
                        graph.add_edge(token.i, surface_form, label="is_entity")
            else:
                len_split = len(tokens_surface_form)
                for num in range(len(doc) - len_split):
                    splice = doc[num:num+len_split]
                    splice_texts = [token.text for token in splice]
                    splice_positions = [token.i for token in splice]

                    if tokens_surface_form == splice_texts:
                        for position in splice_positions:
                            graph.add_edge(position, surface_form, label='part_of_entity')
            for edge in edges:
                print(surface_form, r[edge], edge)
                graph.add_edge(surface_form, r[edge], label=edge)

    
    if format_output == 'graphml':
        nx.write_graphml(graph, '{}.graphml'.format(output_filename))
    elif format_output == 'pickle':
        nx.write_gpickle(graph, '{}.pickle'.format(output_filename))
