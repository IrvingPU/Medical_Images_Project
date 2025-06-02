import numpy as np
from scipy.ndimage import affine_transform

def rigid_register(fixed, moving, matrix=None):
    """Apply rigid transform (matrix) to moving volume."""
    if matrix is None:
        matrix = np.eye(4)
    # Only translation/rotation in upper 3x3 and last column
    transform = matrix[:3, :3]
    offset = matrix[:3, 3]
    return affine_transform(moving, transform, offset=offset)
