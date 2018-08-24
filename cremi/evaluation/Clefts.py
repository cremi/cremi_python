import numpy as np
from scipy import ndimage

class Clefts:

    def __init__(self, test, truth):

        test_clefts = test
        truth_clefts = truth

        self.truth_clefts_invalid = truth_clefts.data.value == 0xfffffffffffffffe

        self.test_clefts_mask = np.logical_or(test_clefts.data.value == 0xffffffffffffffff, self.truth_clefts_invalid)
        self.truth_clefts_mask = np.logical_or(truth_clefts.data.value == 0xffffffffffffffff, self.truth_clefts_invalid)

        self.test_clefts_edt = ndimage.distance_transform_edt(self.test_clefts_mask, sampling=test_clefts.resolution)
        self.truth_clefts_edt = ndimage.distance_transform_edt(self.truth_clefts_mask, sampling=truth_clefts.resolution)

    def count_false_positives(self, threshold = 200):

        mask1 = np.invert(self.test_clefts_mask)
        mask2 = self.truth_clefts_edt > threshold
        false_positives = self.truth_clefts_edt[np.logical_and(mask1, mask2)]
        return false_positives.size

    def count_false_negatives(self, threshold = 200):

        mask1 = np.invert(self.truth_clefts_mask)
        mask2 = self.test_clefts_edt > threshold
        false_negatives = self.test_clefts_edt[np.logical_and(mask1, mask2)]
        return false_negatives.size

    def acc_false_positives(self):

        mask = np.invert(self.test_clefts_mask)
        false_positives = self.truth_clefts_edt[mask]
        stats = {
            'mean': np.mean(false_positives),
            'std': np.std(false_positives),
            'max': np.amax(false_positives),
            'count': false_positives.size,
            'median': np.median(false_positives)}
        return stats

    def acc_false_negatives(self):

        mask = np.invert(self.truth_clefts_mask)
        false_negatives = self.test_clefts_edt[mask]
        stats = {
            'mean': np.mean(false_negatives),
            'std': np.std(false_negatives),
            'max': np.amax(false_negatives),
            'count': false_negatives.size,
            'median': np.median(false_negatives)}
        return stats

