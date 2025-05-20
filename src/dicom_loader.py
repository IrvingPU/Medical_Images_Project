import os
import pydicom
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

def load_dicom_series(folder_path):
    """Load and sort DICOM slices by InstanceNumber."""
    dicom_files = [os.path.join(folder_path, f)
                   for f in os.listdir(folder_path)
                   if f.endswith('.dcm') or not '.' in f]
    slices = [pydicom.dcmread(f) for f in dicom_files]
    slices.sort(key=lambda x: float(x.InstanceNumber))
    print(f"Loaded {len(slices)} slices from {folder_path}")
    return slices

def get_spacing(slices):
    """Return spacing in mm as (row_spacing, col_spacing, z_spacing)."""
    pixel_spacing = slices[0].PixelSpacing
    slice_thickness = getattr(slices[0], 'SliceThickness', 1.0)
    spacing_between = getattr(slices[0], 'SpacingBetweenSlices', slice_thickness)
    return float(pixel_spacing[0]), float(pixel_spacing[1]), float(spacing_between)

def stack_slices_to_volume(slices):
    """Stack slices into a 3D NumPy volume."""
    return np.stack([s.pixel_array for s in slices], axis=0)

def rescale_volume(volume, spacing):
    """Rescale 3D volume to isotropic spacing based on Y-axis resolution."""
    factors = [
        spacing[2] / spacing[0],  # Z/Y
        1.0,                      # Y
        spacing[1] / spacing[0]   # X/Y
    ]
    print(f"Rescaling volume with factors (z, y, x): {factors}")
    return scipy.ndimage.zoom(volume, zoom=factors, order=1)


#0 a 600
#Alfa fucion
#Los detalles finos tienen coincidir
#Slide between spaces
#Windwin