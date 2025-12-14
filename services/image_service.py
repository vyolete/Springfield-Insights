"""
Servicio optimizado para manejo de imágenes de personajes de Los Simpsons
Implementa caching, lazy loading y fallbacks robustos
"""
import streamlit as st
import requests
from typing import Optional, Dict, Any, List
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class ImageService:
    """Servicio para obtener y optimizar imágenes de personajes"""
    
    def __init__(self):
        self.base_url = "https://thesimpsonsapi.com/api/characters"
        self.cdn_base = "https://cdn.thesimpsonsapi.com"
        self.timeout = settings.API_TIMEOUT
        
        # Tamaños disponibles en la CDN
        self.sizes = {
            'small': '200',      # Para listas
            'medium': '500',     # Para tarjetas (por defecto)
            'large': '1280'      # Para vistas detalladas
        }
        
        # Cache local de mapeo personaje -> imagen
        self.character_image_cache = {}
    
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def get_characters_with_images(_self, page: int = 1) -> List[Dict[str, Any]]:
        """
        Obtiene personajes con sus imágenes desde la API
        
        Args:
            page: Página de resultados a obtener
            
        Returns:
            Lista de personajes con datos de imagen
        """
        try:
            response = requests.get(
                f"{_self.base_url}?page={page}",
                timeout=_self.timeout,
                headers={'User-Agent': 'Springfield-Insights-Academic/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Procesar datos de personajes
                characters = []
                if isinstance(data, dict) and 'docs' in data:
                    characters = data['docs']
                elif isinstance(data, list):
                    characters = data
                
                # Filtrar personajes con imágenes válidas
                valid_characters = []
                for char in characters:
                    if char.get('name') and char.get('image'):
                        valid_characters.append({
                            'name': char['name'],
                            'image': char['image'],
                            'description': char.get('description', ''),
                            'occupation': char.get('occupation', [])
                        })
                
                logger.info(f"✅ Obtenidos {len(valid_characters)} personajes con imágenes")
                return valid_characters
                
            else:
                logger.warning(f"API de personajes retornó código {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error obteniendo personajes: {e}")
            return []
    
    @st.cache_data(ttl=1800)  # Cache por 30 minutos
    def get_character_image_url(_self, character_name: str, size: str = 'medium') -> Optional[str]:
        """
        Obtiene URL optimizada de imagen para un personaje específico
        
        Args:
            character_name: Nombre del personaje
            size: Tamaño de imagen ('small', 'medium', 'large')
            
        Returns:
            URL de imagen optimizada o None
        """
        # Normalizar nombre del personaje
        normalized_name = _self._normalize_character_name(character_name)
        
        # Buscar en cache local primero
        if normalized_name in _self.character_image_cache:
            image_path = _self.character_image_cache[normalized_name]
            return _self._build_cdn_url(image_path, size)
        
        # Buscar en API de personajes
        characters = _self.get_characters_with_images()
        
        for char in characters:
            if _self._normalize_character_name(char['name']) == normalized_name:
                image_path = char['image']
                _self.character_image_cache[normalized_name] = image_path
                return _self._build_cdn_url(image_path, size)
        
        # No encontrado, usar fallback
        logger.info(f"Imagen no encontrada para {character_name}, usando fallback")
        return _self._get_fallback_image(character_name, size)
    
    def _normalize_character_name(self, name: str) -> str:
        """
        Normaliza nombre de personaje para búsqueda
        
        Args:
            name: Nombre original
            
        Returns:
            Nombre normalizado
        """
        return name.lower().strip().replace("'", "").replace(".", "")
    
    def _build_cdn_url(self, image_path: str, size: str) -> str:
        """
        Construye URL de CDN con tamaño específico
        
        Args:
            image_path: Ruta de imagen desde la API
            size: Tamaño deseado
            
        Returns:
            URL completa de CDN
        """
        size_code = self.sizes.get(size, self.sizes['medium'])
        
        # Limpiar ruta de imagen
        if image_path.startswith('/'):
            image_path = image_path[1:]
        
        return f"{self.cdn_base}/{size_code}/{image_path}"
    
    def _get_fallback_image(self, character_name: str, size: str) -> str:
        """
        Genera imagen de fallback personalizada
        
        Args:
            character_name: Nombre del personaje
            size: Tamaño deseado
            
        Returns:
            URL de imagen placeholder
        """
        # Dimensiones según tamaño
        dimensions = {
            'small': '200x150',
            'medium': '500x375', 
            'large': '800x600'
        }
        
        dim = dimensions.get(size, dimensions['medium'])
        safe_name = character_name.replace(' ', '+').replace("'", "")
        
        return f"https://via.placeholder.com/{dim}/FFD700/2F4F4F?text={safe_name}"
    
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def validate_image_url(_self, url: str) -> bool:
        """
        Valida que una URL de imagen sea accesible
        
        Args:
            url: URL a validar
            
        Returns:
            True si la imagen es accesible
        """
        try:
            response = requests.head(url, timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def get_optimized_image_for_character(self, character_name: str, fallback_url: str = "") -> str:
        """
        Obtiene imagen optimizada con múltiples fallbacks
        
        Args:
            character_name: Nombre del personaje
            fallback_url: URL de fallback opcional
            
        Returns:
            URL de imagen válida garantizada
        """
        # Intentar obtener imagen de la API
        api_image = self.get_character_image_url(character_name, 'medium')
        
        if api_image and self.validate_image_url(api_image):
            return api_image
        
        # Intentar fallback proporcionado
        if fallback_url and self.validate_image_url(fallback_url):
            return fallback_url
        
        # Usar placeholder como último recurso
        return self._get_fallback_image(character_name, 'medium')
    
    def preload_popular_characters(self) -> None:
        """
        Precarga imágenes de personajes populares en background
        """
        popular_characters = [
            'Homer Simpson', 'Marge Simpson', 'Bart Simpson', 'Lisa Simpson',
            'Ned Flanders', 'Moe Szyslak', 'Chief Wiggum', 'Apu Nahasapeemapetilon'
        ]
        
        for character in popular_characters:
            try:
                self.get_character_image_url(character)
            except Exception as e:
                logger.debug(f"Error precargando imagen de {character}: {e}")
    
    def get_character_gallery(self, limit: int = 12) -> List[Dict[str, str]]:
        """
        Obtiene galería de personajes con imágenes para mostrar
        
        Args:
            limit: Número máximo de personajes
            
        Returns:
            Lista de personajes con datos para galería
        """
        characters = self.get_characters_with_images()
        
        gallery = []
        for char in characters[:limit]:
            image_url = self.get_character_image_url(char['name'], 'small')
            
            gallery.append({
                'name': char['name'],
                'image_url': image_url,
                'description': char.get('description', '')[:100] + '...' if char.get('description') else '',
                'occupation': ', '.join(char.get('occupation', [])[:2])
            })
        
        return gallery