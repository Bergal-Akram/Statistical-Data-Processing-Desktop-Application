import numpy as np
import random

class SOMModel:
    
    def __init__(self, data, grid_size=(2,2), alpha=0.5, epochs=10, tol=0.001):
        
        self.data = data
        self.face_names = list(data.keys())

        self.grid_size = grid_size
        self.num_neurons = grid_size[0]*grid_size[1]
        
        self.alpha = alpha
        
        self.epochs = epochs
        
        self.tol = tol

        
        feature_dim = len(list(data.values())[0])
        self.weights = np.random.rand(self.num_neurons, feature_dim)

       
        self.neighbors = {0:[1,2],1:[0,3],2:[0,3],3:[1,2]}
        
        
        self.neuron_faces = {i: [] for i in range(self.num_neurons)}
        
        self.face_colors = {}

       
        for name in data:
            self.add_face(name, data[name], train=False)

    def train_step(self):
        
        data_vectors = np.array(list(self.data.values()))
        max_change = 0 

        for x in data_vectors:
            
            distances = np.linalg.norm(self.weights - x, axis=1)
            
            bmu = np.argmin(distances)

            
            old_w = self.weights[bmu].copy()
            
            self.weights[bmu] += self.alpha * (x - self.weights[bmu])
            
            
            max_change = max(max_change, np.linalg.norm(self.weights[bmu]-old_w))

           
            for n in self.neighbors[bmu]:
                old_w_n = self.weights[n].copy()
                
                self.weights[n] += self.alpha * (x - self.weights[n])
                
               
                max_change = max(max_change, np.linalg.norm(self.weights[n]-old_w_n))
                
        return max_change

    def map_face(self, vector):
        
        distances = np.linalg.norm(self.weights - vector, axis=1)
        bmu = np.argmin(distances)
        
        similar_faces = self.neuron_faces[bmu].copy() 
        return bmu, similar_faces

    def add_face(self, name, vector, train=True):
       
        self.data[name] = vector
        self.face_names.append(name)
        
        if name not in self.face_colors:
            self.face_colors[name] = "#%06x" % random.randint(0, 0xFFFFFF)
            
        distances = np.linalg.norm(self.weights - vector, axis=1)
        bmu = np.argmin(distances)
        
        self.neuron_faces[bmu].append(name)
        
        if train:
            self.train_until_stable()
            
        return bmu

    def train_until_stable(self):
     
        for _ in range(self.epochs):
            max_change = self.train_step()
            if max_change < self.tol:
                break