# 🍩 Springfield Insights

**Explorando la filosofía y crítica social de Los Simpsons mediante inteligencia artificial**

## 📋 Descripción del Proyecto

Springfield Insights es una aplicación académica desarrollada en Python que utiliza inteligencia artificial para analizar citas de la serie animada Los Simpsons desde una perspectiva filosófica y de crítica social. La aplicación combina el consumo de una API pública de citas con el poder analítico de GPT-4 para generar explicaciones contextuales profundas.

## 🎯 Objetivos Académicos

- **Demostrar el valor cultural**: Evidenciar la profundidad filosófica y crítica social presente en la cultura popular
- **Aplicación de IA**: Mostrar cómo los modelos de lenguaje pueden ser utilizados para análisis cultural y académico
- **Arquitectura modular**: Implementar buenas prácticas de ingeniería de software en un contexto académico
- **Interfaz accesible**: Crear una herramienta educativa intuitiva y visualmente atractiva

## 🏗️ Arquitectura del Sistema

### Estructura Modular

```
springfield_insights/
│
├── app.py                     # Punto de entrada Streamlit
├── config/
│   └── settings.py            # Configuración centralizada
├── services/
│   ├── simpsons_api.py        # Consumo de API de citas
│   └── llm_service.py         # Integración con GPT-4
├── logic/
│   └── quote_processor.py     # Orquestación de datos + LLM
├── ui/
│   └── theme.py               # Tema visual Los Simpsons
├── utils/
│   └── validators.py          # Validaciones y manejo de errores
├── requirements.txt           # Dependencias
└── README.md                  # Documentación
```

### Componentes Principales

1. **Capa de Presentación** (`app.py`, `ui/theme.py`)
   - Interfaz Streamlit con tema personalizado
   - Componentes visuales inspirados en Los Simpsons
   - Manejo de estado de sesión

2. **Capa de Lógica de Negocio** (`logic/quote_processor.py`)
   - Orquestación entre servicios
   - Procesamiento y validación de datos
   - Manejo de errores y reintentos

3. **Capa de Servicios** (`services/`)
   - `simpsons_api.py`: Consumo de API externa
   - `llm_service.py`: Integración con OpenAI GPT-4

4. **Capa de Utilidades** (`utils/validators.py`, `config/settings.py`)
   - Validaciones de datos
   - Configuración centralizada
   - Manejo de errores

## 🚀 Instrucciones de Ejecución Local

### Prerrequisitos

- Python 3.10 o superior
- Clave API de OpenAI (GPT-4)
- Conexión a internet

### Instalación

#### Opción 1: Setup Automatizado (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd springfield_insights
   ```

2. **Ejecutar setup automatizado**
   ```bash
   python setup.py
   ```
   
   El script automáticamente:
   - Verifica la versión de Python
   - Crea directorios necesarios
   - Instala dependencias
   - Configura archivos de entorno
   - Ejecuta tests básicos

#### Opción 2: Instalación Manual

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd springfield_insights
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   OPENAI_API_KEY=tu-clave-api-de-openai
   ```
   
   O usar el archivo de ejemplo:
   ```bash
   cp .env.example .env
   # Editar .env con tu API key
   ```

### Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 🔧 Variables de Entorno Requeridas

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | Clave API de OpenAI para GPT-4 | ✅ Sí |

### Configuración Alternativa

También puedes configurar las variables usando Streamlit secrets:

1. Crear directorio `.streamlit/` en la raíz del proyecto
2. Crear archivo `secrets.toml`:
   ```toml
   OPENAI_API_KEY = "tu-clave-api-de-openai"
   ```

## 🤖 Justificación del Uso de GPT-4

### Capacidades Analíticas

GPT-4 fue seleccionado por sus capacidades superiores en:

1. **Análisis Contextual**: Comprende referencias culturales y contexto histórico
2. **Razonamiento Filosófico**: Puede identificar y explicar conceptos filosóficos complejos
3. **Crítica Social**: Reconoce y articula elementos de sátira y crítica social
4. **Adaptabilidad**: Se adapta al tono y personalidad de diferentes personajes

### Metodología de Prompting

