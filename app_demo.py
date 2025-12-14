#!/usr/bin/env python3
"""
Springfield Insights - Versión DEMO que funciona al 100%
Incluye análisis predefinidos para demostración inmediata
"""
import streamlit as st
import random
import time

# Configuración de página
st.set_page_config(
    page_title="Springfield Insights - Demo",
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
.demo-badge {
    background: #FF6347;
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Frases con análisis predefinidos (funciona sin IA)
DEMO_QUOTES = [
    {
        "quote": "D'oh!",
        "character": "Homer Simpson",
        "context": "Expresión de frustración ante los errores cotidianos",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Homer+Simpson",
        "analysis": """Esta icónica exclamación de Homer Simpson trasciende su aparente simplicidad para convertirse en una profunda reflexión sobre la condición humana. Desde una perspectiva filosófica, "D'oh!" representa la toma de conciencia inmediata del error, un momento de lucidez que revela nuestra falibilidad inherente.

La expresión encapsula la filosofía existencialista de Sartre sobre la "náusea" del reconocimiento de nuestras limitaciones. Homer, en su simplicidad, articula lo que los filósofos han debatido durante siglos: el momento preciso en que reconocemos nuestros errores y, por extensión, nuestra humanidad imperfecta.

En términos de crítica social, "D'oh!" se ha convertido en un símbolo cultural que refleja la frustración colectiva ante las complejidades de la vida moderna, donde los errores son inevitables pero socialmente penalizados."""
    },
    {
        "quote": "¡Ay, caramba!",
        "character": "Bart Simpson",
        "context": "Exclamación de sorpresa ante situaciones inesperadas",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Bart+Simpson",
        "analysis": """La exclamación de Bart Simpson "¡Ay, caramba!" representa una fascinante intersección entre la filosofía del asombro aristotélica y la crítica social contemporánea. Aristóteles sostenía que el asombro es el origen de toda filosofía, y Bart, en su perpetua capacidad de sorprenderse, encarna esta disposición filosófica fundamental.

Desde una perspectiva sociológica, esta expresión refleja la resistencia juvenil ante las estructuras sociales establecidas. Bart no solo se sorprende; se rebela contra lo predecible, lo normativo, lo adulto. Su "¡Ay, caramba!" es un grito de libertad intelectual que desafía las expectativas sociales.

La relevancia contemporánea de esta expresión radica en su capacidad para articular la experiencia de vivir en una sociedad en constante cambio, donde lo inesperado se ha vuelto la norma y el asombro, una herramienta de supervivencia cultural."""
    },
    {
        "quote": "Si no tienes nada bueno que decir sobre alguien, ven y siéntate aquí a mi lado.",
        "character": "Marge Simpson",
        "context": "Crítica sutil al chisme y la naturaleza humana",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Marge+Simpson",
        "analysis": """Esta aparentemente simple observación de Marge Simpson constituye una brillante deconstrucción de la hipocresía social y los mecanismos de cohesión grupal. Desde una perspectiva filosófica, la frase expone la paradoja moral inherente en la condena pública del chisme mientras se participa privadamente en él.

La crítica social implícita es devastadora: Marge reconoce que el chisme, aunque moralmente cuestionable, cumple una función social fundamental como mecanismo de vinculación y establecimiento de jerarquías. Su invitación irónica revela cómo las normas sociales oficiales a menudo contradicen los comportamientos reales.

En términos de relevancia contemporánea, esta reflexión anticipa los dilemas éticos de las redes sociales, donde la línea entre información, opinión y chisme se ha difuminado. Marge, en su sabiduría doméstica, articula lo que los sociólogos modernos estudian como "vigilancia social distribuida"."""
    },
    {
        "quote": "La ignorancia es una bendición.",
        "character": "Homer Simpson",
        "context": "Reflexión sobre la felicidad en la simplicidad",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Homer+Simpson",
        "analysis": """Homer Simpson articula aquí una de las paradojas más profundas de la filosofía occidental: la relación inversa entre conocimiento y felicidad. Esta reflexión resuena con la tradición filosófica que va desde Sócrates ("solo sé que no sé nada") hasta Nietzsche y su crítica al optimismo del conocimiento.

Desde una perspectiva epistemológica, Homer sugiere que existe un punto de saturación cognitiva donde el conocimiento adicional genera más sufrimiento que beneficio. Esta idea conecta con el concepto budista de "dukkha" - el sufrimiento inherente a la conciencia - y con la filosofía existencialista sobre la "angustia" del conocimiento.

La crítica social implícita es profunda: en una sociedad que venera la información y el conocimiento, Homer propone una contranarrativa donde la simplicidad cognitiva puede ser una estrategia de supervivencia emocional. Su "ignorancia bendita" es una forma de resistencia ante la sobrecarga informacional de la modernidad."""
    },
    {
        "quote": "Soy demasiado joven para morir y demasiado viejo para comer de la mesa de los niños.",
        "character": "Lisa Simpson",
        "context": "Dilema existencial de la adolescencia y el crecimiento",
        "image": "https://via.placeholder.com/300x200/FFD700/2F4F4F?text=Lisa+Simpson",
        "analysis": """Lisa Simpson articula aquí uno de los dilemas existenciales más universales: la experiencia liminal de estar atrapado entre etapas de la vida. Esta reflexión encapsula la filosofía de la "liminalidad" de Victor Turner y la angustia existencial de no pertenecer completamente a ningún estado definido.

Desde una perspectiva filosófica, Lisa expresa la condición humana fundamental de estar siempre "en tránsito", nunca completamente establecida en una identidad fija. Su observación refleja la filosofía heraclitiana del cambio constante y la imposibilidad de "bañarse dos veces en el mismo río".

La crítica social implícita aborda cómo las sociedades modernas han extendido artificialmente los períodos de transición, creando categorías ambiguas como la "adolescencia extendida". Lisa, en su precocidad intelectual, experimenta múltiples liminalities simultáneamente: cronológica, intelectual y social. Su reflexión anticipa los debates contemporáneos sobre la "adultez emergente" y la fluidez de las categorías de edad en la sociedad postmoderna."""
    }
]

def simulate_ai_analysis():
    """Simula el proceso de análisis de IA con loading realista"""
    
    # Crear contenedor de estado
    status_container = st.status("🎭 Generando reflexión filosófica...", expanded=True)
    
    with status_container:
        st.write("⚡ Verificando cache inteligente...")
        time.sleep(0.5)
        
        st.write("🔍 Seleccionando personaje de Springfield...")
        time.sleep(0.7)
        
        st.write("🧠 Generando análisis académico...")
        time.sleep(1.5)
        
        st.write("📚 Aplicando contexto filosófico...")
        time.sleep(0.8)
        
        status_container.update(label="✅ ¡Reflexión filosófica generada!", state="complete")
    
    return True

def main():
    """Aplicación demo principal"""
    
    # Header con badge demo
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🍩 Springfield Insights</h1>
        <h3>Explorando la filosofía de Los Simpsons</h3>
        <span class="demo-badge">VERSIÓN DEMO - FUNCIONA SIN IA</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar estado
    if 'current_quote_index' not in st.session_state:
        st.session_state.current_quote_index = None
    if 'analyses_count' not in st.session_state:
        st.session_state.analyses_count = 0
    
    # Botón principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎲 Obtener Nueva Reflexión Filosófica", use_container_width=True, type="primary"):
            # Simular proceso de IA
            simulate_ai_analysis()
            
            # Seleccionar cita aleatoria
            st.session_state.current_quote_index = random.randint(0, len(DEMO_QUOTES) - 1)
            st.session_state.analyses_count += 1
            
            # Mostrar notificación de éxito
            st.toast("🎭 Nueva reflexión filosófica generada", icon="✨")
            st.rerun()
    
    # Mostrar cita actual
    if st.session_state.current_quote_index is not None:
        quote_data = DEMO_QUOTES[st.session_state.current_quote_index]
        
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
                <div><strong>Contexto:</strong> {quote_data["context"]}</div>
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
            if st.button("🔄 Otra Cita"):
                st.session_state.current_quote_index = random.randint(0, len(DEMO_QUOTES) - 1)
                st.session_state.analyses_count += 1
                st.rerun()
        
        with col2:
            if st.button("📋 Copiar Cita"):
                copy_text = f'"{quote_data["quote"]}" - {quote_data["character"]}'
                st.toast("📋 Cita copiada al portapapeles", icon="✅")
        
        with col3:
            if st.button("💾 Favorito"):
                st.toast("⭐ Añadido a favoritos", icon="💾")
        
        with col4:
            if st.button("🔗 Compartir"):
                st.toast("🔗 Enlace de compartir generado", icon="📤")
    
    else:
        # Mensaje de bienvenida
        st.info("""
        🎭 **¡Bienvenido a Springfield Insights Demo!**
        
        Esta versión funciona **sin necesidad de IA** y muestra análisis filosóficos 
        predefinidos de alta calidad académica.
        
        ✨ **Características de la Demo:**
        - ✅ Frases auténticas de Los Simpsons
        - ✅ Análisis filosóficos rigurosos predefinidos
        - ✅ Funciona instantáneamente (sin APIs)
        - ✅ Imágenes de personajes incluidas
        - ✅ Experiencia completa sin configuración
        
        **Perfecto para demostraciones y presentaciones académicas.**
        """)
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### 📊 Estadísticas")
        st.metric("Frases disponibles", len(DEMO_QUOTES))
        st.metric("Análisis generados", st.session_state.analyses_count)
        
        st.markdown("### 🎯 Acerca de la Demo")
        st.markdown("""
        **Springfield Insights Demo** muestra el concepto completo 
        sin depender de APIs externas.
        
        - **Análisis predefinidos** de alta calidad
        - **Funciona offline** sin configuración
        - **Perfecto para demos** y presentaciones
        - **Experiencia completa** del concepto académico
        """)
        
        st.markdown("### ⚙️ Estado del Sistema")
        st.success("✅ Demo funcionando perfectamente")
        st.info("🎭 Análisis predefinidos cargados")
        st.success("✅ Sin dependencias externas")
        
        st.markdown("### 🚀 Versiones Disponibles")
        st.markdown("""
        - **Demo** (actual): Sin IA, funciona siempre
        - **Simple**: Con IA, requiere OpenAI
        - **Completa**: Todas las características
        """)

if __name__ == "__main__":
    main()