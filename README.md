# Medical Images Project

This project involves the visualization and analysis of liver CT scans and their segmentations. The goals include:

- Loading and visualizing DICOM volumes
- Overlaying tumor and liver segmentations
- Generating rotating MIP projections
- Performing rigid registration between multi-phase scans

## Folder Structure

```
MEDICAL_IMAGES_PROJECT/
├── data/                  # Raw and processed DICOM and segmentation files
│   ├── raw/
│   │   └── 1720/
│   │       ├── DICOM/
│   │       └── SEGMENTATIONS/
│   └── processed/
├── notebooks/             # Jupyter notebooks for each task
├── reports/               # Project reports
├── results/               # Generated images, projections, overlays
├── slides/                # Presentation slides
├── src/                   # Reusable Python scripts
├── README.md              # Project overview (this file)
└── requirements.txt       # Python dependencies
```

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Launch the main notebook:

```bash
cd notebooks
jupyter notebook
```

3. Modify paths if needed, using relative references like `../data/raw/...`.

## Authors

- Your Name – MSc Student at UIB

