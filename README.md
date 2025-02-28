## **Hamonic Density Analysis Tools**

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

## **Additional Notes for macOS and Linux Users**
macOS:

You may need to install Python with Tkinter support. If you installed Python from python.org, Tkinter is usually included by default. If you use Homebrew, you can run:

## **Installation**
Before using the tools, install the required dependencies:

```bash
pip install -r REQUIREMENTS.txt

## **Additional Notes for macOS and Linux Users**
macOS:

You may need to install Python with Tkinter support. If you installed Python from python.org, Tkinter is usually included by default. If you use Homebrew, you can run:

```
brew install python
```


