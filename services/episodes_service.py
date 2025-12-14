"""
Servicio para gestión de episodios de Los Simpsons
Implementa caching inteligente, paginación y búsqueda optimizada
"""
import streamlit as st
import requests
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
from config.settings import settings

logger = logging.getLogger(__name__)

class EpisodesService:
    """
    Servicio optimizado para gestión del catálogo de episodios
    Implementa caching, paginación y búsqueda semántica
    """
    
    def __init__(self):
        self.base_url = "https://thesimpsonsapi.com/api/episodes"
        self.cdn_base = "https://cdn.thesimpsonsapi.com"
        self.timeout = settings.API_TIMEOUT
        
        # Configuración de paginación
        self.episodes_per_page = 20
        self.max_pages = 40  # Aproximadamente 800 episodios
        
        # Cache local para búsquedas rápidas
        self._episodes_cache = {}
        self._search_index = {}
    
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def get_episodes_page(_self, page: int = 1) -> Dict[str, Any]:
        """
        Obtiene una página específica de episodios
        
        Args:
            page: Número de página (1-based)
            
        Returns:
            Dict con episodios y metadatos de paginación
        """
        try:
            response = requests.get(
                f"{_self.base_url}?page={page}",
                timeout=_self.timeout,
                headers={'User-Agent': 'Springfield-Insights-Academic/2.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Procesar estructura de respuesta
                if isinstance(data, dict):
                    episodes = data.get('docs', [])
                    total_pages = data.get('totalPages', 1)
                    total_episodes = data.get('totalDocs', len(episodes))
                elif isinstance(data, list):
                    episodes = data
                    total_pages = 1
                    total_episodes = len(episodes)
                else:
                    episodes = []
                    total_pages = 1
                    total_episodes = 0
                
                # Normalizar datos de episodios
                normalized_episodes = []
                for ep in episodes:
                    normalized_ep = _self._normalize_episode_data(ep)
                    if normalized_ep:
                        normalized_episodes.append(normalized_ep)
                
                logger.info(f"✅ Página {page}: {len(normalized_episodes)} episodios obtenidos")
                
                return {
                    'episodes': normalized_episodes,
                    'current_page': page,
                    'total_pages': min(total_pages, _self.max_pages),
                    'total_episodes': total_episodes,
                    'has_next': page < min(total_pages, _self.max_pages),
                    'has_prev': page > 1
                }
            
            else:
                logger.warning(f"API de episodios retornó código {response.status_code}")
                return _self._get_empty_page_response(page)
                
        except Exception as e:
            logger.error(f"Error obteniendo página {page} de episodios: {e}")
            return _self._get_empty_page_response(page)
    
    def _normalize_episode_data(self, episode_raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Normaliza datos de episodio desde la API
        
        Args:
            episode_raw: Datos crudos del episodio
            
        Returns:
            Episodio normalizado o None si es inválido
        """
        try:
            # Campos requeridos
            episode_id = episode_raw.get('id')
            name = episode_raw.get('name', '').strip()
            
            if not episode_id or not name:
                return None
            
            # Procesar temporada y número de episodio
            season = episode_raw.get('season', 0)
            episode_number = episode_raw.get('episode_number', 0)
            
            # Procesar fecha de emisión
            airdate = episode_raw.get('airdate', '')
            formatted_date = self._format_airdate(airdate)
            
            # Procesar sinopsis
            synopsis = episode_raw.get('synopsis', '').strip()
            if not synopsis:
                synopsis = f"Episodio {episode_number} de la temporada {season} de Los Simpsons."
            
            # Procesar imagen
            image_path = episode_raw.get('image_path', '')
            image_url = self._build_episode_image_url(image_path) if image_path else ''
            
            return {
                'id': episode_id,
                'name': name,
                'season': int(season) if season else 0,
                'episode_number': int(episode_number) if episode_number else 0,
                'airdate': airdate,
                'formatted_date': formatted_date,
                'synopsis': synopsis,
                'image_path': image_path,
                'image_url': image_url,
                'search_text': f"{name} {synopsis}".lower()
            }
            
        except Exception as e:
            logger.error(f"Error normalizando episodio: {e}")
            return None
    
    def _format_airdate(self, airdate: str) -> str:
        """
        Formatea fecha de emisión para mostrar
        
        Args:
            airdate: Fecha en formato ISO o string
            
        Returns:
            Fecha formateada para mostrar
        """
        if not airdate:
            return "Fecha desconocida"
        
        try:
            # Intentar parsear diferentes formatos
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']:
                try:
                    date_obj = datetime.strptime(airdate[:19], fmt[:10])
                    return date_obj.strftime("%d de %B, %Y")
                except ValueError:
                    continue
            
            # Si no se puede parsear, devolver como está
            return airdate
            
        except Exception:
            return airdate
    
    def _build_episode_image_url(self, image_path: str) -> str:
        """
        Construye URL de imagen del episodio
        
        Args:
            image_path: Ruta de imagen desde la API
            
        Returns:
            URL completa de imagen
        """
        if not image_path:
            return ""
        
        # Limpiar ruta
        if image_path.startswith('/'):
            image_path = image_path[1:]
        
        return f"{self.cdn_base}/500/{image_path}"
    
    def _get_empty_page_response(self, page: int) -> Dict[str, Any]:
        """
        Respuesta vacía para errores
        
        Args:
            page: Número de página
            
        Returns:
            Respuesta vacía estructurada
        """
        return {
            'episodes': [],
            'current_page': page,
            'total_pages': 1,
            'total_episodes': 0,
            'has_next': False,
            'has_prev': False
        }
    
    @st.cache_data(ttl=1800)  # Cache por 30 minutos
    def get_episode_detail(_self, episode_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalle completo de un episodio específico
        
        Args:
            episode_id: ID del episodio
            
        Returns:
            Datos completos del episodio o None
        """
        try:
            response = requests.get(
                f"{_self.base_url}/{episode_id}",
                timeout=_self.timeout,
                headers={'User-Agent': 'Springfield-Insights-Academic/2.0'}
            )
            
            if response.status_code == 200:
                episode_raw = response.json()
                normalized = _self._normalize_episode_data(episode_raw)
                
                if normalized:
                    logger.info(f"✅ Detalle obtenido para episodio {episode_id}")
                    return normalized
            
            logger.warning(f"No se pudo obtener detalle del episodio {episode_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo detalle del episodio {episode_id}: {e}")
            return None
    
    @st.cache_data(ttl=1800)
    def search_episodes(_self, query: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca episodios por texto y/o temporada
        
        Args:
            query: Texto a buscar en nombre y sinopsis
            season: Temporada específica (opcional)
            
        Returns:
            Lista de episodios que coinciden
        """
        if not query and season is None:
            return []
        
        query_lower = query.lower().strip() if query else ""
        results = []
        
        # Buscar en múltiples páginas (limitado para performance)
        max_search_pages = 10  # Buscar en primeras 10 páginas
        
        for page in range(1, max_search_pages + 1):
            try:
                page_data = _self.get_episodes_page(page)
                episodes = page_data.get('episodes', [])
                
                for episode in episodes:
                    # Filtrar por temporada si se especifica
                    if season is not None and episode.get('season') != season:
                        continue
                    
                    # Filtrar por texto si se especifica
                    if query_lower:
                        search_text = episode.get('search_text', '')
                        if query_lower not in search_text:
                            continue
                    
                    results.append(episode)
                
                # Si no hay más páginas, parar
                if not page_data.get('has_next', False):
                    break
                    
            except Exception as e:
                logger.error(f"Error buscando en página {page}: {e}")
                continue
        
        logger.info(f"🔍 Búsqueda '{query}' temporada {season}: {len(results)} resultados")
        return results[:50]  # Limitar resultados para performance
    
    @st.cache_data(ttl=3600)
    def get_seasons_summary(_self) -> Dict[int, Dict[str, Any]]:
        """
        Obtiene resumen de temporadas disponibles
        
        Returns:
            Dict con información de cada temporada
        """
        seasons_data = {}
        
        # Obtener primeras páginas para construir resumen
        for page in range(1, 6):  # Primeras 5 páginas
            try:
                page_data = _self.get_episodes_page(page)
                episodes = page_data.get('episodes', [])
                
                for episode in episodes:
                    season = episode.get('season', 0)
                    if season > 0:
                        if season not in seasons_data:
                            seasons_data[season] = {
                                'season': season,
                                'episode_count': 0,
                                'episodes': []
                            }
                        
                        seasons_data[season]['episode_count'] += 1
                        seasons_data[season]['episodes'].append({
                            'id': episode.get('id'),
                            'name': episode.get('name'),
                            'episode_number': episode.get('episode_number')
                        })
                
                if not page_data.get('has_next', False):
                    break
                    
            except Exception as e:
                logger.error(f"Error obteniendo resumen de temporada en página {page}: {e}")
                continue
        
        # Ordenar episodios dentro de cada temporada
        for season_data in seasons_data.values():
            season_data['episodes'].sort(key=lambda x: x.get('episode_number', 0))
        
        logger.info(f"📊 Resumen de temporadas: {len(seasons_data)} temporadas encontradas")
        return seasons_data
    
    def get_episode_context_for_llm(self, episode_id: str) -> Dict[str, str]:
        """
        Obtiene contexto del episodio optimizado para LLM
        
        Args:
            episode_id: ID del episodio
            
        Returns:
            Contexto estructurado para GPT-4
        """
        episode = self.get_episode_detail(episode_id)
        
        if not episode:
            return {
                'episode_name': 'Episodio desconocido',
                'season': '0',
                'episode_number': '0',
                'synopsis': 'Información del episodio no disponible.',
                'context_summary': 'Episodio de Los Simpsons sin contexto específico.'
            }
        
        return {
            'episode_name': episode.get('name', 'Sin título'),
            'season': str(episode.get('season', 0)),
            'episode_number': str(episode.get('episode_number', 0)),
            'synopsis': episode.get('synopsis', ''),
            'airdate': episode.get('formatted_date', ''),
            'context_summary': f"Episodio '{episode.get('name')}' (T{episode.get('season')}E{episode.get('episode_number')}) - {episode.get('synopsis', '')[:200]}..."
        }
    
    def validate_episode_exists(self, episode_id: str) -> bool:
        """
        Valida que un episodio existe
        
        Args:
            episode_id: ID del episodio a validar
            
        Returns:
            True si el episodio existe
        """
        episode = self.get_episode_detail(episode_id)
        return episode is not None
    
    def get_random_episode(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene un episodio aleatorio para exploración
        
        Returns:
            Episodio aleatorio o None
        """
        import random
        
        # Obtener página aleatoria
        random_page = random.randint(1, 10)  # Primeras 10 páginas
        
        try:
            page_data = self.get_episodes_page(random_page)
            episodes = page_data.get('episodes', [])
            
            if episodes:
                return random.choice(episodes)
            
        except Exception as e:
            logger.error(f"Error obteniendo episodio aleatorio: {e}")
        
        return None