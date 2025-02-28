## **Hamonic Density Analysis Tools**

This repository contains a suite of Python scripts designed for the **density analysis** of musical structures. These tools compute **spectral moments**, measure **interval densities**, and analyze **spectral metrics** for different instruments across multiple operating systems (Windows, macOS, and Linux).

---

## Overview

This project provides both **command-line** and **graphical** tools to evaluate musical densities and spectral features. The primary objectives include:

- **Extracting spectral moments**: computing spectral centroid, spread, and skewness.
- **Measuring intervallic densities**: analyzing interval structures in microtonal and traditional scales.
- **Instrument-specific spectral calculations**: estimating density profiles for different instruments based on their spectral characteristics.
- **Data visualization**: generating interactive plots for spectral metrics, interval densities, and kernel density estimations.
- **Graphical Interface**: a Tkinter-based GUI that allows users to input musical structures and receive detailed analyses.

---

## Features

### 1. Spectral Analysis
- Computes **spectral centroid** (in frequency and note representation).
- Estimates **spectral spread** to measure variance in spectral distribution.
- Computes **spectral skewness**, indicating spectral asymmetry.

### 2. Interval Density Analysis
- Computes **interval-based density measurements** for musical structures.
- Supports **microtonal and traditional tuning systems**.

### 3. Instrument-Based Spectral Calculation
- Supports multiple instruments with **predefined spectral characteristics**.
- Can predict intermediate **dynamic levels** for missing data.
- Analyzes spectral behavior based on **amplitude-weighted densities**.

### 4. Data Visualization
- Plots spectral metrics for a given set of musical notes.
- Displays intervallic distributions using Gaussian-based decay models.
- Applies **Kernel Density Estimation (KDE)** to analyze spectral energy distributions.

### 5. Graphical Interface (Tkinter)
- Interactive UI for inputting musical notes, instruments, and dynamics.
- Real-time spectral and density analysis based on user input.
- Adjustable weighting factors for balancing different density calculations.

---

## Installation

Before using these tools, ensure you have **Python 3.7+** installed.

1. **Clone** or **download** this repository.
2. **Open a terminal** (Command Prompt on Windows, Terminal on macOS/Linux) in the repository directory.
3. Install the required dependencies:

   ```bash
   pip install -r REQUIREMENTS.txt
   ```

### Additional Notes for macOS and Linux Users

#### macOS
- **Tkinter Support**:  
  You may need to install Python with Tkinter support. If you installed Python from [python.org](https://www.python.org/), Tkinter is usually included.
- **Homebrew Users**:  
  If you use Homebrew, run:
  
  ```bash
  brew install python
  ```
  
  Ensure you're using the Homebrew-installed Python.
- **Display Issues**:  
  If you experience display issues, verify that **XQuartz** is installed (mainly for older macOS versions). Modern macOS systems should work with the native Tk.

#### Linux
- **Tkinter Support**:  
  Ensure you have Python 3 with Tkinter support. For Ubuntu/Debian-based systems, install with:
  
  ```bash
  sudo apt-get update
  sudo apt-get install python3 python3-tk
  ```
- **Other Distributions**:  
  Other distributions may have different package names; ensure the equivalent of `python3-tk` is installed.

#### Windows
- The official Python installer from [python.org](https://www.python.org/) includes Tkinter by default. Just make sure to add Python to your system `PATH` during installation.

---

## Usage

### Graphical Interface
1. Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
2. Navigate to the repository directory.
3. Launch the graphical interface:

   ```bash
   python Main.py
   ```

   A Tkinter window will open, allowing you to select notes, instruments, dynamics, and other parameters for spectral density analysis.

### Command-Line Execution
You can also run individual scripts for specific analyses:

- **`plot_metr_espectrais.py`**  
  Generates plots for spectral metric calculations (e.g., spectral centroid, spread).

- **`advanced_density_analysis.py`**  
  Computes spectral moments (centroid, spread, skewness), converts MIDI values to frequency and note names, and applies Kernel Density Estimation (KDE).

- **`density_calculations.py`**  
  Provides functions to compute interval density, overall spectral mass, and volume.

**Example usage for `plot_metr_espectrais.py`:**

```bash
python plot_metr_espectrais.py
```

---

## Module Breakdown

1. **Main.py**
   - Launches the **graphical user interface**.
   - Handles user input and processes spectral density calculations.
   - Allows users to select instruments, enter notes, and adjust weight factors.

2. **plot_metr_espectrais.py**
   - Converts MIDI note numbers into musical note names.
   - Computes and visualizes spectral metrics, including centroid and spread.
   - Displays results in an interactive plot.

3. **advanced_density_analysis.py**
   - Computes **spectral centroid, spread, and skewness**.
   - Converts MIDI values to frequency and note names.
   - Applies **Kernel Density Estimation** to improve spectral resolution.

4. **density_calculations.py**
   - Computes **total density** for a given musical segment.
   - Estimates **intervallic densities** based on semitone distances.
   - Determines overall **spectral mass** and **volume**.

5. **densidade_intervalar.py**
   - Implements **microtonal interval density** calculations.
   - Defines a custom **24-tone microtonal scale**.
   - Uses a **Gaussian decay** function to model intervallic strength.

6. **Den_alg_Lin_10.py**
   - Performs **Gaussian Process Regression (GPR)** and **XGBoost-based** predictions.
   - Uses machine learning to interpolate missing density values.

7. **flauta.py**
   - Stores **predefined spectral data** for a flute.
   - Predicts spectral characteristics based on **dynamic levels**.

---

## Dependencies

The project requires the following Python packages:

```plaintext
numpy
matplotlib
scipy
pandas
scikit-learn
xgboost
tkinter
```

To install all dependencies, run:

```bash
pip install -r REQUIREMENTS.txt
```

---

## License and Attribution

This project is distributed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**. You must give appropriate credit to the author, as well as to the supporting and funding institutions, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

---

## Acknowledgments

This project was developed by **Luís Raimundo**, created with the **support and funding** of **Fundação para a Ciência e Tecnologia (FCT)** and **Universidade NOVA de Lisboa**.
