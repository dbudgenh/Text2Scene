
import xml.etree.ElementTree as ET
import spacy

class XMLTree:

    def __init__(self,filepath):
        self.filepath = filepath
        self._initModel()
        self._initTree()

    def _initTree(self):
        #Load xml tree
        self.tree = ET.parse(self.filepath)
        #Get the root of xml file (<SpaceEvalTaskv1.2>)
        self.root = self.tree.getroot()
        self.data = self.root[0].text
        self.tags = self.root[1]

    def _initModel(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_PoS(self):
        doc = self.nlp(self.data)