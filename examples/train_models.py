from map_generator import MapGenerator, GANModel, RLModel
from map_generator.data.dataset_manager import DatasetManager
import os

def train_models():
    # Cria diretórios necessários
    os.makedirs("models", exist_ok=True)
    os.makedirs("data/maps", exist_ok=True)
    
    # Inicializa os modelos
    gan_model = GANModel()
    rl_model = RLModel()
    dataset_manager = DatasetManager()
    
    # Estilos disponíveis
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    
    # Treina cada estilo
    for style in styles:
        print(f"\nTreinando modelo GAN para estilo: {style}")
        
        # Treina com dados sintéticos primeiro
        print("Fase 1: Treinamento com dados sintéticos")
        gan_model.train(style, epochs=50, batch_size=32, use_synthetic=True)
        
        # Tenta carregar dados reais se disponíveis
        print("Fase 2: Treinamento com dados reais (se disponíveis)")
        try:
            gan_model.train(style, epochs=100, batch_size=32, use_synthetic=False)
        except Exception as e:
            print(f"Não foi possível carregar dados reais para {style}: {e}")
            print("Continuando com dados sintéticos...")
            gan_model.train(style, epochs=50, batch_size=32, use_synthetic=True)
    
    # Treina o modelo RL
    print("\nTreinando modelo RL para balanceamento")
    experiences = []
    
    # Gera experiências de treinamento
    for style in styles:
        print(f"Gerando experiências para estilo: {style}")
        
        # Gera mapas de exemplo
        maps = dataset_manager.generate_synthetic_data(style, num_samples=100)
        
        for map_data in maps:
            # Testa diferentes níveis de dificuldade
            for difficulty in ['easy', 'medium', 'hard', 'very_hard']:
                # Gera mapa balanceado
                balanced_map = rl_model.balance_map(map_data, difficulty)
                
                # Calcula recompensa
                reward = calculate_reward(map_data, balanced_map, difficulty)
                
                # Adiciona experiência
                experiences.append((map_data, balanced_map, reward, balanced_map))
    
    # Treina o modelo RL
    rl_model.train(experiences, batch_size=32)
    
    # Salva os modelos
    print("\nSalvando modelos treinados...")
    gan_model.save_weights("models/gan_final.weights.h5")
    rl_model.save_weights("models/rl_final.weights.h5")

def calculate_reward(original_map, balanced_map, difficulty):
    """
    Calcula a recompensa para o modelo RL.
    
    Args:
        original_map (numpy.ndarray): Mapa original
        balanced_map (numpy.ndarray): Mapa balanceado
        difficulty (str): Nível de dificuldade alvo
        
    Returns:
        float: Recompensa calculada
    """
    from map_generator.utils.map_utils import calculate_difficulty, validate_map
    
    # Valores alvo de dificuldade
    target_difficulties = {
        'easy': 0.3,
        'medium': 0.5,
        'hard': 0.7,
        'very_hard': 0.9
    }
    
    # Calcula métricas
    current_difficulty = calculate_difficulty(balanced_map)
    target_difficulty = target_difficulties[difficulty]
    
    # Penaliza se o mapa não for jogável
    if not validate_map(balanced_map):
        return -1.0
    
    # Calcula recompensa baseada na proximidade da dificuldade alvo
    difficulty_diff = abs(current_difficulty - target_difficulty)
    reward = 1.0 - difficulty_diff
    
    return reward

if __name__ == "__main__":
    train_models() 