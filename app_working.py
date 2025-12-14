#!/usr/bin/env python3
"""
Springfield Insights - Versión Funcional Simplificada
Basada en la versión original que funcionaba correctamente
"""
import streamlit as st
import logging
import sys
from pathlib import Path
import time
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import random

# Cargar variables de entorno
load_dotenv()

# Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

# Datos de personajes (fallback)
FALLBACK_CHARACTERS = [
    {
        "name": "Homer Simpson",
        "description": "Padre de familia, trabajador de planta nuclear",
        "philosophical_context": "Reflexiones sobre la vida cotidiana, el trabajo y la felicidad simple",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Homer+Simpson"
    },
    {
        "name": "Lisa Simpson", 
        "description": "Niña prodigio, saxofonista, activista",
        "philosophical_context": "Pensamiento crítico, justicia social y búsqueda de la verdad",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Lisa+Simpson"
    },
    {
        "name": "Bart Simpson",
        "description": "Niño travieso, rebelde por naturaleza",
        "philosophical_context": "Cuestionamiento de la autoridad y libertad individual",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Bart+Simpson"
    },
    {
        "name": "Marge Simpson",
        "description": "Madre de familia, voz de la razón",
        "philosophical_context": "Moralidad, paciencia y sabiduría doméstica",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Marge+Simpson"
    }
]

def get_random_character():
    """Obtiene un personaje aleatorio"""
    return random.choice(FALLBACK_CHARACTERS)

def generate_philosophical_analysis(character_data):
    """Genera análisis filosófico usando OpenAI"""
    
    if not OPENAI_API_KEY:
        return {
            'success': False,
            'error': 'OpenAI API Key no configurada'
        }
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""Genera una reflexión filosófica original para {character_data['name']} de Los Simpsons.

Personaje: {character_data['name']}
Descripción: {character_data['description']}
Contexto filosófico: {character_data['philosophical_context']}

Crea:
1. Una reflexión de 2-3 oraciones que {character_data['name']} podría decir sobre la vida, la sociedad o la condición humana
2. Un análisis académico de 200-250 palabras que explore los conceptos filosóficos, crítica social y relevancia contemporánea

Formato:
REFLEXIÓN: [La reflexión del personaje]
ANÁLISIS: [El análisis académico profundo]"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un experto en filosofía especializado en Los Simpsons. Genera contenido original y académicamente riguroso."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=400,
            temperature=0.7,
            timeout=15
        )
        
        if response.choices:
            content = response.choices[0].message.content.strip()
            
            # Parsear respuesta
            if "REFLEXIÓN:" in content and "ANÁLISIS:" in content:
                parts = content.split("ANÁLISIS:")
                reflection = parts[0].replace("REFLEXIÓN:", "").strip()
                analysis = parts[1].strip()
                
                return {
                    'success': True,
                    'quote': reflection,
                    'character': character_data['name'],
                    'image': character_data['image'],
                    'analysis': analysis
                }
            else:
                # Fallback si el formato no es correcto
                return {
                    'success': True,
                    'quote': content[:200] + "..." if len(content) > 200 else content,
                    'character': character_data['name'],
                    'image': character_data['image'],
                    'analysis': content
                }
        
        return {
            'success': False,
            'error': 'No se recibió respuesta del modelo'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generando análisis: {str(e)}'
        }

def main():
    """Aplicación principal"""
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🍩 Springfield Insights</h1>
        <h3>Explorando la filosofía de Los Simpsons</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar configuración
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY no configurada")
        st.markdown("""
        ### 🔧 Configuración Requerida
        
        Crea un archivo `.env` con:
        ```
        OPENAI_API_KEY=tu_api_key_aqui
        ```
        """)
        st.stop()
    
    # Inicializar estado de sesión
    if 'current_quote' not in st.session_state:
        st.session_state.current_quote = None
    if 'quotes_analyzed' not in st.session_state:
        st.session_state.quotes_analyzed = 0
    
    # Botón principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎲 Obtener Nueva Reflexión Filosófica", use_container_width=True, type="primary"):
            
            # Mostrar estado de carga
            with st.spinner("🧠 Generando reflexión filosófica..."):
                
                # Obtener personaje aleatorio
                character_data = get_random_character()
                
                # Generar análisis
                result = generate_philosophical_analysis(character_data)
                
                if result['success']:
                    st.session_state.current_quote = result
                    st.session_state.quotes_analyzed += 1
                    st.success("✅ ¡Reflexión filosófica generada!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result['error']}")
    
    # Mostrar cita actual
    if st.session_state.current_quote:
        quote_data = st.session_state.current_quote
        
        # Layout principal
        col_img, col_content = st.columns([1, 2])
        
        # Imagen del personaje
        with col_img:
            st.image(
                quote_data["image"], 
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
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis filosófico
        st.markdown("### 📚 Análisis Filosófico")
        
        st.markdown(f"""
        <div class="analysis-section">
            {quote_data["analysis"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Acciones
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Otra Reflexión"):
                # Limpiar cita actual para forzar nueva generación
                st.session_state.current_quote = None
                st.rerun()
        
        with col2:
            if st.button("📋 Copiar"):
                copy_text = f'"{quote_data["quote"]}" - {quote_data["character"]}'
                st.toast("📋 Reflexión copiada", icon="✅")
        
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
        
        Haz clic en el botón para generar una reflexión filosófica original 
        al estilo de Los Simpsons, creada por inteligencia artificial.
        
        ✨ **Características:**
        - Reflexiones originales generadas por GPT-3.5
        - Análisis filosófico académico riguroso
        - Personajes auténticos de la serie
        - Contexto cultural y social profundo
        """)
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### 📊 Estadísticas")
        st.metric("Reflexiones generadas", st.session_state.quotes_analyzed)
        
        st.markdown("### 🎯 Acerca de")
        st.markdown("""
        **Springfield Insights** utiliza inteligencia artificial para generar 
        reflexiones filosóficas originales al estilo de Los Simpsons.
        
        - **IA Generativa**: GPT-3.5 para contenido original
        - **Análisis Riguroso**: Perspectiva académica
        - **Personajes Auténticos**: Fieles al espíritu de la serie
        """)
        
        st.markdown("### ⚙️ Estado")
        if OPENAI_API_KEY:
            st.success("✅ OpenAI configurado")
        else:
            st.error("❌ OpenAI no configurado")

if __name__ == "__main__":
    main()