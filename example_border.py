#!/usr/bin/env python

import numpy as np
import skimage.io as io
from skimage.viewer import CollectionViewer

import cremi.evaluation as evaluation
import cremi.io.CremiFile as CremiFile


if __name__ == "__main__":
    img = [io.imread('example.png')]
    
    for w in (0, 2, 4, 10):
        target = np.copy(img[0])[...,np.newaxis]
        evaluation.create_border_mask(img[0][...,np.newaxis],target,w,105,axis=2)
        img.append(target[...,0])

    v = CollectionViewer(img)
    v.show()

    cfIn  = CremiFile('example.h5', 'r')
    cfOut = CremiFile('output.h5', 'a')

    evaluation.create_and_write_masked_neuron_ids(cfIn, cfOut, 3, 240, overwrite=True)
