import re
import numpy as np
import os

def read_dat(filepath):
    values = []
    with open(filepath, 'r') as f:
        for l in f:
            l = l.strip()

            data = l.split('\t')
            try:
                prec, rec = float(data[0]), float(data[1])
                values.append((prec, rec))
            except:
                print('ERROR: Could not parse line "{}"'.format(l))
    return values

# They use a "recall_multiplier" when generating the scores in *.dat
# Therefore, the PR Curve does not go to the right border (1.0 recall) of the plot
# This method stretches the graph to the right border (=undo's the recall_multiplier)
def stretch_values(values):
    rc = values[-1][1]
    factor = 1 * 1./ rc
    res = [(p, factor*r) for p, r in values]
    return res

def auc_score(values):
    res = 0
    last_r = 0
    for p, r in values:
        res += p * (r - last_r)
        last_r = r
    return res



def calc_improvement_perc(s1, s2):
    return (s2 - s1) * 100./ s1


def find_dat_files(directory):
    filepaths = []
    for f in os.listdir(DIRECTORY):
        if f.endswith('.dat'):
            filepaths.append(os.path.join(DIRECTORY, f))
    return filepaths

def calculate_scores(filepath):
    values = read_dat(filepath)
    auc = auc_score(values) # average precision == AUC
    avgP = auc_score(stretch_values(values)) # average precision == AUC
    p = values[-1][0]
    r = values[-1][1]
    return {'auc':auc, 'p': p, 'avgP': avgP, 'r': r}

if __name__ == '__main__':
    DIRECTORY = './survey_plots1'

    for filepath in find_dat_files(DIRECTORY):
        print()
        print(filepath)
        scores = calculate_scores(filepath)
        for k in scores.keys():
            print('\t{:<10}: {:.3f}'.format(k, scores[k]))

    print('#'*100)

    # calculate improvements
    
    DIRECTORY = './survey_plots2'
    compare_files = [
        (DIRECTORY + '/ClausIE.dat', DIRECTORY + '/FW_ClausIE.dat'),
        (DIRECTORY + '/OLLIE.dat', DIRECTORY + '/FW_OLLIE.dat'),
        (DIRECTORY + '/OpenIE-4.dat', DIRECTORY + '/FW_OpenIE-4.dat'),
        (DIRECTORY + '/ReVerb.dat', DIRECTORY + '/FW_ReVerb.dat'),
        (DIRECTORY + '/Stanford.dat', DIRECTORY + '/FW_Stanford.dat')
    ]

    for f1, f2 in compare_files:
        print()
        print('{} <-> {}'.format(f1, f2))
        scores1, scores2 = calculate_scores(f1), calculate_scores(f2)
        for k in scores1.keys():
            impr = calc_improvement_perc(scores1[k], scores2[k])
            print('\t{:<10}: {}{:.0f}'.format(k, '+ ' if impr >= 0 else '', impr))

