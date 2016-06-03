#!/usr/bin/python

from cremi.io import CremiFile
from cremi.evaluation import NeuronIds, Clefts, SynapticPartners

test = CremiFile('test.hdf', 'r')
truth = CremiFile('groundtruth.hdf', 'r')

neuron_ids_evaluation = NeuronIds(truth.read_neuron_ids())

(voi_split, voi_merge) = neuron_ids_evaluation.voi(test.read_neuron_ids())
adapted_rand = neuron_ids_evaluation.adapted_rand(test.read_neuron_ids())

print "Neuron IDs"
print "=========="
print "\tvoi split   : " + str(voi_split)
print "\tvoi merge   : " + str(voi_merge)
print "\tadapted RAND: " + str(adapted_rand)

clefts_evaluation = Clefts(test.read_clefts(), truth.read_clefts())

false_positive_count = clefts_evaluation.count_false_positives()
false_negative_count = clefts_evaluation.count_false_negatives()

false_positive_stats = clefts_evaluation.acc_false_positives()
false_negative_stats = clefts_evaluation.acc_false_negatives()

print "Clefts"
print "======"

print "\tfalse positives: " + str(false_positive_count)
print "\tfalse negatives: " + str(false_negative_count)

print "\tdistance to ground truth: " + str(false_positive_stats)
print "\tdistance to proposal    : " + str(false_negative_stats)

synaptic_partners_evaluation = SynapticPartners()
fscore = synaptic_partners_evaluation.fscore(test.read_annotations(), truth.read_annotations(), truth.read_neuron_ids())

print "Synaptic partners"
print "================="
print "\tfscore: " + str(fscore)
