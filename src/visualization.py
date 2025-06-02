import matplotlib.pyplot as plt
import numpy as np
from config import ALPHA_OVERLAY, COLORS


def show_slice(volume, index, cmap='gray', title=None):
    plt.imshow(volume[index], cmap=cmap)
    if title: plt.title(title)
    plt.axis('off')
    plt.show()

def overlay_masks(image, mask, class_map=COLORS):
    """Overlay a label mask over a grayscale image."""
    image_norm = (image - np.min(image)) / (np.max(image) - np.min(image))
    overlay = plt.cm.gray(image_norm)[..., :3]
    for label, color in class_map.items():
        mask_binary = (mask == list(class_map.keys()).index(label) + 1)
        overlay[mask_binary] = np.array(color)
    return overlay
