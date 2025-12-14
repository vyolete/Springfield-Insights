"""
Springfield Insights - Aplicación principal
Explorando la filosofía y crítica social de Los Simpsons
"""
import streamlit as st
import logging
from config.settings import settings
from logic.quote_processor import QuoteProcessor
from ui.theme import SimpsonsTheme
from utils.validators import ErrorHandler

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpringfieldInsightsApp:
    """Aplicación principal de Springfield Insights"""
    
    def __init__(self):
        self.quote_processor = QuoteProcessor()
        self.theme = SimpsonsTheme()
        
    def run(self):
        """Ejecuta la aplicación principal"""
        # Configuración de página
        st.set_page_config(
            page_title=settings.APP_TITLE,
            page_icon="🍩",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Aplicar tema personalizado
        self.theme.apply_custom_css()
        
        # Verificar configuración
        if not self._check_configuration():
            return
        
        # Renderizar interfaz principal
        self._render_main_interface()
    
    def _check_configuration(self) -> bool:
        """
        Verifica que la configuración sea válida
        
        Returns:
            True si la configuración es correcta, False en caso contrario
        """
        if not settings.validate_config():
            st.error("⚠️ Configuración incompleta")
            st.markdown("""
            ### Configuración Requerida
            
            Para usar Springfield Insights, necesitas configurar:
            
            1. **OPENAI_API_KEY**: Tu clave de API de OpenAI
            
            #### Cómo configurar:
            
            **Opción 1: Variable de entorno**
            ```bash
            export OPENAI_API_KEY="tu-api-key-aqui"
            ```
            
            **Opción 2: Archivo .env**
            ```
            OPENAI_API_KEY=tu-api-key-aqui
            ```
            
            **Opción 3: Streamlit secrets**
            ```toml
            # .streamlit/secrets.toml
            OPENAI_API_KEY = "tu-api-key-aqui"
            ```
            """)
            return False
        
        return True
    
    def _render_main_interface(self):
        """Renderiza la interfaz principal de la aplicación"""
        
        # Header principal
        self.theme.create_header(
            title="🍩 Springfield Insights",
            subtitle="Explorando la filosofía y crítica social de Los Simpsons"
        )
        
        # Sidebar con información
        self._render_sidebar()
        
        # Contenido principal
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Botón principal para obtener cita
            if st.button("🎲 Obtener Nueva Cita Filosófica", key="main_button"):
                self._handle_new_quote_request()
            
            # Mostrar cita si existe en session state
            if 'current_quote' in st.session_state:
                self._display_current_quote()
    
    def _render_sidebar(self):
        """Renderiza la barra lateral con información adicional"""
        with st.sidebar:
            st.markdown("### 📚 Acerca del Proyecto")
            
            st.markdown("""
            **Springfield Insights** es un proyecto académico que utiliza 
            inteligencia artificial para analizar las citas de Los Simpsons 
            desde una perspectiva filosófica y de crítica social.
            """)
            
            st.markdown("### 🎯 Objetivos")
            st.markdown("""
            - Explorar la profundidad filosófica de la serie
            - Analizar la crítica social implícita
            - Demostrar el valor cultural de la animación
            - Aplicar IA para análisis cultural
            """)
            
            st.markdown("### 🔧 Tecnologías")
            st.markdown("""
            - **Python 3.10+**
            - **Streamlit** (Interfaz)
            - **GPT-4** (Análisis)
            - **API de Simpsons** (Datos)
            """)
            
            # Estadísticas de sesión
            if 'quotes_analyzed' not in st.session_state:
                st.session_state.quotes_analyzed = 0
            
            st.markdown("### 📊 Estadísticas de Sesión")
            st.metric("Citas Analizadas", st.session_state.quotes_analyzed)
            
            # Botón para limpiar sesión
            if st.button("🔄 Nueva Sesión"):
                st.session_state.clear()
                st.rerun()
    
    def _handle_new_quote_request(self):
        """Maneja la solicitud de una nueva cita"""
        
        # Mostrar indicador de carga
        with st.spinner("🧠 Obteniendo cita y generando análisis filosófico..."):
            try:
                # Obtener cita analizada
                result = self.quote_processor.get_analyzed_quote()
                
                if result['success']:
                    # Guardar en session state
                    st.session_state.current_quote = result
                    st.session_state.quotes_analyzed += 1
                    
                    # Mostrar mensaje de éxito
                    self.theme.show_success_message("¡Análisis generado exitosamente!")
                    
                    # Recargar para mostrar la nueva cita
                    st.rerun()
                    
                else:
                    # Mostrar error
                    error_msg = result.get('error_message', 'Error desconocido')
                    self.theme.show_error_message(f"Error: {error_msg}")
                    
            except Exception as e:
                logger.error(f"Error en _handle_new_quote_request: {e}")
                error_msg = ErrorHandler.handle_api_error(e, "obtención de cita")
                self.theme.show_error_message(error_msg)
    
    def _display_current_quote(self):
        """Muestra la cita actual almacenada en session state"""
        
        quote_data = st.session_state.current_quote
        
        if not quote_data.get('success', False):
            self.theme.show_error_message("No hay cita válida para mostrar")
            return
        
        # Mostrar cita
        self.theme.create_quote_card(
            quote=quote_data.get('quote', ''),
            character=quote_data.get('character', ''),
            image_url=quote_data.get('image', '')
        )
        
        # Mostrar análisis
        analysis = quote_data.get('analysis', '')
        if analysis:
            self.theme.create_analysis_section(analysis)
        
        # Opciones adicionales
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Otra Cita"):
                self._handle_new_quote_request()
        
        with col2:
            if st.button("📋 Copiar Análisis"):
                st.write("Análisis copiado al portapapeles")
                # Nota: La funcionalidad de copiar requiere JavaScript adicional
        
        with col3:
            if st.button("💾 Guardar Favorito"):
                self._save_favorite_quote(quote_data)
    
    def _save_favorite_quote(self, quote_data):
        """
        Guarda una cita como favorita
        
        Args:
            quote_data: Datos de la cita a guardar
        """
        if 'favorite_quotes' not in st.session_state:
            st.session_state.favorite_quotes = []
        
        # Evitar duplicados
        quote_id = f"{quote_data.get('character', '')}_{quote_data.get('quote', '')[:50]}"
        
        existing_ids = [
            f"{fav.get('character', '')}_{fav.get('quote', '')[:50]}"
            for fav in st.session_state.favorite_quotes
        ]
        
        if quote_id not in existing_ids:
            st.session_state.favorite_quotes.append(quote_data)
            self.theme.show_success_message("¡Cita guardada en favoritos!")
        else:
            st.warning("Esta cita ya está en tus favoritos")
    
    def _render_favorites_section(self):
        """Renderiza la sección de citas favoritas"""
        
        if 'favorite_quotes' not in st.session_state or not st.session_state.favorite_quotes:
            st.info("No tienes citas favoritas aún")
            return
        
        st.markdown("### ⭐ Tus Citas Favoritas")
        
        for i, quote_data in enumerate(st.session_state.favorite_quotes):
            with st.expander(f"Cita {i+1}: {quote_data.get('character', 'Desconocido')}"):
                self.theme.create_quote_card(
                    quote=quote_data.get('quote', ''),
                    character=quote_data.get('character', ''),
                    image_url=quote_data.get('image', '')
                )
                
                # Mostrar análisis resumido
                analysis = quote_data.get('analysis', '')
                if analysis:
                    st.markdown(f"**Análisis:** {analysis[:200]}...")

def main():
    """Función principal de la aplicación"""
    try:
        app = SpringfieldInsightsApp()
        app.run()
        
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {e}")
        st.error("Error crítico en la aplicación. Consulta los logs para más detalles.")

if __name__ == "__main__":
    main()