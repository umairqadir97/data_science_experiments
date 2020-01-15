import numpy as np

def get_iou_score(target, prediction):
     """

    Args:
      target: numpy ground truth image
      prediction: numpy prediction image

    Returns:
      iou_score: intersection over union score
    """
    intersection = np.logical_and(target, prediction)
    union = np.logical_or(target, prediction)
    iou_score = np.sum(intersection) / np.sum(union)
    return iou_score