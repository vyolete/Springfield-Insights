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
        """Renderiza la imagen del personaje"""
        try:
            st.image(
                quote_data["image"], 
                caption=quote_data["character"],
                width='stretch'
            )
        except:
            # Fallback a placeholder
            placeholder_img = self._get_placeholder_image(quote_data["character"])
            st.image(
                placeholder_img,
                caption=quote_data["character"],
                width='stretch'
            )
    
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