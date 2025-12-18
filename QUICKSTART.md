# Quick Start Guide

## Setup (5 minutes)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-institution/bearing-envelope-analysis-lab.git
   cd bearing-envelope-analysis-lab
   ```

2. **Create and activate virtual environment**:
   
   **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

## Lab Structure

### Notebook 1: Bearing Envelope Analysis (~30 min)
- Load and visualize vibration data
- Apply band-pass filtering
- Compute envelope using Hilbert transform
- Extract time-domain features (RMS, peak, kurtosis)
- Compare healthy vs. faulty bearings

**Start here**: Open `Notebook1_BearingEnvelopeAnalysis.ipynb`

### Notebook 2: Fault Classification Metrics (~30 min)
- Build feature dataset from multiple samples
- Train Random Forest classifier
- Evaluate with confusion matrix
- Analyze ROC and Precision-Recall curves
- Understand class imbalance effects

**Continue with**: Open `Notebook2_BearingFaultMetrics.ipynb`

## Data Files

The `data/` folder contains 8 sample files (`.mat` format):
- 4 bearing conditions: H (Healthy), IR (Inner Race), OR (Outer Race), Roller
- 2 speeds: 353 rpm, 877 rpm
- Each file: 2 seconds of vibration data @ 20.48 kHz

Load with: `load_sample('H_353rpm_sample.mat')`

## Troubleshooting

**Jupyter not found?**
```bash
pip install jupyter
```

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Can't activate venv on Windows?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

After completing both notebooks:
- Explore the "Extensions" section in README.md
- Try implementing spectral kurtosis
- Experiment with other classifiers (SVM, Neural Networks)
- Apply different feature extraction techniques

## Need Help?

- Read the full [README.md](README.md) for detailed explanations
- Check notebook markdown cells for guidance
- All functions have docstrings explaining parameters
- Open an issue on GitHub if you encounter problems

Good luck! 🎓
