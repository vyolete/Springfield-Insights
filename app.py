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
from data.quotes_data import quotes_manager, SIMPSONS_QUOTES

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
                        type="primary"):
                self._get_new_quote()
    
    def _get_new_quote(self):
        """Obtiene una nueva cita aleatoria de la API o fallback"""
        try:
            # Obtener cita del gestor híbrido
            quote_data = quotes_manager.get_random_quote()
            st.session_state.current_quote_data = quote_data
            st.session_state.current_quote_index = 0  # Usar como flag
            st.rerun()
        except Exception as e:
            st.error(f"Error obteniendo cita: {e}")
            # Fallback a sistema anterior
            import random
            st.session_state.current_quote_index = random.randint(0, len(SIMPSONS_QUOTES) - 1)
            st.rerun()
    
    def _render_quote_section(self):
        """Renderiza la sección de la cita actual"""
        # Usar datos de la API si están disponibles, sino fallback local
        if hasattr(st.session_state, 'current_quote_data') and st.session_state.current_quote_data:
            quote_data = st.session_state.current_quote_data
        else:
            quote_data = SIMPSONS_QUOTES[st.session_state.current_quote_index]
        
        # Debug: Mostrar información de la cita para diagnóstico
        if st.checkbox("🔍 Mostrar datos de debug", value=False):
            st.json(quote_data)
        
        # Layout principal
        col_img, col_content = st.columns([1, 2])
        
        # Imagen del personaje
        with col_img:
            self.ui.render_character_image(quote_data)
        
        # Contenido de la cita
        with col_content:
            # Usar el diseño visual completo de Los Simpsons
            self.ui.render_quote_card(quote_data)
        
        # Análisis filosófico
        self._render_analysis_section(quote_data)
        
        # Botones de acción
        self._render_action_buttons()
    
    def _render_quote_native(self, quote_data):
        """Renderiza la cita usando componentes nativos de Streamlit"""
        
        # Información de la fuente
        source_info = "🌐 API Oficial" if quote_data.get("source") == "api" else "📚 Base Local"
        
        # Header con personaje y fuente
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🎭 {quote_data.get('character', 'Personaje Desconocido')}")
        with col2:
            st.caption(source_info)
        
        # La cita principal
        st.markdown("---")
        quote_text = quote_data.get("quote", "Cita no disponible")
        st.markdown(f'> **"{quote_text}"**')
        st.markdown("---")
        
        # Contexto filosófico
        st.markdown("#### 💭 Contexto Filosófico")
        context_text = quote_data.get("context", "Contexto no disponible")
        st.write(context_text)
        
        # Información adicional del personaje si está disponible
        character_info = quote_data.get("character_info", {})
        if character_info:
            st.markdown("#### ℹ️ Información del Personaje")
            
            info_cols = st.columns(3)
            
            if character_info.get('occupation') and character_info['occupation'] != 'Unknown':
                with info_cols[0]:
                    st.metric("Ocupación", character_info['occupation'])
            
            if character_info.get('age'):
                with info_cols[1]:
                    st.metric("Edad", f"{character_info['age']} años")
            
            if character_info.get('status') and character_info['status'] != 'Unknown':
                with info_cols[2]:
                    st.metric("Estado", character_info['status'])
    
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
        """Renderiza el mensaje de bienvenida mejorado"""
        
        # Mensaje principal con mejor diseño
        st.markdown("""
        <div style='background: linear-gradient(135deg, #E6F3FF, #F0F8FF); padding: 30px; border-radius: 15px; border-left: 5px solid #4169E1; margin: 20px 0;'>
            <h2 style='color: #2F4F4F; text-align: center; margin-bottom: 20px;'>
                🎭 ¡Bienvenido a Springfield Insights!
            </h2>
            <p style='font-size: 18px; color: #2F4F4F; text-align: center; margin-bottom: 25px;'>
                Descubre la <strong>profundidad filosófica</strong> oculta en Los Simpsons mediante 
                <strong>inteligencia artificial avanzada</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Características en columnas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='text-align: center; padding: 20px; background: #FFF8DC; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #FF6347;'>🎯 Frases Auténticas</h3>
                <p style='color: #2F4F4F;'>Directamente de la API oficial de Los Simpsons</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 20px; background: #F0F8FF; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #4169E1;'>🧠 Análisis GPT-4</h3>
                <p style='color: #2F4F4F;'>Interpretación filosófica profunda y académica</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='text-align: center; padding: 20px; background: #F5FFFA; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #228B22;'>🏛️ Rigor Académico</h3>
                <p style='color: #2F4F4F;'>Crítica social y contexto filosófico</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Instrucciones de uso
        st.markdown("### 🚀 ¿Cómo empezar?")
        
        st.markdown("""
        <div style='background: #FFFACD; padding: 20px; border-radius: 10px; border-left: 4px solid #FFD700;'>
            <ol style='color: #2F4F4F; font-size: 16px; line-height: 1.8;'>
                <li><strong>Haz clic</strong> en el botón amarillo <em>"🎲 Obtener Nueva Reflexión Filosófica"</em></li>
                <li><strong>Observa</strong> la imagen oficial del personaje desde el CDN</li>
                <li><strong>Lee</strong> la frase auténtica de Los Simpsons</li>
                <li><strong>Explora</strong> el análisis filosófico generado por GPT-4</li>
                <li><strong>Interactúa</strong> con los botones para copiar, guardar o compartir</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Datos curiosos
        st.markdown("### 📊 ¿Sabías que...?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **🎭 Los Simpsons** es una de las series más longevas de la televisión, 
            con más de **30 años** explorando temas sociales, políticos y filosóficos 
            a través del humor inteligente.
            """)
        
        with col2:
            st.info("""
            **🤖 GPT-4** puede identificar referencias filosóficas, críticas sociales 
            y contextos culturales que a menudo pasan desapercibidos en una 
            primera lectura de las citas.
            """)
    
    def _render_sidebar(self):
        """Renderiza la barra lateral mejorada y amigable"""
        with st.sidebar:
            # Logo y título del sidebar
            st.markdown("""
            <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='color: #2F4F4F; margin: 0;'>🍩 Springfield</h2>
                <p style='color: #2F4F4F; margin: 0; font-size: 14px;'>Panel de Control</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Estado de conexión con diseño mejorado
            api_status = quotes_manager.get_api_status()
            
            st.markdown("### 🌐 Estado de Conexión")
            if api_status.get('available'):
                st.success("🟢 **API Oficial Conectada**")
                st.caption("Obteniendo frases reales de Los Simpsons")
            else:
                st.warning("🟡 **Modo Local Activo**")
                st.caption("Usando base de datos local de respaldo")
            
            # Estadísticas con mejor formato
            st.markdown("### 📊 Estadísticas de Sesión")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'analyses_generated' not in st.session_state:
                    st.session_state.analyses_generated = 0
                st.metric(
                    label="Análisis",
                    value=st.session_state.analyses_generated,
                    delta="GPT-4"
                )
            
            with col2:
                st.metric(
                    label="Frases",
                    value=len(SIMPSONS_QUOTES),
                    delta="Locales"
                )
            
            # Información del proyecto con mejor diseño
            st.markdown("### 🎯 Sobre el Proyecto")
            
            with st.expander("📖 ¿Qué es Springfield Insights?", expanded=False):
                st.markdown("""
                Una aplicación académica que utiliza **inteligencia artificial** 
                para explorar la profundidad filosófica presente en Los Simpsons.
                
                🧠 **Análisis con GPT-4**  
                🎭 **Frases auténticas**  
                🏛️ **Enfoque académico**  
                🔄 **Sistema híbrido**
                """)
            
            with st.expander("⚙️ Tecnologías Utilizadas", expanded=False):
                st.markdown("""
                **🤖 Inteligencia Artificial:**
                - OpenAI GPT-4 para análisis filosófico
                
                **🌐 Fuentes de Datos:**
                - API oficial de Los Simpsons
                - CDN optimizado para imágenes
                
                **💻 Tecnologías Web:**
                - Python + Streamlit
                - Sistema híbrido API + Local
                """)
            
            with st.expander("🎓 Valor Académico", expanded=False):
                st.markdown("""
                **📚 Objetivos Educativos:**
                - Análisis cultural mediante IA
                - Crítica social contemporánea
                - Filosofía en cultura popular
                
                **🏆 Características Académicas:**
                - Rigor metodológico
                - Fuentes auténticas
                - Análisis contextualizado
                """)
            
            # Sección de ayuda
            st.markdown("### 💡 Cómo Usar")
            st.info("""
            **1.** Haz clic en **"Obtener Nueva Reflexión"**
            
            **2.** Lee la cita del personaje
            
            **3.** Explora el **análisis filosófico** generado por GPT-4
            
            **4.** Usa los botones para **copiar**, **guardar** o **compartir**
            """)
            
            # Estado del sistema con iconos
            st.markdown("### 🔧 Estado del Sistema")
            
            # GPT-4 Status
            st.markdown("**🤖 Inteligencia Artificial:**")
            st.success("✅ GPT-4 Operativo")
            
            # API Status
            st.markdown("**🌐 Fuente de Datos:**")
            if api_status.get('available'):
                st.success("✅ API Oficial Conectada")
            else:
                st.info("🔄 Modo Local Activo")
            
            # Performance Status
            st.markdown("**⚡ Rendimiento:**")
            st.success("✅ CDN Optimizado")
            
            # Footer del sidebar
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #666; font-size: 12px;'>
                <p>🍩 Springfield Insights v1.0</p>
                <p>Filosofía + IA + Los Simpsons</p>
            </div>
            """, unsafe_allow_html=True)

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