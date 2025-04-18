from map_generator import MapGenerator
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Cria o gerador de mapas
    generator = MapGenerator()
    
    # Estilos disponíveis
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    
    # Gera e visualiza um mapa para cada estilo
    for style in styles:
        print(f"\nGerando mapa no estilo {style}...")
        
        # Gera o mapa visual
        visual_map = generator.generate_map(style=style, visual=True)
        
        # Converte para uint8 se necessário
        if visual_map.dtype != np.uint8:
            visual_map = (visual_map * 255).astype(np.uint8)
        
        # Visualiza o mapa
        plt.figure(figsize=(10, 10))
        plt.imshow(visual_map)
        plt.title(f"Mapa {style}")
        plt.axis('off')
        plt.show(block=False)  # Não bloqueia a execução
        plt.pause(2)  # Mostra por 2 segundos
        plt.close()  # Fecha a janela
        
        # Salva o mapa
        generator.save_map(visual_map, f"examples/maps/{style}_map.png")
        print(f"Mapa salvo em examples/maps/{style}_map.png")

if __name__ == "__main__":
    main() 