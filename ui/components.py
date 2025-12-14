"""
Componentes de interfaz de usuario para Springfield Insights
"""
import streamlit as st

class UIComponents:
    """Componentes reutilizables de la interfaz de usuario"""
    
    def apply_custom_css(self):
        """Aplica estilos CSS personalizados"""
        st.markdown("""
        <style>
        .quote-card {
            background: linear-gradient(135deg, #FFD700, #FFA500);
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #FF6347;
            margin: 10px 0;
        }
        .character-name {
            font-size: 24px;
            font-weight: bold;
            color: #2F4F4F;
            margin-bottom: 10px;
        }
        .quote-text {
            font-size: 18px;
            font-style: italic;
            color: #2F4F4F;
            margin-bottom: 15px;
        }
        .analysis-section {
            background: linear-gradient(135deg, #F0F8FF, #E6F3FF);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #4169E1;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(65, 105, 225, 0.1);
        }
        .main-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        /* Optimización de imágenes */
        .stImage > img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        
        .stImage > img:hover {
            transform: scale(1.02);
        }
        
        /* Loading placeholder */
        .image-loading {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Mejoras generales de legibilidad */
        .stMarkdown p {
            line-height: 1.6;
        }
        
        .stButton > button {
            border-radius: 20px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Sidebar mejorado */
        .css-1d391kg {
            background-color: #FAFAFA;
        }
        
        /* Métricas mejoradas */
        .metric-container {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
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
        """Renderiza la tarjeta de la cita con diseño mejorado"""
        
        # Obtener información adicional si está disponible
        character_info = quote_data.get("character_info", {})
        source_info = "🌐 API Oficial" if quote_data.get("source") == "api" else "📚 Base Local"
        
        st.markdown(f"""
        <div class="quote-card">
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                <div class="character-name">{quote_data["character"]}</div>
                <div style='font-size: 12px; color: #666; background: rgba(255,255,255,0.7); padding: 4px 8px; border-radius: 12px;'>
                    {source_info}
                </div>
            </div>
            
            <div class="quote-text" style='font-size: 20px; line-height: 1.6; margin-bottom: 20px; text-align: center; font-weight: 500;'>
                "{quote_data["quote"]}"
            </div>
            
            <div style='background: rgba(255,255,255,0.8); padding: 12px; border-radius: 8px; border-left: 3px solid #FF6347;'>
                <strong style='color: #FF6347;'>💭 Contexto Filosófico:</strong>
                <div style='margin-top: 8px; line-height: 1.5;'>{quote_data["context"]}</div>
            </div>
            
            {self._render_character_details(character_info)}
        </div>
        """, unsafe_allow_html=True)
    
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
        """Renderiza la sección de análisis con formato mejorado"""
        
        # Procesar el análisis para mejor presentación
        formatted_analysis = self._format_analysis_text(analysis)
        
        st.markdown(f"""
        <div class="analysis-section">
            <h4 style='color: #4169E1; margin-bottom: 15px; display: flex; align-items: center;'>
                🧠 Análisis Filosófico Generado por GPT-4
            </h4>
            <div style='line-height: 1.8; font-size: 16px; color: #2F4F4F;'>
                {formatted_analysis}
            </div>
            <div style='margin-top: 15px; padding-top: 10px; border-top: 1px solid #E0E0E0; font-size: 12px; color: #666;'>
                <em>💡 Análisis generado automáticamente por inteligencia artificial</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
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
        paragraphs = analysis.split('\n\n')
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