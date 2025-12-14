"""
Servicio para conectarse a la API real de Los Simpsons
"""
import requests
import random
import streamlit as st
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SimpsonsAPIService:
    """Servicio para obtener datos reales de la API de Los Simpsons"""
    
    def __init__(self):
        self.base_url = "https://thesimpsonsapi.com/api"
        self.timeout = 10
        
        # IDs de personajes principales con frases interesantes
        self.main_characters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def get_character_with_phrases(_self, character_id: int) -> Optional[Dict]:
        """
        Obtiene un personaje con sus frases desde la API
        
        Args:
            character_id: ID del personaje
            
        Returns:
            Dict con datos del personaje y sus frases
        """
        try:
            url = f"{_self.base_url}/characters/{character_id}"
            response = requests.get(url, timeout=_self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar que tenga frases
                if data.get('phrases') and len(data['phrases']) > 0:
                    return {
                        'id': data.get('id'),
                        'name': data.get('name'),
                        'description': data.get('description', ''),
                        'phrases': data.get('phrases', []),
                        'portrait_path': data.get('portrait_path', ''),
                        'occupation': data.get('occupation', 'Unknown'),
                        'age': data.get('age'),
                        'status': data.get('status', 'Unknown')
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo personaje {character_id}: {e}")
            return None
    
    def get_random_quote_from_api(self) -> Optional[Dict]:
        """
        Obtiene una cita aleatoria de un personaje aleatorio
        
        Returns:
            Dict con cita, personaje y contexto
        """
        # Intentar varios personajes hasta encontrar uno con frases
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            character_id = random.choice(self.main_characters)
            character_data = self.get_character_with_phrases(character_id)
            
            if character_data and character_data.get('phrases'):
                # Seleccionar frase aleatoria
                phrase = random.choice(character_data['phrases'])
                
                # Generar contexto basado en la descripción del personaje
                context = self._generate_context(character_data, phrase)
                
                # Construir URL de imagen
                image_url = self._build_image_url(character_data.get('portrait_path', ''))
                
                return {
                    'quote': phrase,
                    'character': character_data['name'],
                    'context': context,
                    'image': image_url,
                    'source': 'api',
                    'character_info': {
                        'occupation': character_data.get('occupation'),
                        'age': character_data.get('age'),
                        'status': character_data.get('status')
                    }
                }
            
            attempts += 1
        
        # Si no se pudo obtener de la API, usar fallback
        return None
    
    def _generate_context(self, character_data: Dict, phrase: str) -> str:
        """
        Genera contexto filosófico basado en el personaje y la frase
        
        Args:
            character_data: Datos del personaje
            phrase: Frase del personaje
            
        Returns:
            Contexto filosófico de la frase
        """
        character_name = character_data.get('name', '')
        occupation = character_data.get('occupation', '')
        
        # Contextos específicos por personaje
        context_map = {
            'Homer Simpson': 'Reflexión sobre la condición humana desde la perspectiva del hombre común',
            'Marge Simpson': 'Sabiduría maternal y equilibrio moral en la vida familiar',
            'Bart Simpson': 'Rebeldía juvenil y cuestionamiento de la autoridad establecida',
            'Lisa Simpson': 'Idealismo intelectual y conciencia social progresista',
            'Maggie Simpson': 'Inocencia infantil y percepción pura del mundo',
            'Ned Flanders': 'Moralidad religiosa y fe inquebrantable en tiempos modernos',
            'Moe Szyslak': 'Cinismo urbano y reflexión sobre la soledad contemporánea',
            'Chief Wiggum': 'Crítica a la incompetencia institucional y el absurdo burocrático',
            'Apu Nahasapeemapetilon': 'Experiencia del inmigrante y multiculturalismo americano'
        }
        
        # Usar contexto específico o generar uno basado en la ocupación
        if character_name in context_map:
            return context_map[character_name]
        elif occupation and occupation != 'Unknown':
            return f'Perspectiva desde el rol de {occupation.lower()} en la sociedad moderna'
        else:
            return 'Reflexión filosófica desde la experiencia de Springfield'
    
    def _build_image_url(self, portrait_path: str) -> str:
        """
        Construye la URL completa de la imagen del personaje
        
        Args:
            portrait_path: Ruta relativa de la imagen
            
        Returns:
            URL completa de la imagen
        """
        if portrait_path:
            return f"https://thesimpsonsapi.com{portrait_path}"
        else:
            return "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Simpson+Character"
    
    def get_api_status(self) -> Dict[str, bool]:
        """
        Verifica si la API está disponible
        
        Returns:
            Dict con estado de la API
        """
        try:
            response = requests.get(f"{self.base_url}/characters/1", timeout=5)
            return {
                'available': response.status_code == 200,
                'status_code': response.status_code
            }
        except Exception as e:
            logger.error(f"Error verificando API: {e}")
            return {
                'available': False,
                'status_code': None,
                'error': str(e)
            }