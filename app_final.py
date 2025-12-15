#!/usr/bin/env python3
"""
Springfield Insights - Versión Final Funcional
SÚPER SIMPLE - Solo lo esencial que funciona
"""
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import random

# Cargar variables de entorno (local) o secrets (cloud)
load_dotenv()

# Configuración básica
st.set_page_config(page_title="Springfield Insights", page_icon="🍩")

# Verificar API Key - Prioridad: secrets > .env
try:
    # Intentar usar Streamlit secrets primero (para cloud)
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    # Fallback a variables de entorno locales
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ Configura OPENAI_API_KEY en Streamlit Secrets o archivo .env")
    st.stop()

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Personajes simples
PERSONAJES = [
    "Homer Simpson - Padre de familia que trabaja en una planta nuclear",
    "Lisa Simpson - Niña inteligente y activista social", 
    "Bart Simpson - Niño travieso que cuestiona la autoridad",
    "Marge Simpson - Madre paciente con sabiduría práctica"
]

def generar_reflexion():
    """Genera reflexión filosófica simple"""
    personaje = random.choice(PERSONAJES)
    
    prompt = f"""Eres {personaje} de Los Simpsons. 

Genera:
1. Una frase corta (1-2 oraciones) que dirías sobre la vida
2. Un análisis filosófico de 100 palabras sobre esa frase

Formato:
FRASE: [tu frase]
ANÁLISIS: [análisis filosófico]"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

# Interfaz
st.title("🍩 Springfield Insights")
st.write("Reflexiones filosóficas de Los Simpsons")

if st.button("🎲 Generar Reflexión"):
    with st.spinner("Generando..."):
        resultado = generar_reflexion()
        
        # Mostrar resultado
        if "FRASE:" in resultado and "ANÁLISIS:" in resultado:
            partes = resultado.split("ANÁLISIS:")
            frase = partes[0].replace("FRASE:", "").strip()
            analisis = partes[1].strip()
            
            st.success("✅ Reflexión generada!")
            
            # Mostrar frase
            st.markdown("### 💭 Frase")
            st.info(f'"{frase}"')
            
            # Mostrar análisis
            st.markdown("### 📚 Análisis Filosófico")
            st.write(analisis)
            
        else:
            st.markdown("### 📝 Contenido Generado")
            st.write(resultado)

# Información
with st.sidebar:
    st.markdown("### ℹ️ Acerca de")
    st.write("Aplicación simple que genera reflexiones filosóficas usando IA.")
    st.write("Requiere OpenAI API Key en archivo .env")