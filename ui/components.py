"""
Componentes de interfaz de usuario para Springfield Insights
"""
import streamlit as st

class UIComponents:
    """Componentes reutilizables de la interfaz de usuario"""
    
    def apply_custom_css(self, dark_mode: bool = False):
        """Aplica estilos CSS personalizados con soporte para tema oscuro"""
        
        # Definir paleta de colores basada en el tema
        if dark_mode:
            bg_color = "#1E1E1E"
            text_color = "#FFFFFF"
            card_bg = "linear-gradient(135deg, #2C2C2C, #424242)"
            shadow_color = "#000000"
            quote_text_bg = "#333333"
            quote_text_color = "#EDEDED"
        else:
            bg_color = "#FFFFFF"
            text_color = "#121212"
            card_bg = "linear-gradient(135deg, #FFD90F, #FFC107)"
            shadow_color = "#000000"
            quote_text_bg = "#FFFFFF"
            quote_text_color = "#000000"
            
        st.markdown(f"""
        <style>
        /* Importar fuentes estilo Simpsons */
        @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Gloria+Hallelujah&display=swap');

        /* Aplicar fuentes con grosor reducido */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Luckiest Guy', cursive !important;
            letter-spacing: 0.5px; /* Reducido de 1px */
            color: {text_color};
            font-weight: 400 !important; /* Forzar peso normal */
            text-shadow: 1px 1px 0px #FFD700; /* Sombra reducida para menos saturation */
        }}
        
        div.stMarkdown > div > p {{
             font-family: 'Gloria Hallelujah', cursive;
             font-size: 1.1rem;
             color: {text_color};
        }}

        .quote-card {{
            background: {card_bg};
            padding: 20px;
            border-radius: 15px;
            border: 2px solid {shadow_color}; /* Borde reducido a 2px */
            box-shadow: 3px 3px 0px {shadow_color}; /* Sombra reducida */
            margin: 10px 0;
        }}
        
        .character-name {{
            font-family: 'Luckiest Guy', cursive;
            font-size: 28px;
            color: {text_color} !important;
            text-shadow: 1px 1px 0px {shadow_color};
            margin-bottom: 10px;
        }}
        
        .quote-text {{
            font-family: 'Gloria Hallelujah', cursive;
            font-size: 20px;
            color: {quote_text_color};
            background: {quote_text_bg};
            padding: 15px;
            border-radius: 10px;
            border: 2px dashed {shadow_color};
            margin-bottom: 15px;
        }}
        
        .analysis-section {{
            background: #009DD9; /* Simpson Marge Hair Blue */
            color: white;
            padding: 25px;
            border-radius: 15px;
            border: 3px solid #000;
            box-shadow: 3px 3px 0px #000;
            margin-top: 20px;
        }}
        
        .main-header {{
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
            border-radius: 10px;
            margin-bottom: 20px;
            border: 2px solid #000;
        }}
        
        .main-header h1, .main-header h3 {{
             color: #121212 !important;
             text-shadow: none !important;
        }}
        
        /* Optimización de imágenes */
        .stImage > img {{
            border-radius: 10px;
            box-shadow: 3px 3px 0px #000;
            transition: transform 0.2s ease;
            border: 2px solid #000;
        }}
        
        .stImage > img:hover {{
            transform: scale(1.02);
        }}
        
        /* Loading placeholder */
        .image-loading {{
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }}
        
        @keyframes loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
        
        /* Mejoras generales de legibilidad */
        .stMarkdown p {{
            line-height: 1.6;
        }}
        
        .stButton > button {{
            border-radius: 20px;
            border: 2px solid #000;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            /* Estilo Simpsons: Amarillo */
            background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%); 
            color: #2F4F4F !important; /* Texto oscuro para contraste */
            box-shadow: 3px 3px 0px rgba(0,0,0,1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 5px 5px 0px rgba(0,0,0,1);
            background: linear-gradient(135deg, #FFC107 0%, #FFA000 100%);
            color: #000000 !important;
        }}
        
        /* Asegurar que el botón primario de Streamlit también siga este estilo */
        div[data-testid="stBaseButton-secondary"], div[data-testid="stBaseButton-primary"] {{
             background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
             color: #2F4F4F;
             border: 2px solid #000;
             box-shadow: 3px 3px 0px #000;
        }}
        
        /* Sidebar mejorado */
        .css-1d391kg {{
            background-color: {bg_color};
        }}
        
        /* General Background Override (trickier in global scope but trying via .stApp) */
        .stApp {{
            background-color: {bg_color};
        }}
        
        /* Métricas mejoradas */
        .metric-container {{
            background: {quote_text_bg};
            padding: 15px;
            border-radius: 10px;
            box-shadow: 3px 3px 0px #000;
            margin: 10px 0;
            border: 2px solid #000;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            /* Ajustes para móviles */
            .main-header {{
                padding: 10px;
            }}
            .main-header h1 {{
                font-size: 1.8rem !important;
            }}
            .main-header h3 {{
                font-size: 1rem !important;
            }}
            
            .quote-card, .quote-container, .analysis-section {{
                padding: 15px !important;
                margin: 10px 0 !important;
            }}
            
            .character-name {{
                font-size: 20px !important;
            }}
            
            .quote-text {{
                font-size: 16px !important;
            }}
            
            .stButton > button {{
                width: 100%;
                margin-bottom: 5px;
            }}
            
            .block-container {{
                padding-top: 2rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Renderiza el header principal"""
        st.markdown("""
        <div class="main-header">
            <h1>🍩 Springfield Insights</h1>
            <h3>Explorando la filosofía de Los Simpsons</h3>
        </div>
        """, unsafe_allow_html=True)
    
    def render_character_image(self, quote_data):
        """
        Renderiza la imagen del personaje con lazy loading y optimización CDN
        """
        character_name = quote_data.get("character", "Personaje Desconocido")
        image_url = quote_data.get("image", "")
        
        # Información adicional del personaje si está disponible
        character_info = quote_data.get("character_info", {})
        
        try:
            # Usar imagen optimizada del CDN
            st.image(
                image_url, 
                caption=self._build_image_caption(character_name, character_info),
                width='stretch'
            )
            
            # Mostrar fuente de datos si está disponible
            if quote_data.get("source") == "api":
                st.caption("📡 Imagen oficial desde CDN de Los Simpsons")
            
        except Exception as e:
            # Fallback a placeholder con información del error
            placeholder_img = self._get_placeholder_image(character_name)
            st.image(
                placeholder_img,
                caption=f"{character_name} (imagen no disponible)",
                width='stretch'
            )
            st.caption("⚠️ Usando imagen placeholder")
    
    def _build_image_caption(self, character_name: str, character_info: dict) -> str:
        """
        Construye caption informativo para la imagen del personaje
        
        Args:
            character_name: Nombre del personaje
            character_info: Información adicional del personaje
            
        Returns:
            Caption formateado con información del personaje
        """
        caption_parts = [character_name]
        
        # Añadir información adicional si está disponible
        if character_info.get('occupation') and character_info['occupation'] != 'Unknown':
            caption_parts.append(f"({character_info['occupation']})")
        
        if character_info.get('age'):
            caption_parts.append(f"- {character_info['age']} años")
        
        return " ".join(caption_parts)
    
    def render_quote_card(self, quote_data):
        """Renderiza la tarjeta de la cita usando componentes nativos de Streamlit"""
        
        # Obtener información adicional si está disponible
        character_info = quote_data.get("character_info", {})
        source_info = "🌐 API Oficial" if quote_data.get("source") == "api" else "📚 Base Local"
        
        # Crear contenedor con estilo personalizado
        with st.container():
            # CSS para este contenedor específico
            st.markdown("""
            <style>
            .quote-container {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                padding: 25px;
                border-radius: 15px;
                border: 3px solid #000;
                box-shadow: 4px 4px 0px #000; /* Sombra comic */
                margin: 15px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Header con nombre del personaje y fuente
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 🎭 {quote_data['character']}")
            with col2:
                st.caption(source_info)
            
            # Frase principal con estilo destacado
            st.markdown("---")
            st.markdown(f"""
            <div style='text-align: center; font-size: 22px; font-style: italic; 
                        color: #2F4F4F; margin: 20px 0; font-weight: 500; 
                        background: rgba(255,255,255,0.7); padding: 15px; 
                        border-radius: 10px; border: 2px dashed #000;'>
                "{quote_data["quote"]}"
            </div>
            """, unsafe_allow_html=True)
            
            # Contexto filosófico
            st.markdown("**💭 Contexto Filosófico:**")
            st.info(quote_data["context"])
            
            # Información adicional del personaje si está disponible
            if character_info:
                st.markdown("**ℹ️ Información del Personaje:**")
                
                info_cols = st.columns(3)
                
                if character_info.get('occupation') and character_info['occupation'] != 'Unknown':
                    with info_cols[0]:
                        st.metric("👔 Ocupación", character_info['occupation'])
                
                if character_info.get('age'):
                    with info_cols[1]:
                        st.metric("🎂 Edad", f"{character_info['age']} años")
                
                if character_info.get('status') and character_info['status'] != 'Unknown':
                    with info_cols[2]:
                        st.metric("📊 Estado", character_info['status'])
    
    def _render_character_details(self, character_info: dict) -> str:
        """
        Renderiza detalles adicionales del personaje si están disponibles
        
        Args:
            character_info: Información del personaje
            
        Returns:
            HTML con detalles del personaje
        """
        if not character_info:
            return ""
        
        details = []
        
        if character_info.get('occupation') and character_info['occupation'] != 'Unknown':
            details.append(f"👔 <strong>Ocupación:</strong> {character_info['occupation']}")
        
        if character_info.get('age'):
            details.append(f"🎂 <strong>Edad:</strong> {character_info['age']} años")
        
        if character_info.get('status') and character_info['status'] != 'Unknown':
            details.append(f"📊 <strong>Estado:</strong> {character_info['status']}")
        
        if details:
            details_html = "<br>".join(details)
            return f"""
            <div style='margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.6); border-radius: 6px; font-size: 14px;'>
                <strong style='color: #4169E1;'>ℹ️ Información del Personaje:</strong><br>
                <div style='margin-top: 8px;'>{details_html}</div>
            </div>
            """
        
        return ""
    
    def render_analysis(self, analysis):
        """Renderiza la sección de análisis usando componentes nativos de Streamlit"""
        
        # Contenedor para el análisis
        with st.container():
            # CSS para el contenedor de análisis
            st.markdown("""
            <style>
            .analysis-header {
                background: linear-gradient(135deg, #F0F8FF, #E6F3FF);
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #4169E1;
                margin: 20px 0 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Header del análisis
            st.markdown("""
            <div class="analysis-header">
                <h4 style='color: #4169E1; margin: 0; display: flex; align-items: center;'>
                    🧠 Análisis Filosófico Generado por GPT-4
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Contenido del análisis con mejor formato
            if analysis:
                # Dividir el análisis en párrafos para mejor legibilidad
                paragraphs = analysis.split('\\n\\n')
                
                for paragraph in paragraphs:
                    if paragraph.strip():
                        # Detectar si es un título (termina con :)
                        if paragraph.strip().endswith(':') and len(paragraph.strip()) < 100:
                            st.markdown(f"**{paragraph.strip()}**")
                        else:
                            st.write(paragraph.strip())
            else:
                st.warning("No se pudo generar el análisis filosófico.")
            
            # Footer con información
            st.caption("💡 Análisis generado automáticamente por inteligencia artificial")
    
    def _format_analysis_text(self, analysis: str) -> str:
        """
        Formatea el texto del análisis para mejor legibilidad
        
        Args:
            analysis: Texto del análisis sin formato
            
        Returns:
            Texto formateado con HTML para mejor presentación
        """
        if not analysis:
            return "<p><em>No se pudo generar el análisis.</em></p>"
        
        # Dividir en párrafos
        paragraphs = analysis.split('\\n\\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Detectar títulos (líneas que terminan con :)
                if paragraph.strip().endswith(':') and len(paragraph.strip()) < 100:
                    formatted_paragraphs.append(f"<h5 style='color: #FF6347; margin: 20px 0 10px 0;'>{paragraph.strip()}</h5>")
                else:
                    # Párrafo normal con mejor espaciado
                    formatted_paragraphs.append(f"<p style='margin-bottom: 15px; text-align: justify;'>{paragraph.strip()}</p>")
        
        return ''.join(formatted_paragraphs)
    
    def _get_placeholder_image(self, character: str) -> str:
        """Genera imagen placeholder para personajes"""
        safe_name = character.replace(' ', '+').replace("'", "")
        return f"https://via.placeholder.com/300x200/FFD700/2F4F4F?text={safe_name}"