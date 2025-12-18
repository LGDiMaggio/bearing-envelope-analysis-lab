# Bearing Envelope Analysis Lab

**Educational Project for MSc Engineering Students**

---

## Overview

This repository contains educational materials for a hands-on lab on **vibration signal analysis** and **rolling-element bearing fault diagnosis**. Students will learn envelope analysis techniques and classification metrics through two interactive Jupyter notebooks.

**Total lab time**: ~1 hour

---

## Learning Objectives

By completing this lab, you will be able to:

1. **Understand bearing fault mechanisms** and their vibration signatures
2. **Apply envelope analysis** using the Hilbert transform to detect bearing faults
3. **Use band-pass filtering** to enhance fault detection in vibration signals
4. **Compute time-domain features** (RMS, peak, kurtosis) for fault diagnosis
5. **Train and evaluate classifiers** for multi-class bearing fault detection
6. **Interpret classification metrics** (accuracy, precision, recall, F1-score)
7. **Analyze confusion matrices** to diagnose classifier weaknesses
8. **Use ROC and Precision-Recall curves** to evaluate performance
9. **Understand the impact of class imbalance** on model evaluation

---

## Repository Structure

```
.
├── README.md                                  # This file
├── requirements.txt                            # Python dependencies
├── prepare_public_dataset.py                   # Data preparation script (instructor only)
├── data/                                       # Public dataset (2-second samples)
│   ├── H_353rpm_sample.mat
│   ├── H_877rpm_sample.mat
│   ├── IR_353rpm_sample.mat
│   ├── IR_877rpm_sample.mat
│   ├── OR_353rpm_sample.mat
│   ├── OR_877rpm_sample.mat
│   ├── Roller_353rpm_sample.mat
│   └── Roller_877rpm_sample.mat
├── Notebook1_BearingEnvelopeAnalysis.ipynb     # Lab 1: Envelope analysis
└── Notebook2_BearingFaultMetrics.ipynb         # Lab 2: Classification metrics
```

---

## Dataset Description

### Test Rig Conditions

The data come from a bearing test rig operating under:

- **Radial load**: 124.8 kN
- **Axial load**: 0 kN
- **Rotational speeds**: 353 rpm and 877 rpm

### Bearing Conditions

Four bearing health states were tested:

| Label  | Condition              | Description                    |
|--------|------------------------|--------------------------------|
| **H**  | Healthy                | No damage                      |
| **IR** | Inner Race Fault       | Localized damage on inner race |
| **OR** | Outer Race Fault       | Localized damage on outer race |
| **Roller** | Rolling Element Fault | Damage on rolling element      |

### Dataset Files

Each `.mat` file in the `data/` folder contains a **2-second snippet** of vibration data:

- `time_acc`: Time vector for acceleration (s)
- `acc_m_s2`: Acceleration from sensor 4 (m/s²)
- `acc_g`: Acceleration from sensor 4 (g)
- `fs_acc`: Sampling frequency of acceleration (Hz)
- `time_rpm`: Time vector for tacho rpm (s)
- `rpm`: Rotational speed time series (rpm)
- `fs_rpm`: Sampling frequency of rpm (Hz)
- `mean_rpm`: Mean rotational speed (rpm)
- `condition`: Bearing condition label (H, IR, OR, Roller)
- `rpm_nominal`: Nominal rotational speed (353 or 877 rpm)

**Data format**: MATLAB `.mat` files, loadable with `scipy.io.loadmat()` in Python or directly in MATLAB.

**Note**: The full dataset (longer recordings) is private and not included in this repository.

---

## Installation and Setup

### Requirements

