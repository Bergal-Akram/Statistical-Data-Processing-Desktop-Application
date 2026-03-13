import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BivarieePage(ttk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.controller = controller
        self.data = data if data is not None else pd.DataFrame()

        # ===== UI ELEMENTS =====
        ttk.Label(self, text="Bivariate Statistics", font=("Arial", 16, "bold")).pack(pady=10)

        # Form area
        form = ttk.Frame(self)
        form.pack(pady=10)

        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.op_var = tk.StringVar()

        ttk.Label(form, text="X column:").grid(row=0, column=0, padx=5, pady=5)
        self.x_box = ttk.Combobox(form, textvariable=self.x_var, state="readonly")
        self.x_box.grid(row=0, column=1)

        ttk.Label(form, text="Y column:").grid(row=1, column=0, padx=5, pady=5)
        self.y_box = ttk.Combobox(form, textvariable=self.y_var, state="readonly")
        self.y_box.grid(row=1, column=1)

        ttk.Label(form, text="Operation:").grid(row=2, column=0, padx=5, pady=5)
        self.op_box = ttk.Combobox(
            form, textvariable=self.op_var, state="readonly",
            values=["Covariance", "Correlation", "Linear Regression"]
        )
        self.op_box.grid(row=2, column=1)

        ttk.Button(self, text="Calculate", command=self.calculate).pack(pady=10)

        self.result_label = ttk.Label(self, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

        # Plot area
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def set_data(self, data: pd.DataFrame):
        """Load DataFrame and update combobox values"""
        self.data = data
        cols = list(data.columns)
        self.x_box["values"] = cols
        self.y_box["values"] = cols

    def calculate(self):
        """Perform selected operation"""
        x_col, y_col, op = self.x_var.get(), self.y_var.get(), self.op_var.get()

        if not (x_col and y_col and op):
            messagebox.showwarning("Warning", "Select X, Y, and an operation.")
            return
        if x_col == y_col:
            messagebox.showwarning("Warning", "X and Y must be different.")
            return

        try:
            x = pd.to_numeric(self.data[x_col], errors="coerce").dropna()
            y = pd.to_numeric(self.data[y_col], errors="coerce").dropna()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid column data: {e}")
            return

        if x.empty or y.empty:
            messagebox.showwarning("Warning", "Columns must have numeric data.")
            return

        # Perform operation
        if op == "Covariance":
            result = self.controller.model.covariance(x, y)
            self.result_label.config(text=f"Covariance = {result:.4f}")

        elif op == "Correlation":
            result = self.controller.model.correlation(x, y)
            self.result_label.config(text=f"Correlation = {result:.4f}")

        elif op == "Linear Regression":
            slope, intercept = self.controller.model.linear_regression(x, y)
            self.result_label.config(text=f"y = {slope:.4f}x + {intercept:.4f}")

        # Draw the plot
        self.draw_plot(op, x, y, slope if op == "Linear Regression" else None,
                       intercept if op == "Linear Regression" else None)

    def draw_plot(self, op, x, y, slope=None, intercept=None):
        """Draw scatter plot and regression line if needed"""
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        ax.scatter(x, y, label="Data")

        if op == "Linear Regression" and slope is not None:
            ax.plot(x, slope * x + intercept, color="red", label="Regression Line")

        ax.set_xlabel(self.x_var.get())
        ax.set_ylabel(self.y_var.get())
        ax.set_title(op)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
