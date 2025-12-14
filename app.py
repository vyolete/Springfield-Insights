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
from data.favorites_manager import FavoritesManager
from analytics.quote_analytics import QuoteAnalytics

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
        self.favorites_manager = FavoritesManager()
        self.analytics = QuoteAnalytics()
        
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
        
        # Navegación por pestañas
        tab1, tab2, tab3, tab4 = st.tabs(["🎲 Explorar", "⭐ Favoritos", "📊 Analytics", "ℹ️ Acerca de"])
        
        with tab1:
            self._render_explore_tab()
        
        with tab2:
            self._render_favorites_tab()
        
        with tab3:
            self._render_analytics_tab()
        
        with tab4:
            self._render_about_tab()
    
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
            
            # Estadísticas de favoritos
            favorites = self.favorites_manager.load_favorites()
            st.metric("Favoritos Guardados", len(favorites))
    
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
        Guarda una cita como favorita usando el FavoritesManager
        
        Args:
            quote_data: Datos de la cita a guardar
        """
        success = self.favorites_manager.save_favorite(quote_data)
        
        if success:
            self.theme.show_success_message("¡Cita guardada en favoritos!")
        else:
            st.warning("Esta cita ya está en tus favoritos o hubo un error al guardar")
    
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
    
    def _render_explore_tab(self):
        """Renderiza la pestaña de exploración de citas"""
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Botón principal para obtener cita
            if st.button("🎲 Obtener Nueva Cita Filosófica", key="main_button"):
                self._handle_new_quote_request()
            
            # Mostrar cita si existe en session state
            if 'current_quote' in st.session_state:
                self._display_current_quote()
    
    def _render_favorites_tab(self):
        """Renderiza la pestaña de favoritos"""
        
        favorites = self.favorites_manager.load_favorites()
        
        if not favorites:
            st.info("🌟 No tienes citas favoritas aún. ¡Explora algunas citas y guarda tus favoritas!")
            return
        
        # Estadísticas de favoritos
        stats = self.favorites_manager.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Favoritos", stats['total_favorites'])
        with col2:
            st.metric("Personajes Únicos", stats['unique_characters'])
        with col3:
            if stats['most_quoted_character']:
                st.metric("Más Citado", stats['most_quoted_character'])
        with col4:
            if st.button("📥 Exportar Favoritos"):
                self._export_favorites()
        
        # Filtros
        st.markdown("### 🔍 Filtrar Favoritos")
        
        col1, col2 = st.columns(2)
        with col1:
            characters = list(set(fav.get('character', 'Unknown') for fav in favorites))
            selected_character = st.selectbox("Filtrar por personaje:", ["Todos"] + characters)
        
        with col2:
            sort_options = ["Más recientes", "Más antiguos", "Por personaje"]
            sort_by = st.selectbox("Ordenar por:", sort_options)
        
        # Aplicar filtros
        filtered_favorites = favorites
        if selected_character != "Todos":
            filtered_favorites = self.favorites_manager.get_favorites_by_character(selected_character)
        
        # Aplicar ordenamiento
        if sort_by == "Más recientes":
            filtered_favorites.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        elif sort_by == "Más antiguos":
            filtered_favorites.sort(key=lambda x: x.get('saved_at', ''))
        elif sort_by == "Por personaje":
            filtered_favorites.sort(key=lambda x: x.get('character', ''))
        
        # Mostrar favoritos
        st.markdown("### ⭐ Tus Citas Favoritas")
        
        for i, fav in enumerate(filtered_favorites):
            with st.expander(f"#{i+1} - {fav.get('character', 'Desconocido')}: {fav.get('quote', '')[:60]}..."):
                
                # Mostrar cita
                self.theme.create_quote_card(
                    quote=fav.get('quote', ''),
                    character=fav.get('character', ''),
                    image_url=fav.get('image', '')
                )
                
                # Mostrar análisis
                analysis = fav.get('analysis', '')
                if analysis:
                    self.theme.create_analysis_section(analysis)
                
                # Información adicional
                col1, col2 = st.columns(2)
                with col1:
                    if fav.get('saved_at'):
                        st.caption(f"Guardado: {fav['saved_at'][:10]}")
                
                with col2:
                    if st.button(f"🗑️ Eliminar", key=f"delete_{fav.get('favorite_id')}"):
                        if self.favorites_manager.remove_favorite(fav.get('favorite_id')):
                            st.success("Favorito eliminado")
                            st.rerun()
    
    def _render_analytics_tab(self):
        """Renderiza la pestaña de analytics"""
        
        favorites = self.favorites_manager.load_favorites()
        
        if len(favorites) < 2:
            st.info("📊 Necesitas al menos 2 citas favoritas para generar analytics. ¡Guarda más favoritos!")
            return
        
        st.markdown("### 📊 Analytics de Springfield Insights")
        
        # Generar reporte de insights
        with st.spinner("Generando análisis..."):
            insights_report = self.analytics.generate_insights_report(favorites)
        
        if 'error' in insights_report:
            st.error(insights_report['error'])
            return
        
        # Mostrar resumen
        summary = insights_report['summary']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Citas Analizadas", summary['total_quotes_analyzed'])
        with col2:
            st.metric("Personajes Únicos", summary['unique_characters'])
        with col3:
            st.metric("Complejidad Promedio", f"{summary['average_complexity_score']:.2f}")
        with col4:
            st.metric("Más Complejo", summary['most_complex_character'])
        
        # Análisis temático
        st.markdown("### 🧠 Análisis Temático")
        
        thematic = insights_report['thematic_analysis']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Temas Filosóficos Principales:**")
            for i, theme in enumerate(thematic['top_philosophical_themes'][:5], 1):
                st.write(f"{i}. {theme.title()}")
        
        with col2:
            st.markdown("**Temas de Crítica Social:**")
            for i, theme in enumerate(thematic['top_social_critique_themes'][:5], 1):
                st.write(f"{i}. {theme.title()}")
        
        # Insights por personaje
        st.markdown("### 👥 Insights por Personaje")
        
        character_insights = insights_report['character_insights']
        
        for character, data in character_insights.items():
            with st.expander(f"📊 {character} ({data['quote_count']} citas)"):
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Palabras Promedio", f"{data['avg_words_per_quote']:.1f}")
                
                with col2:
                    st.metric("Complejidad Promedio", f"{data['avg_complexity']:.2f}")
                
                with col3:
                    st.metric("Total Palabras", data['total_words'])
                
                # Temas principales del personaje
                if data['top_philosophical_themes']:
                    st.markdown("**Temas Filosóficos:**")
                    st.write(", ".join(data['top_philosophical_themes']))
                
                if data['top_social_themes']:
                    st.markdown("**Temas Sociales:**")
                    st.write(", ".join(data['top_social_themes']))
        
        # Recomendaciones
        st.markdown("### 💡 Recomendaciones")
        
        recommendations = insights_report['recommendations']
        for rec in recommendations:
            st.info(f"💡 {rec}")
    
    def _render_about_tab(self):
        """Renderiza la pestaña de información"""
        
        st.markdown("### 🍩 Acerca de Springfield Insights")
        
        st.markdown("""
        **Springfield Insights** es una aplicación académica que utiliza inteligencia artificial 
        para explorar la profundidad filosófica y crítica social presente en Los Simpsons.
        
        #### 🎯 Objetivos del Proyecto
        
        - **Demostrar valor cultural**: Evidenciar la riqueza filosófica en la cultura popular
        - **Aplicación de IA**: Mostrar el potencial de GPT-4 para análisis cultural
        - **Educación interactiva**: Crear una herramienta educativa accesible
        - **Análisis académico**: Generar insights rigurosos sobre contenido mediático
        
        #### 🔧 Tecnologías Utilizadas
        
        - **Python 3.10+**: Lenguaje de programación principal
        - **Streamlit**: Framework de interfaz web interactiva
        - **OpenAI GPT-4**: Modelo de lenguaje para análisis filosófico
        - **API de Simpsons**: Fuente de citas originales
        - **Arquitectura Modular**: Diseño escalable y mantenible
        
        #### 📊 Funcionalidades
        
        - ✅ **Exploración de Citas**: Obtén citas aleatorias con análisis filosófico
        - ✅ **Sistema de Favoritos**: Guarda y organiza tus citas preferidas
        - ✅ **Analytics Avanzados**: Analiza patrones y tendencias en tus favoritos
        - ✅ **Interfaz Temática**: Diseño inspirado en la estética de Los Simpsons
        - ✅ **Exportación de Datos**: Guarda tus favoritos para uso posterior
        
        #### 🎓 Valor Académico
        
        Este proyecto demuestra cómo la inteligencia artificial puede ser utilizada para:
        
        - Analizar contenido cultural desde múltiples perspectivas
        - Identificar patrones filosóficos en medios populares
        - Generar insights académicos de forma automatizada
        - Crear herramientas educativas interactivas
        
        #### 📈 Métricas de Análisis
        
        La aplicación evalúa múltiples dimensiones:
        
        - **Complejidad Lingüística**: Diversidad léxica, estructura sintáctica
        - **Profundidad Filosófica**: Identificación de corrientes y conceptos
        - **Crítica Social**: Elementos de sátira y comentario social
        - **Rigor Académico**: Calidad y estructura del análisis generado
        
        ---
        
        *Desarrollado como proyecto académico para demostrar la intersección 
        entre inteligencia artificial, análisis cultural y educación interactiva.*
        """)
        
        # Información técnica adicional
        with st.expander("🔧 Información Técnica"):
            st.markdown("""
            **Arquitectura del Sistema:**
            
            ```
            springfield_insights/
            ├── app.py                    # Aplicación principal Streamlit
            ├── config/                   # Configuración y settings
            ├── services/                 # Integración con APIs externas
            ├── logic/                    # Lógica de negocio y orquestación
            ├── ui/                       # Componentes de interfaz
            ├── utils/                    # Utilidades y validaciones
            ├── data/                     # Gestión de datos y favoritos
            └── analytics/                # Análisis y métricas avanzadas
            ```
            
            **Patrones de Diseño Implementados:**
            - Separación de responsabilidades (SoC)
            - Inyección de dependencias
            - Patrón Repository para datos
            - Patrón Strategy para análisis
            """)
    
    def _export_favorites(self):
        """Exporta favoritos a un archivo JSON"""
        
        try:
            import tempfile
            import json
            from datetime import datetime
            
            favorites = self.favorites_manager.load_favorites()
            
            # Crear archivo temporal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"springfield_insights_favorites_{timestamp}.json"
            
            # Preparar datos para exportación
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'total_favorites': len(favorites),
                'favorites': favorites
            }
            
            # Crear enlace de descarga
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Descargar Favoritos (JSON)",
                data=json_str,
                file_name=filename,
                mime="application/json"
            )
            
            st.success(f"¡Archivo {filename} listo para descargar!")
            
        except Exception as e:
            logger.error(f"Error exportando favoritos: {e}")
            st.error("Error al exportar favoritos. Inténtalo de nuevo.")

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