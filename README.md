README.md# Spectral Density Analysis Tools

This repository contains a suite of Python scripts designed for the spectral analysis of musical structures. These tools compute spectral moments, measure interval densities, and analyze spectral metrics for different instruments.

## **Overview**

The project provides both command-line and graphical tools to evaluate musical densities and spectral features. The primary objectives of this toolset include:
- **Extracting spectral moments**: computing spectral centroid, spread, and skewness.
- **Measuring intervallic densities**: analyzing interval structures in microtonal and traditional scales.
- **Instrument-specific spectral calculations**: estimating density profiles for different instruments based on their spectral characteristics.
- **Data visualization**: generating interactive plots for spectral metrics, interval densities, and kernel density estimations.
- **Graphical Interface**: a Tkinter-based GUI that allows users to input musical structures and receive detailed analyses.

---

## **Features**
### **1. Spectral Analysis**
- Computes **spectral centroid** (in frequency and note representation).
- Estimates **spectral spread** to measure variance in spectral distribution.
- Computes **spectral skewness**, indicating spectral asymmetry.

### **2. Interval Density Analysis**
- Computes **interval-based density measurements** for musical structures.
- Supports **microtonal and traditional tuning systems**.

### **3. Instrument-Based Spectral Calculation**
- Supports multiple instruments with **predefined spectral characteristics**.
- Can predict intermediate **dynamic levels** for missing data.
- Analyzes spectral behavior based on **amplitude-weighted densities**.

### **4. Data Visualization**
- Plots spectral metrics for a given set of musical notes.
- Displays intervallic distributions using Gaussian-based decay models.
- Applies **Kernel Density Estimation (KDE)** to analyze spectral energy distributions.

### **5. Graphical Interface (Tkinter)**
- Interactive UI for inputting musical notes, instruments, and dynamics.
- Real-time spectral and density analysis based on user input.
- Adjustable weighting factors for balancing different density calculations.

---

## **Installation**
Before using the tools, install the required dependencies:

```bash
pip install -r REQUIREMENTS.txt

Usage
Graphical Interface
Run the main script to launch the interactive GUI for spectral analysis:

python Main.py

Command-Line Execution
You can also run individual scripts for specific analyses:

plot_metr_espectrais.py - Generates plots for spectral metric calculations.
advanced_density_analysis.py - Computes spectral moments (centroid, spread, skewness).
density_calculations.py - Provides interval density computations.
Example usage for plot_metr_espectrais.py:

python plot_metr_espectrais.py

Module Breakdown
1. Main.py
Launches the graphical user interface.
Handles user input and processes spectral density calculations.
Allows users to select instruments, enter notes, and adjust weight factors.
2. plot_metr_espectrais.py
Converts MIDI note numbers into musical note names.
Computes and visualizes spectral metrics, including centroid and spread.
Displays results in an interactive plot.
3. advanced_density_analysis.py
Computes spectral centroid, spread, and skewness.
Converts MIDI values to frequency and note names.
Applies Kernel Density Estimation to improve spectral resolution.
4. density_calculations.py
Computes total density for a given musical segment.
Estimates intervallic densities based on semitone distances.
Determines overall spectral mass and volume.
5. densidade_intervalar.py
Implements microtonal interval density calculations.
Defines a custom 24-tone microtonal scale.
Uses a Gaussian decay function to model intervallic strength.
6. Den_alg_Lin_10.py
Performs Gaussian Process Regression (GPR) and XGBoost-based predictions.
Uses machine learning to interpolate missing density values.
7. flauta.py
Stores predefined spectral data for a flute.
Predicts spectral characteristics based on dynamic levels.

Dependencies
The project requires the following Python packages:

numpy
matplotlib
scipy
pandas
scikit-learn
xgboost
tkinter


To install all dependencies, use:

pip install -r REQUIREMENTS.txt


Acknowledgments
This project was developed with support from Fundação para a Ciência e Tecnologia (FCT) and Universidade NOVA de Lisboa.



