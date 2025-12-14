"""
Servicio mejorado para gestión de citas con integración de episodios
Permite asociar citas con episodios específicos y búsqueda contextual
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import logging
import random
from services.episodes_service import EpisodesService
from services.simpsons_api import SimpsonsAPIService

logger = logging.getLogger(__name__)

class QuotesService:
    """
    Servicio avanzado para gestión de citas con contexto de episodios
    Integra generación de citas con información episódica
    """
    
    def __init__(self):
        self.episodes_service = EpisodesService()
        self.simpsons_service = SimpsonsAPIService()
        
        # Mapeo de personajes principales a episodios temáticos
        self.character_episode_themes = {
            'Homer Simpson': {
                'themes': ['trabajo', 'familia', 'cerveza', 'donuts', 'nuclear'],
                'typical_episodes': ['Marge vs. the Monorail', 'Last Exit to Springfield']
            },
            'Lisa Simpson': {
                'themes': ['educación', 'música', 'vegetarianismo', 'budismo', 'activismo'],
                'typical_episodes': ['Lisa the Vegetarian', 'Lisa the Buddhist']
            },
            'Bart Simpson': {
                'themes': ['travesuras', 'escuela', 'rebeldía', 'skateboard'],
                'typical_episodes': ['Bart Gets an F', 'Bart the Genius']
            },
            'Marge Simpson': {
                'themes': ['familia', 'moralidad', 'paciencia', 'hogar'],
                'typical_episodes': ['Marge in Chains', 'Marge vs. Singles']
            }
        }
    
    def generate_quote_with_episode_context(self, episode_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Genera una cita filosófica con contexto de episodio específico
        
        Args:
            episode_id: ID del episodio (opcional, si no se proporciona se elige aleatorio)
            
        Returns:
            Dict con cita, personaje, episodio y contexto para LLM
        """
        try:
            # Obtener episodio (específico o aleatorio)
            if episode_id:
                episode = self.episodes_service.get_episode_detail(episode_id)
                if not episode:
                    logger.warning(f"Episodio {episode_id} no encontrado, usando aleatorio")
                    episode = self.episodes_service.get_random_episode()
            else:
                episode = self.episodes_service.get_random_episode()
            
            if not episode:
                # Fallback a generación sin episodio
                return self.simpsons_service.get_random_quote()
            
            # Seleccionar personaje apropiado para el episodio
            character_data = self._select_character_for_episode(episode)
            
            # Obtener contexto del episodio para LLM
            episode_context = self.episodes_service.get_episode_context_for_llm(episode['id'])
            
            # Preparar contexto completo
            enhanced_context = {
                'character': character_data['name'],
                'description': character_data['description'],
                'philosophical_context': character_data['philosophical_context'],
                'episode_context': episode_context,
                'source': 'episode_integrated',
                'quote_type': 'episode_contextual',
                'image': character_data.get('image', ''),
                'success': True
            }
            
            logger.info(f"🎭 Cita generada para {character_data['name']} en episodio '{episode['name']}'")
            return enhanced_context
            
        except Exception as e:
            logger.error(f"Error generando cita con contexto de episodio: {e}")
            # Fallback a generación estándar
            return self.simpsons_service.get_random_quote()
    
    def _select_character_for_episode(self, episode: Dict[str, Any]) -> Dict[str, Any]:
        """
        Selecciona personaje apropiado basado en el tema del episodio
        
        Args:
            episode: Datos del episodio
            
        Returns:
            Datos del personaje seleccionado
        """
        episode_name = episode.get('name', '').lower()
        episode_synopsis = episode.get('synopsis', '').lower()
        episode_text = f"{episode_name} {episode_synopsis}"
        
        # Buscar personaje más relevante basado en palabras clave
        best_character = None
        best_score = 0
        
        for character, data in self.character_episode_themes.items():
            score = 0
            
            # Puntuar basado en temas del personaje
            for theme in data['themes']:
                if theme in episode_text:
                    score += 2
            
            # Puntuar si el personaje aparece en el nombre del episodio
            character_first_name = character.split()[0].lower()
            if character_first_name in episode_name:
                score += 5
            
            if score > best_score:
                best_score = score
                best_character = character
        
        # Si no hay coincidencia clara, usar personaje aleatorio
        if not best_character or best_score == 0:
            best_character = random.choice(list(self.character_episode_themes.keys()))
        
        # Obtener datos del personaje desde el servicio base
        fallback_characters = self.simpsons_service.fallback_characters
        
        for char_data in fallback_characters:
            if char_data['name'] == best_character:
                return char_data
        
        # Fallback final
        return fallback_characters[0]
    
    def search_quotes_by_episode(self, episode_query: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca episodios y genera citas contextuales para cada uno
        
        Args:
            episode_query: Texto a buscar en episodios
            season: Temporada específica (opcional)
            
        Returns:
            Lista de citas con contexto de episodio
        """
        try:
            # Buscar episodios relevantes
            episodes = self.episodes_service.search_episodes(episode_query, season)
            
            if not episodes:
                return []
            
            # Generar citas para los primeros episodios encontrados
            quotes_with_context = []
            max_results = 5  # Limitar para performance
            
            for episode in episodes[:max_results]:
                try:
                    quote_context = self.generate_quote_with_episode_context(episode['id'])
                    
                    if quote_context and quote_context.get('success'):
                        # Añadir información del episodio a la cita
                        quote_context['episode_info'] = {
                            'id': episode['id'],
                            'name': episode['name'],
                            'season': episode['season'],
                            'episode_number': episode['episode_number'],
                            'synopsis': episode['synopsis'],
                            'image_url': episode.get('image_url', '')
                        }
                        
                        quotes_with_context.append(quote_context)
                        
                except Exception as e:
                    logger.error(f"Error generando cita para episodio {episode['id']}: {e}")
                    continue
            
            logger.info(f"🔍 Búsqueda '{episode_query}': {len(quotes_with_context)} citas generadas")
            return quotes_with_context
            
        except Exception as e:
            logger.error(f"Error buscando citas por episodio: {e}")
            return []
    
    def get_quotes_for_season(self, season: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Genera citas para episodios de una temporada específica
        
        Args:
            season: Número de temporada
            limit: Máximo número de citas a generar
            
        Returns:
            Lista de citas de la temporada
        """
        try:
            # Buscar episodios de la temporada
            episodes = self.episodes_service.search_episodes("", season)
            
            if not episodes:
                return []
            
            # Seleccionar episodios aleatorios de la temporada
            selected_episodes = random.sample(episodes, min(limit, len(episodes)))
            
            season_quotes = []
            for episode in selected_episodes:
                try:
                    quote_context = self.generate_quote_with_episode_context(episode['id'])
                    
                    if quote_context and quote_context.get('success'):
                        quote_context['episode_info'] = {
                            'id': episode['id'],
                            'name': episode['name'],
                            'season': episode['season'],
                            'episode_number': episode['episode_number'],
                            'synopsis': episode['synopsis'][:200] + '...',
                            'image_url': episode.get('image_url', '')
                        }
                        
                        season_quotes.append(quote_context)
                        
                except Exception as e:
                    logger.error(f"Error generando cita para episodio {episode['id']}: {e}")
                    continue
            
            logger.info(f"📺 Temporada {season}: {len(season_quotes)} citas generadas")
            return season_quotes
            
        except Exception as e:
            logger.error(f"Error obteniendo citas de temporada {season}: {e}")
            return []
    
    def get_character_episodes(self, character_name: str) -> List[Dict[str, Any]]:
        """
        Busca episodios relevantes para un personaje específico
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            Lista de episodios donde el personaje es relevante
        """
        try:
            # Buscar por nombre del personaje
            first_name = character_name.split()[0].lower()
            episodes = self.episodes_service.search_episodes(first_name)
            
            # Filtrar episodios más relevantes
            relevant_episodes = []
            
            for episode in episodes:
                episode_name = episode.get('name', '').lower()
                episode_synopsis = episode.get('synopsis', '').lower()
                
                # Puntuar relevancia
                relevance_score = 0
                
                if first_name in episode_name:
                    relevance_score += 10
                
                if first_name in episode_synopsis:
                    relevance_score += 5
                
                # Buscar temas relacionados con el personaje
                if character_name in self.character_episode_themes:
                    themes = self.character_episode_themes[character_name]['themes']
                    for theme in themes:
                        if theme in episode_name or theme in episode_synopsis:
                            relevance_score += 3
                
                if relevance_score > 0:
                    episode['relevance_score'] = relevance_score
                    relevant_episodes.append(episode)
            
            # Ordenar por relevancia
            relevant_episodes.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            logger.info(f"👤 {character_name}: {len(relevant_episodes)} episodios relevantes encontrados")
            return relevant_episodes[:10]  # Top 10 más relevantes
            
        except Exception as e:
            logger.error(f"Error buscando episodios para {character_name}: {e}")
            return []
    
    def get_episode_quote_suggestions(self, episode_id: str) -> List[str]:
        """
        Genera sugerencias de temas para citas basadas en un episodio
        
        Args:
            episode_id: ID del episodio
            
        Returns:
            Lista de sugerencias temáticas
        """
        try:
            episode = self.episodes_service.get_episode_detail(episode_id)
            
            if not episode:
                return []
            
            episode_name = episode.get('name', '')
            synopsis = episode.get('synopsis', '')
            
            # Generar sugerencias basadas en palabras clave
            suggestions = []
            
            # Sugerencias basadas en el título
            if 'love' in episode_name.lower():
                suggestions.append("Reflexión sobre el amor y las relaciones")
            
            if 'work' in episode_name.lower() or 'job' in episode_name.lower():
                suggestions.append("Filosofía del trabajo y la productividad")
            
            if 'family' in episode_name.lower():
                suggestions.append("Valores familiares y vínculos sociales")
            
            # Sugerencias basadas en la sinopsis
            if 'school' in synopsis.lower():
                suggestions.append("Crítica al sistema educativo")
            
            if 'money' in synopsis.lower():
                suggestions.append("Reflexión sobre el materialismo y la riqueza")
            
            if 'friend' in synopsis.lower():
                suggestions.append("La importancia de la amistad")
            
            # Sugerencias genéricas si no hay específicas
            if not suggestions:
                suggestions = [
                    "Reflexión existencial sobre la vida cotidiana",
                    "Crítica social desde la perspectiva de Springfield",
                    "Filosofía práctica aplicada a situaciones familiares"
                ]
            
            return suggestions[:3]  # Máximo 3 sugerencias
            
        except Exception as e:
            logger.error(f"Error generando sugerencias para episodio {episode_id}: {e}")
            return []