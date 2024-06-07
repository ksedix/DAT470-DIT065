#!/usr/bin/env python3

import numpy as np
import numpy.typing as npt
import pandas as pd
import csv
import argparse
import time
from typing import Dict, Tuple, List, Optional

def load_glove(filename: str)->Tuple[Dict[str,int],Dict[int,str],
                                        npt.NDArray[np.float64]]:
    """
    Loads the glove dataset. Returns three things:
    A dictionary that contains a map from words to rows in the dataset.
    A reverse dictionary that maps rows to words.
    The embeddings dataset as a NumPy array.
    """
    df = pd.read_table(filename, sep=' ', index_col=0, header=None,
                           quoting=csv.QUOTE_NONE)
    word_to_idx: Dict[str,int] = dict()
    idx_to_word: Dict[int,str] = dict()
    for (i,word) in enumerate(df.index):
        word_to_idx[word] = i
        idx_to_word[i] = word
    return (word_to_idx, idx_to_word, df.to_numpy())

def normalize(X: npt.NDArray[np.float64])->npt.NDArray[np.float64]:
    """
    Reads an n*d matrix and normalizes all rows to have unit-length (L2 norm)
    
    Implement this function using array operations! No loops allowed.
    """
    # Calculate the L2 norm of each row (axis=1)
    norms = np.linalg.norm(X, axis=1)

    # Ensure no division by zero
    norms[norms == 0] = 1

    # Divide each row by its L2 norm
    normalized_matrix = X / norms[:,np.newaxis]

    # Return Normalized Matrix
    return normalized_matrix

def construct_queries(queries_fn: str, word_to_idx: Dict[str,int],
                          X: npt.NDArray[np.float64]) -> \
                          Tuple[npt.NDArray[np.float64],List[str]]:
    """
    Reads queries (one string per line) and returns:
    - The query vectors as a matrix Q (one query per row)
    - Query labels as a list of strings
    """
    with open(queries_fn, 'r') as f:
        queries = f.read().splitlines()
    Q = np.zeros((len(queries), X.shape[1]))
    for i in range(len(queries)):
        Q[i,:] = X[word_to_idx[queries[i]],:]
    return (Q,queries)

class RandomHyperplanes:
    """
    This class mimics the interface of sklearn:
    - the constructor sets the number of hyperplanes
    - the random hyperplanes are drawn when fit() is called 
      (input dimension is set)
    - transform actually transforms the vectors
    - fit_transform does fit first, followed by transform
    """
    def __init__(self, d: int, seed: Optional[int] = None)->None:
        """
        Sets the number of hyperplanes (d) and the optional random number seed
        """
        self._d = d
        self._seed = seed

    def fit(self, X: npt.NDArray[np.float64])-> npt.NDArray[np.float64]:
        """
        Draws _d random hyperplanes, that is, by drawing _d Gaussian unit 
        vectors of length determined by the second dimension (number of 
        columns) of X
        """
        rng = np.random.default_rng(self._seed)
        d = X.shape[1]
        hyperplanes = np.zeros((self._d,d))
        for i in range(self._d):
            hyperplane = rng.standard_normal(d)
            hyperplanes[i] = hyperplane
        self.R = normalize(hyperplanes)

    def transform(self, X: npt.NDArray[np.float64])->npt.NDArray[np.uint8]:
        """
        Project the rows of X into binary vectors
        """
        start = time.time()
        X_prime = X @ self.R.T
        X_double_prime = (X_prime > 0).astype(int)
        end = time.time()
        print(f'Transformation took {end-start} seconds')

    def fit_transform(self, X: npt.NDArray[np.float64])->npt.NDArray[np.uint8]:
        """
        Calls fit() followed by transform()
        """
        self.fit(X)
        return self.transform(X)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='Random hyperplanes dimension', type=int,
                            required = True)
    parser.add_argument('dataset', help='Glove dataset filename',
                            type=str)
    parser.add_argument('queries', help='Queries filename', type=str)
    args = parser.parse_args()
    
    (word_to_idx, idx_to_word, X) = load_glove(args.dataset)

    X = normalize(X)

    (Q,queries) = construct_queries(args.queries, word_to_idx, X)

    start = time.time()

    rh = RandomHyperplanes(args.d, 1234)
    X2 = rh.fit_transform(X)
    Q2 = rh.transform(Q)

    end = time.time()

    print(end-start)







