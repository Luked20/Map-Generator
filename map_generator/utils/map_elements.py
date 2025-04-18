import numpy as np
from PIL import Image
import os
import random

class MapElements:
    def __init__(self, tiles_dir="data/tiles"):
        self.tiles_dir = tiles_dir
        self.tiles = self._load_tiles()
        
        # Se não houver tiles, gera tiles básicos
        if not any(self.tiles.values()):
            self._generate_basic_tiles()
        
    def _generate_basic_tiles(self):
        """Gera tiles básicos quando não há tiles disponíveis."""
        tile_size = 32
        self.tiles = {
            'floor': [self._create_tile(tile_size, (100, 100, 100))],    # Cinza escuro
            'wall': [self._create_tile(tile_size, (50, 50, 50))],       # Cinza muito escuro
            'path': [self._create_tile(tile_size, (150, 150, 150))],    # Cinza médio
            'water': [self._create_tile(tile_size, (0, 0, 100))],       # Azul escuro
            'door': [self._create_tile(tile_size, (139, 69, 19))],      # Marrom
            'chest': [self._create_tile(tile_size, (184, 134, 11))],    # Dourado
            'enemy': [self._create_tile(tile_size, (150, 0, 0))]        # Vermelho
        }
        
    def _create_tile(self, size: int, color: tuple) -> np.ndarray:
        """
        Cria um tile básico com uma cor sólida.
        
        Args:
            size (int): Tamanho do tile
            color (tuple): Cor RGB do tile
            
        Returns:
            np.ndarray: Tile gerado
        """
        tile = np.zeros((size, size, 3), dtype=np.uint8)
        tile[:, :] = color
        return tile
        
    def _load_tiles(self):
        """Carrega os tiles de diferentes elementos do mapa."""
        tiles = {
            'floor': [],
            'wall': [],
            'path': [],
            'water': [],
            'door': [],
            'chest': [],
            'enemy': []
        }
        
        # Cria o diretório se não existir
        os.makedirs(self.tiles_dir, exist_ok=True)
        
        # Carrega os tiles de cada tipo
        for element_type in tiles.keys():
            element_dir = os.path.join(self.tiles_dir, element_type)
            os.makedirs(element_dir, exist_ok=True)
            
            # Carrega todas as imagens do diretório
            for file in os.listdir(element_dir):
                if file.endswith(('.png', '.jpg')):
                    img = Image.open(os.path.join(element_dir, file))
                    tiles[element_type].append(np.array(img))
                    
        return tiles
    
    def convert_to_tiles(self, difficulty_map):
        """
        Converte um mapa de dificuldade em tiles.
        
        Args:
            difficulty_map (numpy.ndarray): Mapa de dificuldade (32x32)
            
        Returns:
            Dict[str, Dict]: Dicionário de tiles com seus valores e pesos
        """
        # Define os limites para cada tipo de elemento
        thresholds = {
            'floor': (0.0, 0.3),
            'path': (0.3, 0.5),
            'wall': (0.5, 0.7),
            'water': (0.7, 0.9),
            'enemy': (0.9, 1.0)
        }
        
        # Define os valores e pesos para cada tipo de tile
        tiles_dict = {}
        for type_name, (min_val, max_val) in thresholds.items():
            if type_name in self.tiles and self.tiles[type_name]:
                # Cria um dicionário para cada tipo de tile
                tiles_dict[type_name] = {
                    'value': np.array([
                        [min_val + (max_val - min_val) / 2]  # Valor médio do intervalo
                    ], dtype=np.float32),
                    'weight': 1.0,  # Peso padrão
                    'constraints': {
                        'top': [],
                        'right': [],
                        'bottom': [],
                        'left': []
                    }
                }
                
                # Adiciona restrições básicas
                if type_name == 'floor':
                    tiles_dict[type_name]['constraints'] = {
                        'top': ['floor', 'path', 'enemy'],
                        'right': ['floor', 'path', 'enemy'],
                        'bottom': ['floor', 'path', 'enemy'],
                        'left': ['floor', 'path', 'enemy']
                    }
                elif type_name == 'wall':
                    tiles_dict[type_name]['constraints'] = {
                        'top': ['wall'],
                        'right': ['wall'],
                        'bottom': ['wall'],
                        'left': ['wall']
                    }
                elif type_name == 'path':
                    tiles_dict[type_name]['constraints'] = {
                        'top': ['floor', 'path', 'enemy'],
                        'right': ['floor', 'path', 'enemy'],
                        'bottom': ['floor', 'path', 'enemy'],
                        'left': ['floor', 'path', 'enemy']
                    }
                elif type_name == 'water':
                    tiles_dict[type_name]['constraints'] = {
                        'top': ['water'],
                        'right': ['water'],
                        'bottom': ['water'],
                        'left': ['water']
                    }
                elif type_name == 'enemy':
                    tiles_dict[type_name]['constraints'] = {
                        'top': ['floor', 'path'],
                        'right': ['floor', 'path'],
                        'bottom': ['floor', 'path'],
                        'left': ['floor', 'path']
                    }
        
        return tiles_dict
    
    def convert_to_difficulty(self, tile_map):
        """
        Converte um mapa de tiles em mapa de dificuldade.
        
        Args:
            tile_map (numpy.ndarray): Mapa de tiles (HxWx3)
            
        Returns:
            numpy.ndarray: Mapa de dificuldade (32x32)
        """
        # Define os valores de dificuldade para cada tipo de tile
        difficulty_values = {
            'floor': 0.2,
            'path': 0.4,
            'wall': 0.6,
            'water': 0.8,
            'enemy': 1.0
        }
        
        # Cria o mapa de dificuldade
        difficulty_map = np.zeros((32, 32))
        tile_size = tile_map.shape[0] // 32
        
        for y in range(32):
            for x in range(32):
                # Extrai o tile
                tile = tile_map[y*tile_size:(y+1)*tile_size,
                              x*tile_size:(x+1)*tile_size]
                
                # Determina o tipo de tile
                tile_type = None
                for type_name in difficulty_values.keys():
                    if any(np.array_equal(tile, t) for t in self.tiles[type_name]):
                        tile_type = type_name
                        break
                
                if tile_type:
                    difficulty_map[y, x] = difficulty_values[tile_type]
        
        return difficulty_map
    
    def create_map_from_difficulty(self, difficulty_map, style):
        """
        Cria um mapa visual a partir do mapa de dificuldade.
        
        Args:
            difficulty_map (numpy.ndarray): Mapa de dificuldade (32x32)
            style (str): Estilo do mapa
            
        Returns:
            numpy.ndarray: Mapa visual (32x32x3)
        """
        # Cria um mapa vazio com 3 canais (RGB)
        visual_map = np.zeros((32, 32, 3), dtype=np.uint8)
        
        # Define os limites para cada tipo de elemento baseado na dificuldade
        thresholds = {
            'floor': (0.0, 0.3),
            'path': (0.3, 0.5),
            'wall': (0.5, 0.7),
            'water': (0.7, 0.9),
            'enemy': (0.9, 1.0)
        }
        
        # Aplica os elementos baseado no estilo
        if style == 'dungeon':
            self._apply_dungeon_style(visual_map, difficulty_map, thresholds)
        elif style == 'open_world':
            self._apply_open_world_style(visual_map, difficulty_map, thresholds)
        elif style == 'cyberpunk':
            self._apply_cyberpunk_style(visual_map, difficulty_map, thresholds)
        elif style == 'medieval':
            self._apply_medieval_style(visual_map, difficulty_map, thresholds)
        elif style == 'sci_fi':
            self._apply_sci_fi_style(visual_map, difficulty_map, thresholds)
            
        return visual_map
    
    def _apply_dungeon_style(self, visual_map, difficulty_map, thresholds):
        """Aplica o estilo dungeon ao mapa."""
        # Define cores para cada elemento
        colors = {
            'floor': (100, 100, 100),    # Cinza escuro
            'path': (150, 150, 150),     # Cinza médio
            'wall': (50, 50, 50),        # Cinza muito escuro
            'water': (0, 0, 100),        # Azul escuro
            'enemy': (150, 0, 0)         # Vermelho
        }
        
        # Aplica as cores baseado nos valores de dificuldade
        for i in range(32):
            for j in range(32):
                value = difficulty_map[i, j]
                if value < thresholds['floor'][1]:
                    visual_map[i, j] = colors['floor']
                elif value < thresholds['path'][1]:
                    visual_map[i, j] = colors['path']
                elif value < thresholds['wall'][1]:
                    visual_map[i, j] = colors['wall']
                elif value < thresholds['water'][1]:
                    visual_map[i, j] = colors['water']
                else:
                    visual_map[i, j] = colors['enemy']
                    
        # Adiciona elementos específicos de dungeon
        self._add_doors(visual_map)
        self._add_chests(visual_map)
        self._add_enemies(visual_map)
        
    def _apply_open_world_style(self, visual_map, difficulty_map, thresholds):
        """Aplica o estilo mundo aberto ao mapa."""
        # Define cores para cada elemento
        colors = {
            'floor': (34, 139, 34),      # Verde floresta
            'path': (184, 134, 11),      # Dourado
            'wall': (47, 79, 79),        # Cinza ardósia
            'water': (0, 191, 255),      # Azul céu
            'enemy': (178, 34, 34)       # Vermelho tijolo
        }
        
        # Aplica as cores baseado nos valores de dificuldade
        for i in range(32):
            for j in range(32):
                value = difficulty_map[i, j]
                if value < thresholds['floor'][1]:
                    visual_map[i, j] = colors['floor']
                elif value < thresholds['path'][1]:
                    visual_map[i, j] = colors['path']
                elif value < thresholds['wall'][1]:
                    visual_map[i, j] = colors['wall']
                elif value < thresholds['water'][1]:
                    visual_map[i, j] = colors['water']
                else:
                    visual_map[i, j] = colors['enemy']
                    
        # Adiciona elementos específicos de mundo aberto
        self._add_trees(visual_map)
        self._add_rocks(visual_map)
        self._add_rivers(visual_map)
        
    def _apply_cyberpunk_style(self, visual_map, difficulty_map, thresholds):
        """Aplica o estilo cyberpunk ao mapa."""
        # Define cores para cada elemento
        colors = {
            'floor': (25, 25, 25),       # Preto
            'path': (0, 255, 255),       # Ciano
            'wall': (75, 0, 130),        # Roxo
            'water': (0, 0, 128),        # Azul marinho
            'enemy': (255, 0, 255)       # Magenta
        }
        
        # Aplica as cores baseado nos valores de dificuldade
        for i in range(32):
            for j in range(32):
                value = difficulty_map[i, j]
                if value < thresholds['floor'][1]:
                    visual_map[i, j] = colors['floor']
                elif value < thresholds['path'][1]:
                    visual_map[i, j] = colors['path']
                elif value < thresholds['wall'][1]:
                    visual_map[i, j] = colors['wall']
                elif value < thresholds['water'][1]:
                    visual_map[i, j] = colors['water']
                else:
                    visual_map[i, j] = colors['enemy']
                    
        # Adiciona elementos específicos de cyberpunk
        self._add_neon_lights(visual_map)
        self._add_tech_elements(visual_map)
        self._add_holograms(visual_map)
        
    def _apply_medieval_style(self, visual_map, difficulty_map, thresholds):
        """Aplica o estilo medieval ao mapa."""
        # Define cores para cada elemento
        colors = {
            'floor': (139, 69, 19),      # Marrom
            'path': (160, 82, 45),       # Marrom claro
            'wall': (101, 67, 33),       # Marrom escuro
            'water': (0, 105, 148),      # Azul marinho
            'enemy': (139, 0, 0)         # Vermelho escuro
        }
        
        # Aplica as cores baseado nos valores de dificuldade
        for i in range(32):
            for j in range(32):
                value = difficulty_map[i, j]
                if value < thresholds['floor'][1]:
                    visual_map[i, j] = colors['floor']
                elif value < thresholds['path'][1]:
                    visual_map[i, j] = colors['path']
                elif value < thresholds['wall'][1]:
                    visual_map[i, j] = colors['wall']
                elif value < thresholds['water'][1]:
                    visual_map[i, j] = colors['water']
                else:
                    visual_map[i, j] = colors['enemy']
                    
        # Adiciona elementos específicos de medieval
        self._add_castle_walls(visual_map)
        self._add_towers(visual_map)
        self._add_bridges(visual_map)
        
    def _apply_sci_fi_style(self, visual_map, difficulty_map, thresholds):
        """Aplica o estilo sci-fi ao mapa."""
        # Define cores para cada elemento
        colors = {
            'floor': (47, 79, 79),       # Cinza ardósia
            'path': (0, 255, 127),       # Verde primavera
            'wall': (25, 25, 112),       # Azul meia-noite
            'water': (0, 191, 255),      # Azul céu
            'enemy': (255, 0, 0)         # Vermelho
        }
        
        # Aplica as cores baseado nos valores de dificuldade
        for i in range(32):
            for j in range(32):
                value = difficulty_map[i, j]
                if value < thresholds['floor'][1]:
                    visual_map[i, j] = colors['floor']
                elif value < thresholds['path'][1]:
                    visual_map[i, j] = colors['path']
                elif value < thresholds['wall'][1]:
                    visual_map[i, j] = colors['wall']
                elif value < thresholds['water'][1]:
                    visual_map[i, j] = colors['water']
                else:
                    visual_map[i, j] = colors['enemy']
                    
        # Adiciona elementos específicos de sci-fi
        self._add_tech_panels(visual_map)
        self._add_energy_fields(visual_map)
        self._add_portals(visual_map)
        
    def _add_doors(self, visual_map):
        """Adiciona portas ao mapa."""
        door_color = (139, 69, 19)  # Marrom
        
        # Procura por paredes onde pode adicionar portas
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é uma parede
                if np.array_equal(visual_map[y, x], (50, 50, 50)):
                    # Verifica se tem piso dos dois lados (horizontal ou vertical)
                    if (np.array_equal(visual_map[y, x-1], (100, 100, 100)) and 
                        np.array_equal(visual_map[y, x+1], (100, 100, 100))):
                        if random.random() < 0.2:  # 20% de chance
                            visual_map[y, x] = door_color
                    elif (np.array_equal(visual_map[y-1, x], (100, 100, 100)) and 
                          np.array_equal(visual_map[y+1, x], (100, 100, 100))):
                        if random.random() < 0.2:  # 20% de chance
                            visual_map[y, x] = door_color
                            
    def _add_chests(self, visual_map):
        """Adiciona baús ao mapa."""
        chest_color = (184, 134, 11)  # Dourado
        
        # Procura por pisos onde pode adicionar baús
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso
                if np.array_equal(visual_map[y, x], (100, 100, 100)):
                    # Verifica se tem parede adjacente
                    has_wall = False
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        if np.array_equal(visual_map[y+dy, x+dx], (50, 50, 50)):
                            has_wall = True
                            break
                            
                    if has_wall and random.random() < 0.1:  # 10% de chance
                        visual_map[y, x] = chest_color
                        
    def _add_enemies(self, visual_map):
        """Adiciona inimigos ao mapa."""
        enemy_color = (150, 0, 0)  # Vermelho
        
        # Procura por pisos onde pode adicionar inimigos
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso
                if np.array_equal(visual_map[y, x], (100, 100, 100)):
                    # Verifica se tem espaço suficiente (não tem outros inimigos próximos)
                    has_enemy_nearby = False
                    for dy in [-2, -1, 0, 1, 2]:
                        for dx in [-2, -1, 0, 1, 2]:
                            ny, nx = y + dy, x + dx
                            if (0 <= ny < visual_map.shape[0] and 
                                0 <= nx < visual_map.shape[1] and
                                np.array_equal(visual_map[ny, nx], enemy_color)):
                                has_enemy_nearby = True
                                break
                                
                    if not has_enemy_nearby and random.random() < 0.15:  # 15% de chance
                        visual_map[y, x] = enemy_color
        
    def _add_trees(self, visual_map):
        """Adiciona árvores ao mapa."""
        tree_color = (34, 139, 34)  # Verde floresta escuro
        
        # Procura por pisos onde pode adicionar árvores
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso adequado
                if np.array_equal(visual_map[y, x], (34, 139, 34)):  # Verde floresta
                    if random.random() < 0.3:  # 30% de chance
                        visual_map[y, x] = tree_color
                        
    def _add_rocks(self, visual_map):
        """Adiciona rochas ao mapa."""
        rock_color = (105, 105, 105)  # Cinza
        
        # Procura por pisos onde pode adicionar rochas
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso adequado
                if np.array_equal(visual_map[y, x], (34, 139, 34)):  # Verde floresta
                    if random.random() < 0.2:  # 20% de chance
                        visual_map[y, x] = rock_color
                        
    def _add_rivers(self, visual_map):
        """Adiciona rios ao mapa."""
        river_color = (0, 191, 255)  # Azul céu
        
        # Escolhe pontos de início para os rios
        for _ in range(random.randint(1, 3)):  # 1-3 rios
            x = random.randint(0, visual_map.shape[1] - 1)
            y = 0
            
            # Faz o rio fluir para baixo
            while y < visual_map.shape[0]:
                visual_map[y, x] = river_color
                
                # Move para baixo com alguma variação horizontal
                y += 1
                if y < visual_map.shape[0]:
                    dx = random.choice([-1, 0, 1])
                    new_x = x + dx
                    if 0 <= new_x < visual_map.shape[1]:
                        x = new_x
        
    def _add_neon_lights(self, visual_map):
        """Adiciona luzes neon ao mapa."""
        neon_colors = [
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Ciano
            (255, 255, 0)   # Amarelo
        ]
        
        # Procura por paredes onde pode adicionar luzes neon
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é uma parede
                if np.array_equal(visual_map[y, x], (75, 0, 130)):  # Roxo
                    if random.random() < 0.15:  # 15% de chance
                        visual_map[y, x] = random.choice(neon_colors)
                        
    def _add_tech_elements(self, visual_map):
        """Adiciona elementos tecnológicos ao mapa."""
        tech_color = (0, 255, 127)  # Verde neon
        
        # Procura por pisos onde pode adicionar elementos tech
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso
                if np.array_equal(visual_map[y, x], (25, 25, 25)):  # Preto
                    if random.random() < 0.1:  # 10% de chance
                        visual_map[y, x] = tech_color
                        
    def _add_holograms(self, visual_map):
        """Adiciona hologramas ao mapa."""
        hologram_color = (0, 191, 255)  # Azul brilhante
        
        # Procura por espaços adequados para hologramas
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso
                if np.array_equal(visual_map[y, x], (25, 25, 25)):  # Preto
                    # Verifica se tem espaço suficiente
                    if (np.array_equal(visual_map[y-1, x], (25, 25, 25)) and
                        np.array_equal(visual_map[y+1, x], (25, 25, 25)) and
                        np.array_equal(visual_map[y, x-1], (25, 25, 25)) and
                        np.array_equal(visual_map[y, x+1], (25, 25, 25))):
                        if random.random() < 0.05:  # 5% de chance
                            visual_map[y, x] = hologram_color
        
    def _add_castle_walls(self, visual_map):
        """Adiciona muralhas ao mapa."""
        wall_color = (101, 67, 33)  # Marrom escuro
        
        # Adiciona muralhas nas bordas do mapa
        for i in range(visual_map.shape[1]):
            if random.random() < 0.8:  # 80% de chance
                visual_map[0, i] = wall_color
                visual_map[-1, i] = wall_color
                
        for i in range(visual_map.shape[0]):
            if random.random() < 0.8:  # 80% de chance
                visual_map[i, 0] = wall_color
                visual_map[i, -1] = wall_color
                
    def _add_towers(self, visual_map):
        """Adiciona torres ao mapa."""
        tower_color = (139, 69, 19)  # Marrom
        
        # Adiciona torres nos cantos
        corners = [(0, 0), (0, -1), (-1, 0), (-1, -1)]
        for y, x in corners:
            if random.random() < 0.75:  # 75% de chance
                visual_map[y, x] = tower_color
                
    def _add_bridges(self, visual_map):
        """Adiciona pontes ao mapa."""
        bridge_color = (160, 82, 45)  # Marrom claro
        
        # Procura por água onde pode adicionar pontes
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é água
                if np.array_equal(visual_map[y, x], (0, 105, 148)):  # Azul marinho
                    # Verifica se tem piso dos dois lados
                    if (np.array_equal(visual_map[y, x-1], (139, 69, 19)) and 
                        np.array_equal(visual_map[y, x+1], (139, 69, 19))):
                        if random.random() < 0.4:  # 40% de chance
                            visual_map[y, x] = bridge_color
                            
    def _add_tech_panels(self, visual_map):
        """Adiciona painéis tecnológicos ao mapa."""
        panel_color = (0, 255, 127)  # Verde primavera
        
        # Procura por paredes onde pode adicionar painéis
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é uma parede
                if np.array_equal(visual_map[y, x], (25, 25, 112)):  # Azul meia-noite
                    if random.random() < 0.2:  # 20% de chance
                        visual_map[y, x] = panel_color
                        
    def _add_energy_fields(self, visual_map):
        """Adiciona campos de energia ao mapa."""
        energy_color = (0, 191, 255)  # Azul céu
        
        # Procura por espaços adequados para campos de energia
        for y in range(1, visual_map.shape[0] - 1):
            for x in range(1, visual_map.shape[1] - 1):
                # Verifica se é um piso
                if np.array_equal(visual_map[y, x], (47, 79, 79)):  # Cinza ardósia
                    if random.random() < 0.1:  # 10% de chance
                        visual_map[y, x] = energy_color
                        
    def _add_portals(self, visual_map):
        """Adiciona portais ao mapa."""
        portal_color = (255, 0, 255)  # Magenta
        
        # Adiciona alguns pares de portais
        portals_added = 0
        max_portals = 2
        
        while portals_added < max_portals:
            # Encontra duas posições adequadas para os portais
            positions = []
            for _ in range(2):
                attempts = 0
                while attempts < 100:
                    y = random.randint(1, visual_map.shape[0] - 2)
                    x = random.randint(1, visual_map.shape[1] - 2)
                    
                    # Verifica se é um piso adequado
                    if np.array_equal(visual_map[y, x], (47, 79, 79)):  # Cinza ardósia
                        # Verifica se tem espaço suficiente
                        has_space = True
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if np.array_equal(visual_map[y+dy, x+dx], portal_color):
                                    has_space = False
                                    break
                                    
                        if has_space:
                            positions.append((y, x))
                            break
                            
                    attempts += 1
                    
            if len(positions) == 2:
                for y, x in positions:
                    visual_map[y, x] = portal_color
                portals_added += 1 