import pydicom
import numpy as np
from pathlib import Path

def load_dicom_series(folder: Path):
    """Load and stack a sorted DICOM series from a folder."""
    slices = [pydicom.dcmread(f, force=True) for f in sorted(folder.glob("*.dcm"))]
    slices = [s for s in slices if hasattr(s, "pixel_array")]
    slices.sort(key=lambda x: x.ImagePositionPatient[2])
    volume = np.stack([s.pixel_array for s in slices])
    return volume, slices

def load_segmentation(path: Path):
    """Load a DICOM segmentation mask."""
    return pydicom.dcmread(path).pixel_array
