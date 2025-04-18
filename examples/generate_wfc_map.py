from map_generator import MapGenerator
import matplotlib.pyplot as plt
import numpy as np

def generate_and_visualize_map(style: str, difficulty: str):
    """
    Gera e visualiza um mapa com o estilo e dificuldade especificados.
    
    Args:
        style (str): Estilo do mapa
        difficulty (str): Nível de dificuldade
    """
    # Cria um gerador de mapas
    generator = MapGenerator(style=style, difficulty=difficulty, size=(32, 32))
    
    # Gera o mapa
    map_data = generator.generate_map(visual=True)
    
    # Visualiza o mapa
    plt.figure(figsize=(10, 10))
    plt.imshow(map_data)
    plt.title(f'Mapa {style.capitalize()} - Dificuldade: {difficulty.capitalize()}')
    plt.axis('off')
    plt.show()
    
    # Salva o mapa
    generator.save_map(map_data, f"maps/{style}_{difficulty}_map.png")

def main():
    """Função principal que gera mapas com diferentes estilos e dificuldades."""
    # Estilos disponíveis
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    
    # Dificuldades disponíveis
    difficulties = ['easy', 'medium', 'hard', 'very_hard']
    
    # Gera um mapa para cada combinação de estilo e dificuldade
    for style in styles:
        for difficulty in difficulties:
            print(f"\nGerando mapa {style} com dificuldade {difficulty}...")
            try:
                generate_and_visualize_map(style, difficulty)
                print(f"Mapa {style} com dificuldade {difficulty} gerado com sucesso!")
            except Exception as e:
                print(f"Erro ao gerar mapa {style} com dificuldade {difficulty}: {str(e)}")

if __name__ == "__main__":
    main() 