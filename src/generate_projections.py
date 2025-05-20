import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.ndimage

from dicom_loader import (
    load_dicom_series,
    get_spacing,
    stack_slices_to_volume,
    rescale_volume
)

def rotate_volume(volume, angle_deg):
    """Rotate around axial plane (y-axis rotation)."""
    return scipy.ndimage.rotate(volume, angle=angle_deg, axes=(1, 2), reshape=False)

def generate_rotating_projection(volume, spacing, output_path, projection_type="MIP", num_frames=36, save_frames=False):
    """Generate rotating MIP/AIP projection GIF."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img_min, img_max = np.min(volume), np.max(volume)
    cmap = plt.cm.bone
    angles = np.linspace(0, 360, num_frames, endpoint=False)
    frames = []

    fig, ax = plt.subplots()
    for i, angle in enumerate(angles):
        rotated = rotate_volume(volume, angle)
        projection = np.max(rotated, axis=2) if projection_type == "MIP" else np.mean(rotated, axis=2)

        if save_frames:
            fig = plt.figure(figsize=(6, 6))
            plt.imshow(projection, cmap=cmap, vmin=img_min, vmax=img_max)
            plt.axis("off")
            plt.savefig(f"{output_path}_frame_{i:03d}.png", bbox_inches='tight', pad_inches=0)
            plt.close()

        frames.append([plt.imshow(projection, cmap=cmap, vmin=img_min, vmax=img_max, animated=True)])

    anim = animation.ArtistAnimation(fig, frames, interval=100, blit=True)
    anim.save(output_path)
    print(f"Saved GIF: {output_path}")
    plt.close()

if __name__ == "__main__":
    folder = r"D:\IrvingPU\UIB\Second Semester\Medical_Images_Project\data\raw\1720\DICOM\31_EQP_Ax5.00mm"
    slices = load_dicom_series(folder)
    spacing = get_spacing(slices)
    volume = stack_slices_to_volume(slices)
    volume = rescale_volume(volume, spacing)

    generate_rotating_projection(volume, spacing, output_path="results/mip_rotation.gif", projection_type="MIP")
    generate_rotating_projection(volume, spacing, output_path="results/aip_rotation.gif", projection_type="AIP")


