import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,os.pardir)))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda
import pickle
import numpy as np

db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
psda.set_url(db_url)

schema = 'shared'
tables = [u'validated_01_2014',
          u'validated_02_2014',
          u'validated_03_2014',
          u'validated_04_2014',
          u'validated_05_2014',]

'''
all_car_ids = []
for table in tables:
    all_car_ids.append(psda.get_dataids_with_real_values(schema,table,'car1'))

common_car_ids = sorted(da.utils.get_common_ids(all_car_ids))

all_use_ids = []
for table in tables:
    all_use_ids.append(psda.get_dataids_with_real_values(schema,table,'use'))

common_use_ids = sorted(da.utils.get_common_ids(all_use_ids))
'''

common_car_ids = [624, 661, 1714, 1782, 1953,
                  2470, 2638, 2769, 2814, 3192,
                  3367, 3482, 3723, 3795, 4135,
                  4505, 4526, 4641, 4767, 4957,
                  4998, 5109, 5357, 6139, 6836,
                  6910, 6941, 7850, 7863, 7875,
                  7940, 8046, 8142, 8197, 8645,
                  8669, 9484, 9609, 9729, 9830,
                  9932, 9934]

common_use_ids = [86, 93, 94, 410, 484,
                  585, 624, 661, 739, 744,
                  821, 871, 936, 1167, 1283,
                  1334, 1632, 1714, 1718, 1782,
                  1790, 1800, 1953, 1994, 2094,
                  2129, 2156, 2158, 2171, 2233,
                  2242, 2337, 2449, 2470, 2575,
                  2606, 2638, 2769, 2814, 2829,
                  2864, 2945, 2953, 2974, 3092,
                  3192, 3221, 3263, 3367, 3394,
                  3456, 3482, 3504, 3544, 3649,
                  3652, 3723, 3736, 3778, 3795,
                  3893, 3918, 4031, 4135, 4154,
                  4298, 4313, 4447, 4505, 4526,
                  4641, 4732, 4767, 4874, 4922,
                  4956, 4957, 4998, 5026, 5109,
                  5209, 5218, 5262, 5275, 5357,
                  5395, 5545, 5568, 5677, 5785,
                  5814, 5874, 5938, 5949, 5972,
                  6139, 6412, 6636, 6673, 6730,
                  6836, 6910, 6941, 7062, 7319,
                  7390, 7531, 7536, 7617, 7731,
                  7769, 7788, 7800, 7850, 7863,
                  7875, 7940, 7951, 8046, 8079,
                  8084, 8142, 8197, 8292, 8317,
                  8342, 8419, 8467, 8645, 8669,
                  8741, 8829, 8852, 8956, 9019,
                  9036, 9121, 9160, 9343, 9356,
                  9484, 9555, 9578, 9609, 9643,
                  9654, 9701, 9729, 9737, 9771,
                  9830, 9875, 9915, 9922, 9926,
                  9932, 9934, 9937, 9938, 9939,
                  9982, 9983]

non_car_ids = [86, 93, 94, 410, 484,
               585, 739, 744, 821, 871,
               936, 1167, 1283, 1334, 1632,
               1718, 1790, 1800, 1994, 2094,
               2129, 2156, 2158, 2171, 2233,
               2242, 2337, 2449, 2575, 2606,
               2829, 2864, 2945, 2953, 2974,
               3092, 3221, 3263, 3394, 3456,
               3504, 3544, 3649, 3652, 3736,
               3778, 3893, 3918, 4031, 4154,
               4298, 4313, 4447, 4732, 4874,
               4922, 4956, 5026, 5209, 5218,
               5262, 5275, 5395, 5545, 5568,
               5677, 5785, 5814, 5874, 5938,
               5949, 5972, 6412, 6636, 6673,
               6730, 7062, 7319, 7390, 7531,
               7536, 7617, 7731, 7769, 7788,
               7800, 7951, 8079, 8084, 8292,
               8317, 8342, 8419, 8467, 8741,
               8829, 8852, 8956, 9019, 9036,
               9121, 9160, 9343, 9356, 9555,
               9578, 9643, 9654, 9701, 9737,
               9771, 9875, 9915, 9922, 9926,
               9937, 9938, 9939, 9982, 9983]

print "hi"
#car_use = psda.generate_traces_for_appliance_by_dataids(
#    schema, tables[0], "use", common_car_ids)
#with open('../../data/car_use_validated_01_2014.pkl','r') as f:
#    car_use = pickle.load(f)

n_cars = len(common_car_ids)
n_non_cars = len(non_car_ids)

# split into training, validation, and testing
np.random.seed(1)

def get_train_valid_test_indices(n):
    indices = np.arange(n)
    np.random.shuffle(indices)
    n_train = n/2
    n_valid = n/4
    n_test = n - n_train - n_valid
    assert(n == n_train + n_valid + n_test)
    return (indices[:n_train],
           indices[n_train:n_train+n_valid],
           indices[n_train+n_valid:])

def trace_windows(trace,window_length,window_step):
    import pdb;pdb.set_trace()

car_train_i, car_valid_i, car_test_i = get_train_valid_test_indices(n_cars)
non_car_train_i, non_car_valid_i, non_car_test_i =\
    get_train_valid_test_indices(n_non_cars)

car_training_traces = []
for i in car_train_i:
    print 'car train {}'.format(i)
    with open('../../data/car_use/trace_{0:03d}.pkl'.format(i),'r') as f:
        trace = pickle.load(f)
    arrays = trace_windows(trace,672,12) # one week, steps of 3 hours
    car_training_traces.append((trace,1))

