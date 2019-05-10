from oie_readers.oieReader import OieReader
from oie_readers.extraction import Extraction

class ReVerbReader2(OieReader):
    
    def __init__(self):
        self.name = 'ReVerb2'
    
    def read(self, fn):
        d = {}
        with open(fn) as fin:
            for line in fin:
                data = line.strip().split('\t')
                text, confidence, arg1, rel, arg2 = data[0:5]
                
                curExtraction = Extraction(pred = rel, sent = text, confidence = float(confidence))
                curExtraction.addArg(arg1)
                curExtraction.addArg(arg2)
                d[text] = d.get(text, []) + [curExtraction]
        self.oie = d   


