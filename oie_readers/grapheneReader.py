import re, math
from oie_readers.oieReader import OieReader
from oie_readers.extraction import Extraction

class GrapheneReader(OieReader):
    
    def __init__(self):
        self.name = 'Graphene'
    
    def calc_confidence(self, text):
        return 1./(0.005*len(text)+1)

    def read(self, fn):
        d = {}

        with open(fn) as fin:
            for line in fin:
                line = line.strip('\n')

                data = line.strip().split('\t')
                if len(data) < 5:
                    continue

                arg2 = ''
                context_args = []
                if len(data) == 5:
                    text, identifier, context_layer, arg1, pred = data[:5]
                else:
                    text, identifier, context_layer, arg1, pred, arg2 = data[:6]
                    context_args = data[6:]
                context_layer = int(context_layer)
                confidence = self.calc_confidence(text)

                simple_contexts = []
                linked_contexts = []
                separator = '\|\|'
                for c in context_args:
                    sm = re.match('^\W*S:(?P<class>\w+)\((?P<text>.*?)\)\W*$', c)
                    lm = re.match('^\W*L:(?P<class>\w+)\((?P<arg1>.*?)' + separator + '(?P<pred>.*?)' + separator + '(?P<arg2>.*?)\)\W*$', c)
                    if bool(sm):
                        simple_contexts.append((sm.group('class'), sm.group('text')))
                    if bool(lm):
                        linked_contexts.append((lm.group('class'), lm.group('arg1'), lm.group('pred'), lm.group('arg2')))

                # create extraction
                curExtraction = Extraction(pred = pred, sent = text, confidence = float(confidence))
                curExtraction.addArg(arg1)
                curExtraction.addArg(arg2)

                for cl, t in simple_contexts:
                    curExtraction.addArg(t)

                for cl, a1, p, a2 in linked_contexts:
                    curExtraction.addArg(' '.join([a1, p, a2]))

                
                add = True

                # is there already an extraction for the sentence that has the same relation?
                if text in d:
                    for i in range(len(d[text])):
                        if d[text][i].pred == curExtraction.pred:
                            add = False
                            for a in curExtraction.args:
                                d[text][i].addArg(a)
                            break

                if add:
                    d[text] = d.get(text, []) + [curExtraction]

        self.oie = d
