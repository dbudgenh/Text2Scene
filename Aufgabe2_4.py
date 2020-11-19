from XMLDocument import XMLDocument
import networkx as nx
import matplotlib.pyplot as plt

def main():
    paths = ['Traning\\RFC\\Bicycles.xml','Traning\\ANC\\WhereToMadrid\\Highlights_of_the_Prado_Museum.xml']
    for path in paths:
        #Load the xml file
        xml_doc = XMLDocument(path)
        #Get the PoS
        pos_dict = xml_doc.extract_PoS()
        #Get the tags
        tags_dict = xml_doc.extract_tags()
        #Get all the sentences
        sentences = xml_doc.extract_sentences()
        #Get the length of all sentences
        sentences_length = xml_doc.extract_sentences_length()
        #PLACE, SPATIAL_ENTITY
        nodes = []
        color = []

        for places in tags_dict['PLACE']:
            nodes.append((places['id']))
            color.append('red')
        for spatial_entity in tags_dict['SPATIAL_ENTITY']:
            nodes.append((spatial_entity['id']))
            color.append('blue')
        for path in tags_dict['PATH']:
            nodes.append((path['id']))
            color.append('green')

    G = nx.Graph()
    G.add_nodes_from(nodes)
    nx.draw(G, node_color = color,with_labels=True, font_weight='bold')
    plt.show()
if __name__ == '__main__':
    main()