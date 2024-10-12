import psycopg2
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('--dataset',
                    default="queries",
                    type=str)

parser.add_argument('--sf',
                    default=1,
                    type=int)

parser.add_argument('--budget',
                    default=0.1,
                    type=float)

lava_qerror = {0.1 : [1.038, 1.138, 1.478, 1.526],
               0.2 : [1.029, 1.11, 1.325, 1.424],
               0.4 : [1.029, 1.085, 1.244, 1.398],
               0.8 : [1.02, 1.087, 1.194, 1.343],
               1.6 : [1.016, 1.052, 1.134, 1.128],
               3.2 : [1.016, 1.049, 1.137, 1.082]}

args = parser.parse_args()

queries_file = "../../queries/california_queries/{}.sql".format(args.dataset)
card_file = "../../queries/california_queries/{}_card.csv".format(args.dataset)

conn = psycopg2.connect(
    host="localhost",
    database="california",
    user="postgres",
    port="5435"
)

cur = conn.cursor()

queries = open(
    queries_file, "r")
cards = open(
    card_file, "r")

card_list = []
for line in cards:
    card_list.append(int(float(line.strip())))

query_list = []
for line in queries:
    query_list.append(line.strip())

start = time.time()

n_test_queries = len(query_list)
q_error_list = []
result_list = []
for i in range(n_test_queries):
    # print('No.{}'.format(i + 1), query_list[i])
    cur.execute(query_list[i])
    result = cur.fetchone()[0] / args.sf
    if result == 0:
        result = 1
    q_error = max(result/card_list[i], card_list[i]/result)
    # print("True cardinality: {}, test cardinality: {}, q error; {}".format(
            # card_list[i], result, q_error))
    q_error_list.append(q_error)
    result_list.append(result)

end = time.time()
print("Total time takes for executing {} queries: {}".format(
        n_test_queries, end - start))

q_error_list = np.array(q_error_list)
result_list = np.array(result_list)

print("Max q error: {}".format(np.max(q_error_list)))
print("99 percentile q error: {}".format(np.percentile(q_error_list, 99)))
print("95 percentile q error: {}".format(np.percentile(q_error_list, 95)))
print("90 percentile q error: {}".format(np.percentile(q_error_list, 90)))
print("75 percentile q error: {}".format(np.percentile(q_error_list, 75)))
print("50 percentile q error: {}".format(np.percentile(q_error_list, 50)))
print("Average q error: {}".format(np.mean(q_error_list)))
qerror_50 = np.percentile(q_error_list, 50)
qerror_75 = np.percentile(q_error_list, 75) 
qerror_90 = np.percentile(q_error_list, 90) 
qerror_mean = np.mean(q_error_list)
print("50th: {}%".format(round(-(qerror_50 - lava_qerror[args.budget][0]) / (lava_qerror[args.budget][0] - 1)  * 100, 1)))
print("75th: {}%".format(round(-(qerror_75 - lava_qerror[args.budget][1]) / (lava_qerror[args.budget][1] - 1) * 100, 1)))
print("90th: {}%".format(round(-(qerror_90 - lava_qerror[args.budget][2]) / (lava_qerror[args.budget][2] - 1) * 100, 1)))
print("mean: {}%".format(round(-(qerror_mean - lava_qerror[args.budget][3]) / (lava_qerror[args.budget][3] - 1) * 100, 1)))
