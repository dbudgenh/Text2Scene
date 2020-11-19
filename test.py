import matplotlib.pyplot as plt
from XMLDocument import XMLDocument
from functools import reduce
from utils import concatenate_dicts
import numpy as np

#Enter the paths to the xml documents.
paths = ['Traning\\CP\\46_N_22_E.xml','Traning\\RFC\\Honduras.xml']
#For every document, store the information in a list
complete_PoS = [] #PoS:[Token] [{'NOUN':['David'],'VERB':['attack','do']},{'NOUN':['Leo']}]
complete_tags = [] #Tag:{attrib:value}
complete_sentences = [] #[Words]
complete_sentences_length = [] #[length of sentence]

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

    #For every xml file, add them to the list
    complete_PoS.append(pos_dict)
    complete_tags.append(tags_dict)
    complete_sentences.append(sentences)
    complete_sentences_length.append(sentences_length)
    

#Aufgabe 2.3.1
complete_dict_pos = reduce(lambda x,y: concatenate_dicts(x,y),complete_PoS)
for key in complete_dict_pos:
    print(f"Der PoS {key} kommt {len(complete_dict_pos[key])} Mal vor")
print("-----------------------------------------------------------------")

#Aufgabe 2.3.2
complete_dict_tags = reduce(lambda x,y: concatenate_dicts(x,y),complete_tags)
for tag in complete_dict_tags:
    print(f"{tag} kommt {len(complete_dict_tags[tag])} Mal vor")
print("-----------------------------------------------------------------")

#Aufgabe 2.3.3
qslink_dict = {} #dict for every qlink type
for qslink in complete_dict_tags['QSLINK']:
    qslink_dict.setdefault(qslink['relType'],[]).append(1)

#print every qlink, and their occurences
for qslink_type in qslink_dict:
    print(f"Der QSLINK {qslink_type} kommt {len(qslink_dict[qslink_type])} Mal vor")

#Aufgabe 2.3.4
#Flatten 2d list to 1d (could also use numpy..)
complete_list_sentence_length = reduce(lambda x,y: x+y,complete_sentences_length)
plt.hist(complete_list_sentence_length,bins=np.arange(0,max(complete_list_sentence_length))-0.5)
plt.xticks(range(0,max(complete_list_sentence_length)+1))
plt.yticks(range(0,max(np.bincount(complete_list_sentence_length)+1)))
plt.title('Satzlänge und deren Häufigkeit')
plt.ylabel('Häufigkeit')
plt.xlabel('Satzlänge (in Wörter)')
plt.tight_layout()
plt.show()
print("-----------------------------------------------------------------")

#Aufgabe 2.3.5
#create a list of tuples for each qslink,trigger pair
qslink_trigger_pairs = []
for qslink in complete_dict_tags['QSLINK']:
    qslink_trigger_pairs.append((qslink['id'],qslink['trigger']))

#create a list of tuples for each oslink,trigger pair
olink_trigger_pairs = []
for olink in complete_dict_tags['OLINK']:
    olink_trigger_pairs.append((olink['id'],olink['trigger']))

#Print out qslink pairs
for pair in qslink_trigger_pairs:
    print(f"QSLINK mit id {pair[0]} wurde durch id {pair[1]} getriggert")
print("-----------------------------------------------------------------")

#Print out olink pairs
for pair in olink_trigger_pairs:
    print(f"OLINK mit id {pair[0]} wurde durch id {pair[1]} getriggert")
print("-----------------------------------------------------------------")

#Aufgabe 2.3.6
motion_dict = {}
for motion in complete_dict_tags['MOTION']:
    motion_dict.setdefault(motion['motion_class'],[]).append(1)
#sort ascending by most occured verb
sorted_motion_list = sorted(motion_dict.items(), key = lambda e: len(e[1]))

#Read the top 5 verbs and their occurence
for pair in list(reversed(sorted_motion_list))[:5]:
    print(f"Das Movement-Verb {pair[0]} kommt genau {len(pair[1])} Mal vor.")

