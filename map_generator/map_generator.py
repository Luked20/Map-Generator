import numpy as np
import tensorflow as tf
from .models.gan import GANModel
from .models.rl import RLModel

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
        
        # Carrega os pesos dos modelos treinados
        try:
            self.gan_model.load_weights("models/gan_final.weights.h5")
            self.rl_model.load_weights("models/rl_final.weights.h5")
            print("Modelos carregados com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar os modelos: {e}")
            print("Usando modelos não treinados...")
        
    def generate_map(self, style=None, difficulty=None, size=None):
        """
        Gera um novo mapa baseado nos parâmetros definidos.
        
        Args:
            style (str, optional): Estilo do mapa ('dungeon', 'open_world', 'cyberpunk', etc.)
            difficulty (str, optional): Nível de dificuldade ('easy', 'medium', 'hard', 'very_hard')
            size (tuple, optional): Tamanho do mapa (largura, altura)
            
        Returns:
            numpy.ndarray: Matriz representando o mapa gerado
        """
        # Usa os parâmetros fornecidos ou os valores padrão
        style = style if style is not None else self.style
        difficulty = difficulty if difficulty is not None else self.difficulty
        size = size if size is not None else self.size
        
        # Gera o mapa base usando GAN
        base_map = self.gan_model.generate(style, size)
        
        # Ajusta a dificuldade usando RL
        balanced_map = self.rl_model.balance_map(base_map, difficulty)
        
        return balanced_map
    
    def visualize_map(self, map_data):
        """
        Visualiza o mapa gerado.
        
        Args:
            map_data (numpy.ndarray): Dados do mapa a serem visualizados
        """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 10))
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
        np.save(filename, map_data)
    
    def load_map(self, filename):
        """
        Carrega um mapa de um arquivo.
        
        Args:
            filename (str): Nome do arquivo a ser carregado
            
        Returns:
            numpy.ndarray: Dados do mapa carregado
        """
        return np.load(filename) 