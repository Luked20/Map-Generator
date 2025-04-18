# Gerador de Mapas Procedurais

Um sistema avançado de geração procedural de mapas para jogos, utilizando GAN (Generative Adversarial Network) e RL (Reinforcement Learning) para criar mapas únicos e balanceados.

## Características

- Geração de mapas em diferentes estilos:
  - Dungeon
  - Mundo Aberto
  - Cyberpunk
  - Medieval
  - Sci-Fi
- Sistema de dificuldade adaptativa
- Descrições textuais automáticas dos mapas
- Visualização e exportação de mapas
- Suporte a diferentes formatos de saída

## Requisitos

- Python 3.11+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/map-generator.git
cd map-generator
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Geração de Mapas

```python
from map_generator import MapGenerator

# Cria um gerador de mapas
generator = MapGenerator(style='dungeon', difficulty='medium')

# Gera um mapa com descrição
map_data, description = generator.generate_map()

# Visualiza o mapa
generator.visualize_map(map_data)

# Salva o mapa e sua descrição
generator.save_map(map_data, 'meu_mapa.png')
with open('descricao.txt', 'w', encoding='utf-8') as f:
    f.write(description)
```

### Exemplos

O projeto inclui vários exemplos de uso:

1. Geração de mapas com descrições:
```bash
python examples/generate_maps_with_descriptions.py
```

2. Treinamento dos modelos:
```bash
python examples/train_models.py
```

## Estrutura do Projeto

```
map_generator/
├── models/
│   ├── gan.py          # Modelo GAN para geração de mapas
│   └── rl.py           # Modelo RL para balanceamento
├── utils/
│   ├── map_elements.py # Sistema de elementos visuais
│   ├── map_descriptor.py # Gerador de descrições
│   └── wfc.py          # Wave Function Collapse
├── examples/
│   ├── train_models.py
│   └── generate_maps_with_descriptions.py
└── map_generator.py    # Interface principal
```

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

