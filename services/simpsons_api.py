"""
Servicio para consumir la API de Los Simpsons
Implementa estrategia robusta con fallbacks y generación de contenido
"""
import requests
import random
from typing import Dict, Optional, Any, List
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class SimpsonsAPIService:
    """
    Servicio robusto para obtener datos de Los Simpsons
    Implementa múltiples estrategias de fallback para garantizar funcionalidad
    """
    
    def __init__(self):
        self.timeout = settings.API_TIMEOUT
        
        # Múltiples endpoints para robustez
        self.endpoints = {
            'characters': 'https://thesimpsonsapi.com/api/characters',
            'episodes': 'https://thesimpsonsapi.com/api/episodes', 
            'locations': 'https://thesimpsonsapi.com/api/locations'
        }
        
        # Personajes principales con contexto filosófico
        self.fallback_characters = [
            {
                'name': 'Homer Simpson',
                'description': 'Padre de familia que representa la búsqueda de la felicidad simple',
                'philosophical_context': 'hedonismo, existencialismo cotidiano, crítica al consumismo'
            },
            {
                'name': 'Lisa Simpson', 
                'description': 'Niña prodigio con fuerte conciencia moral y social',
                'philosophical_context': 'idealismo, activismo social, búsqueda de la verdad'
            },
            {
                'name': 'Bart Simpson',
                'description': 'Niño rebelde que cuestiona la autoridad establecida',
                'philosophical_context': 'anarquismo juvenil, crítica a las instituciones'
            },
            {
                'name': 'Marge Simpson',
                'description': 'Madre que equilibra moralidad y pragmatismo familiar',
                'philosophical_context': 'ética del cuidado, moralidad práctica'
            },
            {
                'name': 'Ned Flanders',
                'description': 'Vecino religioso que representa la fe inquebrantable',
                'philosophical_context': 'fundamentalismo religioso, moralidad absoluta'
            },
            {
                'name': 'Moe Szyslak',
                'description': 'Cantinero cínico que refleja el desencanto social',
                'philosophical_context': 'nihilismo, crítica social, soledad urbana'
            },
            {
                'name': 'Chief Wiggum',
                'description': 'Jefe de policía que satiriza la incompetencia institucional',
                'philosophical_context': 'crítica a la autoridad, absurdo burocrático'
            },
            {
                'name': 'Apu Nahasapeemapetilon',
                'description': 'Inmigrante trabajador que representa el sueño americano',
                'philosophical_context': 'multiculturalismo, ética del trabajo, identidad'
            }
        ]
    
    def get_random_quote(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos para generar una reflexión filosófica
        Implementa estrategia de fallback robusta
        
        Returns:
            Dict con estructura para generar contenido filosófico
        """
        # Estrategia 1: Intentar obtener personaje de la API
        character_data = self._try_get_character_from_api()
        
        if character_data:
            logger.info("✅ Datos obtenidos de API externa")
            return self._prepare_quote_context(character_data, source="api")
        
        # Estrategia 2: Usar datos de fallback locales
        logger.info("🔄 Usando datos de fallback locales")
        fallback_character = random.choice(self.fallback_characters)
        return self._prepare_quote_context(fallback_character, source="fallback")
    
    def _try_get_character_from_api(self) -> Optional[Dict[str, Any]]:
        """
        Intenta obtener un personaje de la API externa
        Maneja errores 401, 403 y otros códigos HTTP de forma robusta
        """
        try:
            response = requests.get(
                self.endpoints['characters'],
                timeout=self.timeout,
                headers={'User-Agent': 'Springfield-Insights-Academic-Project/1.0'}
            )
            
            # Manejo específico de errores de autenticación
            if response.status_code == 401:
                logger.warning("🔐 API requiere autenticación (401 Unauthorized)")
                return None
            elif response.status_code == 403:
                logger.warning("🚫 Acceso prohibido a la API (403 Forbidden)")
                return None
            elif response.status_code == 429:
                logger.warning("⏱️ Límite de rate excedido (429 Too Many Requests)")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            # Procesar respuesta de la API
            if isinstance(data, list) and len(data) > 0:
                # Seleccionar personaje aleatorio
                character = random.choice(data)
                
                # Validar estructura mínima
                if 'name' in character:
                    return {
                        'name': character.get('name', 'Personaje Desconocido'),
                        'description': character.get('description', 'Habitante de Springfield'),
                        'philosophical_context': 'reflexión sobre la condición humana'
                    }
            
            logger.warning("📊 Estructura de API inesperada")
            return None
            
        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Timeout conectando a API ({self.timeout}s)")
            return None
        except requests.exceptions.ConnectionError:
            logger.warning("🌐 Error de conexión con API externa")
            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"🔗 Error HTTP: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado en API: {e}")
            return None
    
    def _prepare_quote_context(self, character_data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Prepara el contexto para generar una reflexión filosófica
        
        Args:
            character_data: Datos del personaje
            source: Fuente de los datos ('api' o 'fallback')
            
        Returns:
            Contexto estructurado para el LLM
        """
        return {
            'character': character_data.get('name', 'Habitante de Springfield'),
            'description': character_data.get('description', 'Personaje de Los Simpsons'),
            'philosophical_context': character_data.get('philosophical_context', 'reflexión existencial'),
            'source': source,
            'quote_type': 'generated',  # Indica que la cita será generada por LLM
            'image': self._get_character_image_placeholder(character_data.get('name', '')),
            'success': True
        }
    
    def _get_character_image_placeholder(self, character_name: str) -> str:
        """
        Genera URL de imagen placeholder para el personaje
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            URL de imagen placeholder
        """
        # Usar servicio de placeholder con tema de Los Simpsons
        safe_name = character_name.replace(' ', '+')
        return f"https://via.placeholder.com/300x200/FFD700/000000?text={safe_name}"
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Verifica el estado de los endpoints de la API
        Útil para diagnóstico y monitoreo
        
        Returns:
            Estado de cada endpoint
        """
        status = {}
        
        for endpoint_name, url in self.endpoints.items():
            try:
                response = requests.head(url, timeout=5)
                status[endpoint_name] = {
                    'status_code': response.status_code,
                    'accessible': response.status_code == 200,
                    'error': None
                }
            except Exception as e:
                status[endpoint_name] = {
                    'status_code': None,
                    'accessible': False,
                    'error': str(e)
                }
        
        return status
    
    def validate_quote_data(self, quote_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de la cita tengan la estructura correcta
        
        Args:
            quote_data: Diccionario con los datos de la cita
            
        Returns:
            True si la estructura es válida, False en caso contrario
        """
        if not isinstance(quote_data, dict):
            return False
        
        required_fields = ['quote', 'character']
        return all(
            field in quote_data and 
            isinstance(quote_data[field], str) and 
            quote_data[field].strip()
            for field in required_fields
        )