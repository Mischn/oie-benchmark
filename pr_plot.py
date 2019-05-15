""" Usage:
   pr_plot --in=DIR_NAME --out=OUTPUT_FILENAME 

Options:
  --in=DIR_NAME            Folder in which to search for *.dat files, all of which should be in a P/R column format (outputs from benchmark.py)
  --out=OUTPUT_FILENAME    Output filename, filetype will determine the format. Possible formats: pdf, pgf, png


"""

import os
import ntpath
import itertools
import random
import numpy as np
from glob import glob
from docopt import docopt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level = logging.INFO)

def trend_name(path):
    ''' return a system trend name from dat file path '''
    head, tail = ntpath.split(path)
    ret = tail or ntpath.basename(head)
    return ret.split('.')[0]

def get_pr(path):
    ''' get PR curve from file '''
    with open(path) as fin:
        # remove header line
        fin.readline()
        [p, r] = zip(*[map(lambda x: float(x), line.strip().split('\t')) for line in fin])
        return p, r

EVAL_FRAMEWORK = False

def get_unique_id(name):
    if 'Stanford' in name:
        return 0
    if 'OLLIE' in name:
        return 1
    if 'ReVerb' in name:
        return 2
    if 'ClausIE' in name:
        return 3
    if 'OpenIE-4' in name:
        return 4
    else:
        return 5

def is_framework(name):
    return 'FW_' in name

if __name__ == '__main__':
    args = docopt(__doc__)
    input_folder = args['--in']
    output_file = args['--out']
    
    _markers = ['o', 'v', '^', '+', 'x', 'p', 'd', '*']
    _colors = ['#2ca02c', '#7f7f7f', '#17becf', '#ff7f0e', '#e377c2', '#9467bd', '#bcbd22', '#d62728', '#1f77b4', '#8c564b']
    random.shuffle(_colors)

    markers = itertools.cycle(_markers)
    colors = itertools.cycle(_colors)

    # plot graphs for all *.dat files in input path
    files = glob(os.path.join(input_folder, '*.dat'))
    for _file in files:
        p, r = get_pr(_file)
        name = trend_name(_file)

        if EVAL_FRAMEWORK:
            color = _colors[get_unique_id(name)]
            marker = _markers[get_unique_id(name)]
            linestyle = '-' if is_framework(name) else '--'
        else:
            color = next(colors)
            marker = next(markers)
            linestyle = '-'

        plt.plot(r, p, color = color, linestyle = linestyle)
        # draw marker
        plt.plot(r[-1], p[-1], marker = marker, color = color, label = name, linestyle = linestyle)

    # Set figure properties and save
    logging.info("Plotting P/R graph to {}".format(output_file))
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend(loc="lower right", prop={'size': 9 if not EVAL_FRAMEWORK else 8.5})
    plt.savefig(output_file, dpi=300)
