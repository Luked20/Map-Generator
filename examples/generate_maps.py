from map_generator import MapGenerator
import matplotlib.pyplot as plt
import numpy as np

def generate_and_visualize_maps():
    # Inicializa o gerador de mapas
    generator = MapGenerator()
    
    # Estilos disponíveis
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    difficulties = ['easy', 'medium', 'hard', 'very_hard']
    
    # Define paletas de cores para cada estilo
    color_maps = {
        'dungeon': plt.cm.Greys,
        'open_world': plt.cm.terrain,
        'cyberpunk': plt.cm.plasma,
        'medieval': plt.cm.RdBu,
        'sci_fi': plt.cm.viridis
    }
    
    # Gera e visualiza mapas para cada combinação de estilo e dificuldade
    for style in styles:
        print(f"\nGerando mapas para estilo: {style}")
        
        # Cria uma figura para cada estilo
        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle(f'Mapas {style.capitalize()}', fontsize=16)
        
        for i, difficulty in enumerate(difficulties):
            # Gera o mapa
            map_data = generator.generate_map(style=style, difficulty=difficulty)
            
            # Imprime informações de debug
            print(f"Mapa {style} - {difficulty}:")
            print(f"Shape: {map_data.shape}")
            print(f"Min: {map_data.min():.4f}, Max: {map_data.max():.4f}")
            print(f"Mean: {map_data.mean():.4f}, Std: {map_data.std():.4f}")
            
            # Plota o mapa
            row = i // 2
            col = i % 2
            ax = axes[row, col]
            im = ax.imshow(map_data, cmap=color_maps[style], vmin=0, vmax=1)
            ax.set_title(f'Dificuldade: {difficulty.capitalize()}')
            ax.axis('off')
            
            # Adiciona colorbar
            plt.colorbar(im, ax=ax)
        
        # Ajusta o layout e salva a figura
        plt.tight_layout()
        plt.savefig(f'maps_{style}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Mapas para {style} salvos em 'maps_{style}.png'")

if __name__ == "__main__":
    generate_and_visualize_maps() 