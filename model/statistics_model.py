import numpy as np
import pandas as pd
import math
from collections import Counter


class StatisticsModel:
    def __init__(self):
        self.data = pd.DataFrame()

    def set_data(self, data):
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()

    # ---------------- Univariate ----------------
    def calculate_mean(self, data):
        values = self._to_numeric_list(data)
        if not values:
            return None
        return sum(values) / len(values)

    def calculate_mode(self, data):
        values = [v for v in data if pd.notna(v)]
        if not values:
            return None
        
        counter = Counter(values)
        max_count = max(counter.values())
        
        modes = [key for key, count in counter.items() if count == max_count]
        return modes

    def calculate_median(self, data):
        values = sorted(self._to_numeric_list(data))
        n = len(values)
        if n == 0:
            return None
        mid = n // 2
        return (values[mid - 1] + values[mid]) / 2 if n % 2 == 0 else values[mid]

    def calculate_quantile(self, data):
        values = sorted(self._to_numeric_list(data))
        if not values:
            return None
        return {
            "Q1": self._get_quantile(values, 0.25),
            "Q2": self._get_quantile(values, 0.50),
            "Q3": self._get_quantile(values, 0.75),
        }

    def calculate_frequency(self, data):
        values = [v for v in data if pd.notna(v)]
        return dict(Counter(values))

    def calculate_cumulative_frequency(self, data):
        freq = self.calculate_frequency(data)
        cum_freq = {}
        total = 0
        for key in sorted(freq.keys()):
            total += freq[key]
            cum_freq[key] = total
        return cum_freq

    # ---------------- Bivariate ----------------
    def covariance(self, x, y):
        x_vals, y_vals = self._align_numeric_pairs(x, y)
        n = len(x_vals)
        if n < 2:
            return None

        mean_x = self.calculate_mean(x_vals)
        mean_y = self.calculate_mean(y_vals)

        total = sum((x_vals[i] - mean_x) * (y_vals[i] - mean_y) for i in range(n))
        return total / (n - 1)

    def correlation(self, x, y):
        cov = self.covariance(x, y)
        if cov is None:
            return None

        var_x = self.covariance(x, x)
        var_y = self.covariance(y, y)

        if var_x == 0 or var_y == 0:
            return None

        return cov / math.sqrt(var_x * var_y)

    def linear_regression(self, x, y):
        x_vals, y_vals = self._align_numeric_pairs(x, y)
        n = len(x_vals)
        if n < 2:
            return None, None

        mean_x = self.calculate_mean(x_vals)
        mean_y = self.calculate_mean(y_vals)

        num = sum((x_vals[i] - mean_x) * (y_vals[i] - mean_y) for i in range(n))
        den = sum((x_vals[i] - mean_x) ** 2 for i in range(n))

        if den == 0:
            return None, None

        slope = num / den
        intercept = mean_y - slope * mean_x
        return slope, intercept

    # ---------------- ACP / PCA ----------------
    def run_pca_step_by_step(self, columns, n_components=2):
        if self.data.empty:
            raise ValueError("No data available for PCA.")
    
        X = self.data[columns].apply(pd.to_numeric, errors='coerce').dropna().to_numpy(dtype=float)
        
        if X.shape[0] < 2:
             raise ValueError("Not enough valid data points for PCA after cleaning.")
    
        # 1.(Centering)
        mean = X.mean(axis=0)
        X_centered = X - mean
        
        # 2. (Scaling/Reduction)
        std = X.std(axis=0)
        # avoid divide with zero
        std[std == 0] = 1 
        X_reduced = X_centered / std
    
        cov_matrix = np.cov(X_reduced, rowvar=False)
        corr_matrix = np.corrcoef(X_reduced, rowvar=False)
    
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        individuals_matrix = X_reduced @ eigenvectors[:, :n_components]
        variables_matrix = eigenvectors[:, :n_components] * np.sqrt(eigenvalues[:n_components])
    
        df_centered = pd.DataFrame(X_centered, columns=columns)
        df_reduced = pd.DataFrame(X_reduced, columns=columns)
        df_cov = pd.DataFrame(cov_matrix, columns=columns, index=columns)
        df_corr = pd.DataFrame(corr_matrix, columns=columns, index=columns)
        df_eigenvectors = pd.DataFrame(eigenvectors, index=columns, columns=[f"Comp {i+1}" for i in range(len(columns))])
        df_individuals = pd.DataFrame(individuals_matrix, columns=[f"PC{i+1}" for i in range(individuals_matrix.shape[1])])
        df_variables = pd.DataFrame(variables_matrix, index=columns, columns=[f"PC{i+1}" for i in range(variables_matrix.shape[1])])
    
        return {
            "centered_matrix": df_centered,
            "reduced_matrix": df_reduced,
            "covariance_matrix": df_cov,
            "correlation_matrix": df_corr,
            "eigenvalues": eigenvalues,
            "eigenvectors": df_eigenvectors,
            "individuals_all": df_individuals,
            "variables_all": df_variables,
            "n_components": n_components  
        }
    
    # ---------------- Helpers ----------------
    def _to_numeric_list(self, data):
        return [float(v) for v in data if self._is_number(v)]

    def _align_numeric_pairs(self, x, y):
        pairs = [
            (float(a), float(b))
            for a, b in zip(x, y)
            if self._is_number(a) and self._is_number(b)
        ]
        if not pairs:
            return [], []
        return zip(*pairs) 

    def _is_number(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _get_quantile(self, sorted_values, p):
        n = len(sorted_values)
        if n == 0:
            return None
            
        index = p * (n - 1) 
        
        if index.is_integer():
            return sorted_values[int(index)]
        
        lower_index = int(index)
        upper_index = lower_index + 1
        fraction = index - lower_index
        
        if upper_index >= n:
            return sorted_values[lower_index]
        
        return sorted_values[lower_index] + fraction * (sorted_values[upper_index] - sorted_values[lower_index])