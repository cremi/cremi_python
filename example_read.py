#!/usr/bin/python

from cremi import Annotations, Volume
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
raw = file.read_raw()
neuron_ids = file.read_neuron_ids()
clefts = file.read_clefts()
annotations = file.read_annotations()

print "Read raw: " + str(raw) + \
    ", resolution " + str(raw.resolution) + \
    ", offset " + str(raw.offset) + \
    ("" if raw.comment == None else ", comment \"" + raw.comment + "\"")

print "Read neuron_ids: " + str(neuron_ids) + \
    ", resolution " + str(neuron_ids.resolution) + \
    ", offset " + str(neuron_ids.offset) + \
    ("" if neuron_ids.comment == None else ", comment \"" + neuron_ids.comment + "\"")

print "Read clefts: " + str(clefts) + \
    ", resolution " + str(clefts.resolution) + \
    ", offset " + str(clefts.offset) + \
    ("" if clefts.comment == None else ", comment \"" + clefts.comment + "\"")

print "Read annotations:"
for (id, type, location) in zip(annotations.ids(), annotations.types(), annotations.locations()):
    print str(id) + " of type " + type + " at " + str(np.array(location)+np.array(annotations.offset))
print "Pre- and post-synaptic partners:"
for (pre, post) in annotations.pre_post_partners:
    print str(pre) + " -> " + str(post)
