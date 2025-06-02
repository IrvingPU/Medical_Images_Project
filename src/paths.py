from pathlib import Path

# === Task 1 Paths ===
def get_raw_dicom_path(patient_id: str, phase: str):
    """
    Returns the path to a specific DICOM phase for a patient.
    Example: get_raw_dicom_path("patient_1720", "31_EQP_Ax5.00mm")
    """
    return Path(f"../data/raw/{patient_id}/DICOM/{phase}")

def get_segmentation_path(patient_id: str, label: str):
    """
    Returns the path to a specific segmentation DICOM file.
    Example: get_segmentation_path("patient_1720", "31_EQP_Ax5.00mm_ManualROI_Liver")
    """
    return Path(f"../data/raw/{patient_id}/SEGMENTATIONS/{label}.dcm")

# === Task 2 Paths ===
from pathlib import Path

def get_project_root():
    """
    Returns the absolute path to the root of the project.
    """
    return Path(__file__).resolve().parents[1]

def get_task2_paths():
    """
    Returns absolute paths to phantom and scan directories for Task 2.
    """
    base_dir = get_project_root() / "data" / "raw" / "patient_1720" / "DICOM"
    phantom_dir = base_dir / "10_AP_Ax5.00mm"
    scan_dir = base_dir / "31_EQP_Ax5.00mm"
    return phantom_dir, scan_dir






