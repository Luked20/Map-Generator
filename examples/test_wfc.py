from map_generator import MapGenerator
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Cria o gerador de mapas
    generator = MapGenerator()
    
    # Estilos disponíveis
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    
    print("Testando geração de mapas com WFC...")
    
    for style in styles:
        print(f"\nGerando mapa no estilo {style}...")
        
        # Gera o mapa com WFC
        map_data = generator.generate_map(style=style, use_wfc=True)
        
        # Visualiza o mapa
        plt.figure(figsize=(10, 10))
        plt.imshow(map_data)
        plt.title(f"Mapa {style} (com WFC)")
        plt.axis('off')
        plt.show(block=False)
        plt.pause(2)
        plt.close()
        
        # Salva o mapa
        generator.save_map(map_data, f"examples/maps/{style}_wfc.png")
        print(f"Mapa salvo em examples/maps/{style}_wfc.png")
        
        # Gera o mapa sem WFC para comparação
        print(f"\nGerando mapa no estilo {style} (sem WFC)...")
        map_data_no_wfc = generator.generate_map(style=style, use_wfc=False)
        
        # Visualiza o mapa sem WFC
        plt.figure(figsize=(10, 10))
        plt.imshow(map_data_no_wfc)
        plt.title(f"Mapa {style} (sem WFC)")
        plt.axis('off')
        plt.show(block=False)
        plt.pause(2)
        plt.close()
        
        # Salva o mapa sem WFC
        generator.save_map(map_data_no_wfc, f"examples/maps/{style}_no_wfc.png")
        print(f"Mapa salvo em examples/maps/{style}_no_wfc.png")

if __name__ == "__main__":
    main() 