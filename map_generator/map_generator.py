import numpy as np
import tensorflow as tf
from .models.gan import GANModel
from .models.rl import RLModel
from .utils.map_elements import MapElements
from .utils.map_descriptor import MapDescriptor
import matplotlib.pyplot as plt
from PIL import Image
import os

class MapGenerator:
    def __init__(self, style="dungeon", difficulty="medium", size=(32, 32)):
        """
        Inicializa o gerador de mapas.
        
        Args:
            style (str): Estilo do mapa ('dungeon', 'open_world', 'cyberpunk')
            difficulty (str): Nível de dificuldade ('easy', 'medium', 'hard')
            size (tuple): Tamanho do mapa (largura, altura)
        """
        self.style = style
        self.difficulty = difficulty
        self.size = size
        
        # Inicializa os modelos
        self.gan_model = GANModel()
        self.rl_model = RLModel()
        self.map_elements = MapElements()
        self.map_descriptor = MapDescriptor()
        
        # Carrega os pesos dos modelos treinados
        try:
            self.gan_model.load_weights("models/gan_final.weights.h5")
            self.rl_model.load_weights("models/rl_final.weights.h5")
            print("Modelos carregados com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar os modelos: {e}")
            print("Usando modelos não treinados...")
        
    def generate_map(self, style=None, difficulty=None, size=None, visual=True):
        """
        Gera um novo mapa baseado nos parâmetros definidos.
        
        Args:
            style (str, optional): Estilo do mapa ('dungeon', 'open_world', 'cyberpunk', etc.)
            difficulty (str, optional): Nível de dificuldade ('easy', 'medium', 'hard', 'very_hard')
            size (tuple, optional): Tamanho do mapa (largura, altura)
            visual (bool, optional): Se True, retorna o mapa visual em RGB
            
        Returns:
            tuple: (map_data, description) onde map_data é o mapa gerado e description é a descrição textual
        """
        # Usa os parâmetros fornecidos ou os valores padrão
        style = style if style is not None else self.style
        difficulty = difficulty if difficulty is not None else self.difficulty
        size = size if size is not None else self.size
        
        print(f"Gerando mapa {style}...")
        
        # Gera o mapa base usando GAN
        base_map = self.gan_model.generate(style, size)
        print("Mapa gerado com sucesso usando GAN para", style)
        print(f"Min: {base_map.min():.4f}, Max: {base_map.max():.4f}")
        print(f"Mean: {base_map.mean():.4f}, Std: {base_map.std():.4f}")
        
        # Ajusta a dificuldade usando RL
        balanced_map = self.rl_model.balance_map(base_map, difficulty)
        
        # Gera a descrição textual do mapa
        description = self.map_descriptor.generate_description(balanced_map[..., 0], style, difficulty)
        print("\nDescrição do mapa:")
        print(description)
        
        if visual:
            # Converte o mapa para visual usando MapElements
            return self.map_elements.create_map_from_difficulty(balanced_map[..., 0], style), description
        else:
            return balanced_map, description
    
    def visualize_map(self, map_data):
        """
        Visualiza o mapa gerado.
        
        Args:
            map_data (numpy.ndarray): Dados do mapa a serem visualizados
        """
        plt.figure(figsize=(10, 10))
        if len(map_data.shape) == 3:  # Mapa visual RGB
            plt.imshow(map_data)
        else:  # Mapa de dificuldade
            plt.imshow(map_data, cmap='viridis')
        plt.title(f"Mapa {self.style} - Dificuldade: {self.difficulty}")
        plt.colorbar()
        plt.show()
    
    def save_map(self, map_data, filename):
        """
        Salva o mapa em um arquivo.
        
        Args:
            map_data (numpy.ndarray): Dados do mapa
            filename (str): Nome do arquivo de saída
        """
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if len(map_data.shape) == 3:  # Mapa visual RGB
            img = Image.fromarray(map_data)
            img.save(filename)
        else:  # Mapa de dificuldade
            np.save(filename, map_data)
    
    def load_map(self, filename):
        """
        Carrega um mapa de um arquivo.
        
        Args:
            filename (str): Nome do arquivo a ser carregado
            
        Returns:
            numpy.ndarray: Dados do mapa carregado
        """
        if filename.endswith(('.png', '.jpg')):
            return np.array(Image.open(filename))
        else:
            return np.load(filename) 