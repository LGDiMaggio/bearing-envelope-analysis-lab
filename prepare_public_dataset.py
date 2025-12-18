"""
Data Preparation Script for Public Bearing Vibration Dataset
==============================================================

PURPOSE:
--------
This script is intended for INSTRUCTORS ONLY. It processes the private full-length
.mat files containing bearing vibration data and creates a reduced public dataset
suitable for sharing with students on GitHub.

The script:
1. Reads the original .mat files from the private data folder
2. Extracts only the first 2 seconds of data from each recording
3. Saves simplified .npz files containing acceleration and tacho data
4. Creates a 'data/' folder with sample files that students will use

REQUIREMENTS:
-------------
- Access to the private raw data folder containing the original .mat files
- Python packages: numpy, scipy

USAGE:
------
1. Ensure the RAW_DATA_PATH below points to your private data folder
2. Run this script: python prepare_public_dataset.py
3. The script will create a 'data/' folder with .npz sample files
4. These .npz files can be committed to GitHub for student use

Author: Generated for MSc Engineering Course on Bearing Fault Diagnosis
Date: 2025
"""

import os
import numpy as np
from scipy.io import loadmat, savemat

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Path to the private raw data folder (INSTRUCTOR ONLY)
RAW_DATA_PATH = r"C:\Users\d044653\OneDrive - Politecnico di Torino\e-rotors-module\Data"

# Output folder for public sample data
OUTPUT_DIR = "data"

# Duration of samples to extract (seconds)
SAMPLE_DURATION = 2.0

# List of expected .mat files
MAT_FILES = [
    "H_353rpm_124.8kN_0kN.mat",
    "H_877rpm_124.8kN_0kN.mat",
    "IR_353rpm_124.8kN_0kN.mat",
    "IR_877rpm_124.8kN_0kN.mat",
    "OR_353rpm_124.8kN_0kN.mat",
    "OR_877rpm_124.8kN_0kN.mat",
    "Roller_353rpm_124.8kN_0kN.mat",
    "Roller_877rpm_124.8kN_0kN.mat",
]

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def parse_filename(filename):
    """
    Extract condition and nominal rpm from filename.
    
    Parameters:
    -----------
    filename : str
        Name of .mat file (e.g., 'IR_877rpm_124.8kN_0kN.mat')
    
    Returns:
    --------
    condition : str
        Bearing condition ('H', 'IR', 'OR', or 'Roller')
    rpm_nominal : int
        Nominal rotational speed (353 or 877)
    """
    # Remove .mat extension
    name = filename.replace('.mat', '')
    
    # Split by underscore
    parts = name.split('_')
    
    # First part is condition
    condition = parts[0]
    
    # Second part contains rpm
    rpm_str = parts[1].replace('rpm', '')
    rpm_nominal = int(rpm_str)
    
    return condition, rpm_nominal


def find_signal_by_label(mat_data, label_target):
    """
    Find Signal_k in mat_data where y_values.quantity.label matches label_target.
    
    Parameters:
    -----------
    mat_data : dict
        Loaded MATLAB structure
    label_target : str
        Target label to search for ('g', 'rpm', 's', etc.)
    
    Returns:
    --------
    signal : dict or None
        The matching Signal_k structure, or None if not found
    signal_name : str or None
        Name of the signal (e.g., 'Signal_1')
    """
    # Iterate through all keys in mat_data
    for key in mat_data.keys():
        if key.startswith('Signal_'):
            signal = mat_data[key]
            
            # Navigate to y_values.quantity.label
            try:
                # Access the structured array
                y_values = signal['y_values'][0, 0]
                quantity = y_values['quantity'][0, 0]
                label_array = quantity['label']
                
                # Label is stored as nested array, extract the actual string array
                if isinstance(label_array, np.ndarray) and label_array.dtype == object:
                    # Extract the inner array
                    label_array = label_array[0, 0]
                
                # Convert array of characters to string
                if isinstance(label_array, np.ndarray):
                    if label_array.dtype.kind == 'U':  # Unicode string array
                        label_str = ''.join(label_array.flatten())
                    else:
                        label_str = str(label_array)
                else:
                    label_str = str(label_array)
                
                if label_str == label_target:
                    return signal, key
            except (KeyError, IndexError, TypeError) as e:
                continue
    
    return None, None


