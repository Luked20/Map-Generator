from map_generator import MapGenerator
import matplotlib.pyplot as plt

def main():
    # Cria um gerador de mapas para dungeon
    generator = MapGenerator(style="dungeon", difficulty="medium", size=(32, 32))
    
    # Gera um mapa
    map_data = generator.generate_map()
    
    # Visualiza o mapa
    generator.visualize_map(map_data)
    
    # Salva o mapa
    generator.save_map(map_data, "dungeon_map.npy")
    
    # Carrega e visualiza o mapa salvo
    loaded_map = generator.load_map("dungeon_map.npy")
    generator.visualize_map(loaded_map)

if __name__ == "__main__":
    main() 