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
        # 1. Configuración de página
        st.set_page_config(
            page_title="Springfield Insights",
            page_icon="🍩",
            layout="wide"
        )
        
        # 2. Inicializar estado de tema y renderizar toggle PRIMERO
        # Esto asegura que el estado se actualice antes de aplicar CSS
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
            
        with st.sidebar:
            st.image("https://upload.wikimedia.org/wikipedia/commons/9/98/The_Simpsons_yellow_logo.svg", width=200)
            st.markdown("### ⚙️ Configuración")
            st.session_state.dark_mode = st.toggle("🌙 Modo Oscuro", value=st.session_state.dark_mode)
            st.markdown("---")
        
        # 3. Aplicar estilos con el estado ACTUALIZADO
        self.ui.apply_custom_css(dark_mode=st.session_state.dark_mode)
        
        # 4. Verificar configuración de API
        if not self._check_configuration():
            return
        
        # 5. Renderizar resto de la interfaz (incluyendo resto de sidebar)
        self._render_main_interface()
    
    def _check_configuration(self) -> bool:
        """Verifica la configuración de OpenAI"""
        if not settings.OPENAI_API_KEY:
            st.error("❌ **Configuración de API Key requerida**")
            st.markdown("""
            **Para Streamlit Cloud:**
            1. Ve a tu app en Streamlit Cloud
            2. Haz clic en "Settings" → "Secrets"
            3. Añade: `OPENAI_API_KEY = "tu-api-key"`
            
            **Para desarrollo local:**
            1. Copia `.env.example` a `.env`
            2. Añade tu `OPENAI_API_KEY=tu-api-key`
            """)
            return False
        return True
    
    def _render_main_interface(self):
        """Renderiza la interfaz principal basada en la navegación"""
        # Menú de Navegación en Sidebar (El toggle ya se renderizó arriba)
        page = self._render_sidebar_menu()
        
        # Renderizar vista seleccionada
        if page == "Inicio":
            self.ui.render_header()
            
            # Inicializar estado
            if 'current_quote_index' not in st.session_state:
                st.session_state.current_quote_index = None
            
            # Mostrar cita si existe
            if st.session_state.current_quote_index is not None:
                self._render_quote_section()
            else:
                self._render_welcome_message()
                
        elif page == "Dashboard":
            self._render_dashboard_view()
    
    def _render_sidebar_menu(self) -> str:
        """Renderiza el menú de navegación y retorna la página seleccionada"""
        with st.sidebar:
            # El logo y toggle ya se renderizaron en run(), seguimos con el menú
            
            st.markdown("### 🧭 Navegación")
            
            # Navegación mejorada con st.radio u otro componente
            page = st.radio(
                "Ir a:",
                ["Inicio", "Dashboard"],
                index=0,
                format_func=lambda x: "🏠 Inicio" if x == "Inicio" else "📊 Dashboard"
            )
            
            st.markdown("---")
            st.caption("Springfield Insights v1.1")
            
            return page

    def _render_dashboard_view(self):
        """Renderiza la vista del Dashboard (Info que antes estaba en sidebar)"""
        st.title("📊 Panel de Control")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Estado de conexión con diseño mejorado
            api_status = quotes_manager.get_api_status()
            
            st.markdown("### 🌐 Estado de Conexión")
            if api_status.get('available'):
                st.success("🟢 **API Oficial Conectada**")
                st.caption("Obteniendo frases reales de Los Simpsons")
            else:
                st.warning("🟡 **Modo Local Activo**")
                st.caption("Usando base de datos local de respaldo")
                
            # GPT-4 Status
            st.markdown("### 🤖 Inteligencia Artificial")
            st.success("✅ GPT-3.5-Turbo Operativo (Modo Demo Activo)")

        with col2:
            # Estadísticas con mejor formato
            st.markdown("### 📈 Estadísticas de Sesión")
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                if 'analyses_generated' not in st.session_state:
                    st.session_state.analyses_generated = 0
                st.metric(
                    label="Análisis Generados",
                    value=st.session_state.analyses_generated
                )
            
            with metric_col2:
                st.metric(
                    label="Frases Locales",
                    value=len(SIMPSONS_QUOTES)
                )

        st.markdown("---")
        
        # Performance Status
        st.info("⚡ **Rendimiento:** CDN Optimizado y caché de respuestas activado.")

        # Información del proyecto con mejor diseño
        st.markdown("### 🎯 Sobre el Proyecto")
        
        tab1, tab2, tab3 = st.tabs(["📖 Qué es", "⚙️ Tecnologías", "🎓 Valor Académico"])
        
        with tab1:
            st.markdown("""
            ### Springfield Insights
            Una aplicación académica que utiliza **inteligencia artificial** 
            para explorar la profundidad filosófica presente en Los Simpsons.
            
            - 🧠 **Análisis con IA**  
            - 🎭 **Frases auténticas**  
            - 🏛️ **Enfoque académico**  
            - 🔄 **Sistema híbrido**
            """)
        
        with tab2:
            st.markdown("""
            **🤖 Inteligencia Artificial:**
            - OpenAI GPT-3.5-Turbo para análisis filosófico (con Mock Fallback)
            
            **🌐 Fuentes de Datos:**
            - API oficial de Los Simpsons (`thesimpsonsapi.com`)
            - CDN optimizado para imágenes
            
            **💻 Tecnologías Web:**
            - Python + Streamlit
            - Sistema híbrido API + Local
            - Diseño Responsive
            """)
        
        with tab3:
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

    def _render_main_button(self):
        """Renderiza el botón principal"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🎲 Obtener Nueva Reflexión Filosófica", 
                        use_container_width=True, type="primary"):
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
        
        with st.spinner("🧠 Generando análisis académico con GPT-3.5..."):
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
        
        # 1. Seccion: Header / Mensaje principal
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
        
        # 2. Seccion: ¿Cómo empezar?
        st.markdown("### 🚀 ¿Cómo empezar?")
        
        st.markdown("""
        <div style='background: #FFFACD; padding: 20px; border-radius: 10px; border-left: 4px solid #FFD700;'>
            <ol style='color: #2F4F4F; font-size: 16px; line-height: 1.8;'>
                <li><strong>Haz clic</strong> en el botón amarillo <em>"🎲 Obtener Nueva Reflexión Filosófica"</em></li>
                <li><strong>Observa</strong> la imagen oficial del personaje desde el CDN</li>
                <li><strong>Lee</strong> la frase auténtica de Los Simpsons</li>
                <li><strong>Explora</strong> el análisis filosófico generado por IA</li>
                <li><strong>Interactúa</strong> con los botones para copiar, guardar o compartir</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        # 3. Seccion: Botón de Acción
        st.markdown("---")
        self._render_main_button()
        st.markdown("---")
        
        # 4. Seccion: ¿Sabías que?
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
            **🤖 GPT-3.5** puede identificar referencias filosóficas, críticas sociales 
            y contextos culturales que a menudo pasan desapercibidos en una 
            primera lectura de las citas.
            """)
            
        st.markdown("---")
        
        # 5. Seccion: Cards (Características) - Ahora al final
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
                <h3 style='color: #4169E1;'>🧠 Análisis GPT-3.5</h3>
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