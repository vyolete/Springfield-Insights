"""
Springfield Insights - Aplicación Principal Optimizada
Implementa mejores prácticas de UX/UI, performance y arquitectura modular
"""
import streamlit as st
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Configurar path para imports
sys.path.append(str(Path(__file__).parent))

# Imports optimizados con lazy loading
from config.settings import settings
from ui.theme import SimpsonsTheme
from ui.components import (
    UIComponents, LoadingStates, StateManager, 
    ErrorHandler, PerformanceOptimizer, ResponsiveLayout
)
from services.performance_monitor import performance_monitor
from services.cache_optimizer import cache_optimizer, setup_automatic_cleanup

# Configuración de logging optimizada
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpringfieldInsightsOptimized:
    """
    Aplicación principal optimizada de Springfield Insights
    Implementa arquitectura modular, caching inteligente y UX mejorada
    """
    
    def __init__(self):
        """Inicialización optimizada con lazy loading"""
        # Inicializar estado de sesión
        StateManager.initialize_session_state()
        
        # Marcar UI como inicializada
        if not st.session_state.ui_initialized:
            self._initialize_ui()
            st.session_state.ui_initialized = True
        
        # Servicios se cargan bajo demanda
        self._services = None
    
    @property
    def services(self) -> Dict[str, Any]:
        """Lazy loading de servicios pesados"""
        if self._services is None:
            self._services = PerformanceOptimizer.get_cached_services()
        return self._services
    
    def _initialize_ui(self):
        """Inicialización única de la UI"""
        # Configuración de página (solo una vez)
        st.set_page_config(
            page_title=settings.APP_TITLE,
            page_icon="🍩",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Aplicar tema personalizado
        SimpsonsTheme.apply_custom_css()
        
        # Precargar datos críticos en background
        PerformanceOptimizer.preload_critical_data()
    
    def run(self):
        """Ejecuta la aplicación principal con control de flujo optimizado"""
        start_time = time.time()
        
        try:
            # Configurar limpieza automática de cache
            setup_automatic_cleanup()
            
            # Verificar configuración (solo si es necesario)
            if not self._check_configuration():
                return
            
            # Procesar acciones pendientes ANTES del renderizado
            self._process_pending_actions()
            
            # Renderizar interfaz principal
            self._render_main_interface()
            
            # Trackear tiempo de carga de página
            performance_monitor.track_page_load(start_time, "main_app")
            
        except Exception as e:
            logger.error(f"Error crítico en la aplicación: {e}")
            ErrorHandler.show_generic_error(e)
    
    def _check_configuration(self) -> bool:
        """
        Verificación optimizada de configuración (con cache)
        
        Returns:
            True si la configuración es correcta
        """
        # Solo verificar si no se ha hecho antes en esta sesión
        if hasattr(st.session_state, 'config_validated') and st.session_state.config_validated:
            return st.session_state.can_run
        
        # Verificación completa solo la primera vez
        with LoadingStates.show_api_loading("🔍 Validando configuración..."):
            try:
                from config.environment_validator import validate_environment_startup
                can_run, validation_results = validate_environment_startup()
                
                # Cachear resultados
                st.session_state.config_validated = True
                st.session_state.can_run = can_run
                st.session_state.validation_results = validation_results
                
                if not can_run:
                    self._show_configuration_error(validation_results)
                    return False
                
                # Mostrar advertencias si las hay (sin bloquear)
                self._show_configuration_warnings(validation_results)
                return True
                
            except Exception as e:
                logger.error(f"Error en validación: {e}")
                ErrorHandler.show_generic_error(e)
                return False
    
    def _process_pending_actions(self):
        """
        Procesa acciones pendientes ANTES del renderizado para evitar duplicaciones
        """
        # Procesar solicitud de nueva cita
        if StateManager.should_request_new_quote() and not StateManager.is_processing():
            self._handle_new_quote_request_optimized()
            StateManager.clear_request_flags()
        
        # Procesar guardado de favorito
        if st.session_state.get('save_current_quote', False):
            self._handle_save_favorite()
            st.session_state.save_current_quote = False
        
        # Procesar modal de compartir
        if st.session_state.get('show_share_modal', False):
            self._handle_share_modal()
    
    def _handle_new_quote_request_optimized(self):
        """
        Maneja solicitud de nueva cita con UX optimizada y sin duplicaciones
        """
        # Prevenir múltiples ejecuciones
        StateManager.set_processing(True)
        
        # Mostrar estado de carga avanzado
        status_container = LoadingStates.show_quote_generation_loading()
        
        try:
            # Obtener cita analizada
            result = self.services['quote_processor'].get_analyzed_quote()
            
            if result and result.get('success'):
                # Actualizar estado sin rerun
                StateManager.set_current_quote(result)
                StateManager.increment_quotes_analyzed()
                
                # Actualizar status
                status_container.update(label="✅ ¡Reflexión filosófica generada!", state="complete")
                
                # Notificación no intrusiva
                st.toast("🎭 Nueva reflexión filosófica lista", icon="✨")
                
            else:
                error_msg = result.get('error_message', 'Error desconocido') if result else 'Sin respuesta'
                status_container.update(label="❌ Error en generación", state="error")
                ErrorHandler.show_api_error(error_msg)
                
        except Exception as e:
            logger.error(f"Error en generación optimizada: {e}")
            status_container.update(label="❌ Error inesperado", state="error")
            ErrorHandler.show_generic_error(e)
        
        finally:
            # Liberar estado de procesamiento
            StateManager.set_processing(False)
    
    def _handle_save_favorite(self):
        """Maneja guardado de favorito con feedback optimizado"""
        current_quote = StateManager.get_current_quote()
        
        if current_quote:
            success = self.services['favorites_manager'].save_favorite(current_quote)
            
            if success:
                st.toast("💾 Cita guardada en favoritos", icon="⭐")
            else:
                st.toast("⚠️ Esta cita ya está en favoritos", icon="📝")
    
    def _handle_share_modal(self):
        """Maneja modal de compartir"""
        current_quote = StateManager.get_current_quote()
        
        if current_quote:
            with st.expander("🔗 Compartir Reflexión", expanded=True):
                quote_text = current_quote.get('quote', '')
                character = current_quote.get('character', '')
                
                share_text = f'"{quote_text}" - {character} (vía Springfield Insights)'
                
                st.text_area("Texto para compartir:", share_text, height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copiar"):
                        st.session_state.copied_text = share_text
                        st.toast("📋 Copiado al portapapeles", icon="✅")
                
                with col2:
                    if st.button("❌ Cerrar"):
                        st.session_state.show_share_modal = False
                        st.rerun()
    
    def _render_main_interface(self):
        """Renderiza la interfaz principal optimizada"""
        # Header principal
        SimpsonsTheme.create_header(
            title="🍩 Springfield Insights",
            subtitle="Explorando la filosofía y crítica social de Los Simpsons"
        )
        
        # Sidebar optimizado
        self._render_optimized_sidebar()
        
        # Navegación por pestañas
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎲 Explorar", "📺 Episodios", "⭐ Favoritos", "📊 Analytics", "⚡ Performance", "ℹ️ Acerca de"])
        
        with tab1:
            self._render_explore_tab_optimized()
        
        with tab2:
            self._render_episodes_tab_optimized()
        
        with tab3:
            self._render_favorites_tab_optimized()
        
        with tab4:
            self._render_analytics_tab_optimized()
        
        with tab5:
            self._render_performance_tab()
        
        with tab6:
            self._render_about_tab_optimized()
    
    def _render_optimized_sidebar(self):
        """Renderiza sidebar optimizado con métricas en tiempo real"""
        with st.sidebar:
            st.markdown("### 📚 Acerca del Proyecto")
            
            st.markdown("""
            **Springfield Insights** utiliza IA para generar reflexiones filosóficas 
            originales al estilo de Los Simpsons.
            """)
            
            # Métricas de sesión (actualizadas automáticamente)
            st.markdown("### 📊 Estadísticas")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Reflexiones", st.session_state.quotes_analyzed)
            
            with col2:
                favorites_count = len(self.services['favorites_manager'].load_favorites())
                st.metric("Favoritos", favorites_count)
            
            # Métricas de performance
            performance_monitor.render_performance_sidebar()
            
            # Estado del sistema
            st.markdown("### 🔧 Estado del Sistema")
            
            if StateManager.is_processing():
                st.warning("⏳ Procesando...")
            else:
                st.success("✅ Listo")
            
            # Botón de nueva sesión (con confirmación)
            st.markdown("### 🔄 Sesión")
            if st.button("Nueva Sesión", use_container_width=True):
                if st.session_state.quotes_analyzed > 0:
                    st.warning("⚠️ Esto borrará tu progreso actual")
                    if st.button("Confirmar Reset"):
                        st.session_state.clear()
                        st.rerun()
                else:
                    st.session_state.clear()
                    st.rerun()
    
    def _render_explore_tab_optimized(self):
        """Renderiza pestaña de exploración optimizada"""
        # Layout responsivo
        _, col_main, _ = ResponsiveLayout.create_main_layout()
        
        with col_main:
            # Botón principal con estado
            button_disabled = StateManager.is_processing()
            button_text = "⏳ Generando..." if button_disabled else "🎲 Obtener Nueva Reflexión Filosófica"
            
            if st.button(
                button_text, 
                key="main_quote_button",
                disabled=button_disabled,
                use_container_width=True,
                type="primary"
            ):
                # Solo establecer flag, el procesamiento se hace en _process_pending_actions
                st.session_state.request_new_quote = True
                st.rerun()
            
            # Mostrar cita actual (si existe)
            current_quote = StateManager.get_current_quote()
            if current_quote:
                st.markdown("---")
                UIComponents.render_quote_card_optimized(current_quote, show_actions=True)
            
            # Mensaje de bienvenida si no hay cita
            elif not StateManager.is_processing():
                st.info("""
                🎭 **¡Bienvenido a Springfield Insights!**
                
                Haz clic en el botón para generar una reflexión filosófica original 
                al estilo de Los Simpsons, creada especialmente por inteligencia artificial.
                
                💡 **Nuevo:** Explora la pestaña "📺 Episodios" para generar reflexiones 
                basadas en episodios específicos de la serie.
                """)
    
    def _render_episodes_tab_optimized(self):
        """Renderiza pestaña de episodios con navegación y búsqueda"""
        from ui.episodes_components import EpisodesUI
        from services.episodes_service import EpisodesService
        from services.quotes_service import QuotesService
        
        # Inicializar servicios
        episodes_service = EpisodesService()
        quotes_service = QuotesService()
        
        st.markdown("## 📺 Explorar por Episodios")
        st.markdown("Genera reflexiones filosóficas basadas en episodios específicos de Los Simpsons")
        
        # Pestañas secundarias para diferentes modos de exploración
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔍 Buscar Episodios", "📅 Por Temporadas", "👤 Por Personajes"])
        
        with sub_tab1:
            self._render_episode_search_mode(episodes_service, quotes_service)
        
        with sub_tab2:
            self._render_seasons_mode(episodes_service, quotes_service)
        
        with sub_tab3:
            self._render_characters_episodes_mode(episodes_service, quotes_service)
    
    def _render_episode_search_mode(self, episodes_service, quotes_service):
        """Modo de búsqueda de episodios"""
        from ui.episodes_components import EpisodesUI
        
        # Navegador de episodios
        selected_episode_id = EpisodesUI.render_episodes_browser(episodes_service)
        
        if selected_episode_id:
            # Procesar solicitud de cita basada en episodio
            if not StateManager.is_processing():
                self._handle_episode_quote_request(selected_episode_id, quotes_service, episodes_service)
    
    def _render_seasons_mode(self, episodes_service, quotes_service):
        """Modo de exploración por temporadas"""
        from ui.episodes_components import EpisodesUI
        
        st.markdown("### 📅 Explorar por Temporadas")
        
        # Obtener resumen de temporadas
        with st.spinner("📊 Cargando información de temporadas..."):
            seasons_data = episodes_service.get_seasons_summary()
        
        if not seasons_data:
            st.error("No se pudo cargar información de temporadas")
            return
        
        # Renderizar vista de temporadas
        selected_season = EpisodesUI.render_seasons_overview(seasons_data)
        
        if selected_season:
            st.markdown(f"### 🎬 Temporada {selected_season}")
            
            # Generar citas para la temporada
            if st.button(f"🎲 Generar Reflexiones de la Temporada {selected_season}", key=f"season_{selected_season}_quotes"):
                self._handle_season_quotes_request(selected_season, quotes_service)
    
    def _render_characters_episodes_mode(self, episodes_service, quotes_service):
        """Modo de exploración por personajes"""
        from ui.episodes_components import EpisodesUI
        
        st.markdown("### 👤 Episodios por Personajes")
        
        # Selector de personaje
        main_characters = [
            "Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson",
            "Ned Flanders", "Moe Szyslak", "Chief Wiggum", "Apu Nahasapeemapetilon"
        ]
        
        selected_character = st.selectbox(
            "Selecciona un personaje:",
            main_characters,
            key="character_episodes_selector"
        )
        
        if selected_character:
            # Buscar episodios del personaje
            with st.spinner(f"🔍 Buscando episodios de {selected_character}..."):
                character_episodes = quotes_service.get_character_episodes(selected_character)
            
            if character_episodes:
                # Renderizar navegador de episodios del personaje
                selected_episode_id = EpisodesUI.render_character_episodes_browser(
                    selected_character, character_episodes
                )
                
                if selected_episode_id:
                    self._handle_episode_quote_request(selected_episode_id, quotes_service, episodes_service)
            else:
                st.info(f"No se encontraron episodios específicos para {selected_character}")
    
    def _handle_episode_quote_request(self, episode_id: str, quotes_service, episodes_service):
        """Maneja solicitud de cita basada en episodio específico"""
        StateManager.set_processing(True)
        
        status_container = LoadingStates.show_quote_generation_loading()
        status_container.update(label="📺 Obteniendo contexto del episodio...", state="running")
        
        try:
            # Generar cita con contexto de episodio
            result = quotes_service.generate_quote_with_episode_context(episode_id)
            
            if result and result.get('success'):
                # Obtener información completa del episodio
                episode_detail = episodes_service.get_episode_detail(episode_id)
                
                if episode_detail:
                    result['episode_info'] = {
                        'id': episode_detail['id'],
                        'name': episode_detail['name'],
                        'season': episode_detail['season'],
                        'episode_number': episode_detail['episode_number'],
                        'synopsis': episode_detail['synopsis'],
                        'image_url': episode_detail.get('image_url', ''),
                        'formatted_date': episode_detail.get('formatted_date', '')
                    }
                
                # Actualizar estado
                StateManager.set_current_quote(result)
                StateManager.increment_quotes_analyzed()
                
                status_container.update(label="✅ ¡Reflexión episódica generada!", state="complete")
                st.toast("📺 Reflexión basada en episodio lista", icon="🎭")
                
                # Mostrar resultado
                st.markdown("---")
                from ui.episodes_components import EpisodesUI
                EpisodesUI.render_quote_with_episode_context(result)
                
            else:
                error_msg = result.get('error_message', 'Error desconocido') if result else 'Sin respuesta'
                status_container.update(label="❌ Error generando reflexión episódica", state="error")
                ErrorHandler.show_api_error(error_msg)
                
        except Exception as e:
            logger.error(f"Error generando cita de episodio {episode_id}: {e}")
            status_container.update(label="❌ Error inesperado", state="error")
            ErrorHandler.show_generic_error(e)
        
        finally:
            StateManager.set_processing(False)
    
    def _handle_season_quotes_request(self, season: int, quotes_service):
        """Maneja solicitud de citas de una temporada completa"""
        StateManager.set_processing(True)
        
        with st.spinner(f"🎬 Generando reflexiones de la Temporada {season}..."):
            try:
                season_quotes = quotes_service.get_quotes_for_season(season, limit=5)
                
                if season_quotes:
                    st.success(f"✅ {len(season_quotes)} reflexiones generadas para la Temporada {season}")
                    
                    # Mostrar resultados
                    from ui.episodes_components import EpisodesUI
                    EpisodesUI.render_episode_search_results(season_quotes)
                    
                else:
                    st.warning(f"No se pudieron generar reflexiones para la Temporada {season}")
                    
            except Exception as e:
                logger.error(f"Error generando citas de temporada {season}: {e}")
                ErrorHandler.show_generic_error(e)
            
            finally:
                StateManager.set_processing(False)
    
    def _render_performance_tab(self):
        """Renderiza pestaña de métricas de performance"""
        st.markdown("## ⚡ Métricas de Performance")
        st.markdown("Monitoreo en tiempo real del rendimiento de la aplicación")
        
        # Métricas detalladas
        performance_monitor.render_detailed_metrics()
        
        st.markdown("---")
        
        # Estadísticas de cache
        from services.cache_optimizer import render_cache_stats
        render_cache_stats()
        
        st.markdown("---")
        
        # Información del sistema
        st.markdown("### 💻 Información del Sistema")
        
        try:
            import psutil
            import platform
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cpu_percent = psutil.cpu_percent(interval=1)
                st.metric("CPU", f"{cpu_percent:.1f}%")
            
            with col2:
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                st.metric("RAM Sistema", f"{memory_percent:.1f}%")
            
            with col3:
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                st.metric("Disco", f"{disk_percent:.1f}%")
            
            # Información adicional
            with st.expander("🔧 Detalles del Sistema"):
                st.markdown(f"**Sistema Operativo:** {platform.system()} {platform.release()}")
                st.markdown(f"**Procesador:** {platform.processor()}")
                st.markdown(f"**Python:** {platform.python_version()}")
                st.markdown(f"**Arquitectura:** {platform.architecture()[0]}")
                
        except ImportError:
            st.info("📊 Instala `psutil` para ver métricas detalladas del sistema")
        
        # Recomendaciones de optimización
        st.markdown("### 💡 Recomendaciones de Optimización")
        
        summary = performance_monitor.get_performance_summary()
        
        recommendations = []
        
        # Analizar métricas y generar recomendaciones
        if summary.get('current_memory', 0) > 300:
            recommendations.append("🧹 **Memoria alta detectada** - Considera limpiar el cache")
        
        if summary.get('avg_page_load', 0) > 3:
            recommendations.append("⚡ **Carga lenta detectada** - Verifica tu conexión a internet")
        
        cache_efficiency = summary.get('cache_efficiency', {})
        if cache_efficiency:
            avg_cache = sum(cache_efficiency.values()) / len(cache_efficiency)
            if avg_cache < 70:
                recommendations.append("🗄️ **Baja eficiencia de cache** - Los datos se están regenerando frecuentemente")
        
        if summary.get('recent_errors', 0) > 0:
            recommendations.append("🚨 **Errores recientes detectados** - Revisa la configuración de APIs")
        
        if not recommendations:
            recommendations.append("✅ **¡Excelente!** - La aplicación está funcionando de manera óptima")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        # Acciones de optimización
        st.markdown("### 🛠️ Acciones de Optimización")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Limpieza Completa", use_container_width=True):
                cache_optimizer.clear_all_caches()
                performance_monitor._trigger_memory_cleanup()
                st.success("✅ Limpieza completa realizada")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reiniciar Métricas", use_container_width=True):
                # Reiniciar métricas de performance
                performance_monitor.metrics = {
                    'page_load_time': [],
                    'search_time': [],
                    'llm_response_time': [],
                    'memory_usage': [],
                    'cache_hit_rate': {},
                    'api_calls': [],
                    'errors': []
                }
                st.success("✅ Métricas reiniciadas")
                st.rerun()
        
        with col3:
            if st.button("📊 Exportar Métricas", use_container_width=True):
                import json
                from datetime import datetime
                
                metrics_export = {
                    'timestamp': datetime.now().isoformat(),
                    'performance_summary': summary,
                    'cache_stats': cache_optimizer.get_global_cache_stats(),
                    'system_info': {
                        'platform': platform.system(),
                        'python_version': platform.python_version()
                    }
                }
                
                json_str = json.dumps(metrics_export, indent=2, default=str)
                
                st.download_button(
                    label="📥 Descargar Métricas (JSON)",
                    data=json_str,
                    file_name=f"springfield_insights_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    def _render_favorites_tab_optimized(self):
        """Renderiza pestaña de favoritos optimizada"""
        favorites = self.services['favorites_manager'].load_favorites()
        
        if not favorites:
            st.info("🌟 No tienes reflexiones favoritas aún. ¡Explora y guarda las que más te gusten!")
            return
        
        # Estadísticas rápidas
        stats = self.services['favorites_manager'].get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", stats['total_favorites'])
        with col2:
            st.metric("Personajes", stats['unique_characters'])
        with col3:
            if stats['most_quoted_character']:
                st.metric("Más Popular", stats['most_quoted_character'])
        with col4:
            if st.button("📥 Exportar"):
                self._export_favorites_optimized()
        
        # Filtros optimizados
        with st.expander("🔍 Filtros", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                characters = list(set(fav.get('character', 'Unknown') for fav in favorites))
                selected_character = st.selectbox("Por personaje:", ["Todos"] + sorted(characters))
            
            with col2:
                sort_options = ["Más recientes", "Más antiguos", "Por personaje"]
                sort_by = st.selectbox("Ordenar:", sort_options)
        
        # Aplicar filtros
        filtered_favorites = self._apply_favorites_filters(favorites, selected_character, sort_by)
        
        # Mostrar favoritos con paginación
        self._render_favorites_list(filtered_favorites)
    
    def _render_analytics_tab_optimized(self):
        """Renderiza pestaña de analytics optimizada"""
        favorites = self.services['favorites_manager'].load_favorites()
        
        if len(favorites) < 2:
            st.info("📊 Necesitas al menos 2 reflexiones favoritas para generar analytics.")
            return
        
        # Generar analytics con cache
        with st.spinner("📊 Generando insights..."):
            insights = self._get_cached_analytics(favorites)
        
        if 'error' in insights:
            ErrorHandler.show_api_error(insights['error'])
            return
        
        # Mostrar resultados
        self._render_analytics_results(insights)
    
    def _render_about_tab_optimized(self):
        """Renderiza pestaña de información optimizada"""
        st.markdown("""
        ### 🍩 Springfield Insights
        
        Una aplicación académica que utiliza **inteligencia artificial** para generar 
        reflexiones filosóficas originales al estilo de Los Simpsons.
        
        #### 🎯 Características Principales
        
        - **Generación Original**: Reflexiones únicas creadas por GPT-4
        - **Análisis Filosófico**: Interpretaciones académicas profundas
        - **Sistema de Favoritos**: Guarda y organiza tus reflexiones preferidas
        - **Analytics Avanzados**: Descubre patrones en tus favoritos
        - **UX Optimizada**: Interfaz fluida y responsiva
        
        #### 🔧 Tecnologías
        
        - **Python 3.10+** - Lenguaje principal
        - **Streamlit** - Framework de interfaz
        - **OpenAI GPT-4** - Generación de contenido
        - **The Simpsons API** - Datos de personajes
        
        #### 📊 Arquitectura
        
        - **Modular**: Separación clara de responsabilidades
        - **Cacheable**: Optimización de performance
        - **Resiliente**: Múltiples fallbacks y manejo de errores
        - **Escalable**: Diseño preparado para crecimiento
        """)
        
        # Información técnica adicional
        with st.expander("🔧 Detalles Técnicos"):
            st.code("""
            Arquitectura Optimizada:
            ├── UI Components (Modular)
            ├── Services (Cached)
            ├── State Management (Centralized)
            ├── Error Handling (Robust)
            └── Performance (Optimized)
            """)
    
    # Métodos auxiliares optimizados
    
    @st.cache_data(ttl=300)
    def _get_cached_analytics(_self, favorites: list) -> Dict[str, Any]:
        """Analytics con cache de 5 minutos"""
        try:
            return _self.services['analytics'].generate_insights_report(favorites)
        except Exception as e:
            return {'error': str(e)}
    
    def _apply_favorites_filters(self, favorites: list, character: str, sort_by: str) -> list:
        """Aplica filtros a favoritos"""
        filtered = favorites
        
        if character != "Todos":
            filtered = [fav for fav in filtered if fav.get('character') == character]
        
        # Aplicar ordenamiento
        if sort_by == "Más recientes":
            filtered.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        elif sort_by == "Más antiguos":
            filtered.sort(key=lambda x: x.get('saved_at', ''))
        elif sort_by == "Por personaje":
            filtered.sort(key=lambda x: x.get('character', ''))
        
        return filtered
    
    def _render_favorites_list(self, favorites: list):
        """Renderiza lista de favoritos con paginación"""
        # Paginación simple
        items_per_page = 5
        total_pages = (len(favorites) - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox("Página:", range(1, total_pages + 1)) - 1
        else:
            page = 0
        
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        page_favorites = favorites[start_idx:end_idx]
        
        # Mostrar favoritos de la página
        for i, fav in enumerate(page_favorites):
            with st.expander(f"#{start_idx + i + 1} - {fav.get('character', 'Desconocido')}"):
                UIComponents.render_quote_card_optimized(fav, show_actions=False)
                
                # Acciones específicas de favoritos
                col1, col2 = st.columns(2)
                with col1:
                    if fav.get('saved_at'):
                        st.caption(f"📅 Guardado: {fav['saved_at'][:10]}")
                
                with col2:
                    if st.button("🗑️ Eliminar", key=f"delete_{fav.get('favorite_id')}"):
                        if self.services['favorites_manager'].remove_favorite(fav.get('favorite_id')):
                            st.toast("🗑️ Favorito eliminado", icon="✅")
                            st.rerun()
    
    def _render_analytics_results(self, insights: Dict[str, Any]):
        """Renderiza resultados de analytics"""
        summary = insights.get('summary', {})
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Reflexiones", summary.get('total_quotes_analyzed', 0))
        with col2:
            st.metric("Personajes", summary.get('unique_characters', 0))
        with col3:
            st.metric("Complejidad Avg", f"{summary.get('average_complexity_score', 0):.2f}")
        with col4:
            st.metric("Más Complejo", summary.get('most_complex_character', 'N/A'))
        
        # Análisis temático
        thematic = insights.get('thematic_analysis', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧠 Temas Filosóficos")
            themes = thematic.get('top_philosophical_themes', [])
            for i, theme in enumerate(themes[:5], 1):
                st.write(f"{i}. {theme.title()}")
        
        with col2:
            st.subheader("🏛️ Crítica Social")
            themes = thematic.get('top_social_critique_themes', [])
            for i, theme in enumerate(themes[:5], 1):
                st.write(f"{i}. {theme.title()}")
    
    def _export_favorites_optimized(self):
        """Exporta favoritos de forma optimizada"""
        try:
            import json
            from datetime import datetime
            
            favorites = self.services['favorites_manager'].load_favorites()
            
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'app_version': '2.0-optimized',
                'total_favorites': len(favorites),
                'favorites': favorites
            }
            
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Descargar Favoritos (JSON)",
                data=json_str,
                file_name=f"springfield_insights_favorites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            st.toast("📥 Archivo listo para descarga", icon="✅")
            
        except Exception as e:
            logger.error(f"Error exportando favoritos: {e}")
            ErrorHandler.show_generic_error(e)
    
    def _show_configuration_error(self, validation_results: Dict[str, Any]):
        """Muestra errores de configuración de forma optimizada"""
        st.error("🛑 Configuración Incompleta")
        
        with st.expander("🔧 Detalles de Configuración", expanded=True):
            for component, result in validation_results.items():
                if component == 'overall':
                    continue
                
                if result['status'] == 'error':
                    st.markdown(f"#### ❌ {component.replace('_', ' ').title()}")
                    for detail in result['details']:
                        if '❌' in detail:
                            st.write(f"- {detail}")
        
        st.info("""
        💡 **Solución Rápida:**
        
        1. Configura tu `OPENAI_API_KEY` en el archivo `.env`
        2. Reinicia la aplicación
        3. ¡Listo para generar reflexiones filosóficas!
        """)
    
    def _show_configuration_warnings(self, validation_results: Dict[str, Any]):
        """Muestra advertencias de configuración"""
        warnings_found = False
        
        for component, result in validation_results.items():
            if component == 'overall':
                continue
            
            if result['status'] == 'warning':
                if not warnings_found:
                    st.warning("⚠️ Configuración con advertencias (la app funcionará)")
                    warnings_found = True

def main():
    """Función principal optimizada"""
    try:
        app = SpringfieldInsightsOptimized()
        app.run()
        
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        st.error("😵 Error crítico en Springfield. Recarga la página.")

if __name__ == "__main__":
    main()