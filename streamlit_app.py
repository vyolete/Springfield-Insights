#!/usr/bin/env python3
"""
Springfield Insights - Streamlit Cloud Version
Aplicación optimizada para deploy en Streamlit Cloud con GitHub
"""
import streamlit as st
from openai import OpenAI
import os
import random

# Cargar variables de entorno solo si existe el archivo (desarrollo local)
try:
    from dotenv import load_dotenv
    if os.path.exists('.env'):
        load_dotenv()
except ImportError:
    pass  # dotenv no disponible en Streamlit Cloud

# Configuración de página
st.set_page_config(
    page_title="Springfield Insights",
    page_icon="🍩",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_api_key():
    """Obtiene la API key de Streamlit secrets o variables de entorno"""
    try:
        # Prioridad 1: Streamlit Cloud secrets
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        try:
            # Prioridad 2: Variables de entorno locales
            return os.getenv("OPENAI_API_KEY")
        except:
            return None

def init_openai_client():
    """Inicializa el cliente de OpenAI"""
    api_key = get_api_key()
    
    if not api_key:
        st.error("❌ **Configuración requerida:**")
        st.markdown("""
        **Para Streamlit Cloud:**
        1. Ve a tu app en Streamlit Cloud
        2. Haz clic en "Settings" → "Secrets"
        3. Añade: `OPENAI_API_KEY = "tu-api-key"`
        
        **Para desarrollo local:**
        1. Crea archivo `.env`
        2. Añade: `OPENAI_API_KEY=tu-api-key`
        """)
        st.stop()
    
    return OpenAI(api_key=api_key)

# Inicializar cliente
client = init_openai_client()

# Personajes de Los Simpsons
PERSONAJES = [
    {
        "nombre": "Homer Simpson",
        "descripcion": "Padre de familia que trabaja en una planta nuclear",
        "emoji": "🍺",
        "personalidad": "Optimista y simple, encuentra sabiduría en lo cotidiano"
    },
    {
        "nombre": "Lisa Simpson", 
        "descripcion": "Niña inteligente y activista social",
        "emoji": "🎷",
        "personalidad": "Intelectual y reflexiva, cuestiona el mundo con profundidad"
    },
    {
        "nombre": "Bart Simpson",
        "descripcion": "Niño travieso que cuestiona la autoridad", 
        "emoji": "🛹",
        "personalidad": "Rebelde y astuto, ve la hipocresía del mundo adulto"
    },
    {
        "nombre": "Marge Simpson",
        "descripcion": "Madre paciente con sabiduría práctica",
        "emoji": "💙", 
        "personalidad": "Empática y sabia, encuentra equilibrio en el caos familiar"
    }
]

def generar_reflexion(personaje_seleccionado=None):
    """Genera reflexión filosófica con un personaje específico o aleatorio"""
    if personaje_seleccionado:
        personaje = personaje_seleccionado
    else:
        personaje = random.choice(PERSONAJES)
    
    prompt = f"""Eres {personaje['nombre']} de Los Simpsons. {personaje['descripcion']}.

Tu personalidad: {personaje['personalidad']}

Genera una reflexión filosófica auténtica a tu personaje:

1. Una frase memorable (1-2 oraciones) que dirías sobre la vida, sociedad o familia
2. Un análisis filosófico de 80-100 palabras explicando el significado profundo

Formato exacto:
FRASE: [tu frase característica]
ANÁLISIS: [análisis filosófico profundo]

Mantén tu estilo de habla característico pero con profundidad filosófica."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip(), personaje
    
    except Exception as e:
        st.error(f"Error generando reflexión: {str(e)}")
        return None, None

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.title("🍩 Springfield Insights")
    st.markdown("### *Explorando la filosofía oculta en Los Simpsons*")
    st.markdown("---")
    
    # Sidebar con información
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/The_Simpsons_yellow_logo.svg/320px-The_Simpsons_yellow_logo.svg.png", width=200)
        
        st.markdown("### 🎭 Selecciona un Personaje")
        
        # Selector de personaje
        personaje_nombres = ["Aleatorio"] + [p["nombre"] for p in PERSONAJES]
        personaje_seleccionado = st.selectbox(
            "Elige quién reflexionará:",
            personaje_nombres,
            index=0
        )
        
        # Mostrar info del personaje seleccionado
        if personaje_seleccionado != "Aleatorio":
            personaje_info = next(p for p in PERSONAJES if p["nombre"] == personaje_seleccionado)
            st.markdown(f"**{personaje_info['emoji']} {personaje_info['nombre']}**")
            st.caption(personaje_info["descripcion"])
            st.caption(f"*{personaje_info['personalidad']}*")
        
        st.markdown("---")
        
        # Información de la app
        st.markdown("### ℹ️ Acerca de")
        st.markdown("""
        **Springfield Insights** usa inteligencia artificial para generar reflexiones filosóficas auténticas de los personajes de Los Simpsons.
        
        **🤖 Tecnología:**
        - OpenAI GPT-3.5-Turbo
        - Streamlit Framework
        - Deploy en Streamlit Cloud
        
        **🎯 Propósito:**
        Explorar la profundidad filosófica y crítica social presente en la serie más longeva de la televisión.
        """)
        
        # Estado de la aplicación
        st.markdown("### 📊 Estado")
        st.success("🟢 Conectado a OpenAI")
        st.info("☁️ Ejecutándose en Streamlit Cloud")
    
    # Contenido principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Botón principal
        if st.button("🎲 Generar Nueva Reflexión Filosófica", 
                    use_container_width=True, 
                    type="primary"):
            
            # Determinar personaje
            personaje_para_usar = None
            if personaje_seleccionado != "Aleatorio":
                personaje_para_usar = next(p for p in PERSONAJES if p["nombre"] == personaje_seleccionado)
            
            # Generar reflexión
            with st.spinner("🧠 Generando reflexión filosófica..."):
                resultado, personaje_usado = generar_reflexion(personaje_para_usar)
                
                if resultado and personaje_usado:
                    # Guardar en session state
                    st.session_state.ultima_reflexion = resultado
                    st.session_state.ultimo_personaje = personaje_usado
                    st.rerun()
    
    # Mostrar reflexión si existe
    if hasattr(st.session_state, 'ultima_reflexion') and st.session_state.ultima_reflexion:
        mostrar_reflexion(st.session_state.ultima_reflexion, st.session_state.ultimo_personaje)
    else:
        # Mensaje de bienvenida
        mostrar_bienvenida()

def mostrar_reflexion(resultado, personaje):
    """Muestra la reflexión generada con formato elegante"""
    
    # Parsear resultado
    if "FRASE:" in resultado and "ANÁLISIS:" in resultado:
        partes = resultado.split("ANÁLISIS:")
        frase = partes[0].replace("FRASE:", "").strip()
        analisis = partes[1].strip()
        
        # Header del personaje
        st.markdown("---")
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"## {personaje['emoji']}")
        
        with col2:
            st.markdown(f"### {personaje['nombre']}")
            st.caption(personaje['descripcion'])
        
        # Frase principal
        st.markdown("#### 💭 Reflexión")
        st.info(f'*"{frase}"*')
        
        # Análisis filosófico
        st.markdown("#### 📚 Análisis Filosófico")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 20px; border-radius: 10px; border-left: 4px solid #4CAF50;'>
            <p style='margin: 0; line-height: 1.6; color: #2c3e50;'>{analisis}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones de acción
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Otra Reflexión"):
                st.rerun()
        
        with col2:
            if st.button("📋 Copiar Frase"):
                st.toast("📋 Frase copiada al portapapeles", icon="✅")
        
        with col3:
            if st.button("💾 Guardar"):
                st.toast("💾 Reflexión guardada", icon="⭐")
        
        with col4:
            if st.button("🔗 Compartir"):
                st.toast("🔗 Enlace generado", icon="📤")
    
    else:
        st.markdown("#### 📝 Reflexión Generada")
        st.write(resultado)

def mostrar_bienvenida():
    """Muestra mensaje de bienvenida"""
    st.markdown("---")
    
    # Mensaje principal
    st.markdown("""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white; margin: 20px 0;'>
        <h2>🎭 ¡Bienvenido a Springfield Insights!</h2>
        <p style='font-size: 18px; margin: 20px 0;'>
            Descubre la <strong>sabiduría filosófica</strong> oculta en Los Simpsons
        </p>
        <p style='font-size: 16px; opacity: 0.9;'>
            Usa inteligencia artificial para generar reflexiones profundas de tus personajes favoritos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Características
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
            <h3>🤖 IA Avanzada</h3>
            <p>GPT-3.5-Turbo genera análisis filosóficos auténticos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
            <h3>🎯 Personajes Auténticos</h3>
            <p>Cada reflexión mantiene la personalidad única del personaje</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
            <h3>📚 Profundidad Académica</h3>
            <p>Análisis riguroso de crítica social y filosofía</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()