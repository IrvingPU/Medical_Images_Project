import os
import numpy as np
import pydicom
from pathlib import Path
from scipy.ndimage import zoom, rotate


def normalize(input_array: np.ndarray) -> np.ndarray:
    """
    Normalize an array to the [0, 1] range.
    """
    amin = np.min(input_array)
    amax = np.max(input_array)
    return (input_array - amin) / (amax - amin)


def load_dicom_series(folder_path: Path) -> tuple[np.ndarray, list]:
    """
    Load a DICOM series from a folder, returning the stacked volume and slice metadata.
    """
    dcm_files = sorted([f for f in folder_path.glob("*.dcm")])
    dcm_slices = [pydicom.dcmread(f, force=True) for f in dcm_files]
    dcm_slices.sort(key=lambda x: x.InstanceNumber)
    volume = np.stack([s.pixel_array for s in dcm_slices], axis=0)
    return volume, dcm_slices


def rescale_volume(volume: np.ndarray, slice_thickness: float, pixel_spacing: float) -> np.ndarray:
    """
    Rescale a volume to make pixel spacing isotropic in-plane.
    """
    scaling_factors = (1, pixel_spacing, pixel_spacing)
    return zoom(volume, scaling_factors, order=1)


def align_volume_to_reference(volume: np.ndarray, angle: float = 180, crop_slices: int = 19,
                               crop_y: tuple[int, int] = (8, 237), crop_x: tuple[int, int] = (32, 225)) -> np.ndarray:
    """
    Rotate and crop a volume to align it with a reference (phantom).

    Args:
        volume: 3D numpy array to be aligned.
        angle: Rotation angle in degrees.
        crop_slices: Number of slices to remove from the end (Z axis).
        crop_y: Tuple of start and end indices for cropping in Y.
        crop_x: Tuple of start and end indices for cropping in X.

    Returns:
        Aligned and cropped volume.
    """
    rotated = rotate(volume, angle, axes=(1, 2), reshape=False)
    cropped = rotated[:-crop_slices, crop_y[0]:crop_y[1], crop_x[0]:crop_x[1]]
    return cropped
