import numpy as np
from typing import Dict, List, Tuple

class MapDescriptor:
    def __init__(self):
        self.style_descriptions = {
            'dungeon': {
                'elements': {
                    0: 'paredes de pedra',
                    1: 'corredores escuros',
                    2: 'portas de madeira',
                    3: 'armadilhas',
                    4: 'tesouros',
                    5: 'monstros'
                },
                'templates': [
            "Um {difficulty} masmorra com {features}. {atmosphere}",
            "Uma masmorra {difficulty} repleta de {features}. {atmosphere}",
            "Explorando uma masmorra {difficulty} com {features}. {atmosphere}"
        ]
            },
            'open_world': {
                'elements': {
                    0: 'montanhas',
                    1: 'florestas',
                    2: 'rios',
                    3: 'cidades',
                    4: 'estradas',
                    5: 'pontos de interesse'
                },
                'templates': [
            "Um vasto mundo aberto {difficulty} com {features}. {atmosphere}",
            "Explorando um mundo aberto {difficulty} repleto de {features}. {atmosphere}",
            "Um cenário de mundo aberto {difficulty} apresentando {features}. {atmosphere}"
        ]
            },
            'cyberpunk': {
                'elements': {
                    0: 'arranha-céus',
                    1: 'ruas movimentadas',
                    2: 'neon',
                    3: 'tecnologia',
                    4: 'zonas perigosas',
                    5: 'esconderijos'
                },
                'templates': [
            "Uma cidade cyberpunk {difficulty} com {features}. {atmosphere}",
            "Explorando um distrito cyberpunk {difficulty} repleto de {features}. {atmosphere}",
            "Um cenário cyberpunk {difficulty} apresentando {features}. {atmosphere}"
        ]
            },
            'medieval': {
                'elements': {
                    0: 'castelos',
                    1: 'florestas',
                    2: 'vilas',
                    3: 'estradas de terra',
                    4: 'pontes',
                    5: 'monumentos'
                },
                'templates': [
            "Um reino medieval {difficulty} com {features}. {atmosphere}",
            "Explorando um mundo medieval {difficulty} repleto de {features}. {atmosphere}",
            "Um cenário medieval {difficulty} apresentando {features}. {atmosphere}"
        ]
            },
            'sci_fi': {
                'elements': {
                    0: 'naves espaciais',
                    1: 'estações espaciais',
                    2: 'planetas',
                    3: 'portais',
                    4: 'laboratórios',
                    5: 'zonas de perigo'
                },
                'templates': [
            "Um cenário sci-fi {difficulty} com {features}. {atmosphere}",
            "Explorando um mundo sci-fi {difficulty} repleto de {features}. {atmosphere}",
            "Um ambiente sci-fi {difficulty} apresentando {features}. {atmosphere}"
        ]
            }
        }
        
        self.difficulty_descriptions = {
            'easy': 'acessível',
            'medium': 'desafiador',
            'hard': 'difícil',
            'very_hard': 'extremamente desafiador'
        }
        
        self.atmosphere_descriptions = {
            'dungeon': [
                "O ar está pesado e úmido.",
                "Sombras dançam nas paredes.",
                "Um silêncio perturbador paira no ar.",
                "Ecos distantes ecoam pelos corredores."
            ],
            'open_world': [
                "O sol brilha intensamente no céu.",
                "Uma brisa suave sopra entre as árvores.",
                "O horizonte se estende infinitamente.",
                "A natureza mostra toda sua beleza."
            ],
            'cyberpunk': [
                "Neon pisca em todas as direções.",
                "A chuva ácida cai sobre a cidade.",
                "A tecnologia domina a paisagem.",
                "O caos urbano é palpável."
            ],
            'medieval': [
                "O cheiro de madeira queimada paira no ar.",
                "Cavaleiros patrulham as estradas.",
                "O som de ferreiros ecoa nas ruas.",
                "A vida medieval pulsa em cada esquina."
            ],
            'sci_fi': [
                "A tecnologia alienígena brilha intensamente.",
                "Portais dimensionais piscam ao redor.",
                "Robôs patrulham as instalações.",
                "O futuro se mostra em cada detalhe."
            ]
        }

    def analyze_map(self, map_data: np.ndarray, style: str) -> Dict[str, float]:
        """Analisa o mapa e retorna estatísticas sobre seus elementos."""
        unique, counts = np.unique(map_data, return_counts=True)
        total = map_data.size
        
        element_stats = {}
        for element_id, element_name in self.style_descriptions[style]['elements'].items():
            count = counts[unique == element_id][0] if element_id in unique else 0
            element_stats[element_name] = count / total
            
        return element_stats

    def generate_description(self, map_data: np.ndarray, style: str, difficulty: str) -> str:
        """Gera uma descrição textual do mapa."""
        # Analisa o mapa
        element_stats = self.analyze_map(map_data, style)
        
        # Seleciona os elementos mais presentes
        main_features = sorted(
            [(name, freq) for name, freq in element_stats.items() if freq > 0.1],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Formata os elementos principais
        features_text = ", ".join([name for name, _ in main_features])
        
        # Seleciona uma descrição de atmosfera aleatória
        atmosphere = np.random.choice(self.atmosphere_descriptions[style])
        
        # Seleciona um template aleatório
        template = np.random.choice(self.style_descriptions[style]['templates'])
        
        # Gera a descrição final
        description = template.format(
            difficulty=self.difficulty_descriptions[difficulty],
            features=features_text,
            atmosphere=atmosphere
        )
        
        return description 