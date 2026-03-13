import numpy as np
import time
import threading

class SOMController:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        threading.Thread(target=self.dynamic_train, daemon=True).start()

    def dynamic_train(self):
        for _ in range(self.model.epochs):
            max_change = self.model.train_step() 
            
            self.update_label_weights()
            self.view.draw_map()
            
            time.sleep(0.5) 
            
            if max_change < self.model.tol:
                break

    def add_new_face(self, name, vector):
        try:
            vector = np.array([float(x.strip()) for x in vector.split(",")])
        except:
            self.view.update_label("Invalid vector format. Use comma-separated numbers.")
            return

        bmu = self.model.add_face(name, vector, train=True)
        
        _, similar_faces = self.model.map_face(vector)

        if len(similar_faces) > 1:
            text_similar = f"Similar to: {[f for f in similar_faces if f != name]}"
        else:
            text_similar = "New face added"

        text = f"BMU={bmu}, {text_similar}"
        
        self.update_label_weights(text)
        self.view.draw_map()

    def update_label_weights(self, extra_text=""):
        text = "Neuron weights:\n"
        
        for i,w in enumerate(self.model.weights):
            text += f"Neuron {i}: {w.round(3)}\n" 
        
        if extra_text:
            text += "\n" + extra_text
            
        self.view.update_label(text)