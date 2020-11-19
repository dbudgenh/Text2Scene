
import xml.etree.ElementTree as ET
import spacy
import pickle

class XMLDocument:
    def __init__(self,filepath=None):
        """ Constructor 
        Args:
            filepath (string): [path to file of XML document]
        """
        if filepath is not None:
            self.filepath = filepath
            self._initModel()
            self._initTree()
            self._initData()
            self._analyzeDocument()

    def _initTree(self):
        """ initialize the tree by parsing the xml document
        """
        #Load xml tree
        self.tree = ET.parse(self.filepath)
    
    def _initData(self):
        """Set the data
        """
        #Get the root of xml file (<SpaceEvalTaskv1.2>)
        self.root = self.tree.getroot()
        #Get the full text (<![CDATA[)
        self.data = self.root[0].text
        #The tags
        self.tags = self.root[1]

    def _initModel(self):
        """Set the nlp to be used
        """
        self.nlp = spacy.load("en_core_web_sm")

    def _analyzeDocument(self):
        self.doc = self.nlp(self.data)

    def extract_PoS(self):
        """Extract all the pos tags

        Returns:
            dict -- The dict containing the PoS as key, and for every PoS a list of values (text)
        """
        #For every PoS tag, a list of values will be saved
        token_pos = {}
    
        #key -> PoS-tag, value -> list of tokens
        #E.G {'NOUN':['David','Leonidas'],'Verb':['walk']}
        for token in self.doc:
            token_pos.setdefault(token.pos_,[]).append(token.text)
        return token_pos

    def extract_tags(self):
        """Returns a dict contains the information of all tags

        Returns:
            dict: Key -> tag    value -> list of dicts
        """
        #For every tag, a list of dicts will be saved
        tag_values = {}
        
        for child in self.tags:
            tag_values.setdefault(child.tag,[]).append(child.attrib) 
        return tag_values
    
    def extract_sentences(self):
        """Returns the every sentence as a list

        Returns:
            list: every sentence in a document
        """
        sentences = [sent.string.strip() for sent in self.doc.sents]
        return sentences

    def extract_sentences_length(self):
        """Returns the length of every sentence as a list

        Returns:
            list: the length of every sentence
        """
        sentences = self.extract_sentences()
        sentence_length = [len(sentence.split()) for sentence in sentences]
        return sentence_length

    #Save the data (for now saves only the tree)
    def save(self,path):
        if not path.endswith('.pickle'):
            path += '.pickle'
        
        with open(path,'wb') as f:
            pickle.dump(self.tree,f)

    @staticmethod    
    def load(path):
        if not path.endswith('.pickle'):
            path += '.pickle'
        xml_doc = XMLDocument()
        #Read the xmltree from file
        with open(path,'rb') as f:
            xml_doc.tree = pickle.load(f)
        #init default models
        xml_doc._initModel()
        #init data
        xml_doc._initData()
        #analyze document
        xml_doc._analyzeDocument()
        return xml_doc
    

