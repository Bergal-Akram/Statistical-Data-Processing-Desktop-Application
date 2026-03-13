import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AcpPage(ttk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.controller = controller
        self.data = data if data is not None else pd.DataFrame()

        # ===== Title =====
        ttk.Label(
            self,
            text="Analyse en Composantes Principales (ACP)",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ===== Controls (Keep at the top, fixed) =====
        controls_frame = ttk.Frame(self)
        controls_frame.pack(pady=5)

        # Select columns
        ttk.Label(controls_frame, text="Select columns:").grid(row=0, column=0, padx=5)
        self.columns_box = tk.Listbox(
            controls_frame, selectmode="multiple", height=4, # Reduced height to save space
            exportselection=False, width=40
        )
        self.columns_box.grid(row=0, column=1, padx=5)

        # Number of components
        ttk.Label(controls_frame, text="Number of components:").grid(row=1, column=0, padx=5)
        self.n_var = tk.IntVar(value=2)
        ttk.Entry(controls_frame, textvariable=self.n_var, width=10).grid(row=1, column=1, padx=5, pady=5)

        # Run PCA button
        ttk.Button(self, text="Run PCA", command=self.run_pca).pack(pady=5)

        # ===========================================================
        # SPLIT VIEW (PanedWindow)
        # This allows the user to drag the boundary between text and plots
        # ===========================================================
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- Top Pane: Text Results ---
        # We wrap the text in a frame to handle scrollbars better if needed
        self.text_frame = ttk.Frame(self.paned_window)
        self.results_text = tk.Text(self.text_frame, height=8, width=110, wrap="word") # Reduced default height
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add text frame to the pane (weight=1 means it takes less space initially)
        self.paned_window.add(self.text_frame, weight=1)

        # --- Bottom Pane: Plots ---
        self.plots_frame = ttk.Frame(self.paned_window)
        
        # Add plots frame to the pane (weight=3 means it tries to take 3x more space)
        self.paned_window.add(self.plots_frame, weight=3)

    # ===== Set Data for Listbox =====
    def set_data(self, data):
        self.data = data
        self.columns_box.delete(0, tk.END)
        for col in data.columns:
            self.columns_box.insert(tk.END, col)

    # ===== Run PCA =====
    def run_pca(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("No Data", "Please load a dataset first.")
            return

        selected = self.columns_box.curselection()
        if len(selected) < 2:
            messagebox.showwarning("Selection", "Select at least two columns.")
            return
        selected_columns = [self.columns_box.get(i) for i in selected]
        n_components = self.n_var.get()

        try:
            # Assuming run_pca_step_by_step exists in your controller
            results = self.controller.run_pca_step_by_step(selected_columns, n_components)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.show_pca_results(results)

    # ===== Display PCA Results =====
    def show_pca_results(self, results):
        self.results_text.delete(1.0, tk.END)
    
       
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
    
        keys_to_print = [
            ('centered_matrix', 'MATRICE CENTRÉE'),
            ('reduced_matrix', 'MATRICE RÉDUITE'),
            ('covariance_matrix', 'MATRICE DE COVARIANCE'),
            ('correlation_matrix', 'MATRICE DE CORRÉLATION'),
            ('eigenvalues', 'VALEURS PROPRES'),
            ('eigenvectors', 'VECTEURS PROPRES'),
            ('individuals_all', 'COORDONNÉES DES INDIVIDUS (TOUTES)'),
            ('variables_all', 'COORDONNÉES DES VARIABLES (TOUTES)')
        ]
    
        for key, title in keys_to_print:
            self.results_text.insert(tk.END, f"===== {title} =====\n")
            self.results_text.insert(tk.END, f"{results[key]}\n\n")
    
        
        for widget in self.plots_frame.winfo_children():
            widget.destroy()
    
        
        n = results["n_components"]
    
        
        individuals_plot = results["individuals_all"].iloc[:, :n]
        variables_plot = results["variables_all"].iloc[:, :min(2, n)]  # دائرة الارتباط دائماً ثنائية الأبعاد
    
        
        self.show_plots(individuals_plot, variables_plot, n)

        

    # ===== Show Individuals + Variables Plots =====
    def show_plots(self, individuals_df, variables_df, n_components):
        # Clear previous plots
        for widget in self.plots_frame.winfo_children():
            widget.destroy()
    
        if n_components not in [2, 3]:
            raise ValueError("Plotting supports only 2 or 3 components.")
    
        fig = plt.Figure(figsize=(12, 5.5), dpi=100)
        
        if n_components == 2:
            # 2D subplots
            ax0 = fig.add_subplot(1, 2, 1)
            ax1 = fig.add_subplot(1, 2, 2)
            
            # --- Projection des individus ---
            ax0.scatter(individuals_df["PC1"], individuals_df["PC2"], color="green", s=50)
            ax0.axhline(0, color='grey', linewidth=0.8)
            ax0.axvline(0, color='grey', linewidth=0.8)
            ax0.set_xlabel("PC1")
            ax0.set_ylabel("PC2")
            ax0.set_title("Projection des individus")
            ax0.grid(True, linestyle='--', alpha=0.6)
    
            # --- Cercle de corrélation ---
            max_val = 1.1
            ax1.set_xlim(-max_val, max_val)
            ax1.set_ylim(-max_val, max_val)
            for var in variables_df.index:
                x = variables_df.loc[var, "PC1"]
                y = variables_df.loc[var, "PC2"]
                ax1.arrow(0, 0, x, y, color="red", head_width=0.05, length_includes_head=True)
                ax1.text(x * 1.15, y * 1.15, var, fontsize=9, ha='center', va='center')
            circle = plt.Circle((0, 0), 1, color='blue', fill=False, lw=1.5)
            ax1.add_artist(circle)
            ax1.axhline(0, color='grey', linewidth=0.8)
            ax1.axvline(0, color='grey', linewidth=0.8)
            ax1.set_xlabel("PC1")
            ax1.set_ylabel("PC2")
            ax1.set_title("Cercle de corrélation")
            ax1.set_aspect('equal')
            ax1.grid(True, linestyle='--', alpha=0.6)
    
        elif n_components == 3:
            # 3D projection for individuals
            ax0 = fig.add_subplot(1, 2, 1, projection='3d')
            ax1 = fig.add_subplot(1, 2, 2)  # keep 2D correlation circle
    
            # --- Projection des individus 3D ---
            ax0.scatter(individuals_df["PC1"], individuals_df["PC2"], individuals_df["PC3"], color="green", s=50)
            ax0.set_xlabel("PC1")
            ax0.set_ylabel("PC2")
            ax0.set_zlabel("PC3")
            ax0.set_title("Projection des individus (3D)")
    
            # --- Cercle de corrélation ---
            max_val = 1.1
            ax1.set_xlim(-max_val, max_val)
            ax1.set_ylim(-max_val, max_val)
            for var in variables_df.index:
                x = variables_df.loc[var, "PC1"]
                y = variables_df.loc[var, "PC2"]
                ax1.arrow(0, 0, x, y, color="red", head_width=0.05, length_includes_head=True)
                ax1.text(x * 1.15, y * 1.15, var, fontsize=9, ha='center', va='center')
            circle = plt.Circle((0, 0), 1, color='blue', fill=False, lw=1.5)
            ax1.add_artist(circle)
            ax1.axhline(0, color='grey', linewidth=0.8)
            ax1.axvline(0, color='grey', linewidth=0.8)
            ax1.set_xlabel("PC1")
            ax1.set_ylabel("PC2")
            ax1.set_title("Cercle de corrélation")
            ax1.set_aspect('equal')
            ax1.grid(True, linestyle='--', alpha=0.6)
    
        fig.tight_layout(pad=3.0)
    
        # Embed figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
        plt.close(fig)
    
    