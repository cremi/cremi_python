#!/usr/bin/python

from cremi import Annotations
from cremi.io import CremiFile
import numpy as np
import random

# Open a file for reading
file = CremiFile("example.hdf", "r")

# Check the content of the datafile
print "Has raw: " + str(file.has_raw())
print "Has neuron ids: " + str(file.has_neuron_ids())
print "Has clefts: " + str(file.has_clefts())
print "Has annotations: " + str(file.has_annotations())

# Read everything there is.
#
# If you are using the padded versions of the datasets (where raw is larger to 
# provide more context), the offsets of neuron_ids, clefts, and annotations tell 
# you where they are placed in nm relative to (0,0,0) of the raw volume.
#
# In other words, neuron_ids, clefts, and annotations are exactly the same 
# between the padded and unpadded versions, except for the offset attribute.
(raw, raw_resolution, raw_offset, raw_comment) = file.read_raw()
(neuron_ids, neuron_ids_resolution, neuron_ids_offset, neuron_ids_comment) = file.read_neuron_ids()
(clefts, clefts_resolution, clefts_offset, clefts_comment) = file.read_clefts()
(annotations, annotations_offset) = file.read_annotations()

print "Read raw: " + str(raw) + \
    ", resolution " + str(raw_resolution) + \
    ", offset " + str(raw_offset) + \
    ("" if raw_comment == None else ", comment \"" + raw_comment + "\"")

print "Read neuron_ids: " + str(neuron_ids) + \
    ", resolution " + str(neuron_ids_resolution) + \
    ", offset " + str(neuron_ids_offset) + \
    ("" if neuron_ids_comment == None else ", comment \"" + neuron_ids_comment + "\"")

print "Read clefts: " + str(clefts) + \
    ", resolution " + str(clefts_resolution) + \
    ", offset " + str(clefts_offset) + \
    ("" if clefts_comment == None else ", comment \"" + clefts_comment + "\"")

print "Read annotations:"
for (id, type, location) in zip(annotations.ids(), annotations.types(), annotations.locations()):
    print str(id) + " of type " + type + " at " + str(np.array(location)+np.array(annotations_offset))
print "Pre- and post-synaptic partners:"
for (pre, post) in annotations.pre_post_partners:
    print str(pre) + " -> " + str(post)