def extract_acceleration_data(signal, sensor_index=None, duration=2.0):
    """
    Extract acceleration data for a specific sensor or all sensors.
    
    Parameters:
    -----------
    signal : dict
        MATLAB Signal structure containing acceleration data
    sensor_index : int or None
        Sensor index (0-based). If None, uses all sensors or first if only one.
    duration : float
        Duration in seconds to extract
    
    Returns:
    --------
    time : ndarray
        Time vector (re-zeroed to start from 0)
    acc_m_s2 : ndarray
        Acceleration in m/s²
    acc_g : ndarray
        Acceleration in g
    fs : float
        Sampling frequency in Hz
    actual_sensor_index : int
        The actual sensor index used
    """
    # Extract y_values and x_values
    y_values = signal['y_values'][0, 0]
    x_values = signal['x_values'][0, 0]
    
    # Get acceleration values (all sensors)
    # Data is wrapped in a (1, 1) array, extract the actual data
    acc_wrapper = y_values['values']
    
    # Extract the actual data array from the wrapper
    if isinstance(acc_wrapper, np.ndarray) and acc_wrapper.shape == (1, 1):
        acc_all_sensors = acc_wrapper[0, 0]
    else:
        acc_all_sensors = acc_wrapper
    
    # Now acc_all_sensors should have shape (n_samples, 4) for 4 sensors
    if acc_all_sensors.ndim == 2:
        n_samples_total, n_sensors = acc_all_sensors.shape
        
        if sensor_index is not None and sensor_index < n_sensors:
            # Use requested sensor (sensor 4 = index 3)
            acc_m_s2_full = acc_all_sensors[:, sensor_index]
            actual_sensor_index = sensor_index
        else:
            # Use last sensor as fallback
            actual_sensor_index = n_sensors - 1
            acc_m_s2_full = acc_all_sensors[:, actual_sensor_index]
    elif acc_all_sensors.ndim == 1:
        # Single sensor or already extracted
        acc_m_s2_full = acc_all_sensors
        actual_sensor_index = 0
    else:
        # Unexpected shape
        raise ValueError(f"Unexpected acceleration data shape: {acc_all_sensors.shape}")
    
    # Get conversion factor from m/s² to g
    try:
        unit_transform = y_values['quantity'][0, 0]['unit_transformation'][0, 0]
        factor_array = unit_transform['factor']
        # Extract scalar from nested array
        if isinstance(factor_array, np.ndarray):
            factor_to_g = float(factor_array.flatten()[0])
        else:
            factor_to_g = float(factor_array)
    except (KeyError, IndexError, TypeError) as e:
        # Default factor if not found
        factor_to_g = 0.1020
    
    # Build time vector
    start_value_array = x_values['start_value']
    increment_array = x_values['increment']
    number_of_values_array = x_values['number_of_values']
    
    # Extract scalars from nested arrays
    start_value = float(start_value_array.flatten()[0])
    increment = float(increment_array.flatten()[0])
    number_of_values = int(number_of_values_array.flatten()[0])
    
    time_full = start_value + np.arange(number_of_values) * increment
    fs = 1.0 / increment
    
    # Truncate to desired duration
    n_samples = int(duration * fs)
    n_samples = min(n_samples, len(time_full))
    
    time = time_full[:n_samples] - time_full[0]  # Re-zero time
    acc_m_s2 = acc_m_s2_full[:n_samples]
    acc_g = acc_m_s2 * factor_to_g
    
    return time, acc_m_s2, acc_g, fs, actual_sensor_index


