import spacy
import sys
import argparse
import networkx as nx
from spacy import lang
import pandas as pd

possible_formats = ['pickle', 'graphml','tsv']

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
    def __init__(self, text, spacy_model, id_sen):
        self.text = text
        self.spacy_model = spacy_model
        self.id_sen = id_sen
        self.G = nx.DiGraph()

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

            token_id = "{}_{}".format(self.id_sen, source_index)

            target_index = t.head.i
            dep_label = t.dep_
            
            self.G.add_edge(token_id, self.id_sen, label='is_in_sentence')
            
            self.G.add_edge(token_id, "{}_{}".format(self.id_sen, target_index), label=dep_label)

            self.G.add_edge(token_id, source_text.replace('\n', ''), label="has_surface_form")
        
        return self.G, doc



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", help="The input file from which the graph will be created")
    parser.add_argument("--lan", choices=possible_langs, help="The language tag for the input file")
    parser.add_argument("--output", help="The output file for the final graph", default="output")
    parser.add_argument("--format", choices=possible_formats, help="The format for the output file", default="graphml")
    parser.add_argument("--entities", help="A file containing the entities extracted from the input file. While the first column has to be the index of the sentence in which the entity appear, and the second column has to be the entity's surface form (how it appears in the text), the following columns can be wathever kind of information you want. The important thing is that the header defines what kind of information it is", default="None")
    parser.add_argument("--relations", help="A file containaing the relations between the entities extracted from the input file. The accepted format is the following: 'relation\thead\ttail'. Don't include an header. An error will raise if you try to integrate relations without entities", default="None")

    args = parser.parse_args()

    language = args.lan
    doc_full = open(args.input).readlines()
    

    output_filename = args.output
    format_output = args.format

    nlp_name = spacy_models[language]
    
    nlp= spacy.load(nlp_name)
    list_networks = []

    if args.relations != "None":
        assert args.entities != "None"
        df_relations = pd.read_csv(args.relations, delimiter='\t', header=None)

    if args.entities != "None":
        df_entities = pd.read_csv(args.entities, delimiter='\t',header=0)
        column_sentence = df_entities.columns[0]
        column_surface_form = df_entities.columns[1]
        edges = df_entities.columns[1:]

    for enum, text in enumerate(doc_full[:100]):
        print("{}/{}".format(enum,len(doc_full)), end='\r')
        id_sen = int(enum)
        network = DNetwork(text, nlp, id_sen)
        graph, doc = network.getGraph()

        entities = df_entities.loc[df_entities[column_sentence] == id_sen]
        for i, r in entities.iterrows():
            surface_form = r[column_surface_form]
            try:
                tokens_surface_form = surface_form.split()

                if len(tokens_surface_form) == 1:
                    for token in doc:
                        if token.text == tokens_surface_form[0]:
                            graph.add_edge("{}_{}".format(id_sen, token.i), surface_form, label="is_entity")
                else:
                    len_split = len(tokens_surface_form)
                    for num in range(len(doc) - len_split):
                        splice = doc[num:num+len_split]
                        splice_texts = [token.text for token in splice]
                        splice_positions = [token.i for token in splice]

                        if tokens_surface_form == splice_texts:
                            for position in splice_positions:
                                graph.add_edge("{}_{}".format(id_sen, position), surface_form, label='part_of_entity')
                for edge in edges:
                    graph.add_edge(surface_form, r[edge], label=edge)
            except:
                pass

        if args.relations != "None":
            row_relations = df_relations.iloc[enum]
            
            relation_name = row_relations[0]
            head = row_relations[1]
            tail = row_relations[2]
            graph.add_edge(head, tail, label=relation_name)
    
        list_networks.append(graph)
    print("composing the network")
    print("num of networks: ", len(list_networks))
    final_network = nx.compose_all(list_networks)

    print("network composed!")

    if format_output == 'graphml':
        nx.write_graphml(final_network, 'output/{}.graphml'.format(output_filename))
    elif format_output == 'pickle':
        nx.write_gpickle(final_network, 'output/{}.pickle'.format(output_filename))
    elif format_output == 'tsv':
        tsv_file = []
        output_filename_complete = "output/{}".format(output_filename)
        for edge in final_network.edges():
            s = edge[0]
            t = edge[1]
            data = final_network.get_edge_data(s, t)
            relation = data['label']
            tsv_file.append([s, relation, t])

        df = pd.DataFrame(tsv_file)
        df.to_csv(output_filename_complete, header=None, index=False, sep='\t')
    print("done all!")
