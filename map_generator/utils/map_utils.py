import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion

def smooth_map(map_data, iterations=1):
    """
    Suaviza o mapa usando operações morfológicas.
    
    Args:
        map_data (numpy.ndarray): Dados do mapa
        iterations (int): Número de iterações de suavização
        
    Returns:
        numpy.ndarray: Mapa suavizado
    """
    smoothed = map_data.copy()
    for _ in range(iterations):
        smoothed = binary_dilation(smoothed)
        smoothed = binary_erosion(smoothed)
    return smoothed

def add_noise(map_data, intensity=0.1):
    """
    Adiciona ruído ao mapa.
    
    Args:
        map_data (numpy.ndarray): Dados do mapa
        intensity (float): Intensidade do ruído (0-1)
        
    Returns:
        numpy.ndarray: Mapa com ruído
    """
    noise = np.random.normal(0, intensity, map_data.shape)
    return np.clip(map_data + noise, 0, 1)

def calculate_difficulty(map_data):
    """
    Calcula a dificuldade do mapa.
    
    Args:
        map_data (numpy.ndarray): Dados do mapa
        
    Returns:
        float: Valor de dificuldade (0-1)
    """
    # Calcula a complexidade do mapa
    complexity = np.std(map_data)
    
    # Calcula a densidade de obstáculos
    obstacle_density = np.mean(map_data > 0.5)
    
    # Combina as métricas
    difficulty = (complexity + obstacle_density) / 2
    return np.clip(difficulty, 0, 1)

def validate_map(map_data):
    """
    Valida se o mapa é jogável.
    
    Args:
        map_data (numpy.ndarray): Dados do mapa
        
    Returns:
        bool: True se o mapa é válido, False caso contrário
    """
    # Verifica se há caminhos conectados
    if not has_connected_paths(map_data):
        return False
    
    # Verifica se há espaço suficiente para jogabilidade
    if np.mean(map_data < 0.3) < 0.2:  # Menos de 20% de espaço livre
        return False
    
    return True

def has_connected_paths(map_data):
    """
    Verifica se há caminhos conectados no mapa.
    
    Args:
        map_data (numpy.ndarray): Dados do mapa
        
    Returns:
        bool: True se há caminhos conectados, False caso contrário
    """
    from scipy.ndimage import label
    
    # Binariza o mapa
    binary_map = map_data > 0.5
    
    # Encontra regiões conectadas
    labeled_map, num_features = label(binary_map)
    
    # Verifica se há pelo menos uma região grande o suficiente
    region_sizes = np.bincount(labeled_map.ravel())
    return np.any(region_sizes > 0.1 * map_data.size) 