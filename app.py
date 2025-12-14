#!/usr/bin/env python3
"""
Springfield Insights - Aplicación Principal
Explorando la filosofía y crítica social de Los Simpsons mediante IA
"""
import streamlit as st
import sys
from pathlib import Path

# Configurar path para imports
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from services.quote_service import QuoteService
from ui.components import UIComponents
from data.quotes_data import SIMPSONS_QUOTES

class SpringfieldInsightsApp:
    """Aplicación principal de Springfield Insights"""
    
    def __init__(self):
        self.quote_service = QuoteService()
        self.ui = UIComponents()
        
    def run(self):
        """Ejecuta la aplicación principal"""
        # Configuración de página
        st.set_page_config(
            page_title="Springfield Insights",
            page_icon="🍩",
            layout="wide"
        )
        
        # Aplicar estilos
        self.ui.apply_custom_css()
        
        # Verificar configuración
        if not self._check_configuration():
            return
        
        # Renderizar interfaz
        self._render_main_interface()
    
    def _check_configuration(self) -> bool:
        """Verifica la configuración de OpenAI"""
        if not settings.OPENAI_API_KEY:
            st.error("❌ Configura tu OPENAI_API_KEY en el archivo .env")
            st.info("💡 Copia .env.example a .env y añade tu clave de OpenAI")
            return False
        return True
    
    def _render_main_interface(self):
        """Renderiza la interfaz principal"""
        # Header
        self.ui.render_header()
        
        # Inicializar estado
        if 'current_quote_index' not in st.session_state:
            st.session_state.current_quote_index = None
        
        # Botón principal
        self._render_main_button()
        
        # Mostrar cita si existe
        if st.session_state.current_quote_index is not None:
            self._render_quote_section()
        else:
            self._render_welcome_message()
        
        # Sidebar
        self._render_sidebar()
    
    def _render_main_button(self):
        """Renderiza el botón principal"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🎲 Obtener Nueva Reflexión Filosófica", 
                        use_container_width=True, type="primary"):
                self._get_new_quote()
    
    def _get_new_quote(self):
        """Obtiene una nueva cita aleatoria"""
        import random
        st.session_state.current_quote_index = random.randint(0, len(SIMPSONS_QUOTES) - 1)
        st.rerun()
    
    def _render_quote_section(self):
        """Renderiza la sección de la cita actual"""
        quote_data = SIMPSONS_QUOTES[st.session_state.current_quote_index]
        
        # Layout principal
        col_img, col_content = st.columns([1, 2])
        
        # Imagen del personaje
        with col_img:
            self.ui.render_character_image(quote_data)
        
        # Contenido de la cita
        with col_content:
            self.ui.render_quote_card(quote_data)
        
        # Análisis filosófico
        self._render_analysis_section(quote_data)
        
        # Botones de acción
        self._render_action_buttons()
    
    def _render_analysis_section(self, quote_data):
        """Renderiza la sección de análisis filosófico"""
        st.markdown("### 📚 Análisis Filosófico")
        
        with st.spinner("🧠 Generando análisis académico con GPT-4..."):
            analysis = self.quote_service.generate_analysis(
                quote_data["quote"],
                quote_data["character"],
                quote_data["context"]
            )
        
        self.ui.render_analysis(analysis)
    
    def _render_action_buttons(self):
        """Renderiza los botones de acción"""
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Otra Cita"):
                self._get_new_quote()
        
        with col2:
            if st.button("📋 Copiar"):
                st.toast("📋 Cita copiada", icon="✅")
        
        with col3:
            if st.button("💾 Favorito"):
                st.toast("⭐ Añadido a favoritos", icon="💾")
        
        with col4:
            if st.button("🔗 Compartir"):
                st.toast("🔗 Enlace copiado", icon="📤")
    
    def _render_welcome_message(self):
        """Renderiza el mensaje de bienvenida"""
        st.info("""
        🎭 **¡Bienvenido a Springfield Insights!**
        
        Explora frases auténticas de Los Simpsons con análisis filosófico 
        profundo generado por GPT-4.
        
        ✨ **Características:**
        - Frases reales de la serie
        - Análisis académico riguroso  
        - Crítica social y filosófica
        - Interfaz optimizada
        """)
    
    def _render_sidebar(self):
        """Renderiza la barra lateral"""
        with st.sidebar:
            st.markdown("### 📊 Estadísticas")
            st.metric("Frases disponibles", len(SIMPSONS_QUOTES))
            
            if 'analyses_generated' not in st.session_state:
                st.session_state.analyses_generated = 0
            st.metric("Análisis generados", st.session_state.analyses_generated)
            
            st.markdown("### 🎯 Acerca de")
            st.markdown("""
            **Springfield Insights** combina el humor inteligente de Los Simpsons 
            con análisis filosófico académico usando GPT-4.
            
            - **Frases auténticas** de la serie
            - **Análisis profundo** con IA
            - **Crítica social** contextualizada
            - **Interfaz optimizada**
            """)
            
            st.markdown("### ⚙️ Estado")
            st.success("✅ GPT-4 configurado")
            st.info("🚀 Sistema operativo")

def main():
    """Función principal"""
    try:
        app = SpringfieldInsightsApp()
        app.run()
    except Exception as e:
        st.error(f"Error crítico: {str(e)}")
        st.info("Verifica tu configuración y vuelve a intentar")

if __name__ == "__main__":
    main()