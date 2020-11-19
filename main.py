import xml.etree.ElementTree as ET
import os
import spacy

#path = 'Traning\\CP\\46_N_22_E.xml'
paths = ['Traning\\CP\\46_N_22_E.xml','Traning\\RFC\\Amazon.xml']
list_pos_token = []
list_tag_values = []

def concatenate_dicts(d0,d1):
    result = {key: value + d1.get(key,[]) for key, value in d0.items()}
    return result
#For every file, extract the information
for path in paths:
    #Load xml tree
    tree = ET.parse(path)
    #Get the root of xml file (<SpaceEvalTaskv1.2>)
    root = tree.getroot()
    #This contains the actual data (<TEXT>)
    text = root[0]

    #Contains the tags
    tags = root[1]
    #Store the data
    cdata = text.text

    #Load nlp model
    nlp = spacy.load("en_core_web_sm")
    #Analyze the data with our nlp model
    doc = nlp(cdata)

    #For every PoS tag, a list of values will be saved
    token_pos = {}

    #key -> PoS-tag, value -> list of tokens
    for token in doc:
        token_pos.setdefault(token.pos_,[]).append(token.text)
    #key -> tag, value -> dict of attributes
    tag_values = {}
    for child in tags:
        tag_values.setdefault(child.tag,[]).append(child.attrib)


    sentences = [sent.string.strip() for sent in doc.sents]
    sentence_length = [len(sentence.split()) for sentence in sentences]

    #Aufgabe 2.3.1
    for key in token_pos:
        print(f"Der PoS {key} enthält {len(token_pos[key])} Einträge")
    print("-----------------------------------------------------------------")

    #Aufgabe 2.3.2
    for tag in tag_values:
        print(f"Der tag {tag} enthält {len(tag_values[tag])} Einträge")
    print("-----------------------------------------------------------------")

    #Aufgabe 2.3.3
    qslink_occurence = {}
    for qslink in tag_values['QSLINK']:
        qslink_occurence.setdefault(qslink['relType'],[]).append(1)

    for qslink in qslink_occurence:
        print(f"Der QSLINK {qslink} kommt {len(qslink_occurence[qslink])} mal vor")
    print("-----------------------------------------------------------------")

    #Aufgabe 2.3.4
    print(sentence_length)
