from __future__ import absolute_import
from .synaptic_partners import synaptic_partners_fscore

class SynapticPartners:

    def __init__(self, matching_threshold = 400):

        self.matching_threshold = matching_threshold

    def fscore(self, rec_annotations, gt_annotations, gt_segmentation, all_stats = False):

        return synaptic_partners_fscore(rec_annotations, gt_annotations, gt_segmentation, self.matching_threshold, all_stats)
