"""
Componentes UI modulares optimizados para Springfield Insights
Implementa mejores prácticas de UX/UI y performance en Streamlit
"""
import streamlit as st
from typing import Dict, Any, Optional
import logging
from ui.theme import SimpsonsTheme

logger = logging.getLogger(__name__)

class UIComponents:
    """Componentes UI reutilizables y optimizados"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def get_character_image(character_name: str, image_url: str = "") -> Optional[str]:
        """
        Obtiene y cachea imagen del personaje con fallback
        
        Args:
            character_name: Nombre del personaje
            image_url: URL de imagen (opcional)
            
        Returns:
            URL de imagen válida o None
        """
        if image_url:
            try:
                # Validar que la URL sea accesible
                import requests
                response = requests.head(image_url, timeout=3)
                if response.status_code == 200:
                    return image_url
            except:
                pass
        
        # Fallback a placeholder personalizado
        safe_name = character_name.replace(' ', '+').replace("'", "")
        return f"https://via.placeholder.com/500x300/FFD700/2F4F4F?text={safe_name}"
    
    @staticmethod
    def render_quote_card_optimized(quote_data: Dict[str, Any], show_actions: bool = True) -> None:
        """
        Renderiza tarjeta de cita optimizada con imágenes y acciones
        
        Args:
            quote_data: Datos de la cita
            show_actions: Si mostrar botones de acción
        """
        if not quote_data or not quote_data.get('success'):
            st.error("❌ No hay datos de cita válidos")
            return
        
        character = quote_data.get('character', 'Desconocido')
        quote_text = quote_data.get('quote', '')
        analysis = quote_data.get('analysis', '')
        image_url = quote_data.get('image', '')
        
        # Container principal con estilo
        with st.container():
            # Imagen del personaje (optimizada)
            col_img, col_content = st.columns([1, 2])
            
            with col_img:
                optimized_image = UIComponents.get_character_image(character, image_url)
                if optimized_image:
                    st.image(
                        optimized_image, 
                        caption=character,
                        use_column_width=True,
                        alt_text=f"Imagen de {character} de Los Simpsons"
                    )
            
            with col_content:
                # Cita principal
                SimpsonsTheme.create_quote_card(quote_text, character, "")
                
                # Análisis filosófico
                if analysis:
                    SimpsonsTheme.create_analysis_section(analysis)
        
        # Acciones (solo si se solicitan)
        if show_actions:
            UIComponents._render_quote_actions(quote_data)
    
    @staticmethod
    def _render_quote_actions(quote_data: Dict[str, Any]) -> None:
        """
        Renderiza acciones de la cita con control de estado
        
        Args:
            quote_data: Datos de la cita
        """
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Nueva Cita", key="new_quote_action", use_container_width=True):
                st.session_state.request_new_quote = True
                st.rerun()
        
        with col2:
            if st.button("💾 Guardar", key="save_quote_action", use_container_width=True):
                st.session_state.save_current_quote = True
                st.rerun()
        
        with col3:
            if st.button("📋 Copiar", key="copy_quote_action", use_container_width=True):
                # Preparar texto para copiar
                copy_text = f'"{quote_data.get("quote", "")}" - {quote_data.get("character", "")}'
                st.session_state.copied_text = copy_text
                st.toast("📋 Cita copiada al portapapeles", icon="✅")
        
        with col4:
            if st.button("🔗 Compartir", key="share_quote_action", use_container_width=True):
                st.session_state.show_share_modal = True
                st.rerun()

class LoadingStates:
    """Manejo centralizado de estados de carga"""
    
    @staticmethod
    def show_quote_generation_loading():
        """Muestra estado de carga para generación de citas"""
        with st.status("🎭 Generando reflexión filosófica...", expanded=True) as status:
            st.write("🔍 Obteniendo personaje de Springfield...")
            st.write("🧠 Generando reflexión filosófica...")
            st.write("📚 Creando análisis académico...")
            return status
    
    @staticmethod
    def show_api_loading(message: str = "Conectando con Springfield..."):
        """Muestra estado de carga para APIs"""
        return st.spinner(message)
    
    @staticmethod
    def show_processing_toast(message: str):
        """Muestra notificación no intrusiva"""
        st.toast(message, icon="⏳")

class StateManager:
    """Gestor centralizado del estado de la aplicación"""
    
    @staticmethod
    def initialize_session_state():
        """Inicializa el estado de sesión con valores por defecto"""
        defaults = {
            'current_quote': None,
            'quotes_analyzed': 0,
            'is_processing': False,
            'request_new_quote': False,
            'save_current_quote': False,
            'show_share_modal': False,
            'copied_text': '',
            'last_generation_time': None,
            'ui_initialized': False
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def is_processing() -> bool:
        """Verifica si hay un proceso en curso"""
        return st.session_state.get('is_processing', False)
    
    @staticmethod
    def set_processing(processing: bool):
        """Establece el estado de procesamiento"""
        st.session_state.is_processing = processing
    
    @staticmethod
    def should_request_new_quote() -> bool:
        """Verifica si se debe solicitar una nueva cita"""
        return st.session_state.get('request_new_quote', False)
    
    @staticmethod
    def clear_request_flags():
        """Limpia las banderas de solicitud"""
        st.session_state.request_new_quote = False
        st.session_state.save_current_quote = False
    
    @staticmethod
    def increment_quotes_analyzed():
        """Incrementa el contador de citas analizadas"""
        st.session_state.quotes_analyzed += 1
    
    @staticmethod
    def get_current_quote() -> Optional[Dict[str, Any]]:
        """Obtiene la cita actual del estado"""
        return st.session_state.get('current_quote')
    
    @staticmethod
    def set_current_quote(quote_data: Dict[str, Any]):
        """Establece la cita actual en el estado"""
        st.session_state.current_quote = quote_data

class ErrorHandler:
    """Manejo centralizado de errores con UX mejorada"""
    
    @staticmethod
    def show_api_error(error_message: str):
        """Muestra error de API con estilo Springfield"""
        st.error(f"🍩 D'oh! {error_message}")
    
    @staticmethod
    def show_llm_error():
        """Muestra error específico de LLM"""
        st.error("🤖 Moe dice que el generador de sabiduría está temporalmente fuera de servicio...")
    
    @staticmethod
    def show_network_error():
        """Muestra error de red"""
        st.error("🌐 ¡Ay, caramba! Problemas de conexión con Springfield...")
    
    @staticmethod
    def show_generic_error(error: Exception):
        """Muestra error genérico con logging"""
        logger.error(f"Error en la aplicación: {error}")
        st.error("😵 ¡Algo salió mal en Springfield! Inténtalo de nuevo.")

class PerformanceOptimizer:
    """Optimizaciones de performance para la aplicación"""
    
    @staticmethod
    @st.cache_resource
    def get_cached_services():
        """Inicializa y cachea servicios pesados"""
        from services.simpsons_api import SimpsonsAPIService
        from services.llm_service import LLMService
        from services.episodes_service import EpisodesService
        from services.quotes_service import QuotesService
        from logic.quote_processor import QuoteProcessor
        from data.favorites_manager import FavoritesManager
        from analytics.quote_analytics import QuoteAnalytics
        
        return {
            'simpsons_service': SimpsonsAPIService(),
            'llm_service': LLMService(),
            'episodes_service': EpisodesService(),
            'quotes_service': QuotesService(),
            'quote_processor': QuoteProcessor(),
            'favorites_manager': FavoritesManager(),
            'analytics': QuoteAnalytics()
        }
    
    @staticmethod
    def preload_critical_data():
        """Precarga datos críticos en background"""
        try:
            services = PerformanceOptimizer.get_cached_services()
            # Precargar estado de APIs
            services['simpsons_service'].get_api_status()
        except Exception as e:
            logger.warning(f"Error precargando datos: {e}")

class ResponsiveLayout:
    """Layouts responsivos para diferentes tamaños de pantalla"""
    
    @staticmethod
    def create_main_layout():
        """Crea layout principal responsivo"""
        # Detectar ancho de pantalla (aproximado)
        col1, col2, col3 = st.columns([1, 6, 1])
        return col1, col2, col3
    
    @staticmethod
    def create_quote_layout():
        """Crea layout optimizado para mostrar citas"""
        return st.columns([1, 3, 1])
    
    @staticmethod
    def create_action_layout():
        """Crea layout para botones de acción"""
        return st.columns(4)