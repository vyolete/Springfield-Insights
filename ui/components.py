"""
Componentes de interfaz de usuario para Springfield Insights
"""
import streamlit as st

class UIComponents:
    """Componentes reutilizables de la interfaz de usuario"""
    
    def apply_custom_css(self):
        """Aplica sistema de diseño unificado de Springfield Insights"""
        from .design_system import SpringfieldDesignSystem
        
        # Importar fuentes de Google
        st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Comic+Neue:wght@400;700&display=swap" rel="stylesheet">
        """, unsafe_allow_html=True)
        
        # Aplicar sistema de diseño organizado y proporcional
        css_content = """
        <style>
        /* ========================================
           🎨 SISTEMA DE DISEÑO SPRINGFIELD INSIGHTS - ORGANIZADO
           ======================================== */
        
        /* Variables CSS del sistema de diseño */
        :root {
            /* Colores principales de Los Simpsons */
            --simpson-primary-yellow: #FFD700;
            --simpson-primary-orange: #FFA500;
            --simpson-primary-red: #FF6347;
            --simpson-secondary-blue: #87CEEB;
            --simpson-secondary-green: #90EE90;
            --simpson-dark-text: #2F4F4F;
            --simpson-light-bg: #FFF8DC;
            --simpson-white-pure: #FFFFFF;
            --simpson-card-bg: #FFFEF7;
            --simpson-sidebar-bg: #F8F6E8;
            
            /* Estados interactivos */
            --simpson-hover-yellow: #FFED4E;
            --simpson-hover-orange: #FF8C00;
            --simpson-active-red: #FF4500;
            --simpson-success: #32CD32;
            --simpson-warning: #FF8C00;
            --simpson-error: #DC143C;
            --simpson-info: #4169E1;
            
            /* Tipografía responsive */
            --font-primary: 'Fredoka One', cursive;
            --font-secondary: 'Comic Neue', cursive;
            --font-size-hero: clamp(2rem, 5vw, 3.5rem);
            --font-size-h1: clamp(1.8rem, 4vw, 2.5rem);
            --font-size-h2: clamp(1.5rem, 3.5vw, 2rem);
            --font-size-h3: clamp(1.2rem, 3vw, 1.5rem);
            --font-size-body: clamp(1rem, 2.5vw, 1.1rem);
            --font-size-small: clamp(0.875rem, 2vw, 0.95rem);
            --font-weight-normal: 400;
            --font-weight-bold: 700;
            --font-line-height-tight: 1.2;
            --font-line-height-normal: 1.5;
            --font-line-height-relaxed: 1.8;
            
            /* Espaciado proporcional */
            --spacing-xs: 0.5rem;
            --spacing-sm: 1rem;
            --spacing-md: 1.5rem;
            --spacing-lg: 2rem;
            --spacing-xl: 3rem;
            --spacing-container-padding: clamp(1rem, 3vw, 2rem);
            --spacing-card-padding: clamp(1.25rem, 2.5vw, 2rem);
            --spacing-button-padding: clamp(0.75rem, 2vw, 1rem) clamp(1.5rem, 3vw, 2rem);
            --spacing-section-margin: clamp(1.5rem, 4vw, 3rem);
            --spacing-element-margin: clamp(0.75rem, 2vw, 1.25rem);
            
            /* Bordes y sombras */
            --border-radius-sm: 8px;
            --border-radius-md: 12px;
            --border-radius-lg: 20px;
            --border-radius-xl: 25px;
            --border-width: 2px;
            --border-width-thick: 4px;
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 15px rgba(0,0,0,0.15);
            --shadow-lg: 0 8px 25px rgba(0,0,0,0.2);
            --shadow-xl: 0 12px 35px rgba(0,0,0,0.25);
            
            /* Transiciones */
            --transition-fast: 0.2s ease;
            --transition-normal: 0.3s ease;
            --transition-slow: 0.5s ease;
            
            /* Z-index */
            --z-background: -1;
            --z-normal: 1;
            --z-elevated: 10;
        }
        
        /* ========================================
           🏗️ LAYOUT Y ESTRUCTURA PRINCIPAL
           ======================================== */
        
        /* Aplicación base con grid proporcional */
        .stApp {
            background: linear-gradient(135deg, var(--simpson-light-bg) 0%, #F0F8FF 100%) !important;
            font-family: var(--font-secondary) !important;
        }
        
        /* Contenedor principal con máximo ancho y centrado */
        .main .block-container {
            max-width: 1200px !important;
            padding: var(--spacing-container-padding) !important;
            margin: 0 auto !important;
        }
        
        /* Grid de columnas balanceado */
        .stColumns {
            gap: var(--spacing-lg) !important;
        }
        
        /* ========================================
           🎨 COMPONENTES PRINCIPALES
           ======================================== */
        
        /* Header principal con identidad Simpsons */
        .simpson-header, .main-header {
            background: linear-gradient(135deg, 
                var(--simpson-primary-yellow) 0%, 
                var(--simpson-primary-orange) 50%, 
                var(--simpson-primary-red) 100%);
            padding: var(--spacing-card-padding);
            border-radius: var(--border-radius-lg);
            border: var(--border-width-thick) solid var(--simpson-primary-red);
            box-shadow: var(--shadow-lg);
            text-align: center;
            margin-bottom: var(--spacing-section-margin);
        }
        
        .simpson-header h1, .main-header h1 {
            font-family: var(--font-primary);
            font-size: var(--font-size-hero);
            color: var(--simpson-dark-text);
            text-shadow: 2px 2px 4px rgba(47, 79, 79, 0.3);
            margin: 0;
        }
        
        .simpson-header h3, .main-header h3 {
            font-family: var(--font-secondary);
            font-size: var(--font-size-h3);
            color: var(--simpson-dark-text);
            font-weight: var(--font-weight-bold);
            margin: var(--spacing-sm) 0 0 0;
        }
        
        /* Tarjeta de cita con proporción controlada */
        .quote-container {
            background: linear-gradient(135deg, 
                var(--simpson-primary-yellow) 0%, 
                var(--simpson-primary-orange) 100%);
            border: var(--border-width-thick) solid var(--simpson-primary-red);
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-card-padding);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
            min-height: 120px;
            max-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: var(--spacing-element-margin) 0;
        }
        
        .quote-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(180deg); }
        }
        
        /* Texto de la cita con legibilidad garantizada */
        .quote-text-main {
            font-family: var(--font-secondary);
            font-size: var(--font-size-h2);
            font-weight: var(--font-weight-bold);
            color: var(--simpson-dark-text);
            text-align: center;
            line-height: var(--font-line-height-tight);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            position: relative;
            z-index: var(--z-normal);
            word-wrap: break-word;
            max-width: 100%;
            padding: var(--spacing-sm);
        }
        
        /* Análisis filosófico con scroll controlado */
        .analysis-container {
            background: linear-gradient(135deg, #E6F3FF 0%, #F0F8FF 100%);
            border: var(--border-width-thick) solid var(--simpson-info);
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-card-padding);
            box-shadow: var(--shadow-md);
            margin: var(--spacing-section-margin) 0;
            max-height: 600px;
            overflow-y: auto;
        }
        
        .analysis-header {
            font-family: var(--font-primary);
            font-size: var(--font-size-h2);
            color: var(--simpson-info);
            text-align: center;
            margin-bottom: var(--spacing-md);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            position: sticky;
            top: 0;
            background: inherit;
            z-index: var(--z-elevated);
        }
        
        /* Contexto filosófico */
        .context-container {
            background: rgba(255,255,255,0.95);
            border: var(--border-width) solid var(--simpson-primary-red);
            border-radius: var(--border-radius-md);
            padding: var(--spacing-md);
            margin-top: var(--spacing-md);
            box-shadow: var(--shadow-sm);
        }
        
        .context-header {
            font-family: var(--font-primary);
            color: var(--simpson-primary-red);
            font-size: var(--font-size-h3);
            margin-bottom: var(--spacing-sm);
            text-align: center;
        }
        
        .context-content {
            font-family: var(--font-secondary);
            color: var(--simpson-dark-text);
            line-height: var(--font-line-height-relaxed);
            font-size: var(--font-size-body);
            text-align: justify;
        }
        
        /* ========================================
           🎛️ BOTONES Y CONTROLES
           ======================================== */
        
        /* Botones principales con jerarquía clara */
        .stButton > button {
            font-family: var(--font-secondary) !important;
            font-weight: var(--font-weight-bold) !important;
            font-size: var(--font-size-body) !important;
            padding: var(--spacing-button-padding) !important;
            border: var(--border-width) solid var(--simpson-primary-red) !important;
            border-radius: var(--border-radius-xl) !important;
            background: linear-gradient(135deg, 
                var(--simpson-primary-yellow) 0%, 
                var(--simpson-primary-orange) 100%) !important;
            color: var(--simpson-dark-text) !important;
            transition: var(--transition-normal) !important;
            box-shadow: var(--shadow-sm) !important;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5) !important;
            min-width: 120px !important;
            margin: var(--spacing-xs) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: var(--shadow-md) !important;
            border-color: var(--simpson-hover-orange) !important;
            background: linear-gradient(135deg, 
                var(--simpson-hover-yellow) 0%, 
                var(--simpson-hover-orange) 100%) !important;
        }
        
        /* Botón principal destacado */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, 
                var(--simpson-primary-red) 0%, 
                var(--simpson-active-red) 100%) !important;
            color: var(--simpson-white-pure) !important;
            border-color: #8B0000 !important;
            font-size: var(--font-size-h3) !important;
            padding: calc(var(--spacing-sm) * 1.2) var(--spacing-lg) !important;
            min-width: 300px !important;
            margin: var(--spacing-lg) auto !important;
            display: block !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, 
                var(--simpson-active-red) 0%, 
                var(--simpson-primary-red) 100%) !important;
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: var(--shadow-xl) !important;
        }
        
        /* ========================================
           📱 SIDEBAR ORGANIZADO
           ======================================== */
        
        /* Sidebar con contraste mejorado */
        .css-1d391kg, .css-1cypcdb, .stSidebar > div {
            background: linear-gradient(180deg, #F8F6E8 0%, #F0E68C 100%) !important;
            border-right: var(--border-width-thick) solid var(--simpson-primary-orange) !important;
            width: 300px !important;
            min-width: 280px !important;
        }
        
        /* Cards del sidebar visibles y organizadas */
        .css-1d391kg .stMarkdown, 
        .stSidebar .stMarkdown {
            background: rgba(255, 254, 247, 0.95) !important;
            border: var(--border-width) solid var(--simpson-primary-yellow) !important;
            border-radius: var(--border-radius-md) !important;
            padding: var(--spacing-md) !important;
            margin: var(--spacing-sm) 0 !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        /* ========================================
           🖼️ IMÁGENES PROPORCIONALES
           ======================================== */
        
        /* Imágenes de personajes con tamaño controlado */
        .stImage > img {
            border-radius: var(--border-radius-lg) !important;
            border: var(--border-width-thick) solid var(--simpson-primary-yellow) !important;
            box-shadow: var(--shadow-md) !important;
            transition: var(--transition-normal) !important;
            max-width: 100% !important;
            max-height: 300px !important;
            object-fit: cover !important;
        }
        
        .stImage > img:hover {
            transform: scale(1.02) !important;
            border-color: var(--simpson-primary-red) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        /* ========================================
           📊 MÉTRICAS Y CONTENEDORES
           ======================================== */
        
        /* Métricas uniformes */
        .stMetric {
            background: var(--simpson-white-pure) !important;
            border: var(--border-width) solid var(--simpson-primary-yellow) !important;
            border-radius: var(--border-radius-md) !important;
            padding: var(--spacing-md) !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition-normal) !important;
            text-align: center !important;
        }
        
        .stMetric:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        /* Contenedores personalizados con altura uniforme */
        .metric-container {
            background: linear-gradient(135deg, 
                var(--simpson-white-pure) 0%, 
                var(--simpson-light-bg) 100%) !important;
            border: var(--border-width) solid var(--simpson-primary-yellow) !important;
            border-radius: var(--border-radius-md) !important;
            padding: var(--spacing-md) !important;
            box-shadow: var(--shadow-sm) !important;
            margin: var(--spacing-sm) 0 !important;
            transition: var(--transition-normal) !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            text-align: center !important;
        }
        
        .metric-container:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        /* ========================================
           📝 TIPOGRAFÍA Y TEXTO
           ======================================== */
        
        /* Texto base de Streamlit */
        .stMarkdown {
            font-family: var(--font-secondary) !important;
            color: var(--simpson-dark-text) !important;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: var(--font-primary) !important;
            color: var(--simpson-primary-red) !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        }
        
        /* ========================================
           🎨 SCROLLBAR PERSONALIZADA
           ======================================== */
        
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--simpson-light-bg);
            border-radius: var(--border-radius-sm);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, 
                var(--simpson-primary-yellow), 
                var(--simpson-primary-orange));
            border-radius: var(--border-radius-sm);
            border: 2px solid var(--simpson-light-bg);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, 
                var(--simpson-primary-orange), 
                var(--simpson-primary-red));
        }
        
        /* ========================================
           ✨ ANIMACIONES Y EFECTOS
           ======================================== */
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-bounce {
            animation: bounce 2s infinite;
        }
        
        .animate-fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        .hover-lift:hover {
            transform: translateY(-4px);
            transition: var(--transition-normal);
        }
        
        /* ========================================
           🔧 UTILIDADES Y HELPERS
           ======================================== */
        
        /* Utilidades de texto */
        .text-center { text-align: center !important; }
        .text-left { text-align: left !important; }
        .text-right { text-align: right !important; }
        .text-justify { text-align: justify !important; }
        .font-bold { font-weight: var(--font-weight-bold) !important; }
        .text-primary { color: var(--simpson-primary-red) !important; }
        .text-secondary { color: var(--simpson-info) !important; }
        
        /* ========================================
           📱 DISEÑO RESPONSIVE ORGANIZADO
           ======================================== */
        
        /* Móviles (hasta 480px) */
        @media (max-width: 480px) {
            .main .block-container {
                padding: var(--spacing-md) var(--spacing-sm) !important;
            }
            
            .simpson-header, .main-header {
                padding: var(--spacing-md) !important;
                margin-bottom: var(--spacing-lg) !important;
            }
            
            .quote-container {
                padding: var(--spacing-md) !important;
                min-height: 100px !important;
                max-height: 150px !important;
            }
            
            .analysis-container {
                padding: var(--spacing-md) !important;
                margin: var(--spacing-lg) 0 !important;
                max-height: 400px !important;
            }
            
            .metric-container {
                margin: var(--spacing-sm) 0 !important;
                min-height: 100px !important;
            }
            
            .stButton > button[kind="primary"] {
                font-size: 1.2rem !important;
                padding: 16px 30px !important;
                min-width: 280px !important;
            }
            
            .stImage > img {
                max-height: 200px !important;
            }
            
            .css-1d391kg, .css-1cypcdb, .stSidebar > div {
                width: 280px !important;
                min-width: 260px !important;
            }
        }
        
        /* Tablets (481px - 768px) */
        @media (min-width: 481px) and (max-width: 768px) {
            .main .block-container {
                padding: var(--spacing-lg) var(--spacing-md) !important;
            }
            
            .quote-container {
                min-height: 130px !important;
                max-height: 180px !important;
            }
            
            .analysis-container {
                max-height: 500px !important;
            }
            
            .stImage > img {
                max-height: 250px !important;
            }
        }
        
        /* Desktop (769px+) */
        @media (min-width: 769px) {
            .main .block-container {
                padding: var(--spacing-xl) var(--spacing-lg) !important;
            }
            
            .simpson-header, .main-header {
                padding: var(--spacing-xl) !important;
            }
            
            .quote-container {
                padding: var(--spacing-xl) !important;
                min-height: 140px !important;
                max-height: 200px !important;
            }
            
            .analysis-container {
                padding: var(--spacing-xl) !important;
                margin: var(--spacing-xl) 0 !important;
                max-height: 600px !important;
            }
            
            .stColumns {
                gap: var(--spacing-lg) !important;
            }
            
            .stImage > img {
                max-height: 300px !important;
            }
            
            .css-1d391kg, .css-1cypcdb, .stSidebar > div {
                width: 320px !important;
                min-width: 300px !important;
            }
        }
        
        /* ========================================
           🎯 CORRECCIONES FINALES DE LAYOUT
           ======================================== */
        
        /* Asegurar que las columnas no se deformen */
        .stColumns > div {
            min-width: 0 !important;
            flex: 1 !important;
        }
        
        /* Evitar overflow horizontal */
        .stApp, .main, .block-container {
            overflow-x: hidden !important;
        }
        
        /* Centrar botones de acción */
        .stButton {
            display: flex !important;
            justify-content: center !important;
        }
        
        /* Mejorar legibilidad en análisis */
        .analysis-content-container .stMarkdown p {
            margin-bottom: var(--spacing-sm) !important;
            line-height: var(--font-line-height-relaxed) !important;
        }
        
        .analysis-content-container .stMarkdown h4 {
            margin-top: var(--spacing-md) !important;
            margin-bottom: var(--spacing-sm) !important;
            color: var(--simpson-info) !important;
        }
        </style>
        """
        
        st.markdown(css_content, unsafe_allow_html=True)
    
    def render_header(self):
        """Renderiza el header principal usando sistema de diseño unificado"""
        st.markdown("""
        <div class="simpson-header animate-fade-in">
            <h1>🍩 Springfield Insights</h1>
            <h3>Explorando la filosofía de Los Simpsons</h3>
        </div>
        """, unsafe_allow_html=True)
    
    def render_character_image(self, quote_data):
        """
        Renderiza la imagen del personaje con proporciones controladas y optimización CDN
        """
        character_name = quote_data.get("character", "Personaje Desconocido")
        image_url = quote_data.get("image", "")
        
        # Información adicional del personaje si está disponible
        character_info = quote_data.get("character_info", {})
        
        # Contenedor con proporción controlada
        st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; 
                   max-height: 300px; overflow: hidden; border-radius: 20px; 
                   border: 4px solid var(--simpson-primary-yellow); 
                   box-shadow: var(--shadow-md); margin-bottom: 20px;'>
        """, unsafe_allow_html=True)
        
        try:
            # Usar imagen optimizada del CDN con tamaño controlado
            st.image(
                image_url, 
                caption=self._build_image_caption(character_name, character_info),
                use_column_width=True
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
                use_column_width=True
            )
            st.caption("⚠️ Usando imagen placeholder")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
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
        """Renderiza la tarjeta de la cita usando componentes nativos de Streamlit con estilos CSS"""
        
        # Obtener información adicional si está disponible
        character_info = quote_data.get("character_info", {})
        source_info = "🌐 API Oficial" if quote_data.get("source") == "api" else "📚 Base Local"
        
        # Obtener datos de forma segura
        quote_text = quote_data.get("quote", "Cita no disponible")
        character_name = quote_data.get("character", "Personaje Desconocido")
        context_text = quote_data.get("context", "Contexto no disponible")
        
        # Header con personaje y fuente
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🎭 {character_name}")
        with col2:
            st.caption(source_info)
        
        # Cuadro principal de la cita usando sistema unificado con texto garantizado
        st.markdown(f"""
        <div class="quote-container animate-fade-in">
            <div class="quote-text-main">"{quote_text}"</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contexto filosófico usando clases del sistema
        st.markdown(f"""
        <div class="context-container animate-fade-in">
            <div class="context-header">💭 Contexto Filosófico</div>
            <div class="context-content">{context_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Información adicional del personaje si está disponible
        if character_info:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <div style='font-family: "Fredoka One", cursive; color: var(--simpson-blue); 
                           font-size: 20px; margin-bottom: 15px; text-align: center;'>
                    ℹ️ Información del Personaje
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear métricas con estilo personalizado
            info_cols = st.columns(3)
            
            if character_info.get('occupation') and character_info['occupation'] != 'Unknown':
                with info_cols[0]:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style='text-align: center;'>
                            <div style='font-size: 24px; margin-bottom: 5px;'>👔</div>
                            <div style='font-family: "Comic Neue", cursive; font-weight: 700; 
                                       color: var(--simpson-dark); font-size: 14px;'>Ocupación</div>
                            <div style='font-family: "Fredoka One", cursive; color: var(--simpson-red); 
                                       font-size: 16px; margin-top: 5px;'>{character_info['occupation']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if character_info.get('age'):
                with info_cols[1]:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style='text-align: center;'>
                            <div style='font-size: 24px; margin-bottom: 5px;'>🎂</div>
                            <div style='font-family: "Comic Neue", cursive; font-weight: 700; 
                                       color: var(--simpson-dark); font-size: 14px;'>Edad</div>
                            <div style='font-family: "Fredoka One", cursive; color: var(--simpson-red); 
                                       font-size: 16px; margin-top: 5px;'>{character_info['age']} años</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if character_info.get('status') and character_info['status'] != 'Unknown':
                with info_cols[2]:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style='text-align: center;'>
                            <div style='font-size: 24px; margin-bottom: 5px;'>📊</div>
                            <div style='font-family: "Comic Neue", cursive; font-weight: 700; 
                                       color: var(--simpson-dark); font-size: 14px;'>Estado</div>
                            <div style='font-family: "Fredoka One", cursive; color: var(--simpson-red); 
                                       font-size: 16px; margin-top: 5px;'>{character_info['status']}</div>
                        </div>
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
        """Renderiza la sección de análisis GPT-4 usando componentes nativos de Streamlit"""
        
        if analysis:
            # Limpiar el análisis
            clean_analysis = str(analysis).strip()
            
            # Crear contenedor con estilo Simpsons usando CSS personalizado
            st.markdown("""
            <div class="analysis-container">
                <div class="analysis-header">
                    🧠 Análisis Filosófico Generado por GPT-4
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Usar contenedor nativo de Streamlit con estilo personalizado
            with st.container():
                # Aplicar estilo al contenedor
                st.markdown("""
                <style>
                .analysis-content-container {
                    background: rgba(255,255,255,0.95) !important;
                    padding: 25px !important;
                    border-radius: 15px !important;
                    border: 2px solid #4169E1 !important;
                    box-shadow: 0 4px 15px rgba(65, 105, 225, 0.2) !important;
                    margin: 20px 0 !important;
                }
                .analysis-content-container .stMarkdown {
                    font-family: "Comic Neue", sans-serif !important;
                    font-size: 16px !important;
                    line-height: 1.8 !important;
                    color: #1a1a1a !important;
                    text-align: justify !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Dividir en párrafos y renderizar cada uno con Streamlit nativo
                paragraphs = clean_analysis.split('\n\n')
                
                for paragraph in paragraphs:
                    if paragraph.strip():
                        # Detectar títulos (terminan con :)
                        if paragraph.strip().endswith(':') and len(paragraph.strip()) < 100:
                            st.markdown(f"#### {paragraph.strip()}")
                        else:
                            # Párrafo normal
                            st.write(paragraph.strip())
            
            # Footer del análisis
            st.markdown("""
            <div style='text-align: center; margin-top: 20px; padding: 15px; 
                       background: rgba(65, 105, 225, 0.1); border-radius: 10px;'>
                <div style='font-family: "Comic Neue", cursive; font-size: 14px; 
                           color: #4169E1; font-style: italic;'>
                    💡 Análisis generado automáticamente por inteligencia artificial
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Mensaje de error usando componente nativo
            st.error("⚠️ No se pudo generar el análisis filosófico")
            st.info("💡 Intenta obtener una nueva cita para generar un análisis")
    
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