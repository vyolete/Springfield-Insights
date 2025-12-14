"""
Configuración de tema visual inspirado en Los Simpsons
"""
import streamlit as st

class SimpsonsTheme:
    """Configuración de colores y estilos inspirados en Los Simpsons"""
    
    # Paleta de colores principal
    COLORS = {
        'primary_yellow': '#FFD700',      # Amarillo Simpson
        'secondary_blue': '#4169E1',      # Azul característico
        'background_light': '#FFF8DC',    # Fondo claro amarillento
        'text_dark': '#2F4F4F',          # Texto oscuro
        'accent_orange': '#FF8C00',       # Naranja de acento
        'success_green': '#32CD32',       # Verde para éxito
        'error_red': '#DC143C',          # Rojo para errores
        'sidebar_bg': '#F0E68C'          # Fondo de sidebar
    }
    
    # Configuración de fuentes
    FONTS = {
        'primary': 'Arial, sans-serif',
        'secondary': 'Comic Sans MS, cursive',
        'monospace': 'Courier New, monospace'
    }
    
    @classmethod
    def apply_custom_css(cls):
        """Aplica CSS personalizado para el tema de Los Simpsons"""
        
        css = f"""
        <style>
        /* Configuración general */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: {cls.COLORS['background_light']};
        }}
        
        /* Header principal */
        .main-header {{
            background: linear-gradient(90deg, {cls.COLORS['primary_yellow']}, {cls.COLORS['accent_orange']});
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .main-header h1 {{
            color: {cls.COLORS['text_dark']};
            font-family: {cls.FONTS['secondary']};
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .main-header p {{
            color: {cls.COLORS['text_dark']};
            font-family: {cls.FONTS['primary']};
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
        }}
        
        /* Tarjetas de citas */
        .quote-card {{
            background: white;
            border: 3px solid {cls.COLORS['secondary_blue']};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .quote-text {{
            font-family: {cls.FONTS['primary']};
            font-size: 1.3rem;
            color: {cls.COLORS['text_dark']};
            font-style: italic;
            margin-bottom: 1rem;
            line-height: 1.6;
        }}
        
        .quote-character {{
            font-family: {cls.FONTS['secondary']};
            font-size: 1.1rem;
            color: {cls.COLORS['secondary_blue']};
            font-weight: bold;
            text-align: right;
            margin-bottom: 1rem;
        }}
        
        /* Análisis filosófico */
        .analysis-section {{
            background: {cls.COLORS['background_light']};
            border-left: 5px solid {cls.COLORS['primary_yellow']};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 10px 10px 0;
        }}
        
        .analysis-title {{
            font-family: {cls.FONTS['secondary']};
            color: {cls.COLORS['secondary_blue']};
            font-size: 1.4rem;
            margin-bottom: 0.5rem;
        }}
        
        .analysis-text {{
            font-family: {cls.FONTS['primary']};
            color: {cls.COLORS['text_dark']};
            line-height: 1.7;
            font-size: 1rem;
        }}
        
        /* Botones personalizados */
        .stButton > button {{
            background: linear-gradient(90deg, {cls.COLORS['primary_yellow']}, {cls.COLORS['accent_orange']});
            color: {cls.COLORS['text_dark']};
            border: 2px solid {cls.COLORS['secondary_blue']};
            border-radius: 25px;
            font-family: {cls.FONTS['secondary']};
            font-weight: bold;
            font-size: 1.1rem;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(90deg, {cls.COLORS['accent_orange']}, {cls.COLORS['primary_yellow']});
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: {cls.COLORS['sidebar_bg']};
        }}
        
        /* Mensajes de error */
        .error-message {{
            background-color: {cls.COLORS['error_red']};
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-family: {cls.FONTS['primary']};
        }}
        
        /* Mensajes de éxito */
        .success-message {{
            background-color: {cls.COLORS['success_green']};
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-family: {cls.FONTS['primary']};
        }}
        
        /* Loading spinner personalizado */
        .loading-container {{
            text-align: center;
            padding: 2rem;
        }}
        
        .loading-text {{
            font-family: {cls.FONTS['secondary']};
            color: {cls.COLORS['secondary_blue']};
            font-size: 1.2rem;
            margin-top: 1rem;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .main-header h1 {{
                font-size: 2rem;
            }}
            
            .quote-text {{
                font-size: 1.1rem;
            }}
            
            .quote-card {{
                padding: 1rem;
            }}
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    @classmethod
    def create_header(cls, title: str, subtitle: str = ""):
        """
        Crea el header principal de la aplicación
        
        Args:
            title: Título principal
            subtitle: Subtítulo opcional
        """
        header_html = f"""
        <div class="main-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    @classmethod
    def create_quote_card(cls, quote: str, character: str, image_url: str = ""):
        """
        Crea una tarjeta visual para mostrar una cita
        
        Args:
            quote: Texto de la cita
            character: Personaje que la pronuncia
            image_url: URL de imagen del personaje (opcional)
        """
        # Mostrar imagen si está disponible
        if image_url:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                try:
                    st.image(image_url, width=200, caption=character)
                except:
                    pass  # Si falla la imagen, continuar sin ella
        
        # Crear tarjeta de cita
        quote_html = f"""
        <div class="quote-card">
            <div class="quote-text">"{quote}"</div>
            <div class="quote-character">— {character}</div>
        </div>
        """
        st.markdown(quote_html, unsafe_allow_html=True)
    
    @classmethod
    def create_analysis_section(cls, analysis: str):
        """
        Crea la sección de análisis filosófico
        
        Args:
            analysis: Texto del análisis
        """
        analysis_html = f"""
        <div class="analysis-section">
            <div class="analysis-title">🧠 Análisis Filosófico y Social</div>
            <div class="analysis-text">{analysis}</div>
        </div>
        """
        st.markdown(analysis_html, unsafe_allow_html=True)
    
    @classmethod
    def show_error_message(cls, message: str):
        """
        Muestra un mensaje de error con estilo
        
        Args:
            message: Mensaje de error a mostrar
        """
        error_html = f"""
        <div class="error-message">
            ⚠️ {message}
        </div>
        """
        st.markdown(error_html, unsafe_allow_html=True)
    
    @classmethod
    def show_success_message(cls, message: str):
        """
        Muestra un mensaje de éxito con estilo
        
        Args:
            message: Mensaje de éxito a mostrar
        """
        success_html = f"""
        <div class="success-message">
            ✅ {message}
        </div>
        """
        st.markdown(success_html, unsafe_allow_html=True)
    
    @classmethod
    def show_loading(cls, message: str = "Generando análisis filosófico..."):
        """
        Muestra indicador de carga
        
        Args:
            message: Mensaje de carga personalizado
        """
        loading_html = f"""
        <div class="loading-container">
            <div class="loading-text">{message}</div>
        </div>
        """
        st.markdown(loading_html, unsafe_allow_html=True)