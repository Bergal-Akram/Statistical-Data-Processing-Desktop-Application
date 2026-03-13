import tkinter as tk
import math
from model.som_model import SOMModel
from controller.som_controller import SOMController

class SOMPage(tk.Frame):
    
    def __init__(self, parent, faces):
        super().__init__(parent)
        self.root = parent
        self.model = SOMModel(faces)

        self.frame_inputs = tk.Frame(self)
        self.frame_inputs.pack(pady=5)

        tk.Label(self.frame_inputs, text="Face Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame_inputs)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.frame_inputs, text="Feature Vector:").grid(row=1, column=0)
        self.vector_entry = tk.Entry(self.frame_inputs)
        self.vector_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame_inputs, text="Add Face", command=self.add_face)
        self.add_button.grid(row=2, column=0, columnspan=2)

        self.label = tk.Label(self, text="", justify="left", font=("Courier",10))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self, width=350, height=350, bg='white')
        self.canvas.pack()

        self.controller = SOMController(self.model, self)

    def update_label(self, text):
        
        self.label.config(text=text)

    def add_face(self):
        
        name = self.name_entry.get()
        vector = self.vector_entry.get()
        
        if not name or not vector:
            self.update_label("Please enter both name and vector.")
            return
            
        self.controller.add_new_face(name, vector)
        
        self.name_entry.delete(0, tk.END)
        self.vector_entry.delete(0, tk.END)

    def draw_map(self):
        
        self.canvas.delete("all")
        rect_size = 140
        neuron_coords = {}
        
        for i in range(2):
            for j in range(2):
                idx = i*2 + j
                x = j*rect_size + rect_size/2
                y = i*rect_size + rect_size/2
                neuron_coords[idx] = (x,y)
                
                self.canvas.create_oval(x-5,y-5,x+5,y+5, fill='black')
                self.canvas.create_text(x,y-15, text=f"N{idx}", font=("Arial",10))

        for idx, names in self.model.neuron_faces.items():
            cx, cy = neuron_coords[idx] 
            n = len(names)
            if n == 0:
                continue
                
            radius = 20 + max(0,(n-1)*5)
            
            for k, name in enumerate(names):

                angle = 2 * math.pi * k / n
                
                
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                
                
                color = self.model.face_colors.get(name, "#000000")
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color)
                
                self.canvas.create_text(x, y+15, text=name, font=("Arial",8))