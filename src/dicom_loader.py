import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import imageio

def load_dicom_series(folder_path):
    """Load a series of DICOM files from a folder and sort them by InstanceNumber."""
    dicom_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.dcm') or not '.' in f]
    slices = [pydicom.dcmread(f) for f in dicom_files]
    slices.sort(key=lambda x: float(x.InstanceNumber))
    print(f"Loaded {len(slices)} slices from {folder_path}")
    return slices

def get_spacing(slices):
    """Get voxel spacing: (row_spacing, col_spacing, z_spacing) in mm."""
    pixel_spacing = slices[0].PixelSpacing  # [row_spacing, col_spacing]
    slice_thickness = getattr(slices[0], 'SliceThickness', 1.0)
    spacing_between_slices = getattr(slices[0], 'SpacingBetweenSlices', slice_thickness)
    z_spacing = float(spacing_between_slices)  # Use if available

    return float(pixel_spacing[0]), float(pixel_spacing[1]), z_spacing

def stack_slices_to_volume(slices):
    """Stack a list of slices into a 3D NumPy array (Volume)."""
    volume = np.stack([s.pixel_array for s in slices], axis=0)
    return volume

def rescale_volume(volume, spacing):
    """
    Rescale volume across all three dimensions.
    spacing: (row_spacing, col_spacing, z_spacing)
    """
    resize_factors = [
        spacing[2] / spacing[0],  # z (slice) relative to y (row)
        1.0,                      # y stays base
        spacing[1] / spacing[0]   # x (col) relative to y (row)
    ]
    print(f"Rescaling volume with factors (z, y, x): {resize_factors}")
    rescaled = scipy.ndimage.zoom(volume, zoom=resize_factors, order=1)
    return rescaled

def show_slice(slice_data):
    """Display a single DICOM slice."""
    plt.figure(figsize=(6,6))
    plt.imshow(slice_data.pixel_array, cmap="gray")
    plt.axis("off")
    plt.title("Example DICOM Slice")
    plt.show()

def show_mip_projection(volume, axis=0, spacing=(1.0, 1.0, 1.0)):
    """Display a Maximum Intensity Projection with correct physical aspect ratio."""
    mip = np.max(volume, axis=axis)

    if axis == 0:  # axial: x vs y
        phys_height = mip.shape[0] * spacing[0]
        phys_width = mip.shape[1] * spacing[1]
    elif axis == 1:  # coronal: z vs x
        phys_height = mip.shape[0] * spacing[2]
        phys_width = mip.shape[1] * spacing[1]
    elif axis == 2:  # sagittal: z vs y
        phys_height = mip.shape[0] * spacing[2]
        phys_width = mip.shape[1] * spacing[0]
    else:
        phys_height = mip.shape[0]
        phys_width = mip.shape[1]

    aspect_ratio = phys_width / phys_height
    fig_height = 6
    fig_width = fig_height * aspect_ratio

    plt.figure(figsize=(fig_width, fig_height))
    plt.imshow(mip, cmap="gray", extent=[0, phys_width, 0, phys_height])
    plt.axis("off")
    plt.title(f"Maximum Intensity Projection (Axis {axis})")
    plt.show()

def create_rotating_mip_gif(volume, output_path, axis=1, num_frames=36):
    """Create a rotating MIP GIF around the selected axis."""
    print(f"Creating rotating MIP GIF: {output_path}")
    frames = []
    angles = np.linspace(0, 360, num_frames, endpoint=False)

    for angle in angles:
        rotated = scipy.ndimage.rotate(volume, angle=angle, axes=(2, axis), reshape=False, order=1)
        mip = np.max(rotated, axis=0)
        frames.append((mip / np.max(mip) * 255).astype(np.uint8))  # Normalize to 0–255

    imageio.mimsave(output_path, frames, duration=0.1)
    print(f"Saved GIF to {output_path}")

if __name__ == "__main__":
    folder = r"D:\IrvingPU\UIB\Second Semester\Medical_Images_Project\data\raw\1720\DICOM\31_EQP_Ax5.00mm"
    slices = load_dicom_series(folder)

    # Show middle slice
    middle_idx = len(slices) // 2
    show_slice(slices[middle_idx])

    # Stack slices into 3D volume
    volume = stack_slices_to_volume(slices)
    print(f"Original volume shape: {volume.shape}")

    # Get voxel spacing
    spacing = get_spacing(slices)
    print(f"Voxel spacing (row, col, z) [mm]: {spacing}")

    # Rescale volume
    rescaled_volume = rescale_volume(volume, spacing)
    print(f"Rescaled volume shape: {rescaled_volume.shape}")

    # Show corrected MIP projections
    show_mip_projection(rescaled_volume, axis=0, spacing=spacing)  # axial
    show_mip_projection(rescaled_volume, axis=1, spacing=spacing)  # coronal
    show_mip_projection(rescaled_volume, axis=2, spacing=spacing)  # sagittal

    # Create rotating MIP GIF (optional, adjust path as needed)
    output_gif = "rotating_mip.gif"
    create_rotating_mip_gif(rescaled_volume, output_gif, axis=1, num_frames=36)


#0 a 600
#Alfa fucion
#Los detalles finos tienen coincidir
#Slide between spaces
#Windwin