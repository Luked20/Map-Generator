import numpy as np
from typing import List, Tuple, Dict
import random

class WaveFunctionCollapse:
    def __init__(self, width: int, height: int, tiles: Dict[str, np.ndarray]):
        """
        Inicializa o WFC.
        
        Args:
            width (int): Largura do mapa
            height (int): Altura do mapa
            tiles (Dict[str, np.ndarray]): Dicionário de tiles disponíveis
        """
        self.width = width
        self.height = height
        self.tiles = tiles
        
        # Verifica se há tiles disponíveis
        if not tiles:
            raise ValueError("Nenhum tile disponível para o WFC")
            
        # Obtém o tamanho do tile
        first_tile = next(iter(tiles.values()))
        self.tile_size = first_tile.shape[0]
        
        # Inicializa a grade de possibilidades
        self.grid = np.zeros((self.height, self.width), dtype=object)
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y, x] = set(tiles.keys())
        
        # Define as regras de adjacência
        self.rules = self._generate_rules()
        
    def _generate_rules(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Gera as regras de adjacência entre os tiles.
        
        Returns:
            Dict[str, Dict[str, List[str]]]: Regras de adjacência
        """
        rules = {}
        tile_types = list(self.tiles.keys())
        
        for tile_name in tile_types:
            rules[tile_name] = {
                'top': [],
                'right': [],
                'bottom': [],
                'left': []
            }
            
            # Define regras específicas para cada tipo de tile
            if 'floor' in tile_name:
                # Piso pode se conectar com qualquer coisa exceto água
                for other_tile in tile_types:
                    if 'water' not in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
            elif 'wall' in tile_name:
                # Paredes se conectam com paredes e portas
                for other_tile in tile_types:
                    if 'wall' in other_tile or 'door' in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
            elif 'door' in tile_name:
                # Portas se conectam com paredes e pisos
                for other_tile in tile_types:
                    if 'wall' in other_tile or 'floor' in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
            elif 'path' in tile_name:
                # Caminhos se conectam com pisos e outros caminhos
                for other_tile in tile_types:
                    if 'floor' in other_tile or 'path' in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
            elif 'water' in tile_name:
                # Água se conecta apenas com água e alguns tipos de piso
                for other_tile in tile_types:
                    if 'water' in other_tile or 'floor' in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
            elif 'enemy' in tile_name:
                # Inimigos só podem estar em pisos e caminhos
                for other_tile in tile_types:
                    if 'floor' in other_tile or 'path' in other_tile:
                        for direction in ['top', 'right', 'bottom', 'left']:
                            rules[tile_name][direction].append(other_tile)
                            
        return rules
    
    def _get_lowest_entropy_cell(self) -> tuple[int, int]:
        """
        Retorna a célula com menor entropia (menos possibilidades).
        
        Returns:
            tuple[int, int]: Coordenadas (x, y) da célula com menor entropia
        """
        min_entropy = float('inf')
        candidates = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is None:
                    continue
                    
                possibilities = self.grid[y][x]
                entropy = len(possibilities)
                
                if entropy < min_entropy:
                    min_entropy = entropy
                    candidates = [(x, y)]
                elif entropy == min_entropy:
                    candidates.append((x, y))
        
        if not candidates:
            raise ValueError("Nenhuma célula disponível para colapso")
            
        # Se houver empate, escolhe a célula com mais vizinhos já colapsados
        if len(candidates) > 1:
            max_neighbors = -1
            best_candidates = []
            
            for x, y in candidates:
                neighbors = 0
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.grid[ny][nx] is not None:
                            neighbors += 1
                            
                if neighbors > max_neighbors:
                    max_neighbors = neighbors
                    best_candidates = [(x, y)]
                elif neighbors == max_neighbors:
                    best_candidates.append((x, y))
                    
            candidates = best_candidates
            
        return random.choice(candidates)
    
    def _propagate(self, x: int, y: int) -> None:
        """
        Propaga as restrições após o colapso de uma célula.
        
        Args:
            x (int): Coordenada x da célula
            y (int): Coordenada y da célula
        """
        stack = [(x, y)]
        visited = set()
        
        while stack:
            current_x, current_y = stack.pop()
            if (current_x, current_y) in visited:
                continue
                
            visited.add((current_x, current_y))
            current_tile = self.grid[current_y][current_x]
            
            # Verifica vizinhos em todas as direções
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy
                
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] is None:
                        continue
                        
                    # Obtém as possibilidades atuais do vizinho
                    neighbor_possibilities = self.grid[ny][nx]
                    if not neighbor_possibilities:
                        continue
                        
                    # Calcula as novas possibilidades baseadas nas regras
                    new_possibilities = set()
                    for neighbor_tile in neighbor_possibilities:
                        if self._check_compatibility(current_tile, neighbor_tile, dx, dy):
                            new_possibilities.add(neighbor_tile)
                            
                    # Se houve mudança nas possibilidades, atualiza e adiciona à pilha
                    if new_possibilities != neighbor_possibilities:
                        self.grid[ny][nx] = new_possibilities
                        stack.append((nx, ny))
                        
                        # Se não houver mais possibilidades, levanta erro
                        if not new_possibilities:
                            raise ValueError("Contradição encontrada durante propagação")
    
    def _collapse_cell(self, x: int, y: int) -> None:
        """
        Colapsa uma célula para um estado específico.
        
        Args:
            x (int): Coordenada x da célula
            y (int): Coordenada y da célula
        """
        # Obtém os tiles possíveis
        possible_tiles = list(self.possible_tiles[(x, y)])
        
        # Se não houver tiles possíveis, levanta uma exceção
        if not possible_tiles:
            raise ValueError(f"Nenhum tile possível encontrado para a célula ({x}, {y})")
            
        # Escolhe um tile aleatório baseado nos pesos
        weights = [self.tiles[tile]['weight'] for tile in possible_tiles]
        total_weight = sum(weights)
        probabilities = [w/total_weight for w in weights]
        
        # Escolhe o tile baseado nas probabilidades
        chosen_tile = np.random.choice(possible_tiles, p=probabilities)
        
        # Atualiza o grid
        self.grid[y][x] = chosen_tile
        
        # Propaga as restrições
        self._propagate_constraints(x, y)
    
    def _propagate_constraints(self, x: int, y: int) -> None:
        """
        Propaga as restrições para as células vizinhas.
        
        Args:
            x (int): Coordenada x da célula
            y (int): Coordenada y da célula
        """
        # Lista de células para processar
        to_process = [(x, y)]
        processed = set()
        
        while to_process:
            current_x, current_y = to_process.pop(0)
            if (current_x, current_y) in processed:
                continue
                
            processed.add((current_x, current_y))
            current_tile = self.grid[current_y][current_x]
            
            # Verifica os vizinhos
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy
                
                # Verifica se está dentro dos limites
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                    
                # Se a célula já foi processada, pula
                if (nx, ny) in processed:
                    continue
                    
                # Obtém os tiles possíveis antes da propagação
                old_possible = self.possible_tiles[(nx, ny)]
                
                # Filtra os tiles possíveis baseado nas restrições
                new_possible = set()
                for tile in old_possible:
                    if self._check_compatibility(current_tile, tile, dx, dy):
                        new_possible.add(tile)
                
                # Se houve mudança, atualiza e adiciona à lista de processamento
                if new_possible != old_possible:
                    self.possible_tiles[(nx, ny)] = new_possible
                    to_process.append((nx, ny))
                    
                # Se não houver tiles possíveis, levanta uma exceção
                if not new_possible:
                    raise ValueError(f"Contradição encontrada durante propagação em ({nx}, {ny})")
    
    def _check_compatibility(self, tile1: str, tile2: str, dx: int, dy: int) -> bool:
        """
        Verifica se dois tiles são compatíveis em uma determinada direção.
        
        Args:
            tile1 (str): Nome do primeiro tile
            tile2 (str): Nome do segundo tile
            dx (int): Diferença em x entre os tiles
            dy (int): Diferença em y entre os tiles
            
        Returns:
            bool: True se os tiles são compatíveis, False caso contrário
        """
        # Obtém as restrições dos tiles
        if dx == 1:  # Direita
            return tile2 in self.tiles[tile1]['constraints']['right']
        elif dx == -1:  # Esquerda
            return tile2 in self.tiles[tile1]['constraints']['left']
        elif dy == 1:  # Baixo
            return tile2 in self.tiles[tile1]['constraints']['bottom']
        elif dy == -1:  # Cima
            return tile2 in self.tiles[tile1]['constraints']['top']
            
        return False
    
    def generate(self) -> np.ndarray:
        """
        Gera um mapa usando o algoritmo Wave Function Collapse.
        
        Returns:
            np.ndarray: Mapa gerado
        """
        # Inicializa o grid com todos os tiles possíveis
        self.grid = np.full((self.height, self.width), None, dtype=object)
        self.possible_tiles = {(x, y): set(self.tiles.keys()) 
                             for x in range(self.width) 
                             for y in range(self.height)}
        
        try:
            # Colapsa células até que todas estejam definidas
            while None in self.grid:
                # Encontra a célula com menor entropia
                min_entropy = float('inf')
                min_cells = []
                
                for y in range(self.height):
                    for x in range(self.width):
                        if self.grid[y, x] is None:
                            entropy = len(self.possible_tiles[(x, y)])
                            if entropy == 0:
                                raise ValueError(f"Célula ({x}, {y}) sem tiles possíveis")
                            if entropy < min_entropy:
                                min_entropy = entropy
                                min_cells = [(x, y)]
                            elif entropy == min_entropy:
                                min_cells.append((x, y))
                
                if not min_cells:
                    break
                    
                # Escolhe uma célula aleatória entre as de menor entropia
                x, y = random.choice(min_cells)
                
                # Colapsa a célula
                self._collapse_cell(x, y)
                
        except ValueError as e:
            # Se encontrar uma contradição, reinicia a geração
            print(f"Contradição encontrada: {e}. Reiniciando geração...")
            return self.generate()
            
        # Converte o grid para um array numpy
        result = np.zeros((self.height, self.width), dtype=np.float32)
        for y in range(self.height):
            for x in range(self.width):
                tile_name = self.grid[y, x]
                result[y, x] = self.tiles[tile_name]['value'][0, 0]
                
        return result

    def _get_possible_tiles(self, x: int, y: int) -> List[str]:
        """
        Obtém os tiles possíveis para uma célula considerando as restrições dos vizinhos.
        
        Args:
            x (int): Coordenada x da célula
            y (int): Coordenada y da célula
            
        Returns:
            List[str]: Lista de tiles possíveis
        """
        # Se a célula já foi colapsada, retorna apenas o tile atual
        if self.grid[y][x] is not None:
            return [self.grid[y][x]]
            
        # Inicia com todos os tiles possíveis
        possible_tiles = list(self.tiles.keys())
        
        # Verifica as restrições dos vizinhos
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            # Se o vizinho estiver fora dos limites, pula
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
                
            # Se o vizinho não foi colapsado, pula
            if self.grid[ny][nx] is None:
                continue
                
            # Filtra os tiles possíveis baseado no vizinho
            neighbor_tile = self.grid[ny][nx]
            possible_tiles = [
                tile for tile in possible_tiles
                if self._check_compatibility(tile, neighbor_tile, dx, dy)
            ]
            
            # Se não houver tiles possíveis, retorna lista vazia
            if not possible_tiles:
                return []
                
        return possible_tiles 