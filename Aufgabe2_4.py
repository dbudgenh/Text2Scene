from XMLDocument import XMLDocument
import networkx as nx
import matplotlib.pyplot as plt


#Open Log_2020-11-19.pdf to see the output of all exercises.
def main():
    paths = ['Traning\\RFC\\Bicycles.xml','Traning\\ANC\\WhereToMadrid\\Highlights_of_the_Prado_Museum.xml']
    file_name = ['Bicycles.png','Highlights_of_the_Prado_Museum.png']

    for idx,path in enumerate(paths):
        #Load the xml file
        xml_doc = XMLDocument(path)
        #Get the tags
        tags_dict = xml_doc.extract_tags()
        nodes = []
        labels = {}
        
        #Create a node for every entity
        for places in tags_dict['PLACE']:
            #Store the id of the node
            nodes.append(places['id'])
            labels[places['id']] = places['text'] 
        for spatial_entity in tags_dict['SPATIAL_ENTITY']:
            nodes.append(spatial_entity['id'])
            labels[spatial_entity['id']] = spatial_entity['text'] 
        for path in tags_dict['PATH']:
            nodes.append(path['id'])
            #Places sollen ja ausgelassen werden
            #labels[path['id']] = path['text']

        #Create the graph
        G = nx.Graph()
        G.add_nodes_from(nodes)

        for metalink in tags_dict['METALINK']:
            #Wenn es einen METALINK zwischen entitäten gibt, merge die Knoten
            if metalink['fromID'] in G.nodes() and metalink['toID'] in G.nodes():
                G = nx.contracted_nodes(G,metalink['fromID'],metalink['toID'])
        
        #Save colors for every entity
        colors = []
        nodes_in_graph = G.nodes()
        for node in nodes_in_graph:
            #place -> blue
            if node.startswith('pl'):
                colors.append('blue')
                continue
            #Spatial entity -> red
            if node.startswith('se'):
                colors.append('red')
                continue
            #path -> green
            if node.startswith("p"):
                colors.append('green')

        #List of nodes that got removed after merging
        merged_nodes = list(set(labels.keys()) - set(nodes_in_graph))

        #Remove the nodes from the labels
        for node in merged_nodes:
            if node in labels:
                del labels[node]

        #Store the edges
        edge_labels_qslink = {}
        edge_labels_olink = {}

        #Create an edge for every qslink
        #Werden die knoten durch das mergen nicht gelöscht? Hat das Einfluss auf die qslinks/olinks??
        for qslink in tags_dict['QSLINK']:
            if qslink['fromID'] in nodes_in_graph and qslink['toID'] in nodes_in_graph:
                edge_labels_qslink[(qslink['fromID'],qslink['toID'])] = qslink['relType']

        #Create an edge for every olink
        for olink in tags_dict['OLINK']:
            if olink['fromID'] in nodes_in_graph and olink['toID'] in nodes_in_graph:
                edge_labels_olink[(olink['fromID'],olink['toID'])] = olink['relType']

        plt.figure(figsize=(15,10)) 
        #Add draw the edges
        G.add_edges_from(list(edge_labels_qslink.keys()))
        #change the layout for better views..
        pos = nx.circular_layout(G)
        #Draw the nodes
        nx.draw(G,pos=pos,node_color = colors,labels = labels,with_labels=True, font_weight='bold',font_size=12)
        #Color the edges: qslink ->blue
        nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels_qslink,font_color='blue', font_size=12)
        #olink -> red
        nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels_olink,font_color='red', font_size=12)
        plt.savefig(file_name[idx])
        plt.show()
if __name__ == '__main__':
    main()