def extract_rpm_data(signal, duration=2.0):
    """
    Extract tacho rpm data.
    
    Parameters:
    -----------
    signal : dict
        MATLAB Signal structure containing rpm data
    duration : float
        Duration in seconds to extract
    
    Returns:
    --------
    time_rpm : ndarray
        Time vector for rpm data
    rpm : ndarray
        Rotational speed in rpm
    fs_rpm : float
        Sampling frequency of rpm data in Hz
    mean_rpm : float
        Mean rpm over the extracted duration
    """
    # Extract y_values and x_values
    y_values = signal['y_values'][0, 0]
    x_values = signal['x_values'][0, 0]
    
    # Get rpm values (stored in rad/s)
    rpm_wrapper = y_values['values']
    
    # Extract the actual data array from the wrapper
    if isinstance(rpm_wrapper, np.ndarray) and rpm_wrapper.shape == (1, 1):
        rpm_rad_s = rpm_wrapper[0, 0].flatten()
    else:
        rpm_rad_s = rpm_wrapper.flatten()
    
    # Get conversion factor from rad/s to rpm
    try:
        unit_transform = y_values['quantity'][0, 0]['unit_transformation'][0, 0]
        factor_array = unit_transform['factor']
        # Extract scalar from nested array
        if isinstance(factor_array, np.ndarray):
            factor_to_rpm = float(factor_array.flatten()[0])
        else:
            factor_to_rpm = float(factor_array)
    except (KeyError, IndexError, TypeError) as e:
        # Default factor: rad/s to rpm = (60 / 2*pi) ≈ 9.5493
        factor_to_rpm = 9.5493
    
    # Convert to rpm
    rpm_full = rpm_rad_s * factor_to_rpm
    
    # Build time vector
    start_value_array = x_values['start_value']
    increment_array = x_values['increment']
    number_of_values_array = x_values['number_of_values']
    
    # Extract scalars from nested arrays
    start_value = float(start_value_array.flatten()[0])
    increment = float(increment_array.flatten()[0])
    number_of_values = int(number_of_values_array.flatten()[0])
    
    time_rpm_full = start_value + np.arange(number_of_values) * increment
    fs_rpm = 1.0 / increment
    
    # Truncate to desired duration
    n_samples = int(duration * fs_rpm)
    n_samples = min(n_samples, len(time_rpm_full))
    
    time_rpm = time_rpm_full[:n_samples] - time_rpm_full[0]  # Re-zero time
    rpm = rpm_full[:n_samples]
    mean_rpm = np.mean(rpm)
    
    return time_rpm, rpm, fs_rpm, mean_rpm


def process_mat_file(mat_path, condition, rpm_nominal, duration=2.0):
    """
    Process a single .mat file and extract 2-second samples.
    
    Parameters:
    -----------
    mat_path : str
        Path to .mat file
    condition : str
        Bearing condition
    rpm_nominal : int
        Nominal rotational speed
    duration : float
        Duration to extract in seconds
    
    Returns:
    --------
    sample_data : dict
        Dictionary containing all extracted data
    """
    print(f"  Processing {os.path.basename(mat_path)}...")
    
    # Load .mat file (use default loading, not struct_as_record)
    mat_data = loadmat(mat_path)
    
    # Find acceleration signal (label = 'g')
    acc_signal, acc_signal_name = find_signal_by_label(mat_data, 'g')
    if acc_signal is None:
        raise ValueError(f"Could not find acceleration signal in {mat_path}")
    
    print(f"    Found acceleration signal: {acc_signal_name}")
    
    # Extract acceleration data for sensor 4 (index 3)
    time_acc, acc_m_s2, acc_g, fs_acc, sensor_idx = extract_acceleration_data(
        acc_signal, sensor_index=3, duration=duration
    )
    
    print(f"    Acceleration: {len(time_acc)} samples at {fs_acc:.1f} Hz (sensor {sensor_idx + 1})")
    
    # Find tacho rpm signal (label = 'rpm')
    rpm_signal, rpm_signal_name = find_signal_by_label(mat_data, 'rpm')
    if rpm_signal is None:
        print(f"    Warning: Could not find rpm signal in {mat_path}")
        time_rpm = np.array([])
        rpm = np.array([])
        fs_rpm = 0.0
        mean_rpm = rpm_nominal  # Use nominal value as fallback
    else:
        print(f"    Found rpm signal: {rpm_signal_name}")
        time_rpm, rpm, fs_rpm, mean_rpm = extract_rpm_data(rpm_signal, duration=duration)
        print(f"    RPM: {len(time_rpm)} samples at {fs_rpm:.1f} Hz, mean = {mean_rpm:.1f} rpm")
    
    # Package into dictionary
    sample_data = {
        'time_acc': time_acc,
        'acc_m_s2': acc_m_s2,
        'acc_g': acc_g,
        'fs_acc': fs_acc,
        'time_rpm': time_rpm,
        'rpm': rpm,
        'fs_rpm': fs_rpm,
        'mean_rpm': mean_rpm,
        'condition': condition,
        'rpm_nominal': rpm_nominal,
    }
    
    return sample_data


