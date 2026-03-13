# acm 
# drop column or rows

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn import datasets

class UnivarieePage(ttk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.controller = controller
        if data is None:
            self.data = pd.DataFrame({
                "Age": [25, 30, 28],
                "Weight": [70, 60, 80],
                "Height": [170, 160, 180]
            })
        else:
            self.data = data


        # GUI elements
        self._create_widgets()
        self._fill_table()

    # ======== Create GUI ========
    def _create_widgets(self):
        # Top buttons
        top = ttk.Frame(self)
        top.pack(pady=5)
        ttk.Button(top, text="Add Row", command=self.add_row).grid(row=0, column=0, padx=5)
        ttk.Button(top, text="Add Column", command=self.add_column).grid(row=0, column=1, padx=5)
        ttk.Button(top, text="Remove Row", command=self.remove_row).grid(row=0, column=5, padx=5)
        ttk.Button(top, text="Remove Column", command=self.remove_column).grid(row=0, column=6, padx=5)


        # Sklearn dataset selector
        ttk.Label(top, text="Load Dataset:").grid(row=0, column=2, padx=5)
        self.dataset_var = tk.StringVar()
        self.dataset_box = ttk.Combobox(
            top,
            textvariable=self.dataset_var,
            state="readonly",
            values=["Iris", "Wine", "Diabetes", "Breast Cancer"]
        )
        self.dataset_box.grid(row=0, column=3, padx=5)
        ttk.Button(top, text="Load", command=self.load_sklearn_dataset).grid(row=0, column=4, padx=5)

        # Table with scroll
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="x", padx=10, pady=5)
        self.tree = ttk.Treeview(table_frame, show="headings", height=8)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(table_frame, command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<Double-1>", self.edit_cell)

        # Bottom controls
        bottom = ttk.Frame(self)
        bottom.pack(pady=5)
        ttk.Label(bottom, text="Column:").grid(row=0, column=0, padx=5)
        self.col_var = tk.StringVar()
        self.col_box = ttk.Combobox(bottom, textvariable=self.col_var, state="readonly")
        self.col_box.grid(row=0, column=1, padx=5)
        ttk.Label(bottom, text="Operation:").grid(row=0, column=2, padx=5)
        self.op_var = tk.StringVar()
        self.op_box = ttk.Combobox(
            bottom, textvariable=self.op_var, state="readonly",
            values=["Mean", "Median", "Mode", "Quantile", "Frequency", "Cumulative Frequency"]
        )
        self.op_box.grid(row=0, column=3, padx=5)
        ttk.Button(bottom, text="Calculate", command=self.calculate).grid(row=0, column=4, padx=10)

        # Result label 
        self.result_label = ttk.Label(self, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

        # NEW: Scrollable Text Frame for detailed results (Frequency, Quantile, etc.)
        self.detail_frame = ttk.Frame(self)
        self.detail_frame.pack_forget() 
        
        # Text Widget
        self.detail_text = tk.Text(self.detail_frame, height=5, wrap="none", bg="#f0f0f0")
        self.detail_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        self.detail_scroll = ttk.Scrollbar(self.detail_frame, command=self.detail_text.yview)
        self.detail_scroll.pack(side="right", fill="y")
        self.detail_text.config(yscrollcommand=self.detail_scroll.set)

        # Plot frame
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ======== Fill Table ========
    def _fill_table(self):
        # delete old column
        self.tree["columns"] = []
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # add new column
        if not self.data.empty:
            self.tree["columns"] = list(self.data.columns)
            for col in self.data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            for _, row in self.data.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.col_box["values"] = list(self.data.columns)

    # ======== Edit Cell ========
    def edit_cell(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not item or not col:
            return
        col_idx = int(col.replace("#", "")) - 1
        x, y, w, h = self.tree.bbox(item, col)
        value = self.tree.set(item, self.tree["columns"][col_idx])
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, value)
        entry.focus()

        def save(event=None):
            self.tree.set(item, self.tree["columns"][col_idx], entry.get())
            entry.destroy()

        entry.bind("<Return>", save)
        entry.bind("<FocusOut>", save)

    # ======== Add Row ========
    def add_row(self):
        if self.data.empty:
            messagebox.showwarning("Warning", "No columns exist.")
            return
        new_values = []
        for col in self.data.columns:
            val = simpledialog.askstring("New Row", f"Enter value for '{col}':")
            new_values.append(val)
        self.tree.insert("", "end", values=new_values)

    # ======== Add Column ========
    def add_column(self):
        new_col = simpledialog.askstring("Column Name", "Enter new column name:")
        if not new_col:
            return
        self.data[new_col] = ""
        self.refresh_table()

    # ======== Remove Selected Row ========
    def remove_row(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to remove.")
            return
        for item in selected:
            self.tree.delete(item)
        self.update_data()  # sync with self.data

    # ======== Remove Column ========
    def remove_column(self):
        col_to_remove = simpledialog.askstring("Remove Column", "Enter column name to remove:")
        if not col_to_remove:
            return
        if col_to_remove not in self.data.columns:
            messagebox.showerror("Error", f"Column '{col_to_remove}' does not exist.")
            return
        self.data.drop(columns=[col_to_remove], inplace=True)
        self.refresh_table()

    # ======== Refresh Table ========
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self._fill_table()

    # ======== Sync Data ========
    def update_data(self):
        rows = [self.tree.item(i)["values"] for i in self.tree.get_children()]
        columns = self.tree["columns"]
        
        if columns and rows:
            self.data = pd.DataFrame(rows, columns=columns)
        elif columns and not rows:
             self.data = pd.DataFrame(columns=columns)
        else:
             self.data = pd.DataFrame() 

        self.controller.set_data(self.data)

    # ======== Calculate Operation (CORRECTED) ========
    def calculate(self):
        col, op = self.col_var.get(), self.op_var.get()
        if not col or not op:
            messagebox.showwarning("Warning", "Select a column and operation.")
            return

        self.update_data()
        
        # check type of data before send to controller
        is_numeric_op = op in ["Mean", "Median", "Quantile"]
        
        if is_numeric_op:
            numeric_check = pd.to_numeric(self.data[col], errors="coerce").dropna()
            if numeric_check.empty:
                messagebox.showwarning("Warning", f"Column '{col}' must contain numbers for '{op}'.")
                return

        # send to controller
        self.controller.calculate_statistic(op, col)
        
        # plot result
        self.draw_chart(op, col)
        
    # ======== Show Result (CORRECTED to handle Text Widget) ========
    def show_result(self, stat_type, column, result):
        self.detail_text.delete('1.0', tk.END)
        self.detail_frame.pack_forget()
        
        formatted_result = ""

        if result is None:
            formatted_result = "N/A"
            self.result_label.config(text=f"{stat_type} of {column}: {formatted_result}")

        elif stat_type in ["Quantile", "Frequency", "Cumulative Frequency"]:
            
            self.result_label.config(text=f"{stat_type} of {column}: (See details below)")

            detail_text_content = f"--- {stat_type} Result for {column} ---\n\n"
            
            for k, v in result.items():
                if isinstance(v, float):
                    detail_text_content += f"{k}: {v:.4f}\n"
                else:
                    detail_text_content += f"{k}: {v}\n"
            
            self.detail_text.insert(tk.END, detail_text_content)
            self.detail_frame.pack(fill="x", padx=10, pady=5) 
        
        elif stat_type == "Mode":
            formatted_result = ", ".join(map(str, result))
            self.result_label.config(text=f"{stat_type} of {column}: {formatted_result}")

        else:
            formatted_result = f"{result:.4f}" if isinstance(result, float) else str(result)
            self.result_label.config(text=f"{stat_type} of {column}: {formatted_result}")


    # ======== Draw Chart ========
    def draw_chart(self, op, col):
       
        for w in self.plot_frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        
        numeric = pd.to_numeric(self.data[col], errors="coerce").dropna()
    
        if op == "Mean":
            if not numeric.empty:
                mean_val = numeric.mean() 
                ax.hist(numeric, bins=10, color='skyblue', edgecolor='black')
                ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f"Mean={mean_val:.2f}")
                ax.set_title(f"Histogram with Mean of {col}")
                ax.legend()
            else:
                 ax.text(0.5, 0.5, "Data not numeric for Histogram", ha='center')
        # 
        elif op == "Median":
            if not numeric.empty:
                median_val = numeric.median() 
                ax.hist(numeric, bins=10, color='lightgreen', edgecolor='black')
                ax.axvline(median_val, color='red', linestyle='dashed', linewidth=2, label=f"Median={median_val:.2f}")
                ax.set_title(f"Histogram with Median of {col}")
                ax.legend()
            else:
                 ax.text(0.5, 0.5, "Data not numeric for Histogram", ha='center')
    
        elif op == "Mode" or op == "Frequency":
            freq = self.data[col].value_counts()
            ax.bar(freq.index.astype(str), freq.values, color='orange', edgecolor='black')
            ax.set_title(f"Frequency of {col}")
            # 

        elif op == "Quantile":
            if not numeric.empty:
                q25, q50, q75 = numeric.quantile([0.25, 0.5, 0.75])
                ax.boxplot(numeric, patch_artist=True, boxprops=dict(facecolor='lightblue'))
                ax.set_title(f"Box Plot (Quantiles) of {col}")
                ax.text(1.05, q25, f"Q1={q25:.2f}", verticalalignment='center')
                ax.text(1.05, q50, f"Q2={q50:.2f}", verticalalignment='center')
                ax.text(1.05, q75, f"Q3={q75:.2f}", verticalalignment='center')
            else:
                 ax.text(0.5, 0.5, "Data not numeric for Box Plot", ha='center')
            # 

        elif op == "Cumulative Frequency":
            cum = self.data[col].value_counts().sort_index().cumsum()
            ax.step(cum.index.astype(str), cum.values, where="mid", color='brown', linewidth=2)
            ax.set_title(f"Cumulative Frequency of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Cumulative Count")
    
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    # ======== Load scikit-learn Dataset ========
    def load_sklearn_dataset(self):
        choice = self.dataset_var.get()
        if not choice:
            messagebox.showwarning("Warning", "Select a dataset first.")
            return
    
        if choice == "Iris":
            ds = datasets.load_iris()
        elif choice == "Wine":
            ds = datasets.load_wine()
        elif choice == "Diabetes":
            ds = datasets.load_diabetes()
        elif choice == "Breast Cancer":
            ds = datasets.load_breast_cancer()
        else:
            return
    
        columns = ds.feature_names if hasattr(ds, "feature_names") else [f"feature_{i}" for i in range(ds.data.shape[1])]
    
        df = pd.DataFrame(ds.data, columns=columns)
        if hasattr(ds, "target"):
            df["target"] = ds.target
    
        self.data = df.copy()
        self.controller.set_data(self.data)
        self.refresh_table()

        self.col_box["values"] = list(self.data.columns)