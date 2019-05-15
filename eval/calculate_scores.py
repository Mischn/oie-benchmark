import re
import numpy as np

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

if __name__ == '__main__':
    values = read_dat('AllWords-QASRL.dat')
    auc = auc_score(values) # average precision == AUC
    avgP = auc_score(stretch_values(values)) # average precision == AUC
    rc = values[-1][1]

    print('auc  {}'.format(auc))
    print('avgP {}'.format(avgP))
    print('rc   {}'.format(rc))
