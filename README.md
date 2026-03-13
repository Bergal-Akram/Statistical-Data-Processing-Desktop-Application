# 📊 Statistical Data Processing Desktop Application

A modular statistical analysis desktop application built with Python using the Model–View–Controller (MVC) architecture.  
The application provides tools for univariate, bivariate, and multivariate statistical analysis, along with an interactive Self-Organizing Map (SOM) clustering demonstration.

The goal of this project is to demonstrate the implementation of core statistical algorithms and machine learning concepts from scratch, while maintaining a clean, scalable software architecture.

---

# 🎯 Project Objectives

The application was designed to:

- Provide a desktop interface for statistical data exploration.
- Implement fundamental statistical algorithms without relying on high-level machine learning libraries.
- Demonstrate proper separation of concerns using MVC architecture.
- Visualize statistical results and machine learning processes interactively.
- Combine statistics, linear algebra, and software engineering principles in a single tool.

---

# ⚙️ Technologies Used

- Python
- Tkinter – Desktop GUI framework
- Pandas – Data manipulation
- NumPy – Numerical computation
- Matplotlib – Data visualization

These technologies are widely used in the Python scientific ecosystem for data analysis and visualization.

Documentation:

- Python – https://docs.python.org
- NumPy – https://numpy.org
- Pandas – https://pandas.pydata.org
- Matplotlib – https://matplotlib.org

---

# 💻 Installation

Follow these steps to run the project locally.

## 1. Clone the repository

```bash
git clone https://github.com/Bergal-Akram/Statistical-Data-Processing-Desktop-Application.git
cd Statistical-Data-Processing-Desktop-Application
```

## 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

# ▶️ Run the Application

After installing the dependencies, run the application with:

```bash
python main.py
```

This will launch the desktop interface where you can:

- Load CSV datasets
- Perform statistical analysis
- Run PCA visualization
- Explore the Self-Organizing Map demo

# 🧠 Features

## 1️⃣ Dataset Management

The application supports basic data operations:

- Create a new dataset
- Load CSV files
- Edit dataset values
- Save datasets to CSV
- Manage data state within the application

All data handling is performed using **Pandas DataFrames**.

---

# 📈 Statistical Analysis

## Univariate Statistics

The application computes key descriptive statistics for selected variables:

- Mean
- Median
- Mode
- Quantiles (Q1, Q2, Q3)
- Frequency distribution
- Cumulative frequency

These metrics are implemented manually using Python logic and numerical operations.

---

## Bivariate Statistics

The application supports analysis between two variables:

- Covariance
- Pearson correlation
- Linear regression

Linear regression is implemented using the formula:

```
slope = Σ(xi − x̄)(yi − ȳ) / Σ(xi − x̄)²
```

```
intercept = ȳ − slope · x̄
```

Results are visualized with scatter plots and regression lines using **Matplotlib**.

---

# 📊 Principal Component Analysis (PCA)

The project includes a **step-by-step PCA implementation**.

Instead of using libraries such as `sklearn`, the algorithm is implemented manually using linear algebra operations.

## PCA Workflow

### Data Centering

Each variable is centered by subtracting its mean.

### Data Standardization

Data is scaled using standard deviation to produce a reduced matrix.

### Covariance Matrix Calculation

### Correlation Matrix Calculation

### Eigenvalue and Eigenvector Computation

Using NumPy linear algebra functions:

```python
numpy.linalg.eig()
```

### Component Ordering

Eigenvalues and eigenvectors are sorted by decreasing importance.

### Projection

The dataset is projected onto the new principal component space.

## Visualization

The PCA module provides:

- Individuals projection plot (2D / 3D)
- Correlation circle visualization
- Matrix outputs for intermediate steps

These visualizations help interpret variable influence and dimensionality reduction.

---

# 🤖 Self-Organizing Map (SOM) Demo

The application also contains a demonstration of a **Self-Organizing Map**, a type of unsupervised neural network.

A SOM maps high-dimensional data onto a lower-dimensional grid while preserving similarity relationships.

Reference:  
Kohonen Self-Organizing Maps  
https://www.sciencedirect.com/topics/computer-science/self-organizing-map

## SOM Characteristics in the Project

- 2×2 neuron grid
- Random weight initialization
- Euclidean distance for Best Matching Unit (BMU)
- Neighborhood learning
- Iterative training until convergence

### Weight update rule

```
w(t+1) = w(t) + α(x − w(t))
```

Where:

- **w** = neuron weight
- **x** = input vector
- **α** = learning rate

The system visually displays:

- neuron positions
- clustered data points
- similar vectors mapped to the same neuron

Training runs in a **separate thread** to avoid blocking the GUI.

---

# 🏗️ Software Architecture

The project follows the **Model–View–Controller (MVC)** pattern.

Reference:  
Gamma et al., _Design Patterns: Elements of Reusable Object-Oriented Software_

---

## Model

Responsible for all data processing and algorithm implementation.

Modules include:

- `statistics_model.py`
- `som_model.py`

Responsibilities:

- statistical calculations
- PCA computations
- SOM learning
- data storage

The model contains **no GUI logic**, ensuring clean separation.

---

## View

The user interface layer, implemented using Tkinter.

Pages include:

- Univariate statistics page
- Bivariate statistics page
- PCA analysis page
- SOM visualization page

Visualization is handled using **Matplotlib embedded in Tkinter**.

---

## Controller

Controllers coordinate communication between models and views.

Controllers include:

- `app_controller.py`
- `som_controller.py`

Responsibilities:

- user interaction management
- dataset loading and saving
- triggering statistical computations
- updating the GUI with results

The controller ensures the view never directly manipulates the model.

---

# 📁 Project Structure

```
project
│
├── controller
│   ├── app_controller.py
│   └── som_controller.py
│
├── model
│   ├── statistics_model.py
│   └── som_model.py
│
├── view
│   ├── main_view.py
│   └── pages
│       ├── univariee_page.py
│       ├── bivariee_page.py
│       ├── acp_page.py
│       └── som_page.py
│
└── main.py
```

---

# 🚀 Skills Demonstrated

This project demonstrates knowledge in several areas:

## Statistics

- descriptive statistics
- covariance and correlation
- regression analysis

## Linear Algebra

- eigenvalues
- eigenvectors
- dimensionality reduction

## Machine Learning

- unsupervised learning
- Self-Organizing Maps

## Software Engineering

- MVC architecture
- modular design
- separation of concerns
- threaded execution for GUI responsiveness

## Data Visualization

- interactive plots
- dimensionality reduction visualization
- clustering visualization

---

# 🔮 Possible Future Improvements

Potential improvements include:

- converting the GUI to **PyQt6** for more advanced interfaces
- adding **K-Means clustering**
- implementing **explained variance plots for PCA**
- supporting **large datasets**
- exporting analysis reports to **PDF**
- adding **unit tests for statistical algorithms**
