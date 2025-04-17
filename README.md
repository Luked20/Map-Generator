# Gerador de Mapas Procedurais com ML

Este projeto implementa um sistema de geração procedural de mapas para jogos usando técnicas de Machine Learning.

## Funcionalidades

- Geração de mapas baseada em parâmetros (dificuldade, tema, estrutura)
- Suporte a diferentes estilos de mapas (dungeon, mundo aberto, cyberpunk)
- Balanceamento automático de dificuldade
- Visualização em tempo real dos mapas gerados

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```python
from map_generator import MapGenerator

# Criar um gerador de mapas
generator = MapGenerator(style="dungeon", difficulty="medium")

# Gerar um mapa
map_data = generator.generate_map()

# Visualizar o mapa
generator.visualize_map(map_data)
```

## Estrutura do Projeto

- `map_generator/`: Módulo principal do gerador de mapas
- `models/`: Implementações dos modelos de ML
- `utils/`: Funções auxiliares
- `examples/`: Exemplos de uso 