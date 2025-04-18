from map_generator import MapGenerator
import matplotlib.pyplot as plt
import os

def generate_and_visualize_maps():
    # Cria diretório para salvar os mapas se não existir
    os.makedirs("generated_maps", exist_ok=True)
    
    # Estilos e dificuldades para testar
    styles = ['dungeon', 'open_world', 'cyberpunk', 'medieval', 'sci_fi']
    difficulties = ['easy', 'medium', 'hard', 'very_hard']
    
    # Gera um mapa para cada combinação de estilo e dificuldade
    for style in styles:
        for difficulty in difficulties:
            print(f"\nGerando mapa {style} com dificuldade {difficulty}...")
            
            # Cria o gerador de mapas
            generator = MapGenerator(style=style, difficulty=difficulty)
            
            # Gera o mapa e sua descrição
            map_data, description = generator.generate_map()
            
            # Visualiza o mapa
            plt.figure(figsize=(10, 10))
            plt.imshow(map_data)
            plt.title(f"{style.capitalize()} - {difficulty.capitalize()}")
            plt.axis('off')
            
            # Salva o mapa e a descrição
            map_path = f"generated_maps/{style}_{difficulty}.png"
            desc_path = f"generated_maps/{style}_{difficulty}.txt"
            
            plt.savefig(map_path)
            plt.close()
            
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(description)
            
            print(f"Mapa salvo em: {map_path}")
            print(f"Descrição salva em: {desc_path}")
            print("\nDescrição do mapa:")
            print(description)
            print("-" * 80)

if __name__ == "__main__":
    generate_and_visualize_maps() 