import os
import pydicom
import numpy as np

def load_dicom_series(folder_path):
    """Load and sort a DICOM series from the given folder."""
    dicom_files = [os.path.join(folder_path, f)
                   for f in os.listdir(folder_path)
                   if f.endswith('.dcm') or not '.' in f]

    slices = [pydicom.dcmread(f) for f in dicom_files]
    slices.sort(key=lambda s: float(getattr(s, "InstanceNumber", 0)))
    return slices

def check_acquisition_consistency(slices):
    """Check if all slices have the same AcquisitionNumber and spacing."""
    acquisition_numbers = [getattr(s, "AcquisitionNumber", None) for s in slices]
    unique_acquisitions = set(acquisition_numbers)

    spacing_values = [
        getattr(s, "SpacingBetweenSlices", getattr(s, "SliceThickness", None))
        for s in slices
    ]
    spacing_unique = set(np.round(spacing_values, 4))

    print("→ Acquisition Numbers found:", unique_acquisitions)
    print("→ Spacing Between Slices values found:", spacing_unique)

    if len(unique_acquisitions) == 1:
        print("All slices have the same AcquisitionNumber.")
    else:
        print("Inconsistent AcquisitionNumber detected!")

    if len(spacing_unique) == 1:
        print("Consistent SpacingBetweenSlices.")
    else:
        print("SpacingBetweenSlices varies between slices!")

    # Optional debug info
    try:
        positions = [s.ImagePositionPatient[2] for s in slices]
        print(f"→ First slice Z-position: {positions[0]}")
        print(f"→ Last slice Z-position: {positions[-1]}")
    except Exception as e:
        print("Couldn't read ImagePositionPatient:", e)

if __name__ == "__main__":
    folder = r"D:\IrvingPU\UIB\Second Semester\Medical_Images_Project\data\raw\1720\DICOM\31_EQP_Ax5.00mm"
    slices = load_dicom_series(folder)
    check_acquisition_consistency(slices)
