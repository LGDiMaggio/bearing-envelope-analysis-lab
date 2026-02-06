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
5. **Understand binary classification** for bearing fault detection (Healthy vs Faulty)
6. **Interpret classification metrics** (accuracy, precision, recall, F1-score)
7. **Analyze confusion matrices** to diagnose classifier performance
8. **Use ROC and Precision-Recall curves** to evaluate diagnostic systems
9. **Understand the impact of class imbalance** on model evaluation

---

## Repository Structure

```
.
├── README.md                                  # This file
├── QUICKSTART.md                               # Quick start guide for students
├── requirements.txt                            # Python dependencies
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

## Bearing Diagnostics Overview

![Bearing Diagnostics](images/Bearing_diagnostics.png)

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
- Git (for cloning the repository)

### Quick Start

1. **Install Git** (if not already installed):
   
   **Windows**:
   - Download Git from [git-scm.com](https://git-scm.com/download/win)
   - Run the installer and follow the setup wizard (default options work fine)
   - Verify installation: `git --version`

   **macOS**:
   - Install via Homebrew: `brew install git`
   - Or download from [git-scm.com](https://git-scm.com/download/mac)
   - Or install Xcode Command Line Tools: `xcode-select --install`

   **Linux** (Debian/Ubuntu):
   ```bash
   sudo apt-get update && sudo apt-get install git
   ```

   **Linux** (Fedora/RHEL):
   ```bash
   sudo dnf install git
   ```

   After installation, configure your Git identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/LGDiMaggio/bearing-envelope-analysis-lab.git
   cd bearing-envelope-analysis-lab
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Launch Jupyter**:
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

- Understanding binary classification for bearing diagnostics (Healthy vs Faulty)
- Simulating realistic diagnostic scenarios with different error patterns
- Computing and interpreting classification metrics:
  - **Accuracy**
  - **Precision**
  - **Recall**
  - **F1-score**
- Visualizing the **confusion matrix** for binary classification
- Understanding **decision thresholds** and their impact on performance
- Plotting **ROC curves** and computing **AUC**
- Plotting **Precision-Recall curves** and computing **Average Precision**
- Understanding the impact of **class imbalance** on evaluation metrics

**Key takeaways**:
- Accuracy alone is misleading, especially with imbalanced datasets
- Precision and recall provide insight into false positives and false negatives
- For safety-critical applications, prioritize **recall** (catch all faults)
- PR curves are more informative than ROC curves for imbalanced problems
- Always examine the confusion matrix to diagnose system weaknesses

**Note**: This notebook uses **simulated scenarios** to teach metrics concepts, not actual model training. It focuses on understanding how to evaluate diagnostic systems.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

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
