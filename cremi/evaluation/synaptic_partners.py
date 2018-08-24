# coding=utf-8
from __future__ import print_function
from scipy.optimize import linear_sum_assignment
import numpy as np

def synaptic_partners_fscore(rec_annotations, gt_annotations, gt_segmentation, matching_threshold = 400, all_stats = False):
    """Compute the f-score of the found synaptic partners.

    Parameters
    ----------

    rec_annotations: Annotations, containing found synaptic partners

    gt_annotations: Annotations, containing ground truth synaptic partners

    gt_segmentation: Volume, ground truth neuron segmentation

    matching_threshold: float, world units
        Euclidean distance threshold to consider two annotations a potential
        match. Annotations that are `matching_threshold` or more untis apart
        from each other are not considered as potential matches.

    all_stats: boolean, optional
        Whether to also return precision, recall, FP, FN, and matches as a 6-tuple with f-score

    Returns
    -------

    fscore: float
        The f-score of the found synaptic partners.
    precision: float, optional
    recall: float, optional
    fp: int, optional
    fn: int, optional
    filtered_matches: list of tuples, optional
        The indices of the matches with matching costs.
    """

    # get cost matrix
    costs = cost_matrix(rec_annotations, gt_annotations, gt_segmentation, matching_threshold)

    # match using Hungarian method
    print("Finding cost-minimal matches...")
    matches = linear_sum_assignment(costs - np.amax(costs) - 1)
    matches = zip(matches[0], matches[1])  # scipy returns matches as numpy arrays

    filtered_matches = [ (i,j, costs[i][j]) for (i,j) in matches if costs[i][j] <= matching_threshold ]
    print(str(len(filtered_matches)) + " matches found")

    # unmatched in rec = FP
    fp = len(rec_annotations.pre_post_partners) - len(filtered_matches)

    # unmatched in gt = FN
    fn = len(gt_annotations.pre_post_partners) - len(filtered_matches)

    # all ground truth elements - FN = TP
    tp = len(gt_annotations.pre_post_partners) - fn

    precision = float(tp)/(tp + fp)
    recall = float(tp)/(tp + fn)
    fscore = 2.0*precision*recall/(precision + recall)

    if all_stats:
        return (fscore, precision, recall, fp, fn, filtered_matches)
    else:
        return fscore

def cost_matrix(rec, gt, gt_segmentation, matching_threshold):

    print("Computing matching costs...")

    rec_locations = pre_post_locations(rec, gt_segmentation)
    gt_locations = pre_post_locations(gt, gt_segmentation)

    rec_labels = pre_post_labels(rec_locations, gt_segmentation)
    gt_labels = pre_post_labels(gt_locations, gt_segmentation)

    size = max(len(rec_locations), len(gt_locations))
    costs = np.zeros((size, size), dtype=np.float)
    costs[:] = 2*matching_threshold
    num_potential_matches = 0
    for i in range(len(rec_locations)):
        for j in range(len(gt_locations)):
            c = cost(rec_locations[i], gt_locations[j], rec_labels[i], gt_labels[j], matching_threshold)
            costs[i,j] = c
            if c <= matching_threshold:
                num_potential_matches += 1

    print(str(num_potential_matches) + " potential matches found")

    return costs

def pre_post_locations(annotations, gt_segmentation):
    """Get the locations of the annotations relative to the ground truth offset."""

    locations = annotations.locations()
    shift = sub(annotations.offset, gt_segmentation.offset)

    return [
        (add(annotations.get_annotation(pre_id)[1], shift), add(annotations.get_annotation(post_id)[1], shift)) for (pre_id, post_id) in annotations.pre_post_partners
    ]

def pre_post_labels(locations, segmentation):

    return [ (segmentation[pre], segmentation[post]) for (pre, post) in locations ]


def cost(pre_post_location1, pre_post_location2, labels1, labels2, matching_threshold):

    max_cost = 2*matching_threshold

    # pairs do not link the same segments
    if labels1 != labels2:
        return max_cost

    pre_dist = distance(pre_post_location1[0], pre_post_location2[0])
    post_dist = distance(pre_post_location1[1], pre_post_location2[1])

    if pre_dist > matching_threshold or post_dist > matching_threshold:
        return max_cost

    return 0.5*(pre_dist + post_dist)

def distance(a, b):
    return np.linalg.norm(np.array(list(a))-np.array(list(b)))

def add(a, b):
    return tuple([a[d] + b[d] for d in range(len(b))])

def sub(a, b):
    return tuple([a[d] - b[d] for d in range(len(b))])
