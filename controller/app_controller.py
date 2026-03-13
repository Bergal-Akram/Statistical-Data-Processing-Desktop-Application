from tkinter import filedialog, messagebox
import pandas as pd

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.data = pd.DataFrame()

    # ---------- DATA HANDLING ----------
    def set_data(self, data):
        if isinstance(data, pd.DataFrame):
            self.data = data
            self.model.set_data(data)

    # ---------- FILE OPERATIONS ----------
    def new_file(self):
        if not self.data.empty:
            choice = messagebox.askyesnocancel(
                "New File", "Save current work before creating new file?"
            )
            if choice is None:
                return
            if choice and not self.save_csv():
                return

        self.data = pd.DataFrame()
        self.model.set_data(self.data)
        self.view.show_univariee_page(data=self.data)

    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        try:
            self.data = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
            return
        
        self.model.set_data(self.data)
        self.view.show_univariee_page(data=self.data)

    def save_csv(self):
        if self.data.empty:
            messagebox.showwarning("Save CSV", "No data to save!")
            return False

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return False

        self.data.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"File saved at: {path}")
        return True

    def exit_app(self):
        self.view.quit()

    # ---------- UNIVARIATE ----------
    def calculate_statistic(self, stat_type, column):
        
        page = self.view.pages.get("univariee")
        if not page:
            return

        page.update_data()
        df = page.data
        self.set_data(df) 

        if column not in df.columns:
            messagebox.showerror("Error", f"Column '{column}' not found.")
            return

        series = df[column]
        result = None

        try:
            if stat_type == "Mean":
                result = self.model.calculate_mean(series)
            elif stat_type == "Median":
                result = self.model.calculate_median(series)
            elif stat_type == "Mode":
                result = self.model.calculate_mode(series) 
            elif stat_type == "Quantile":
                result = self.model.calculate_quantile(series)
            elif stat_type == "Frequency":
                result = self.model.calculate_frequency(series)
            elif stat_type == "Cumulative Frequency":
                result = self.model.calculate_cumulative_frequency(series)
            else:
                result = "Unknown operation"

            page.show_result(stat_type, column, result)

        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed for {stat_type}: {str(e)}")
            page.show_result(stat_type, column, "ERROR")


    # ---------- BIVARIATE ----------
    def calculate_bivariate(self, operation, x_col, y_col):
        page = self.view.pages.get("bivariee")
        if not page:
            return

        df = self.data

        if x_col not in df.columns or y_col not in df.columns:
            messagebox.showerror("Error", "Selected columns not found.")
            return

        x = df[x_col]
        y = df[y_col]

        if operation == "Covariance":
            result = self.model.covariance(x, y)
        elif operation == "Correlation":
            result = self.model.correlation(x, y)
        elif operation == "Linear Regression":
            result = self.model.linear_regression(x, y)
        else:
            result = "Unknown operation"

        page.show_result(operation, x_col, y_col, result)

    # ---------- ACP / PCA ----------
    def run_pca_step_by_step(self, selected_columns, n_components):
        if self.data.empty:
            raise ValueError("No data available for PCA.")

        self.model.set_data(self.data)
        return self.model.run_pca_step_by_step(selected_columns, n_components)