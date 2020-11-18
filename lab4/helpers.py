import math


def llr_2x2(k11, k12, k21, k22):
    '''Special case of llr with a 2x2 table'''
    # source: https://github.com/tdunning/python-llr/blob/master/llr.py
    return 2 * (denormEntropy([k11 + k12, k21 + k22]) +
                denormEntropy([k11 + k21, k12 + k22]) -
                denormEntropy([k11, k12, k21, k22]))


def denormEntropy(counts):
    '''Computes the entropy of a list of counts scaled by the sum of the counts. If the inputs sum to one, this is just the normal definition of entropy'''
    # source: https://github.com/tdunning/python-llr/blob/master/llr.py
    counts = list(counts)
    total = float(sum(counts))
    # Note tricky way to avoid 0*log(0)
    return -sum([k * math.log(k / total + (k == 0)) for k in counts])
