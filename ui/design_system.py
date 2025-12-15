"""
Sistema de Diseño UI/UX para Springfield Insights
Guía de estilos unificada inspirada en Los Simpsons
"""

class SpringfieldDesignSystem:
    """Sistema de diseño unificado para Springfield Insights"""
    
    # ========================================
    # 🎨 PALETA DE COLORES OFICIAL
    # ========================================
    COLORS = {
        # Colores primarios Simpson
        'primary_yellow': '#FFD700',      # Amarillo Simpson principal
        'primary_orange': '#FFA500',      # Naranja Simpson
        'primary_red': '#FF6347',         # Rojo Simpson suave
        
        # Colores secundarios
        'secondary_blue': '#87CEEB',      # Azul cielo Simpson
        'secondary_green': '#90EE90',     # Verde claro
        'secondary_purple': '#DDA0DD',    # Púrpura suave
        
        # Colores neutros
        'dark_text': '#2F4F4F',          # Texto principal oscuro
        'light_bg': '#FFF8DC',           # Fondo claro crema
        'white_pure': '#FFFFFF',         # Blanco puro
        'shadow_light': 'rgba(0,0,0,0.1)', # Sombra suave
        'shadow_medium': 'rgba(0,0,0,0.2)', # Sombra media
        'shadow_strong': 'rgba(0,0,0,0.3)', # Sombra fuerte
        
        # Estados interactivos
        'hover_yellow': '#FFED4E',       # Amarillo hover
        'hover_orange': '#FF8C00',       # Naranja hover
        'active_red': '#FF4500',         # Rojo activo
        
        # Colores funcionales
        'success': '#32CD32',            # Verde éxito
        'warning': '#FF8C00',            # Naranja advertencia
        'error': '#DC143C',              # Rojo error
        'info': '#4169E1'                # Azul información
    }
    
    # ========================================
    # 📝 TIPOGRAFÍA UNIFICADA
    # ========================================
    TYPOGRAPHY = {
        # Fuentes principales
        'font_primary': "'Fredoka One', cursive",      # Títulos principales
        'font_secondary': "'Comic Neue', cursive",     # Texto general
        'font_fallback': "Arial, sans-serif",          # Fallback
        
        # Tamaños de fuente (responsive con clamp)
        'size_hero': 'clamp(2rem, 5vw, 3.5rem)',      # Título principal
        'size_h1': 'clamp(1.8rem, 4vw, 2.5rem)',      # H1
        'size_h2': 'clamp(1.5rem, 3.5vw, 2rem)',      # H2
        'size_h3': 'clamp(1.2rem, 3vw, 1.5rem)',      # H3
        'size_body': 'clamp(1rem, 2.5vw, 1.1rem)',    # Texto normal
        'size_small': 'clamp(0.875rem, 2vw, 0.95rem)', # Texto pequeño
        'size_caption': 'clamp(0.75rem, 1.8vw, 0.85rem)', # Captions
        
        # Pesos de fuente
        'weight_normal': '400',
        'weight_bold': '700',
        
        # Alturas de línea
        'line_height_tight': '1.2',
        'line_height_normal': '1.5',
        'line_height_relaxed': '1.8'
    }
    
    # ========================================
    # 📐 ESPACIADO Y GRID SYSTEM
    # ========================================
    SPACING = {
        # Espaciado base (8px system)
        'xs': '0.5rem',    # 8px
        'sm': '1rem',      # 16px
        'md': '1.5rem',    # 24px
        'lg': '2rem',      # 32px
        'xl': '3rem',      # 48px
        'xxl': '4rem',     # 64px
        
        # Espaciado específico
        'container_padding': 'clamp(1rem, 3vw, 2rem)',
        'card_padding': 'clamp(1.25rem, 2.5vw, 2rem)',
        'button_padding': 'clamp(0.75rem, 2vw, 1rem) clamp(1.5rem, 3vw, 2rem)',
        
        # Márgenes
        'section_margin': 'clamp(1.5rem, 4vw, 3rem)',
        'element_margin': 'clamp(0.75rem, 2vw, 1.25rem)'
    }
    
    # ========================================
    # 🎯 COMPONENTES VISUALES
    # ========================================
    COMPONENTS = {
        # Bordes redondeados
        'border_radius_sm': '8px',
        'border_radius_md': '12px',
        'border_radius_lg': '20px',
        'border_radius_xl': '25px',
        
        # Bordes
        'border_width': '2px',
        'border_width_thick': '4px',
        
        # Sombras
        'shadow_sm': '0 2px 8px rgba(0,0,0,0.1)',
        'shadow_md': '0 4px 15px rgba(0,0,0,0.15)',
        'shadow_lg': '0 8px 25px rgba(0,0,0,0.2)',
        'shadow_xl': '0 12px 35px rgba(0,0,0,0.25)',
        
        # Transiciones
        'transition_fast': '0.2s ease',
        'transition_normal': '0.3s ease',
        'transition_slow': '0.5s ease',
        
        # Z-index layers
        'z_background': '-1',
        'z_normal': '1',
        'z_elevated': '10',
        'z_modal': '100',
        'z_tooltip': '1000'
    }
    
    # ========================================
    # 📱 BREAKPOINTS RESPONSIVE
    # ========================================
    BREAKPOINTS = {
        'mobile': '480px',
        'tablet': '768px',
        'desktop': '1024px',
        'wide': '1200px'
    }
    
    @classmethod
    def get_css_variables(cls):
        """Genera variables CSS para todo el sistema de diseño"""
        css_vars = ":root {\n"
        
        # Colores
        for name, value in cls.COLORS.items():
            css_vars += f"    --simpson-{name.replace('_', '-')}: {value};\n"
        
        # Tipografía
        for name, value in cls.TYPOGRAPHY.items():
            css_vars += f"    --font-{name.replace('_', '-')}: {value};\n"
        
        # Espaciado
        for name, value in cls.SPACING.items():
            css_vars += f"    --spacing-{name.replace('_', '-')}: {value};\n"
        
        # Componentes
        for name, value in cls.COMPONENTS.items():
            css_vars += f"    --{name.replace('_', '-')}: {value};\n"
        
        css_vars += "}\n"
        return css_vars
    
    @classmethod
    def get_base_styles(cls):
        """Estilos base para toda la aplicación"""
        return f"""
        /* Reset y estilos base */
        * {{
            box-sizing: border-box;
        }}
        
        /* Fondo principal de la aplicación */
        .stApp {{
            background: linear-gradient(135deg, var(--simpson-light-bg) 0%, #F0F8FF 100%);
            font-family: var(--font-secondary);
            color: var(--simpson-dark-text);
            line-height: var(--font-line-height-normal);
        }}
        
        /* Contenedor principal responsive */
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--spacing-container-padding);
        }}
        
        /* Grid system responsive */
        .grid {{
            display: grid;
            gap: var(--spacing-md);
        }}
        
        .grid-2 {{ grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }}
        .grid-3 {{ grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }}
        .grid-4 {{ grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }}
        
        /* Flexbox utilities */
        .flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .flex-center {{ justify-content: center; align-items: center; }}
        .flex-between {{ justify-content: space-between; align-items: center; }}
        .flex-wrap {{ flex-wrap: wrap; }}
        
        /* Spacing utilities */
        .gap-sm {{ gap: var(--spacing-sm); }}
        .gap-md {{ gap: var(--spacing-md); }}
        .gap-lg {{ gap: var(--spacing-lg); }}
        
        .p-sm {{ padding: var(--spacing-sm); }}
        .p-md {{ padding: var(--spacing-md); }}
        .p-lg {{ padding: var(--spacing-lg); }}
        
        .m-sm {{ margin: var(--spacing-sm); }}
        .m-md {{ margin: var(--spacing-md); }}
        .m-lg {{ margin: var(--spacing-lg); }}
        """
    
    @classmethod
    def get_component_styles(cls):
        """Estilos para componentes específicos"""
        return """
        /* ========================================
           🎨 COMPONENTES PRINCIPALES
           ======================================== */
        
        /* Header principal */
        .simpson-header {
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
        
        .simpson-header h1 {
            font-family: var(--font-primary);
            font-size: var(--font-size-hero);
            color: var(--simpson-dark-text);
            text-shadow: 2px 2px 4px var(--simpson-shadow-strong);
            margin: 0;
        }
        
        .simpson-header h3 {
            font-family: var(--font-secondary);
            font-size: var(--font-size-h3);
            color: var(--simpson-dark-text);
            font-weight: var(--font-weight-bold);
            margin: var(--spacing-sm) 0 0 0;
        }
        
        /* Tarjetas de contenido */
        .simpson-card {
            background: var(--simpson-white-pure);
            border: var(--border-width) solid var(--simpson-primary-yellow);
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-card-padding);
            box-shadow: var(--shadow-md);
            transition: var(--transition-normal);
            margin: var(--spacing-element-margin) 0;
        }
        
        .simpson-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: var(--simpson-primary-orange);
        }
        
        /* Tarjeta de cita principal */
        .quote-card {
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
            display: flex;
            align-items: center;
            justify-content: center;
            margin: var(--spacing-element-margin) 0;
        }
        
        .quote-text {
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
        }
        
        /* Botones Simpson */
        .simpson-button {
            font-family: var(--font-secondary);
            font-weight: var(--font-weight-bold);
            font-size: var(--font-size-body);
            padding: var(--spacing-button-padding);
            border: var(--border-width) solid var(--simpson-primary-red);
            border-radius: var(--border-radius-xl);
            background: linear-gradient(135deg, 
                var(--simpson-primary-yellow) 0%, 
                var(--simpson-primary-orange) 100%);
            color: var(--simpson-dark-text);
            cursor: pointer;
            transition: var(--transition-normal);
            box-shadow: var(--shadow-sm);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
            text-decoration: none;
            display: inline-block;
        }
        
        .simpson-button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: var(--shadow-md);
            border-color: var(--simpson-hover-orange);
            background: linear-gradient(135deg, 
                var(--simpson-hover-yellow) 0%, 
                var(--simpson-hover-orange) 100%);
        }
        
        .simpson-button:active {
            transform: translateY(0) scale(0.98);
        }
        
        /* Botón primario */
        .simpson-button-primary {
            background: linear-gradient(135deg, 
                var(--simpson-primary-red) 0%, 
                var(--simpson-active-red) 100%);
            color: var(--simpson-white-pure);
            border-color: #8B0000;
            font-size: var(--font-size-h3);
            padding: calc(var(--spacing-sm) * 1.2) var(--spacing-lg);
        }
        
        .simpson-button-primary:hover {
            background: linear-gradient(135deg, 
                var(--simpson-active-red) 0%, 
                var(--simpson-primary-red) 100%);
            transform: translateY(-3px) scale(1.05);
        }
        
        /* Métricas y estadísticas */
        .simpson-metric {
            background: linear-gradient(135deg, 
                var(--simpson-white-pure) 0%, 
                var(--simpson-light-bg) 100%);
            border: var(--border-width) solid var(--simpson-primary-yellow);
            border-radius: var(--border-radius-md);
            padding: var(--spacing-md);
            text-align: center;
            box-shadow: var(--shadow-sm);
            transition: var(--transition-normal);
        }
        
        .simpson-metric:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .simpson-metric-icon {
            font-size: var(--font-size-h2);
            margin-bottom: var(--spacing-xs);
        }
        
        .simpson-metric-label {
            font-family: var(--font-secondary);
            font-weight: var(--font-weight-bold);
            font-size: var(--font-size-small);
            color: var(--simpson-dark-text);
            margin-bottom: var(--spacing-xs);
        }
        
        .simpson-metric-value {
            font-family: var(--font-primary);
            font-size: var(--font-size-h3);
            color: var(--simpson-primary-red);
        }
        
        /* Análisis filosófico */
        .analysis-container {
            background: linear-gradient(135deg, 
                var(--simpson-secondary-blue) 0%, 
                #E6F3FF 100%);
            border: var(--border-width) solid var(--simpson-info);
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-card-padding);
            box-shadow: var(--shadow-md);
            margin: var(--spacing-section-margin) 0;
        }
        
        .analysis-header {
            font-family: var(--font-primary);
            font-size: var(--font-size-h2);
            color: var(--simpson-info);
            text-align: center;
            margin-bottom: var(--spacing-md);
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        
        .analysis-content {
            font-family: var(--font-secondary);
            font-size: var(--font-size-body);
            line-height: var(--font-line-height-relaxed);
            color: var(--simpson-dark-text);
            text-align: justify;
        }
        
        /* Estados de mensaje */
        .simpson-success {
            background: linear-gradient(135deg, 
                var(--simpson-secondary-green) 0%, 
                #F0FFF0 100%);
            border-color: var(--simpson-success);
        }
        
        .simpson-warning {
            background: linear-gradient(135deg, 
                var(--simpson-primary-orange) 0%, 
                var(--simpson-light-bg) 100%);
            border-color: var(--simpson-warning);
        }
        
        .simpson-error {
            background: linear-gradient(135deg, 
                #FFE4E1 0%, 
                #FFF0F0 100%);
            border-color: var(--simpson-error);
        }
        
        .simpson-info {
            background: linear-gradient(135deg, 
                var(--simpson-secondary-blue) 0%, 
                #F0F8FF 100%);
            border-color: var(--simpson-info);
        }
        """
    
    @classmethod
    def get_responsive_styles(cls):
        """Estilos responsive para todos los dispositivos"""
        return f"""
        /* ========================================
           📱 RESPONSIVE DESIGN
           ======================================== */
        
        /* Mobile First - Base styles */
        @media (max-width: {cls.BREAKPOINTS['mobile']}) {{
            .simpson-header {{
                padding: var(--spacing-md);
                margin-bottom: var(--spacing-lg);
            }}
            
            .simpson-header h1 {{
                font-size: var(--font-size-h1);
            }}
            
            .quote-card {{
                padding: var(--spacing-md);
                min-height: 100px;
            }}
            
            .quote-text {{
                font-size: var(--font-size-h3);
            }}
            
            .simpson-button {{
                padding: var(--spacing-sm) var(--spacing-md);
                font-size: var(--font-size-small);
            }}
            
            .simpson-button-primary {{
                font-size: var(--font-size-body);
                padding: var(--spacing-sm) var(--spacing-lg);
            }}
            
            .grid-2, .grid-3, .grid-4 {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Tablet */
        @media (min-width: {cls.BREAKPOINTS['mobile']}) and (max-width: {cls.BREAKPOINTS['tablet']}) {{
            .grid-3, .grid-4 {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        /* Desktop */
        @media (min-width: {cls.BREAKPOINTS['tablet']}) {{
            .simpson-header {{
                padding: var(--spacing-xl);
            }}
            
            .quote-card {{
                padding: var(--spacing-xl);
                min-height: 140px;
            }}
            
            .analysis-container {{
                padding: var(--spacing-xl);
            }}
        }}
        
        /* Wide screens */
        @media (min-width: {cls.BREAKPOINTS['wide']}) {{
            .main-container {{
                max-width: 1400px;
            }}
        }}
        
        /* Landscape orientation adjustments */
        @media (orientation: landscape) and (max-height: 600px) {{
            .simpson-header {{
                padding: var(--spacing-md);
                margin-bottom: var(--spacing-md);
            }}
            
            .simpson-header h1 {{
                font-size: var(--font-size-h2);
            }}
        }}
        
        /* High DPI displays */
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
            .simpson-header h1,
            .quote-text,
            .analysis-header {{
                text-shadow: 1px 1px 2px var(--simpson-shadow-medium);
            }}
        }}
        
        /* Reduced motion preferences */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Dark mode support (future enhancement) */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --simpson-dark-text: #E0E0E0;
                --simpson-light-bg: #2F2F2F;
                --simpson-white-pure: #1E1E1E;
            }}
        }}
        """
    
    @classmethod
    def get_utility_styles(cls):
        """Clases de utilidad para uso común"""
        return """
        /* ========================================
           🛠️ UTILITY CLASSES
           ======================================== */
        
        /* Visibility */
        .hidden { display: none !important; }
        .visible { display: block !important; }
        
        /* Text alignment */
        .text-left { text-align: left !important; }
        .text-center { text-align: center !important; }
        .text-right { text-align: right !important; }
        .text-justify { text-align: justify !important; }
        
        /* Font weights */
        .font-normal { font-weight: var(--font-weight-normal) !important; }
        .font-bold { font-weight: var(--font-weight-bold) !important; }
        
        /* Colors */
        .text-primary { color: var(--simpson-primary-red) !important; }
        .text-secondary { color: var(--simpson-info) !important; }
        .text-success { color: var(--simpson-success) !important; }
        .text-warning { color: var(--simpson-warning) !important; }
        .text-error { color: var(--simpson-error) !important; }
        
        /* Background colors */
        .bg-primary { background-color: var(--simpson-primary-yellow) !important; }
        .bg-secondary { background-color: var(--simpson-secondary-blue) !important; }
        .bg-white { background-color: var(--simpson-white-pure) !important; }
        
        /* Borders */
        .border-none { border: none !important; }
        .border-primary { border-color: var(--simpson-primary-red) !important; }
        .border-secondary { border-color: var(--simpson-primary-yellow) !important; }
        
        /* Shadows */
        .shadow-none { box-shadow: none !important; }
        .shadow-sm { box-shadow: var(--shadow-sm) !important; }
        .shadow-md { box-shadow: var(--shadow-md) !important; }
        .shadow-lg { box-shadow: var(--shadow-lg) !important; }
        
        /* Border radius */
        .rounded-none { border-radius: 0 !important; }
        .rounded-sm { border-radius: var(--border-radius-sm) !important; }
        .rounded-md { border-radius: var(--border-radius-md) !important; }
        .rounded-lg { border-radius: var(--border-radius-lg) !important; }
        .rounded-full { border-radius: 50% !important; }
        
        /* Overflow */
        .overflow-hidden { overflow: hidden !important; }
        .overflow-auto { overflow: auto !important; }
        
        /* Position */
        .relative { position: relative !important; }
        .absolute { position: absolute !important; }
        .fixed { position: fixed !important; }
        
        /* Z-index */
        .z-background { z-index: var(--z-background) !important; }
        .z-normal { z-index: var(--z-normal) !important; }
        .z-elevated { z-index: var(--z-elevated) !important; }
        
        /* Cursor */
        .cursor-pointer { cursor: pointer !important; }
        .cursor-default { cursor: default !important; }
        
        /* User select */
        .select-none { user-select: none !important; }
        .select-text { user-select: text !important; }
        
        /* Animations */
        .animate-bounce {
            animation: bounce 2s infinite;
        }
        
        .animate-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Hover effects */
        .hover-lift:hover {
            transform: translateY(-4px);
            transition: var(--transition-normal);
        }
        
        .hover-scale:hover {
            transform: scale(1.05);
            transition: var(--transition-normal);
        }
        
        .hover-glow:hover {
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            transition: var(--transition-normal);
        }
        """