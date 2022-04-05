import spacy
import sys
import argparse
import networkx as nx
from spacy import lang

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
            source = t
            target = t.head.text
            dep_label = t.dep_
            
            self.G.add_edge(source, target, label=dep_label)
        
        return self.G



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", help="The input file from which the graph will be created")
    parser.add_argument("--lan", choice = possible_langs, help="The language tag for the input file")
    parser.add_argument("--output", help="The output file for the final graph", default="output")
    parser.add_argument("--format", choice = possible_formats, help="The format for the output file", default="graphml")

    args = parser.parse_args()

    language = args.lang
    text = open(args.input).read()
    output_filename = args.output
    format_output = args.format

    nlp_name = spacy_models[language]
    
    nlp = spacy.load(nlp_name)

    network = DNetwork(text, nlp)
    graph = network.getGraph()
    
    match format_output:
        case 'graphml': nx.write_graphml(graph, '{}.graphml'.format(output_filename))
        case 'pickle': nx.write_gpickle(graph, '{}.pickle'.format(output_filename))
