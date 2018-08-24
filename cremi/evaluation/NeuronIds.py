from __future__ import absolute_import, print_function
import numpy as np
from .border_mask import create_border_mask
from .voi import voi
from .rand import adapted_rand

class NeuronIds:

    def __init__(self, groundtruth, border_threshold = None):
        """Create a new evaluation object for neuron ids against the provided ground truth.

        Parameters
        ----------

            groundtruth: Volume
                The ground truth volume containing neuron ids.

            border_threshold: None or float, in world units
                Pixels within `border_threshold` to a label border in the
                same section will be assigned to background and ignored during
                the evaluation.
        """

        assert groundtruth.resolution[1] == groundtruth.resolution[2], \
            "x and y resolutions of ground truth are not the same (%f != %f)" % \
            (groundtruth.resolution[1], groundtruth.resolution[2])

        self.groundtruth = groundtruth
        self.border_threshold = border_threshold

        if self.border_threshold:

            print("Computing border mask...")

            self.gt = np.zeros(groundtruth.data.shape, dtype=np.uint64)
            create_border_mask(
                groundtruth.data,
                self.gt,
                float(border_threshold)/groundtruth.resolution[1],
                np.uint64(-1))
        else:
            self.gt = np.array(self.groundtruth.data).copy()

        # current voi and rand implementations don't work with np.uint64(-1) as
        # background label, so we make it 0 here and bump all other labels
        self.gt += 1

    def voi(self, segmentation):

        assert list(segmentation.data.shape) == list(self.groundtruth.data.shape)
        assert list(segmentation.resolution) == list(self.groundtruth.resolution)

        print("Computing VOI...")

        return voi(np.array(segmentation.data), self.gt, ignore_groundtruth = [0])

    def adapted_rand(self, segmentation):

        assert list(segmentation.data.shape) == list(self.groundtruth.data.shape)
        assert list(segmentation.resolution) == list(self.groundtruth.resolution)

        print("Computing RAND...")

        return adapted_rand(np.array(segmentation.data), self.gt)
