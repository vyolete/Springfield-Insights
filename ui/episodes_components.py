"""
Componentes UI especializados para la funcionalidad de episodios
Implementa navegación, búsqueda y visualización optimizada de episodios
"""
import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import logging
from ui.theme import SimpsonsTheme
from ui.components import UIComponents, StateManager

logger = logging.getLogger(__name__)

class EpisodesUI:
    """Componentes UI especializados para episodios"""
    
    @staticmethod
    def render_episodes_browser(episodes_service) -> Optional[str]:
        """
        Renderiza navegador de episodios con paginación y búsqueda
        
        Args:
            episodes_service: Servicio de episodios
            
        Returns:
            ID del episodio seleccionado o None
        """
        st.markdown("### 📺 Explorar Episodios")
        
        # Controles de búsqueda y filtros
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "🔍 Buscar episodios",
                placeholder="Nombre del episodio o palabras clave...",
                key="episode_search"
            )
        
        with col2:
            # Obtener temporadas disponibles
            seasons_data = episodes_service.get_seasons_summary()
            season_options = ["Todas"] + [f"Temporada {s}" for s in sorted(seasons_data.keys())]
            
            selected_season_str = st.selectbox("📅 Temporada", season_options, key="season_filter")
            selected_season = None
            if selected_season_str != "Todas":
                selected_season = int(selected_season_str.split()[-1])
        
        with col3:
            if st.button("🎲 Episodio Aleatorio", key="random_episode"):
                random_episode = episodes_service.get_random_episode()
                if random_episode:
                    return random_episode['id']
        
        # Realizar búsqueda si hay query
        if search_query:
            episodes = episodes_service.search_episodes(search_query, selected_season)
            
            if episodes:
                st.success(f"🔍 {len(episodes)} episodios encontrados")
                selected_episode_id = EpisodesUI._render_episodes_grid(episodes, "search_results")
                if selected_episode_id:
                    return selected_episode_id
            else:
                st.info("No se encontraron episodios con esos criterios")
                return None
        
        # Navegación por páginas si no hay búsqueda
        else:
            return EpisodesUI._render_paginated_episodes(episodes_service, selected_season)
    
    @staticmethod
    def _render_paginated_episodes(episodes_service, season_filter: Optional[int]) -> Optional[str]:
        """
        Renderiza episodios con paginación
        
        Args:
            episodes_service: Servicio de episodios
            season_filter: Filtro de temporada opcional
            
        Returns:
            ID del episodio seleccionado
        """
        # Control de página
        if 'episodes_page' not in st.session_state:
            st.session_state.episodes_page = 1
        
        current_page = st.session_state.episodes_page
        
        # Obtener datos de la página
        with st.spinner("📺 Cargando episodios..."):
            page_data = episodes_service.get_episodes_page(current_page)
        
        episodes = page_data.get('episodes', [])
        
        # Filtrar por temporada si se especifica
        if season_filter:
            episodes = [ep for ep in episodes if ep.get('season') == season_filter]
        
        if not episodes:
            st.info("No hay episodios disponibles en esta página")
            return None
        
        # Información de paginación
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if page_data.get('has_prev', False):
                if st.button("⬅️ Anterior", key="prev_page"):
                    st.session_state.episodes_page = max(1, current_page - 1)
                    st.rerun()
        
        with col2:
            st.markdown(f"**Página {current_page} de {page_data.get('total_pages', 1)}**")
            st.caption(f"Total: {page_data.get('total_episodes', 0)} episodios")
        
        with col3:
            if page_data.get('has_next', False):
                if st.button("Siguiente ➡️", key="next_page"):
                    st.session_state.episodes_page = current_page + 1
                    st.rerun()
        
        # Renderizar grid de episodios
        return EpisodesUI._render_episodes_grid(episodes, f"page_{current_page}")
    
    @staticmethod
    def _render_episodes_grid(episodes: List[Dict[str, Any]], key_prefix: str) -> Optional[str]:
        """
        Renderiza grid de episodios
        
        Args:
            episodes: Lista de episodios
            key_prefix: Prefijo para keys únicos
            
        Returns:
            ID del episodio seleccionado
        """
        # Renderizar en grid de 2 columnas
        for i in range(0, len(episodes), 2):
            col1, col2 = st.columns(2)
            
            # Episodio 1
            with col1:
                if i < len(episodes):
                    episode_id = EpisodesUI._render_episode_card(episodes[i], f"{key_prefix}_{i}")
                    if episode_id:
                        return episode_id
            
            # Episodio 2
            with col2:
                if i + 1 < len(episodes):
                    episode_id = EpisodesUI._render_episode_card(episodes[i + 1], f"{key_prefix}_{i+1}")
                    if episode_id:
                        return episode_id
        
        return None
    
    @staticmethod
    def _render_episode_card(episode: Dict[str, Any], key: str) -> Optional[str]:
        """
        Renderiza tarjeta individual de episodio
        
        Args:
            episode: Datos del episodio
            key: Key único para el componente
            
        Returns:
            ID del episodio si se selecciona
        """
        with st.container():
            # Imagen del episodio
            image_url = episode.get('image_url', '')
            if image_url:
                try:
                    st.image(
                        image_url,
                        caption=f"T{episode.get('season')}E{episode.get('episode_number')}",
                        use_column_width=True
                    )
                except:
                    # Fallback si la imagen falla
                    st.markdown("🎬 *Imagen no disponible*")
            else:
                st.markdown("🎬 *Sin imagen*")
            
            # Información del episodio
            st.markdown(f"**{episode.get('name', 'Sin título')}**")
            st.caption(f"Temporada {episode.get('season', 0)} • Episodio {episode.get('episode_number', 0)}")
            
            if episode.get('formatted_date'):
                st.caption(f"📅 {episode.get('formatted_date')}")
            
            # Sinopsis (truncada)
            synopsis = episode.get('synopsis', '')
            if synopsis:
                truncated_synopsis = synopsis[:100] + "..." if len(synopsis) > 100 else synopsis
                st.markdown(f"*{truncated_synopsis}*")
            
            # Botón de selección
            if st.button(
                "🎭 Generar Reflexión",
                key=f"select_episode_{key}",
                use_container_width=True
            ):
                return episode.get('id')
            
            st.markdown("---")
        
        return None
    
    @staticmethod
    def render_episode_detail(episode: Dict[str, Any]):
        """
        Renderiza detalle completo de un episodio
        
        Args:
            episode: Datos completos del episodio
        """
        # Header del episodio
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Imagen del episodio
            image_url = episode.get('image_url', '')
            if image_url:
                try:
                    st.image(
                        image_url,
                        caption=f"T{episode.get('season')}E{episode.get('episode_number')}",
                        use_column_width=True
                    )
                except:
                    st.markdown("🎬 *Imagen no disponible*")
        
        with col2:
            # Información del episodio
            st.markdown(f"## 📺 {episode.get('name', 'Sin título')}")
            
            # Metadatos
            col_meta1, col_meta2 = st.columns(2)
            
            with col_meta1:
                st.metric("Temporada", episode.get('season', 0))
                
            with col_meta2:
                st.metric("Episodio", episode.get('episode_number', 0))
            
            if episode.get('formatted_date'):
                st.markdown(f"**📅 Fecha de emisión:** {episode.get('formatted_date')}")
        
        # Sinopsis completa
        if episode.get('synopsis'):
            st.markdown("### 📖 Sinopsis")
            st.markdown(episode.get('synopsis'))
        
        st.markdown("---")
    
    @staticmethod
    def render_seasons_overview(seasons_data: Dict[int, Dict[str, Any]]) -> Optional[int]:
        """
        Renderiza vista general de temporadas
        
        Args:
            seasons_data: Datos de temporadas
            
        Returns:
            Temporada seleccionada o None
        """
        st.markdown("### 📅 Temporadas de Los Simpsons")
        
        if not seasons_data:
            st.info("No hay datos de temporadas disponibles")
            return None
        
        # Renderizar temporadas en grid
        seasons = sorted(seasons_data.keys())
        
        for i in range(0, len(seasons), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(seasons):
                    season_num = seasons[i + j]
                    season_data = seasons_data[season_num]
                    
                    with col:
                        st.markdown(f"#### Temporada {season_num}")
                        st.metric("Episodios", season_data.get('episode_count', 0))
                        
                        if st.button(
                            f"Ver Temporada {season_num}",
                            key=f"season_{season_num}",
                            use_container_width=True
                        ):
                            return season_num
        
        return None
    
    @staticmethod
    def render_quote_with_episode_context(quote_data: Dict[str, Any]):
        """
        Renderiza cita con contexto completo de episodio
        
        Args:
            quote_data: Datos de la cita con contexto de episodio
        """
        # Información del episodio (si está disponible)
        episode_info = quote_data.get('episode_info')
        
        if episode_info:
            # Header del episodio
            st.markdown("### 📺 Contexto del Episodio")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{episode_info.get('name', 'Sin título')}**")
                st.caption(f"Temporada {episode_info.get('season')} • Episodio {episode_info.get('episode_number')}")
                
                if episode_info.get('synopsis'):
                    with st.expander("📖 Ver sinopsis"):
                        st.markdown(episode_info.get('synopsis'))
            
            with col2:
                # Imagen del episodio
                episode_image = episode_info.get('image_url', '')
                if episode_image:
                    try:
                        st.image(
                            episode_image,
                            caption="Episodio",
                            use_column_width=True
                        )
                    except:
                        pass
            
            st.markdown("---")
        
        # Renderizar la cita con el componente estándar
        UIComponents.render_quote_card_optimized(quote_data, show_actions=True)
    
    @staticmethod
    def render_episode_search_results(quotes_with_episodes: List[Dict[str, Any]]):
        """
        Renderiza resultados de búsqueda de citas por episodio
        
        Args:
            quotes_with_episodes: Lista de citas con contexto de episodio
        """
        if not quotes_with_episodes:
            st.info("No se encontraron resultados para la búsqueda")
            return
        
        st.markdown(f"### 🔍 Resultados de Búsqueda ({len(quotes_with_episodes)} encontrados)")
        
        for i, quote_data in enumerate(quotes_with_episodes):
            with st.expander(
                f"#{i+1} - {quote_data.get('character', 'Desconocido')} en '{quote_data.get('episode_info', {}).get('name', 'Episodio desconocido')}'",
                expanded=i == 0  # Expandir solo el primero
            ):
                EpisodesUI.render_quote_with_episode_context(quote_data)
    
    @staticmethod
    def render_character_episodes_browser(character_name: str, episodes: List[Dict[str, Any]]) -> Optional[str]:
        """
        Renderiza navegador de episodios para un personaje específico
        
        Args:
            character_name: Nombre del personaje
            episodes: Lista de episodios relevantes
            
        Returns:
            ID del episodio seleccionado
        """
        if not episodes:
            st.info(f"No se encontraron episodios relevantes para {character_name}")
            return None
        
        st.markdown(f"### 👤 Episodios de {character_name}")
        st.caption(f"{len(episodes)} episodios encontrados")
        
        # Renderizar episodios ordenados por relevancia
        for i, episode in enumerate(episodes[:5]):  # Mostrar top 5
            with st.expander(
                f"#{i+1} - {episode.get('name', 'Sin título')} (Relevancia: {episode.get('relevance_score', 0)})",
                expanded=i == 0
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Temporada {episode.get('season')} • Episodio {episode.get('episode_number')}**")
                    
                    if episode.get('synopsis'):
                        st.markdown(episode.get('synopsis')[:200] + "...")
                    
                    if st.button(
                        f"🎭 Generar Reflexión de {character_name}",
                        key=f"char_episode_{episode.get('id')}_{i}"
                    ):
                        return episode.get('id')
                
                with col2:
                    if episode.get('image_url'):
                        try:
                            st.image(episode.get('image_url'), use_column_width=True)
                        except:
                            pass
        
        return None