from cremi.io import CremiFile
from cremi.evaluation import Clefts

test = CremiFile('/home/saalfeld/cremi/sample_A_prediction.hdf', 'r')
truth = CremiFile('/home/saalfeld/cremi/sample_A_20160501.hdf', 'r')
threshold = 200 # in nm

clefts = Clefts(test, truth)

false_positive_threshold_count = clefts.count_false_positives(threshold)
false_negative_threshold_count = clefts.count_false_negatives(threshold)

false_positive_stats = clefts.acc_false_positives()
false_negative_stats = clefts.acc_false_negatives()

print("false positives above threshold " + threshold + "nm: ")
print(false_positive_threshold_count)
print("false negatives above threshold " + threshold + "nm: ")
print(false_negative_threshold_count)

print("false positive stats: ")
print(false_positive_stats)
print("false negative stats: ")
print(false_negative_stats)

