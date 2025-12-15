#!/usr/bin/env python3
"""
Springfield Insights - Versión Simplificada para Streamlit Cloud
"""
import streamlit as st
from openai import OpenAI
import os
import random

# Configuración de página
st.set_page_config(
    page_title="Springfield Insights",
    page_icon="🍩",
    layout="wide"
)

def get_api_key():
    """Obtiene la API key de Streamlit secrets o variables de entorno"""
    try:
        # Prioridad 1: Streamlit Cloud secrets
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # Prioridad 2: Variables de entorno locales
        return os.getenv("OPENAI_API_KEY")

def main():
    """Función principal"""
    
    # Header
    st.title("🍩 Springfield Insights")
    st.markdown("### *Explorando la filosofía oculta en Los Simpsons*")
    st.markdown("---")
    
    # Verificar API Key
    api_key = get_api_key()
    
    if not api_key:
        st.error("❌ **Configuración de API Key requerida**")
        st.markdown("""
        **Para Streamlit Cloud:**
        1. Ve a Settings → Secrets en tu app
        2. Añade: `OPENAI_API_KEY = "tu-api-key"`
        
        **Para desarrollo local:**
        1. Crea archivo `.env`
        2. Añade: `OPENAI_API_KEY=tu-api-key`
        """)
        st.stop()
    
    # Inicializar cliente OpenAI
    try:
        client = OpenAI(api_key=api_key)
        st.success("✅ Conectado a OpenAI")
    except Exception as e:
        st.error(f"❌ Error conectando a OpenAI: {e}")
        st.stop()
    
    # Personajes
    personajes = [
        "Homer Simpson - Padre de familia optimista",
        "Lisa Simpson - Niña inteligente y reflexiva", 
        "Bart Simpson - Niño rebelde y astuto",
        "Marge Simpson - Madre sabia y empática"
    ]
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎭 Configuración")
        personaje_seleccionado = st.selectbox(
            "Selecciona personaje:",
            ["Aleatorio"] + personajes
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Acerca de")
        st.write("Genera reflexiones filosóficas de Los Simpsons usando IA")
        st.success("🟢 OpenAI Conectado")
    
    # Botón principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎲 Generar Reflexión Filosófica", 
                    use_container_width=True, 
                    type="primary"):
            
            # Seleccionar personaje
            if personaje_seleccionado == "Aleatorio":
                personaje = random.choice(personajes)
            else:
                personaje = personaje_seleccionado
            
            # Generar reflexión
            with st.spinner("🧠 Generando reflexión..."):
                try:
                    prompt = f"""Eres {personaje} de Los Simpsons.

Genera una reflexión filosófica auténtica:

1. Una frase memorable (1-2 oraciones) sobre la vida
2. Un análisis filosófico de 80 palabras

Formato:
FRASE: [tu frase]
ANÁLISIS: [análisis filosófico]"""

                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200,
                        temperature=0.7
                    )
                    
                    resultado = response.choices[0].message.content.strip()
                    
                    # Mostrar resultado
                    st.markdown("---")
                    st.markdown(f"### 🎭 {personaje.split(' - ')[0]}")
                    
                    if "FRASE:" in resultado and "ANÁLISIS:" in resultado:
                        partes = resultado.split("ANÁLISIS:")
                        frase = partes[0].replace("FRASE:", "").strip()
                        analisis = partes[1].strip()
                        
                        st.markdown("#### 💭 Reflexión")
                        st.info(f'*"{frase}"*')
                        
                        st.markdown("#### 📚 Análisis Filosófico")
                        st.write(analisis)
                    else:
                        st.write(resultado)
                        
                except Exception as e:
                    st.error(f"Error generando reflexión: {e}")
    
    # Mensaje de bienvenida si no hay contenido
    if 'generated' not in st.session_state:
        st.markdown("---")
        st.info("👆 Haz clic en el botón para generar tu primera reflexión filosófica")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🤖 IA Avanzada**
            
            GPT-3.5-Turbo genera análisis filosóficos auténticos
            """)
        
        with col2:
            st.markdown("""
            **🎭 Personajes Únicos**
            
            Cada reflexión mantiene la personalidad del personaje
            """)
        
        with col3:
            st.markdown("""
            **📚 Rigor Académico**
            
            Análisis profundo de crítica social y filosofía
            """)

if __name__ == "__main__":
    main()