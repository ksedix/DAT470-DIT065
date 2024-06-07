#Problem 1 (CPU BATCH)
#Nnquery_default.py
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt
#big glove dataset will not be tested on default algorithm
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt

/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt
/opt/local/bin/run_job.sh -s nnquery_default.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt
#assignment7_problem1.py
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt -b 100

/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_big_names.txt -b 100

/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt -b 100
/opt/local/bin/run_job.sh -s assignment7_problem1.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_big_names.txt -b 1000

#Problem 2 (GPU BATCH)

/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt -b 100

/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt -b 100
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_big_names.txt -b 1000

/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt -b 100
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt -b 1000
/opt/local/bin/run_job.sh -s assignment7_problem2.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_big_names.txt -b 10000

#______________________________________________________________________________________________________

#Problem 3 (CPU MATRIX)
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt -b 1

/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_big_names.txt -b 1

/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem3.py -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_big_names.txt -b 1
#_______________________________________________________________________________________________________

#Problem 4 (GPU MATRIX)

/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt -b 1

/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_big_names.txt -b 10

/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt -b 1
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt -b 10
/opt/local/bin/run_job.sh -s assignment7_problem4.py -p gpu -env cupy -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_big_names.txt -b 100

#______________________________________________________________________________________________________

#Problem 5 (GPU rapids). No batches implemented, not necessary

/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_tiny.txt -l /data/2024-DAT470-DIT065/pub_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_small.txt -l /data/2024-DAT470-DIT065/pub_queries_small_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_medium.txt -l /data/2024-DAT470-DIT065/pub_queries_medium_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/pubs.csv -q /data/2024-DAT470-DIT065/pub_queries_big.txt -l /data/2024-DAT470-DIT065/pub_queries_big_names.txt

/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_small_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_medium_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.6B.50d.txt -q /data/2024-DAT470-DIT065/glove.6B.50d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.6B.50d_queries_big_names.txt

/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_tiny_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_small.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_small_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_medium_names.txt
/opt/local/bin/run_job.sh -s assignment7_problem5.py -p gpu -env rapids -- -d /data/2024-DAT470-DIT065/glove.840B.300d.txt -q /data/2024-DAT470-DIT065/glove.840B.300d_queries_big.txt -l /data/2024-DAT470-DIT065/glove.840B.300d_queries_big_names.txt
