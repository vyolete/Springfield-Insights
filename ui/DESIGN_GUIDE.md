# 🎨 Guía de Estilos UI/UX - Springfield Insights

## 📋 Índice
1. [Paleta de Colores](#paleta-de-colores)
2. [Tipografía](#tipografía)
3. [Espaciado y Grid](#espaciado-y-grid)
4. [Componentes](#componentes)
5. [Responsive Design](#responsive-design)
6. [Mejores Prácticas](#mejores-prácticas)

---

## 🎨 Paleta de Colores

### Colores Primarios Simpson
```css
--simpson-primary-yellow: #FFD700    /* Amarillo Simpson principal */
--simpson-primary-orange: #FFA500    /* Naranja Simpson */
--simpson-primary-red: #FF6347       /* Rojo Simpson suave */
```

### Colores Secundarios
```css
--simpson-secondary-blue: #87CEEB    /* Azul cielo Simpson */
--simpson-secondary-green: #90EE90   /* Verde claro */
--simpson-secondary-purple: #DDA0DD  /* Púrpura suave */
```

### Colores Neutros
```css
--simpson-dark-text: #2F4F4F         /* Texto principal oscuro */
--simpson-light-bg: #FFF8DC          /* Fondo claro crema */
--simpson-white-pure: #FFFFFF        /* Blanco puro */
```

### Estados Interactivos
```css
--simpson-hover-yellow: #FFED4E      /* Amarillo hover */
--simpson-hover-orange: #FF8C00      /* Naranja hover */
--simpson-active-red: #FF4500        /* Rojo activo */
```

### Colores Funcionales
```css
--simpson-success: #32CD32           /* Verde éxito */
--simpson-warning: #FF8C00           /* Naranja advertencia */
--simpson-error: #DC143C             /* Rojo error */
--simpson-info: #4169E1              /* Azul información */
```

---

## 📝 Tipografía

### Fuentes Principales
- **Títulos**: `'Fredoka One', cursive` - Para títulos principales y headers
- **Texto General**: `'Comic Neue', cursive` - Para texto de contenido
- **Fallback**: `Arial, sans-serif` - Fuente de respaldo

### Jerarquía de Tamaños (Responsive)
```css
/* Tamaños que se adaptan automáticamente */
--font-size-hero: clamp(2rem, 5vw, 3.5rem)      /* Título principal */
--font-size-h1: clamp(1.8rem, 4vw, 2.5rem)      /* H1 */
--font-size-h2: clamp(1.5rem, 3.5vw, 2rem)      /* H2 */
--font-size-h3: clamp(1.2rem, 3vw, 1.5rem)      /* H3 */
--font-size-body: clamp(1rem, 2.5vw, 1.1rem)    /* Texto normal */
--font-size-small: clamp(0.875rem, 2vw, 0.95rem) /* Texto pequeño */
```

### Pesos y Alturas de Línea
```css
--font-weight-normal: 400
--font-weight-bold: 700
--font-line-height-tight: 1.2       /* Para títulos */
--font-line-height-normal: 1.5      /* Para texto general */
--font-line-height-relaxed: 1.8     /* Para análisis largos */
```

---

## 📐 Espaciado y Grid System

### Sistema de Espaciado (Base 8px)
```css
--spacing-xs: 0.5rem     /* 8px */
--spacing-sm: 1rem       /* 16px */
--spacing-md: 1.5rem     /* 24px */
--spacing-lg: 2rem       /* 32px */
--spacing-xl: 3rem       /* 48px */
--spacing-xxl: 4rem      /* 64px */
```

### Espaciado Responsive
```css
--spacing-container-padding: clamp(1rem, 3vw, 2rem)
--spacing-card-padding: clamp(1.25rem, 2.5vw, 2rem)
--spacing-button-padding: clamp(0.75rem, 2vw, 1rem) clamp(1.5rem, 3vw, 2rem)
```

### Grid System
```css
.grid { display: grid; gap: var(--spacing-md); }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
.grid-4 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
```

---

## 🎯 Componentes Principales

### 1. Header Principal
```html
<div class="simpson-header animate-fade-in">
    <h1>🍩 Springfield Insights</h1>
    <h3>Explorando la filosofía de Los Simpsons</h3>
</div>
```

**Características:**
- Gradiente amarillo-naranja-rojo
- Bordes redondeados y sombras
- Tipografía Fredoka One para títulos
- Animación de entrada suave

### 2. Tarjeta de Cita
```html
<div class="quote-card animate-fade-in">
    <div class="quote-text">"Texto de la cita aquí"</div>
</div>
```

**Características:**
- Fondo amarillo-naranja con gradiente
- Texto centrado y responsive
- Altura mínima garantizada
- Efecto shimmer sutil

### 3. Botones Simpson
```html
<!-- Botón normal -->
<button class="simpson-button">Texto del botón</button>

<!-- Botón primario -->
<button class="simpson-button simpson-button-primary">Acción Principal</button>
```

**Estados:**
- **Normal**: Amarillo-naranja con borde rojo
- **Hover**: Elevación y cambio de color
- **Active**: Escala reducida
- **Primary**: Rojo con texto blanco

### 4. Métricas y Estadísticas
```html
<div class="simpson-metric">
    <div class="simpson-metric-icon">📊</div>
    <div class="simpson-metric-label">Etiqueta</div>
    <div class="simpson-metric-value">Valor</div>
</div>
```

### 5. Análisis Filosófico
```html
<div class="analysis-container hover-lift animate-fade-in">
    <div class="analysis-header">🧠 Análisis Filosófico</div>
    <div class="analysis-content">Contenido del análisis...</div>
</div>
```

---

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile */
@media (max-width: 480px) { ... }

/* Tablet */
@media (min-width: 481px) and (max-width: 768px) { ... }

/* Desktop */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* Wide */
@media (min-width: 1025px) { ... }
```

### Adaptaciones por Dispositivo

#### Mobile (≤480px)
- Padding reducido en contenedores
- Fuentes más pequeñas
- Grid de una sola columna
- Botones más compactos

#### Tablet (481px-768px)
- Grid de 2 columnas para componentes
- Espaciado intermedio
- Fuentes escaladas proporcionalmente

#### Desktop (≥769px)
- Grid completo (3-4 columnas)
- Espaciado máximo
- Efectos hover completos
- Animaciones suaves

---

## 🛠️ Clases de Utilidad

### Layout
```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-center { justify-content: center; align-items: center; }
.flex-between { justify-content: space-between; align-items: center; }
.grid { display: grid; }
```

### Espaciado
```css
.gap-sm { gap: var(--spacing-sm); }
.gap-md { gap: var(--spacing-md); }
.gap-lg { gap: var(--spacing-lg); }
.p-sm { padding: var(--spacing-sm); }
.m-sm { margin: var(--spacing-sm); }
```

### Texto
```css
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.text-justify { text-align: justify; }
.font-bold { font-weight: var(--font-weight-bold); }
```

### Colores
```css
.text-primary { color: var(--simpson-primary-red); }
.text-secondary { color: var(--simpson-info); }
.bg-primary { background-color: var(--simpson-primary-yellow); }
.bg-white { background-color: var(--simpson-white-pure); }
```

### Efectos
```css
.hover-lift:hover { transform: translateY(-4px); }
.hover-scale:hover { transform: scale(1.05); }
.hover-glow:hover { box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
.animate-bounce { animation: bounce 2s infinite; }
.animate-fade-in { animation: fadeIn 0.5s ease-in-out; }
```

---

## ✅ Mejores Prácticas

### 1. Consistencia Visual
- **Usar siempre las variables CSS** definidas en el sistema
- **Mantener la paleta de colores** Simpson en todos los componentes
- **Aplicar espaciado consistente** usando el sistema de 8px

### 2. Responsive First
- **Diseñar primero para móvil** y escalar hacia desktop
- **Usar `clamp()`** para tamaños de fuente adaptativos
- **Probar en múltiples dispositivos** antes de implementar

### 3. Performance
- **Usar animaciones CSS** en lugar de JavaScript cuando sea posible
- **Optimizar imágenes** con el CDN oficial de Los Simpsons
- **Minimizar reflows** con transforms en lugar de cambios de layout

### 4. Accesibilidad
- **Mantener contraste alto** entre texto y fondo
- **Usar tamaños de fuente legibles** (mínimo 16px en móvil)
- **Proporcionar estados de focus** visibles en botones

### 5. Mantenibilidad
- **Usar clases semánticas** en lugar de estilos inline
- **Documentar componentes nuevos** en esta guía
- **Seguir la nomenclatura BEM** para clases CSS personalizadas

---

## 🎨 Ejemplos de Uso

### Crear una Nueva Tarjeta
```html
<div class="simpson-card hover-lift">
    <h3 class="text-primary font-bold">Título de la Tarjeta</h3>
    <p class="text-justify">Contenido de la tarjeta con texto justificado.</p>
    <button class="simpson-button">Acción</button>
</div>
```

### Layout Responsive
```html
<div class="grid grid-3 gap-md">
    <div class="simpson-metric">Métrica 1</div>
    <div class="simpson-metric">Métrica 2</div>
    <div class="simpson-metric">Métrica 3</div>
</div>
```

### Mensaje de Estado
```html
<div class="simpson-card simpson-success text-center">
    <div class="text-success font-bold">✅ Operación Exitosa</div>
    <p>La cita se ha guardado correctamente.</p>
</div>
```

---

## 🔄 Actualizaciones del Sistema

Para mantener el sistema de diseño actualizado:

1. **Documentar cambios** en esta guía
2. **Actualizar variables CSS** en `design_system.py`
3. **Probar compatibilidad** con componentes existentes
4. **Validar responsive** en todos los breakpoints

---

*Esta guía es un documento vivo que debe actualizarse con cada mejora al sistema de diseño.*