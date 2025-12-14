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
            background: #F0F8FF;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #4169E1;
            margin-top: 15px;
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
        """Renderiza la tarjeta de la cita"""
        st.markdown(f"""
        <div class="quote-card">
            <div class="character-name">{quote_data["character"]}</div>
            <div class="quote-text">"{quote_data["quote"]}"</div>
            <div><strong>Contexto:</strong> {quote_data["context"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_analysis(self, analysis):
        """Renderiza la sección de análisis"""
        st.markdown(f"""
        <div class="analysis-section">
            {analysis}
        </div>
        """, unsafe_allow_html=True)
    
    def _get_placeholder_image(self, character: str) -> str:
        """Genera imagen placeholder para personajes"""
        safe_name = character.replace(' ', '+').replace("'", "")
        return f"https://via.placeholder.com/300x200/FFD700/2F4F4F?text={safe_name}"