- Python 3.8+
- Jupyter Notebook or JupyterLab

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LGDiMaggio/bearing-envelope-analysis-lab.git
   cd bearing-envelope-analysis-lab
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```
   or
   ```bash
   jupyter lab
   ```

Then open the notebooks in order:
1. `Notebook1_BearingEnvelopeAnalysis.ipynb`
2. `Notebook2_BearingFaultMetrics.ipynb`

---

## Notebook Descriptions

### Notebook 1: Envelope Analysis for Bearing Fault Diagnosis

**Topics covered**:

- Loading and visualizing vibration signals from different bearing conditions
- Computing time-domain features (RMS, peak, **kurtosis**)
- Understanding the role of kurtosis in detecting impulsive faults
- Applying **FFT** to analyze frequency content
- Using the **Hilbert transform** to compute signal envelopes
- Comparing envelope spectra with and without **band-pass filtering**
- Conceptual introduction to **spectral kurtosis** and the **kurtogram**
- Demonstrating envelope analysis with a synthetic amplitude-modulated signal

**Key takeaways**:
- Kurtosis is a useful indicator of impulsive behavior in bearing faults
- Envelope analysis reveals fault frequencies more clearly than raw FFT
- Band-pass filtering enhances fault detection by isolating resonance bands

---

### Notebook 2: Classification Metrics for Bearing Fault Diagnosis

**Topics covered**:

- Building a feature dataset from vibration signal segments
- Training a **Random Forest classifier** for multi-class fault detection
- Computing and interpreting classification metrics:
  - **Accuracy**
  - **Precision**
  - **Recall**
  - **F1-score**
  - **Macro, micro, and weighted averages**
- Visualizing the **confusion matrix**
- Plotting **ROC curves** and computing **AUC**
- Plotting **Precision-Recall curves** and computing **Average Precision**
- Understanding the impact of **class imbalance** on evaluation metrics

**Key takeaways**:
- Accuracy alone is insufficient, especially with imbalanced datasets
- Precision and recall provide insight into false positives and false negatives
- PR curves are more informative than ROC curves for imbalanced problems
- Always examine the confusion matrix to diagnose model weaknesses

---

## Instructor Notes

### Data Preparation Script

The `prepare_public_dataset.py` script is for **instructor use only**. It:

1. Reads the original `.mat` files from a private folder (`Data/`)
2. Extracts the first 2 seconds of acceleration (sensor 4) and tacho rpm data
3. Saves simplified `.mat` files in the `data/` folder for student use

**To use the script**:

1. Update `RAW_DATA_PATH` in the script to point to your private data folder
2. Run: `python prepare_public_dataset.py`
3. The script will create the `data/` folder with 8 `.mat` files (~1.6 MB each)
4. These files can be committed to GitHub for student use

**Requirements**: `numpy`, `scipy`

**Note**: The original large `.mat` files (~50 MB each) should **not** be committed to the repository. They are excluded via `.gitignore`.

---

## Extensions and Further Work

After completing the notebooks, students can explore:

### Advanced Signal Processing
- Implement spectral kurtosis and the kurtogram algorithm
- Explore wavelet transforms for time-frequency analysis
- Apply empirical mode decomposition (EMD) or variational mode decomposition (VMD)

### Advanced Classification
- Experiment with other classifiers (SVM, Neural Networks, Gradient Boosting)
- Add more features (envelope spectrum peaks, spectral features, etc.)
- Apply feature selection and dimensionality reduction (PCA, feature importance)

### Handling Class Imbalance
- Use SMOTE (Synthetic Minority Over-sampling Technique)
- Apply class weighting in classifiers
- Explore ensemble methods for imbalanced data

### Real-Time Monitoring
- Implement online/streaming classification
- Develop a simple dashboard for real-time fault detection
- Explore anomaly detection for unsupervised fault detection

---

## References

### Envelope Analysis and Spectral Kurtosis
- Antoni, J. (2006). *The spectral kurtosis: a useful tool for characterising non-stationary signals.* Mechanical Systems and Signal Processing, 20(2), 282-307.
- Antoni, J. (2007). *Fast computation of the kurtogram for the detection of transient faults.* Mechanical Systems and Signal Processing, 21(1), 108-124.
- Randall, R. B., & Antoni, J. (2011). *Rolling element bearing diagnostics—A tutorial.* Mechanical Systems and Signal Processing, 25(2), 485-520.

### Classification and Evaluation Metrics
- Fawcett, T. (2006). *An introduction to ROC analysis.* Pattern Recognition Letters, 27(8), 861-874.
- Saito, T., & Rehmsmeier, M. (2015). *The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets.* PloS one, 10(3), e0118432.
- He, H., & Garcia, E. A. (2009). *Learning from imbalanced data.* IEEE Transactions on Knowledge and Data Engineering, 21(9), 1263-1284.

### Bearing Fault Diagnosis
- McFadden, P. D., & Smith, J. D. (1984). *Model for the vibration produced by a single point defect in a rolling element bearing.* Journal of Sound and Vibration, 96(1), 69-82.
- Lei, Y., et al. (2016). *Applications of machine learning to machine fault diagnosis: A review and roadmap.* Mechanical Systems and Signal Processing, 138, 106587.

---

## License

This project is provided for educational purposes. Please check with your institution regarding data sharing and usage policies.

---

## Contributing

This is an educational project designed for MSc engineering students. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

---

## Acknowledgments

This educational material was developed for hands-on laboratory sessions in vibration analysis and machine fault diagnosis.

---

## Contact

For questions or issues, please contact your course instructor or open an issue on GitHub.

---

**Happy learning!** 🎓⚙️
