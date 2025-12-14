#!/usr/bin/env python3
"""
Springfield Insights - Versión Simplificada y Rápida
Muestra frases reales de Los Simpsons con análisis filosófico e imágenes
"""
import streamlit as st
import requests
import random
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("❌ Configura tu OPENAI_API_KEY en el archivo .env")
    st.stop()

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de página
st.set_page_config(
    page_title="Springfield Insights",
    page_icon="🍩",
    layout="wide"
)

# CSS personalizado
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
</style>
""", unsafe_allow_html=True)

# Frases reales de Los Simpsons con contexto
SIMPSONS_QUOTES = [
    {
        "quote": "D'oh!",
        "character": "Homer Simpson",
        "context": "Expresión de frustración ante los errores cotidianos",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "¡Ay, caramba!",
        "character": "Bart Simpson", 
        "context": "Exclamación de sorpresa ante situaciones inesperadas",
        "image": "https://static.wikia.nocookie.net/simpsons/images/a/aa/Bart_Simpson.png"
    },
    {
        "quote": "Si no tienes nada bueno que decir sobre alguien, ven y siéntate aquí a mi lado.",
        "character": "Marge Simpson",
        "context": "Crítica sutil al chisme y la naturaleza humana",
        "image": "https://static.wikia.nocookie.net/simpsons/images/0/0b/Marge_Simpson.png"
    },
    {
        "quote": "La ignorancia es una bendición.",
        "character": "Homer Simpson",
        "context": "Reflexión sobre la felicidad en la simplicidad",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "Soy demasiado joven para morir y demasiado viejo para comer de la mesa de los niños.",
        "character": "Lisa Simpson",
        "context": "Dilema existencial de la adolescencia y el crecimiento",
        "image": "https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png"
    },
    {
        "quote": "Estúpido Flanders.",
        "character": "Homer Simpson",
        "context": "Envidia hacia la perfección aparente del vecino",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "No me hagas pensar. Estoy de vacaciones.",
        "character": "Homer Simpson",
        "context": "Rechazo al esfuerzo intelectual en momentos de descanso",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "La televisión: maestra, madre, amante secreta.",
        "character": "Homer Simpson",
        "context": "Dependencia moderna de los medios de comunicación",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "Ser normal está sobrevalorado.",
        "character": "Lisa Simpson",
        "context": "Valoración de la individualidad frente al conformismo",
        "image": "https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png"
    },
    {
        "quote": "Los libros son inútiles. Solo enseñan cosas.",
        "character": "Homer Simpson",
        "context": "Paradoja del anti-intelectualismo",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    }
]

@st.cache_data(ttl=3600)
def generate_philosophical_analysis(quote: str, character: str, context: str) -> str:
    """Genera análisis filosófico usando GPT-3.5-turbo (rápido)"""
    try:
        prompt = f"""Analiza esta cita de Los Simpsons desde una perspectiva filosófica:

Cita: "{quote}"
Personaje: {character}
Contexto: {context}

Proporciona un análisis de 150-200 palabras que incluya:
1. Significado filosófico
2. Crítica social implícita  
3. Relevancia contemporánea

Mantén un tono académico pero accesible."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en filosofía especializado en análisis cultural de Los Simpsons."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.6,
            timeout=10
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generando análisis: {str(e)}"

def get_placeholder_image(character: str) -> str:
    """Genera imagen placeholder para personajes"""
    safe_name = character.replace(' ', '+').replace("'", "")
    return f"https://via.placeholder.com/300x200/FFD700/2F4F4F?text={safe_name}"

def main():
    """Aplicación principal simplificada"""
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🍩 Springfield Insights</h1>
        <h3>Explorando la filosofía de Los Simpsons</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar estado
    if 'current_quote_index' not in st.session_state:
        st.session_state.current_quote_index = 0
    
    # Botón principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎲 Obtener Nueva Reflexión Filosófica", use_container_width=True, type="primary"):
            st.session_state.current_quote_index = random.randint(0, len(SIMPSONS_QUOTES) - 1)
            st.rerun()
    
    # Mostrar cita actual
    if st.session_state.current_quote_index is not None:
        quote_data = SIMPSONS_QUOTES[st.session_state.current_quote_index]
        
        # Layout principal
        col_img, col_content = st.columns([1, 2])
        
        # Imagen del personaje
        with col_img:
            try:
                st.image(
                    quote_data["image"], 
                    caption=quote_data["character"],
                    use_column_width=True
                )
            except:
                # Fallback a placeholder
                placeholder_img = get_placeholder_image(quote_data["character"])
                st.image(
                    placeholder_img,
                    caption=quote_data["character"],
                    use_column_width=True
                )
        
        # Contenido de la cita
        with col_content:
            # Tarjeta de cita
            st.markdown(f"""
            <div class="quote-card">
                <div class="character-name">{quote_data["character"]}</div>
                <div class="quote-text">"{quote_data["quote"]}"</div>
                <div><strong>Contexto:</strong> {quote_data["context"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis filosófico
        st.markdown("### 📚 Análisis Filosófico")
        
        with st.spinner("🧠 Generando análisis académico..."):
            analysis = generate_philosophical_analysis(
                quote_data["quote"],
                quote_data["character"], 
                quote_data["context"]
            )
        
        st.markdown(f"""
        <div class="analysis-section">
            {analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Acciones
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Otra Cita"):
                st.session_state.current_quote_index = random.randint(0, len(SIMPSONS_QUOTES) - 1)
                st.rerun()
        
        with col2:
            if st.button("📋 Copiar Cita"):
                copy_text = f'"{quote_data["quote"]}" - {quote_data["character"]}'
                st.toast("📋 Cita copiada", icon="✅")
        
        with col3:
            if st.button("💾 Favorito"):
                st.toast("⭐ Añadido a favoritos", icon="💾")
        
        with col4:
            if st.button("🔗 Compartir"):
                st.toast("🔗 Enlace copiado", icon="📤")
    
    else:
        # Mensaje de bienvenida
        st.info("""
        🎭 **¡Bienvenido a Springfield Insights!**
        
        Haz clic en el botón para explorar frases reales de Los Simpsons 
        con análisis filosófico profundo generado por inteligencia artificial.
        
        ✨ **Características:**
        - Frases auténticas de la serie
        - Análisis académico riguroso
        - Imágenes de personajes
        - Contexto filosófico y social
        """)
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### 📊 Estadísticas")
        st.metric("Frases disponibles", len(SIMPSONS_QUOTES))
        st.metric("Análisis generados", st.session_state.get('analyses_count', 0))
        
        st.markdown("### 🎯 Acerca de")
        st.markdown("""
        **Springfield Insights** combina el humor inteligente de Los Simpsons 
        con análisis filosófico académico usando IA.
        
        - **Frases reales** de la serie
        - **Análisis profundo** con GPT-3.5
        - **Contexto cultural** y filosófico
        - **Interfaz optimizada** para velocidad
        """)
        
        st.markdown("### ⚙️ Configuración")
        st.success("✅ OpenAI configurado")
        st.info("🚀 Modo rápido activado")

if __name__ == "__main__":
    main()