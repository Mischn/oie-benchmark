''' 
Usage:
   benchmark --gold=GOLD_OIE --out=OUTPUT_FILE (--stanford=STANFORD_OIE | --ollie=OLLIE_OIE |--reverb=REVERB_OIE |--reverb2=REVERB2_OIE | --clausie=CLAUSIE_OIE | --openiefour=OPENIEFOUR_OIE | --props=PROPS_OIE | --graphene=GRAPHENE_OIE)

Options:
  --gold=GOLD_OIE              The gold reference Open IE file (by default, it should be under ./oie_corpus/all.oie).
  --out-OUTPUT_FILE            The output file, into which the precision recall curve will be written.
  --clausie=CLAUSIE_OIE        Read ClausIE format from file CLAUSIE_OIE.
  --ollie=OLLIE_OIE            Read OLLIE format from file OLLIE_OIE.
  --openiefour=OPENIEFOUR_OIE  Read Open IE 4 format from file OPENIEFOUR_OIE.
  --props=PROPS_OIE            Read PropS format from file PROPS_OIE
  --reverb=REVERB_OIE          Read ReVerb format from file REVERB_OIE
  --reverb2=REVERB2_OIE        Read ReVerb2 format from file REVERB2_OIE
  --stanford=STANFORD_OIE      Read Stanford format from file STANFORD_OIE
  --graphene=GRAPHENE_OIE      Read Graphene format from file GRAPHENE_OIE
'''
import docopt
import string
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score, recall_score
from sklearn.metrics.base import _average_binary_score
import re
import logging
logging.basicConfig(level = logging.INFO)

from oie_readers.stanfordReader import StanfordReader
from oie_readers.ollieReader import OllieReader
from oie_readers.reVerbReader import ReVerbReader
from oie_readers.reVerbReader2 import ReVerbReader2
from oie_readers.clausieReader import ClausieReader
from oie_readers.openieFourReader import OpenieFourReader
from oie_readers.propsReader import PropSReader
from oie_readers.grapheneReader import GrapheneReader

from oie_readers.goldReader import GoldReader
from matcher import Matcher

