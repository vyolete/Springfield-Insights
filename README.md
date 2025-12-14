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

## 🚀 Ejecución en Entorno Local

### Requisitos Previos

- **Python 3.10+** (verificar con `python --version`)
- **Conexión a internet** (para APIs externas)
- **Clave API de OpenAI** (obtener en [OpenAI Platform](https://platform.openai.com/api-keys))

### Configuración del Entorno

#### 1. Preparación del Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/vyolete/Springfield-Insights.git
cd Springfield-Insights

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

#### 2. Instalación de Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep streamlit
```

#### 3. Configuración de Variables de Entorno

**Opción A: Archivo .env (Recomendado)**

```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tu editor favorito
nano .env  # o vim .env, code .env, etc.
```

Configurar en `.env`:
```env
# Configuración requerida
OPENAI_API_KEY=tu-clave-api-de-openai-aqui
SIMPSONS_API_BASE_URL=https://thesimpsonsquoteapi.glitch.me/quotes

# Configuración opcional
API_TIMEOUT=10
LLM_TIMEOUT=30
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7
```

**Opción B: Variables del Sistema**

```bash
# Configurar variables de entorno
export OPENAI_API_KEY="tu-clave-api-de-openai"
export SIMPSONS_API_BASE_URL="https://thesimpsonsquoteapi.glitch.me/quotes"
```

#### 4. Validación del Entorno

La aplicación incluye **validación automática del entorno** que verifica:

- ✅ Configuración de variables de entorno
- ✅ Conectividad con API de Simpsons
- ✅ Validez de la clave OpenAI
- ✅ Disponibilidad de GPT-4

### Comando de Ejecución

```bash
# Ejecutar aplicación
streamlit run app.py

# Con puerto específico (opcional)
streamlit run app.py --server.port 8501

# Con configuración de desarrollo
streamlit run app.py --server.runOnSave true
```

### Resultado Esperado

Al ejecutar correctamente, verás:

```
🍩 SPRINGFIELD INSIGHTS - CONFIGURACIÓN LOCAL
============================================================
📱 Aplicación: Springfield Insights v1.0.0
🤖 Modelo IA: gpt-4
🔑 API Key: ✅ Configurada
⚙️  Configuración: Tokens=500, Temp=0.7
⏱️  Timeouts: API=10s, LLM=30s
🔧 Debug: False, Log: INFO
✅ Configuración válida - Lista para ejecutar
============================================================

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Solución de Problemas Comunes

#### Error: "OPENAI_API_KEY no configurada"

```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar contenido (sin mostrar la clave)
grep "OPENAI_API_KEY" .env

# Si no existe, crear desde plantilla
cp .env.example .env
```

#### Error: "ModuleNotFoundError"

```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Verificar entorno virtual activo
which python  # Debe mostrar ruta del venv
```

#### Error: "API de Simpsons no accesible"

```bash
# Verificar conectividad
curl https://thesimpsonsquoteapi.glitch.me/quotes

# Verificar configuración de proxy (si aplica)
echo $HTTP_PROXY
```

#### Error: "OpenAI API inválida"

1. Verificar clave en [OpenAI Platform](https://platform.openai.com/api-keys)
2. Asegurar que la clave tiene créditos disponibles
3. Verificar que la clave no ha expirado

### Funcionalidades Disponibles Localmente

Una vez ejecutándose, podrás acceder a:

- **🎲 Explorar**: Obtener citas aleatorias con análisis filosófico
- **📺 Episodios**: Navegar por el catálogo completo de episodios y generar reflexiones contextuales
- **⭐ Favoritos**: Guardar y gestionar citas favoritas
- **📊 Analytics**: Analizar patrones y métricas de tus favoritos
- **ℹ️ Acerca de**: Información del proyecto y documentación técnica

#### 🆕 Funcionalidad de Episodios

La nueva pestaña **"📺 Episodios"** ofrece tres modos de exploración:

1. **🔍 Buscar Episodios**
   - Navegación paginada por el catálogo completo
   - Búsqueda por texto en nombre y sinopsis
   - Filtros por temporada específica
   - Selección de episodios aleatorios

2. **📅 Por Temporadas**
   - Vista general de todas las temporadas
   - Generación de reflexiones temáticas por temporada
   - Estadísticas de episodios por temporada

3. **👤 Por Personajes**
   - Episodios relevantes para personajes específicos
   - Análisis contextual basado en la participación del personaje
   - Reflexiones personalizadas según el protagonista del episodio

#### Integración con APIs

- **Catálogo de Episodios**: `https://thesimpsonsapi.com/api/episodes`
- **Imágenes Optimizadas**: `https://cdn.thesimpsonsapi.com/500/{image_path}`
- **Caching Inteligente**: TTL de 1-3 horas para optimizar performance
- **Fallbacks Robustos**: Múltiples niveles de respaldo ante fallos de API

### Configuración Avanzada

#### Variables de Entorno Opcionales

```env
# Logging
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE=true        # Guardar logs en archivo

# Performance
API_TIMEOUT=15          # Timeout para API de Simpsons
LLM_TIMEOUT=45          # Timeout para OpenAI

# Desarrollo
DEBUG_MODE=true         # Modo debug para desarrollo
STREAMLIT_PORT=8502     # Puerto alternativo
```

#### Configuración de Streamlit

Crear `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FFD700"
backgroundColor = "#FFF8DC"
secondaryBackgroundColor = "#F0E68C"
textColor = "#2F4F4F"

[server]
port = 8501
headless = false
```

### Validación Académica

La aplicación implementa **validación robusta del entorno** siguiendo buenas prácticas académicas:

- **Separación de código y configuración**: Variables sensibles en archivos separados
- **Validación automática**: Verificación de APIs y configuración al inicio
- **Manejo de errores académico**: Mensajes claros y soluciones sugeridas
- **Logging estructurado**: Trazabilidad completa para debugging

Esta configuración cumple con estándares académicos de **ingeniería de software segura** y **buenas prácticas de desarrollo**.

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

## 🔗 Integración con la API de Los Simpsons

### Estrategia Robusta de Datos

El proyecto implementa una **arquitectura resiliente** para el acceso a datos de Los Simpsons:

#### Fuentes de Datos Múltiples

1. **APIs Externas** (Primaria)
   - `https://thesimpsonsapi.com/api/characters`
   - `https://thesimpsonsapi.com/api/episodes`
   - `https://thesimpsonsapi.com/api/locations`

2. **Sistema de Fallback Local** (Secundaria)
   - Personajes predefinidos con contexto filosófico
   - Datos curados académicamente
   - Garantiza funcionalidad sin dependencias externas

#### Limitaciones Identificadas de APIs Públicas

Durante el desarrollo se identificaron las siguientes limitaciones:

- **Error 401 Unauthorized**: Muchas APIs públicas de Los Simpsons requieren autenticación
- **Endpoints obsoletos**: URLs documentadas que ya no funcionan
- **Estructura inconsistente**: Formatos de respuesta variables
- **Disponibilidad intermitente**: Servicios no confiables para uso académico

#### Decisión Técnica Adoptada

**Generación de Contenido Filosófico Original mediante LLM**

En lugar de depender exclusivamente de citas preexistentes, el sistema:

1. **Obtiene contexto del personaje** (API externa o datos locales)
2. **Genera reflexiones filosóficas originales** usando GPT-4
3. **Crea análisis académicos profundos** del contenido generado
4. **Mantiene autenticidad** al estilo de cada personaje

#### Justificación Académica

Esta aproximación ofrece ventajas significativas:

- **Robustez**: Funciona independientemente del estado de APIs externas
- **Originalidad**: Genera contenido único para cada sesión
- **Profundidad**: Permite análisis más ricos que citas predefinidas
- **Escalabilidad**: No limitado por corpus finito de citas existentes
- **Calidad académica**: Contenido generado específicamente para análisis filosófico

## 🤖 Justificación del Uso de GPT-4

### Capacidades Analíticas Expandidas

GPT-4 fue seleccionado por sus capacidades superiores en:

1. **Generación de Contenido Original**: Crea reflexiones auténticas al estilo de cada personaje
2. **Análisis Contextual**: Comprende referencias culturales y contexto histórico
3. **Razonamiento Filosófico**: Identifica y explica conceptos filosóficos complejos
4. **Crítica Social**: Reconoce y articula elementos de sátira y crítica social
5. **Adaptabilidad**: Se adapta al tono y personalidad de diferentes personajes

### Metodología de Prompting Dual

El sistema utiliza **dos estrategias de prompting**:

#### 1. Generación Completa de Contenido
- **Prompt del Sistema**: Define rol como experto en filosofía y Los Simpsons
- **Prompt Específico**: Solicita reflexión original + análisis académico
- **Estructura**: Reflexión auténtica del personaje + análisis profundo

#### 2. Análisis de Citas Existentes (Fallback)
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
- **Originalidad**: Crea contenido único en cada ejecución
- **Robustez**: No depende de APIs externas para contenido principal

## 📊 Funcionalidades Implementadas

### Funcionalidades Principales

- ✅ **Exploración de Citas**: Obtención de citas aleatorias con análisis filosófico GPT-4
- ✅ **🆕 Navegación por Episodios**: Explora el catálogo completo de 768+ episodios de Los Simpsons
- ✅ **🆕 Búsqueda Contextual**: Busca episodios por nombre, temporada o personaje específico
- ✅ **🆕 Reflexiones Episódicas**: Genera análisis filosóficos basados en episodios específicos
- ✅ **🆕 Integración Visual**: Imágenes de episodios desde CDN oficial con lazy loading
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