# ==============================================================================
# MAIN PROCESSING
# ==============================================================================

def main():
    """Main processing function."""
    
    print("="*70)
    print("Bearing Vibration Data Preparation Script")
    print("="*70)
    print()
    print("This script extracts 2-second samples from the private dataset")
    print("and creates a public dataset for student use.")
    print()
    
    # Check if raw data path exists
    if not os.path.exists(RAW_DATA_PATH):
        print(f"ERROR: Raw data path does not exist: {RAW_DATA_PATH}")
        print("Please update RAW_DATA_PATH in the script.")
        return
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}/")
    print()
    
    # Process each .mat file
    processed_files = []
    
    for mat_file in MAT_FILES:
        mat_path = os.path.join(RAW_DATA_PATH, mat_file)
        
        if not os.path.exists(mat_path):
            print(f"WARNING: File not found: {mat_path}")
            print(f"         Skipping...")
            print()
            continue
        
        # Parse filename
        condition, rpm_nominal = parse_filename(mat_file)
        
        print(f"[{len(processed_files)+1}/{len(MAT_FILES)}] {mat_file}")
        print(f"  Condition: {condition}, Nominal RPM: {rpm_nominal}")
        
        try:
            # Process file
            sample_data = process_mat_file(
                mat_path, condition, rpm_nominal, duration=SAMPLE_DURATION
            )
            
            # Create output filename (.mat only)
            output_filename = f"{condition}_{rpm_nominal}rpm_sample.mat"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # Save to .mat (for MATLAB and Python compatibility)
            savemat(output_path, sample_data, oned_as='column')
            
            print(f"    Saved to: {output_filename}")
            processed_files.append(output_filename)
            
        except Exception as e:
            print(f"    ERROR processing file: {e}")
        
        print()
    
    # Print summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Successfully processed {len(processed_files)} files:")
    for fname in processed_files:
        print(f"  - {fname}")
    print()
    print(f"All sample files (.mat format) are in the '{OUTPUT_DIR}/' folder.")
    print("These files can be used with both MATLAB and Python (scipy.io.loadmat).")
    print("Ready to commit to GitHub for student use.")
    print()
    
    # Print basic statistics
    print("Basic statistics of the public dataset:")
    print("-" * 70)
    
    conditions_dict = {'H': 0, 'IR': 0, 'OR': 0, 'Roller': 0}
    rpms_dict = {353: 0, 877: 0}
    
    for fname in processed_files:
        data = loadmat(os.path.join(OUTPUT_DIR, fname))
        # Extract condition and rpm_nominal from loaded mat data
        cond = str(data['condition'][0]) if hasattr(data['condition'], '__len__') else str(data['condition'])
        rpm_nom = int(data['rpm_nominal'].flatten()[0])
        
        if cond in conditions_dict:
            conditions_dict[cond] += 1
        if rpm_nom in rpms_dict:
            rpms_dict[rpm_nom] += 1
    
    print(f"Conditions:")
    for cond, count in conditions_dict.items():
        print(f"  {cond:8s}: {count} files")
    
    print(f"\nRotational speeds:")
    for rpm, count in rpms_dict.items():
        print(f"  {rpm:4d} rpm: {count} files")
    
    print("\nEach file contains ~2 seconds of data from sensor 4 (acceleration)")
    print("and tacho rpm measurements.")
    print("="*70)


if __name__ == "__main__":
    main()