class Benchmark:
    ''' Compare the gold OIE dataset against a predicted equivalent '''
    def __init__(self, gold_fn):
        ''' Load gold Open IE, this will serve to compare against using the compare function '''
        gr = GoldReader() 
        gr.read(gold_fn)
        self.gold = gr.oie

    def compare(self, predicted, matchingFunc, output_fn):
        ''' Compare gold against predicted using a specified matching function. 
            Outputs PR curve to output_fn '''
        
        y_true = []
        y_scores = []
        
        correctTotal = 0
        unmatchedCount = 0        
        predicted = Benchmark.normalizeDict(predicted)
        gold = Benchmark.normalizeDict(self.gold)
                
        for sent, goldExtractions in gold.items():
            if sent not in predicted:
                # The extractor didn't find any extractions for this sentence
                for goldEx in goldExtractions:   
                    unmatchedCount += len(goldExtractions)
                    correctTotal += len(goldExtractions)
                continue
                
            predictedExtractions = predicted[sent]
            
            for goldEx in goldExtractions:
                correctTotal += 1
                found = False
                
                for predictedEx in predictedExtractions:
                    if output_fn in predictedEx.matched:
                        # This predicted extraction was already matched against a gold extraction
                        # Don't allow to match it again
                        continue
                    
                    if matchingFunc(goldEx, 
                                    predictedEx, 
                                    ignoreStopwords = True, 
                                    ignoreCase = True):
                        
                        y_true.append(1)
                        y_scores.append(predictedEx.confidence)
                        predictedEx.matched.append(output_fn)
                        found = True
                        break
                    
                if not found:
                    unmatchedCount += 1
                    
            for predictedEx in [x for x in predictedExtractions if (output_fn not in x.matched)]:
                # Add false positives
                y_true.append(0)
                y_scores.append(predictedEx.confidence)
                
        y_true = y_true
        y_scores = y_scores
        
        # recall on y_true, y  (r')_scores computes |covered by extractor| / |True in what's covered by extractor|
        # to get to true recall we do r' * (|True in what's covered by extractor| / |True in gold|) = |true in what's covered| / |true in gold|
        p, r, _ = Benchmark.prCurve(np.array(y_true), np.array(y_scores),
                       recallMultiplier = ((correctTotal - unmatchedCount)/float(correctTotal)))

        # This is the area under the curve
        auc = Benchmark.my_average_precision_score(np.array(y_true), np.array(y_scores),
                       recallMultiplier = ((correctTotal - unmatchedCount)/float(correctTotal)))

        # this is the average precision score
        avgP = Benchmark.default_average_precision_score(np.array(y_true), np.array(y_scores))

        rc = ((correctTotal - unmatchedCount)/float(correctTotal))

        #print('p    {}'.format(p))
        #print('r    {}'.format(r))
        print('auc  {}'.format(auc))
        print('avgP {}'.format(avgP))
        print('rc   {}'.format(rc))


        # write PR to file
        with open(output_fn, 'w') as fout:
            fout.write('{0}\t{1}\n'.format("Precision", "Recall"))
            for cur_p, cur_r in sorted(zip(p, r), key = lambda (cur_p, cur_r): cur_r):
                fout.write('{0}\t{1}\n'.format(cur_p, cur_r))
    
    @staticmethod
    def prCurve(y_true, y_scores, recallMultiplier, sample_weight=None):
        # Recall multiplier - accounts for the percentage examples unreached by 
        precision, recall, thresholds = precision_recall_curve(y_true, y_scores, sample_weight=sample_weight)

        recall = recall * recallMultiplier
        return precision, recall, thresholds

    @staticmethod
    def my_average_precision_score(y_true, y_score, recallMultiplier, average="macro", sample_weight=None):
        def _binary_uninterpolated_average_precision(y_true, y_score, sample_weight=sample_weight):
            precision, recall, thresholds = Benchmark.prCurve(y_true, y_score, recallMultiplier, sample_weight=sample_weight)
            # Return the step function integral
            # The following works because the last entry of precision is
            # garantee to be 1, as returned by precision_recall_curve
            return -np.sum(np.diff(recall) * np.array(precision)[:-1])

        return _average_binary_score(_binary_uninterpolated_average_precision,
                                     y_true, y_score, average,
                                     sample_weight=sample_weight)


    @staticmethod
    def default_average_precision_score(y_true, y_scores, average="macro", sample_weight=None):
        return average_precision_score(y_true, y_scores, average=average, sample_weight=sample_weight)


    # Helper functions:
    @staticmethod
    def normalizeDict(d):
        return dict([(Benchmark.normalizeKey(k), v) for k, v in d.items()])
    
    @staticmethod
    def normalizeKey(k):
        return Benchmark.removePunct(unicode(Benchmark.PTB_unescape(k.replace(' ','')), errors = 'ignore'))

    @staticmethod
    def PTB_escape(s):
        for u, e in Benchmark.PTB_ESCAPES:
            s = s.replace(u, e)
        return s
    
    @staticmethod
    def PTB_unescape(s):
        for u, e in Benchmark.PTB_ESCAPES:
            s = s.replace(e, u)
        return s
    
    @staticmethod
    def removePunct(s):
        return Benchmark.regex.sub('', s)
    
    # CONSTANTS
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    
    # Penn treebank bracket escapes 
    # Taken from: https://github.com/nlplab/brat/blob/master/server/src/gtbtokenize.py
    PTB_ESCAPES = [('(', '-LRB-'),
                   (')', '-RRB-'),
                   ('[', '-LSB-'),
                   (']', '-RSB-'),
                   ('{', '-LCB-'),
                   ('}', '-RCB-'),]


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    logging.debug(args)
    
    if args['--stanford']:
        predicted = StanfordReader()
        predicted.read(args['--stanford'])
    
    if args['--props']:
        predicted = PropSReader()
        predicted.read(args['--props'])
       
    if args['--ollie']:
        predicted = OllieReader()
        predicted.read(args['--ollie'])
    
    if args['--reverb']:
        predicted = ReVerbReader()
        predicted.read(args['--reverb'])

    if args['--reverb2']:
        predicted = ReVerbReader2()
        predicted.read(args['--reverb2'])
    
    if args['--clausie']:
        predicted = ClausieReader()
        predicted.read(args['--clausie'])
        
    if args['--openiefour']:
        predicted = OpenieFourReader()
        predicted.read(args['--openiefour'])

    if args['--graphene']:
        predicted = GrapheneReader()
        predicted.read(args['--graphene'])

    b = Benchmark(args['--gold'])
    out_filename = args['--out']

    logging.info("Writing PR curve of {} to {}".format(predicted.name, out_filename))
    b.compare(predicted = predicted.oie, 
               matchingFunc = Matcher.lexicalMatch,
               output_fn = out_filename)
    
        
        
