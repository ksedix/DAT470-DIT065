import argparse

from matplotlib import pyplot as plt
from tabulation_hash import TabulationHash

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a uint64 argument')
    parser.add_argument('-s','--seed', type=int, help='The random number generator seed', default=None)
    parser.add_argument('value', type=int, help='The number of unique uint64 integers you want to hash')
    args = parser.parse_args()
    n = args.value
    seed = args.seed
    tabulation_hash = TabulationHash()
    hashes = []
    for i in range(1,n+1):
        hashes.append((i,tabulation_hash(i)))
    values = [tpl[1] for tpl in hashes]
    plt.hist(values, bins=20)
    plt.xlabel('Hash Values')
    plt.ylabel('Frequency')
    plt.title('Distribution of Hash values from tabular hashing')
    plt.show()
