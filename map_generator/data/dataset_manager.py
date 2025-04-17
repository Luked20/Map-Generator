import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

class DatasetManager:
    def __init__(self, data_dir="data/maps"):
        self.data_dir = data_dir
        self.styles = {
            'dungeon': {'path': 'dungeon', 'difficulty_range': (0.4, 0.8)},
            'open_world': {'path': 'open_world', 'difficulty_range': (0.2, 0.6)},
            'cyberpunk': {'path': 'cyberpunk', 'difficulty_range': (0.5, 0.9)},
            'medieval': {'path': 'medieval', 'difficulty_range': (0.3, 0.7)},
            'sci_fi': {'path': 'sci_fi', 'difficulty_range': (0.4, 0.8)}
        }
        
    def load_map(self, file_path):
        """Carrega um mapa de um arquivo de imagem."""
        img = Image.open(file_path).convert('L')
        # Redimensiona para 32x32 pixels
        img = img.resize((32, 32), Image.Resampling.LANCZOS)
        return np.array(img) / 255.0
    
    def load_dataset(self, style, split_ratio=0.8):
        """Carrega o dataset para um estilo específico."""
        style_dir = os.path.join(self.data_dir, self.styles[style]['path'])
        maps = []
        
        print(f"Carregando mapas de {style_dir}...")
        
        for file in os.listdir(style_dir):
            if file.endswith(('.png', '.jpg')):
                try:
                    map_data = self.load_map(os.path.join(style_dir, file))
                    maps.append(map_data)
                    print(f"Mapa carregado: {file}")
                except Exception as e:
                    print(f"Erro ao carregar {file}: {e}")
        
        if not maps:
            raise ValueError(f"Nenhum mapa encontrado em {style_dir}")
            
        maps = np.array(maps)
        print(f"Total de mapas carregados: {len(maps)}")
        return train_test_split(maps, train_size=split_ratio, random_state=42)
    
    def preprocess_map(self, map_data):
        """Pré-processa um mapa para treinamento."""
        # Garante que o mapa tem o tamanho correto
        if map_data.shape != (32, 32):
            map_data = np.array(Image.fromarray(map_data).resize((32, 32), Image.Resampling.LANCZOS))
        
        # Normaliza os valores
        map_data = (map_data - np.min(map_data)) / (np.max(map_data) - np.min(map_data))
        
        # Adiciona dimensão de canal
        if len(map_data.shape) == 2:
            map_data = np.expand_dims(map_data, axis=-1)
            
        # Garante que os valores estejam no intervalo [0, 1]
        map_data = np.clip(map_data, 0, 1)
            
        return map_data
    
    def generate_synthetic_data(self, style, num_samples=1000):
        """Gera dados sintéticos para treinamento inicial."""
        maps = []
        difficulty_range = self.styles[style]['difficulty_range']
        
        for _ in range(num_samples):
            # Gera um mapa base com ruído
            base_map = np.random.normal(0.5, 0.2, (32, 32))
            
            # Ajusta a dificuldade baseado no estilo
            difficulty = np.random.uniform(*difficulty_range)
            base_map = base_map * difficulty
            
            # Aplica pós-processamento específico do estilo
            if style == 'dungeon':
                base_map = self._apply_dungeon_style(base_map)
            elif style == 'cyberpunk':
                base_map = self._apply_cyberpunk_style(base_map)
            elif style == 'open_world':
                base_map = self._apply_open_world_style(base_map)
            elif style == 'medieval':
                base_map = self._apply_medieval_style(base_map)
            elif style == 'sci_fi':
                base_map = self._apply_sci_fi_style(base_map)
                
            maps.append(base_map)
            
        return np.array(maps)
    
    def _apply_dungeon_style(self, map_data):
        """Aplica características de estilo dungeon."""
        # Adiciona corredores e salas
        map_data = np.where(map_data > 0.7, 1.0, map_data)
        map_data = np.where(map_data < 0.3, 0.0, map_data)
        return map_data
    
    def _apply_cyberpunk_style(self, map_data):
        """Aplica características de estilo cyberpunk."""
        # Adiciona padrões geométricos e estruturas futuristas
        for i in range(0, 32, 4):
            map_data[i:i+2, :] = np.maximum(map_data[i:i+2, :], 0.8)
        return map_data
    
    def _apply_open_world_style(self, map_data):
        """Aplica características de estilo mundo aberto."""
        # Suaviza o terreno e adiciona variações naturais
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(map_data, sigma=1)
    
    def _apply_medieval_style(self, map_data):
        """Aplica características de estilo medieval."""
        # Adiciona estruturas de castelo e vilas
        map_data = np.where(map_data > 0.6, 1.0, map_data)
        return map_data
    
    def _apply_sci_fi_style(self, map_data):
        """Aplica características de estilo sci-fi."""
        # Adiciona estruturas tecnológicas e padrões futuristas
        for i in range(0, 32, 4):
            map_data[:, i:i+2] = np.maximum(map_data[:, i:i+2], 0.8)
        return map_data 