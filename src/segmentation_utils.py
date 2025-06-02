import numpy as np

def dice_score(pred, gt, label=1):
    pred_bin = (pred == label)
    gt_bin = (gt == label)
    intersection = np.sum(pred_bin & gt_bin)
    return 2 * intersection / (np.sum(pred_bin) + np.sum(gt_bin) + 1e-6)
