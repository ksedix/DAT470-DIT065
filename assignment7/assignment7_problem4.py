import math
import numpy as np
import argparse
import pandas as pd
import csv
import sys
import time
import cupy as cp # type: ignore

def linear_scan(X, Q, b = None):
    """
    Perform linear scan for querying nearest neighbor.
    X: n*d dataset
    Q: m*d queries
    b: optional batch size (ignored in this implementation)
    Returns an m-vector of indices I; the value i reports the row in X such 
    that the Euclidean norm of ||X[I[i],:]-Q[i]|| is minimal
    """
    #Problem 4 (GPU)
    m = Q.shape[0]
    #X is n*d , Q.T is d*m. Result will be n*m matrix
    X_cupy = cp.asarray(X, dtype = cp.float32, blocking=True)
    Q_cupy = cp.asarray(Q, dtype = cp.float32, blocking=True)
    batch_size = math.ceil(m/b)
    # Specifying dtype=cp.int32 is necessary because otherwise the indices will be float which will cause bug
    I_cupy = cp.zeros(m, dtype=int)
    # result dimension: n
    X_squared_sum = cp.sum(cp.square(X_cupy),axis=1)
    for i in range(0,m,batch_size):
        batch_end = min(i+batch_size,m)
        Q_batch = Q_cupy[i:batch_end]
        #result dimension: n*m
        XQ_T = X_cupy @ Q_batch.T
        # result dimension: m
        Q_squared_sum = cp.sum(cp.square(Q_batch),axis=1)
        # result dimension: n*m
        X_and_Q_sum = X_squared_sum[:,cp.newaxis] + Q_squared_sum[cp.newaxis,:]
        # result dimension: n*m
        result_batch = X_and_Q_sum - 2*XQ_T
        # result dimension: m
        I_cupy_batch = cp.argmin(result_batch,axis=0)

        I_cupy[i:batch_end] = I_cupy_batch

    cp.cuda.Stream.null.synchronize()

    I = cp.asnumpy(I_cupy, blocking=True)

    return I



def load_glove(fn):
    """
    Loads the glove dataset from the file
    Returns (X,L) where X is the dataset vectors and L is the words associated
    with the respective rows.
    """
    df = pd.read_table(fn, sep = ' ', index_col = 0, header = None,
                           quoting = csv.QUOTE_NONE, keep_default_na = False)
    X = np.ascontiguousarray(df, dtype = np.float32)
    L = df.index.tolist()
    return (X, L)

def load_pubs(fn):
    """
    Loads the pubs dataset from the file
    Returns (X,L) where X is the dataset vectors (easting,northing) and 
    L is the list of names of pubs, associated with each row
    """
    df = pd.read_csv(fn)
    L = df['name'].tolist()
    X = np.ascontiguousarray(df[['easting','northing']], dtype = np.float32)
    return (X, L)

def load_queries(fn):
    """
    Loads the m*d array of query vectors from the file
    """
    return np.loadtxt(fn, delimiter = ' ', dtype = np.float32)

def load_query_labels(fn):
    """
    Loads the m-long list of correct query labels from a file
    """
    with open(fn,'r') as f:
        return f.read().splitlines()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( \
          description = 'Perform nearest neighbor queries under the '
          'Euclidean metric using linear scan, measure the time '
          'and optionally verify the correctness of the results')
    parser.add_argument(
        '-d', '--dataset', type=str, required=True,
        help = 'Dataset file (must be pubs or glove)')
    parser.add_argument(
        '-q', '--queries', type=str, required=True,
        help = 'Queries file (must be compatible with the dataset)')
    parser.add_argument(
        '-l', '--labels', type=str, required=False,
        help = 'Optional correct query labels; if provided, the correctness '
        'of returned results is checked')
    parser.add_argument(
        '-b', '--batch-size', type=int, required=False,
        help = 'Size of batches')
    args = parser.parse_args()

    t1 = time.time()
    if 'pubs' in args.dataset:
        (X,L) = load_pubs(args.dataset)
    elif 'glove' in args.dataset:
        (X,L) = load_glove(args.dataset)
    else:
        sys.stderr.write(f'{sys.argv[0]}: error: Only glove/pubs supported\n')
        exit(1)
    t2 = time.time()

    (n,d) = X.shape
    assert len(L) == n

    t3 = time.time()
    Q = load_queries(args.queries)
    t4 = time.time()

    assert X.flags['C_CONTIGUOUS']
    assert Q.flags['C_CONTIGUOUS']
    assert X.dtype == np.float32
    assert Q.dtype == np.float32
    
    m = Q.shape[0]
    assert Q.shape[1] == d

    t5 = time.time()
    QL = None
    if args.labels is not None:
        QL = load_query_labels(args.labels)
        assert len(QL) == m
    t6 = time.time()

    I = linear_scan(X,Q,args.batch_size)
    t7 = time.time()
    assert I.shape == (m,)

    num_erroneous = 0
    if QL is not None:
        for (i,j) in enumerate(I):
            #label of the ith query is equal to name of jth item in X
            if QL[i] != L[j]:
                sys.stderr.write(f'{i}th query was erroneous: got "{L[j]}", '
                                     f'but expected "{QL[i]}"\n')
                num_erroneous += 1

    print(f'Loading dataset ({n} vectors of length {d}) took', t2-t1)
    print(f'Performing {m} NN queries took', t7-t6)
    print(f'Number of erroneous queries: {num_erroneous}')