El sistema utiliza prompting estructurado que incluye:

- **Prompt del Sistema**: Define el rol como experto en filosofía y crítica social
- **Prompt Específico**: Solicita análisis en cuatro dimensiones:
  1. Significado filosófico
  2. Crítica social implícita
  3. Contexto del personaje
  4. Relevancia contemporánea

### Ventajas sobre Alternativas

- **Sin entrenamiento adicional**: Utiliza conocimiento preexistente
- **Flexibilidad**: Adapta el análisis según el contexto
- **Calidad académica**: Genera contenido apropiado para contextos educativos
- **Consistencia**: Mantiene calidad uniforme en los análisis

## 📊 Funcionalidades Implementadas

### Funcionalidades Principales

- ✅ **Exploración de Citas**: Obtención de citas aleatorias con análisis filosófico GPT-4
- ✅ **Sistema de Favoritos Avanzado**: Persistencia local, filtros y exportación
- ✅ **Analytics Inteligentes**: Análisis de patrones, complejidad y temas filosóficos
- ✅ **Interfaz Multi-pestaña**: Navegación intuitiva entre funcionalidades
- ✅ **Gestión de Datos**: Almacenamiento local con formato JSON estructurado
- ✅ **Exportación**: Descarga de favoritos en formato JSON
- ✅ **Métricas Avanzadas**: Análisis de complejidad lingüística y profundidad conceptual

### Características Técnicas Avanzadas

- ✅ **Arquitectura Modular Expandida**: 7 módulos especializados
- ✅ **Sistema de Analytics**: Análisis automático de patrones y tendencias
- ✅ **Persistencia de Datos**: Gestión local de favoritos con FavoritesManager
- ✅ **Logging Avanzado**: Sistema de logs configurable con rotación
- ✅ **Tests Unitarios**: Cobertura de componentes críticos
- ✅ **Setup Automatizado**: Script de instalación y configuración
- ✅ **Validación Robusta**: Múltiples capas de validación de datos
- ✅ **Manejo de Errores**: Sistema centralizado con mensajes contextuales

## 🎨 Diseño Visual

### Paleta de Colores

- **Amarillo Simpson** (`#FFD700`): Color principal
- **Azul característico** (`#4169E1`): Acentos y bordes
- **Fondo claro** (`#FFF8DC`): Fondo general
- **Naranja de acento** (`#FF8C00`): Elementos destacados

### Tipografía

- **Primaria**: Arial, sans-serif (legibilidad)
- **Secundaria**: Comic Sans MS, cursive (personalidad)
- **Monoespaciada**: Courier New (código)

## 🧪 Testing y Validación

### Validaciones Implementadas

1. **Estructura de datos**: Verificación de campos requeridos
2. **Contenido de citas**: Longitud y formato válidos
3. **Análisis LLM**: Calidad y relevancia del contenido generado
4. **APIs externas**: Manejo de errores de red y timeouts

### Manejo de Errores

- Timeouts de red configurables
- Reintentos automáticos para LLM
- Mensajes de error amigables al usuario
- Logging detallado para debugging

## 📈 Posibles Extensiones

### Funcionalidades Futuras

- **Base de datos**: Almacenamiento persistente de citas favoritas
- **Filtros avanzados**: Búsqueda por personaje o tema
- **Exportación**: Generar reportes en PDF
- **Análisis comparativo**: Comparar citas de diferentes personajes
- **API propia**: Exponer funcionalidad como servicio web

### Mejoras Técnicas

- **Cache**: Implementar cache para análisis previos
- **Tests unitarios**: Cobertura completa de testing
- **CI/CD**: Pipeline de integración continua
- **Monitoreo**: Métricas de uso y rendimiento

## 📝 Licencia y Uso Académico

Este proyecto está desarrollado con fines académicos y educativos. El uso de referencias a Los Simpsons se realiza bajo el principio de uso justo para análisis crítico y educativo.

## 👥 Contribuciones

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

Para reportar problemas o sugerir mejoras, crear un issue en el repositorio del proyecto.

---

**Springfield Insights** - Demostrando que la sabiduría puede encontrarse en los lugares más inesperados. 🍩