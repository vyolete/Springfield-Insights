# 🍩 Springfield Insights

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

**Explorando la filosofía y crítica social de Los Simpsons mediante inteligencia artificial**

## 🚀 Demo en Vivo

**[▶️ Abrir Springfield Insights](https://your-app-name.streamlit.app)**

## 📋 Descripción

Springfield Insights es una aplicación académica que utiliza **GPT-3.5-Turbo** para generar análisis filosóficos profundos de Los Simpsons, demostrando la riqueza intelectual presente en la cultura popular. Optimizada para **Streamlit Cloud** con integración automática de GitHub.

## ✨ Características

- 🤖 **Análisis con GPT-3.5-Turbo**: Interpretaciones filosóficas auténticas
- 🎭 **Personajes Únicos**: Reflexiones fieles a Homer, Lisa, Bart y Marge
- 🏛️ **Rigor Académico**: Enfoque en crítica social y contexto filosófico
- ☁️ **Deploy Automático**: Integración completa con Streamlit Cloud y GitHub
- 🎨 **Interfaz Moderna**: Diseño responsive y experiencia optimizada
- 🔄 **CI/CD Automático**: Cada push actualiza la app automáticamente

## 🛠️ Instalación Local

### Prerrequisitos
- Python 3.8+
- Cuenta de OpenAI con API Key (para producción)

### Pasos Rápidos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/springfield-insights.git
cd springfield-insights

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
cp .env.example .env
# Edita .env y añade tu OPENAI_API_KEY

# 4. Ejecutar aplicación
streamlit run app.py
```

## 🧪 Testing y QA Automation

### 🎯 Framework de Testing

Springfield Insights incluye un **framework completo de QA Automation** con:

- ✅ **Tests End-to-End** con Playwright
- ✅ **Mock completo de OpenAI** (sin llamadas reales a la API)
- ✅ **Tests 100% reproducibles** y deterministas
- ✅ **Selectores estables** usando `data-testid`
- ✅ **Listo para CI/CD** automático

### 🚀 Configuración Rápida de Testing

```bash
# 1. Configurar entorno de testing (una sola vez)
python scripts/setup_testing.py

# 2. Ejecutar todos los tests
python scripts/run_tests.py

# 3. Solo tests unitarios (rápidos)
python scripts/run_tests.py --type unit

# 4. Solo tests E2E (completos)
python scripts/run_tests.py --type e2e
```

### 📋 Comandos de Testing Disponibles

```bash
# Configuración inicial (ejecutar una vez)
python scripts/setup_testing.py

# Ejecutar todos los tests
python scripts/run_tests.py

# Tests por tipo
python scripts/run_tests.py --type unit      # Tests unitarios
python scripts/run_tests.py --type e2e       # Tests end-to-end
python scripts/run_tests.py --type coverage  # Con reporte de cobertura

# Verificar dependencias
python scripts/run_tests.py --check-deps

# Instalar navegadores de Playwright
python scripts/run_tests.py --install-playwright
```

### 🎭 Tests End-to-End

Los tests E2E validan el **flujo completo** de la aplicación:

1. **Inicio de Streamlit** automático en puerto de testing
2. **Navegación** a la aplicación con Playwright
3. **Click en botón principal** usando `data-testid="stBaseButton-primary"`
4. **Verificación de cita** generada de Los Simpsons
5. **Validación de análisis** en `data-testid="stMarkdownContainer"`
6. **Mock de OpenAI** completamente funcional

### 🔧 Mock de OpenAI

#### Características del Mock

- **🎯 Determinista**: Misma entrada → misma salida
- **🎭 Por personaje**: Análisis específicos para Homer, Lisa, Bart, Marge
- **⚡ Sin latencia**: Respuestas instantáneas
- **🔒 Sin API calls**: Cero dependencias externas
- **🧪 Testeable**: Incluye simulación de errores

#### Cómo Funciona el Mock

```python
# El mock intercepta llamadas a OpenAI y retorna análisis predefinidos
from tests.mocks.mock_quote_service import MockQuoteService

# Crear mock service
mock_service = MockQuoteService()

# Generar análisis (sin llamadas reales a OpenAI)
analysis = mock_service.generate_analysis(
    quote="D'oh! Life is complicated.",
    character="Homer Simpson", 
    context="Homer reflecting on life"
)

# Resultado: Análisis filosófico completo y determinista
print(analysis)
# Output: "1. **Significado Filosófico**: Esta reflexión de Homer..."
```

#### Configuración del Mock en Tests

El mock se activa automáticamente en los tests usando **dependency injection**:

```python
# En tests E2E
with patch('services.quote_service.QuoteService') as mock_service_class:
    mock_service = Mock()
    mock_service.generate_analysis.return_value = "Análisis mock determinista"
    mock_service_class.return_value = mock_service
    
    # Ahora los tests usan el mock en lugar de OpenAI real
    # Click en botón → Mock analysis → Verificación
```

### 📁 Estructura de Testing

```
tests/
├── conftest.py                    # Configuración global de pytest
├── test_mock_quote_service.py     # Tests unitarios del mock
├── test_e2e_main_flow.py         # Tests end-to-end completos
└── mocks/
    ├── __init__.py
    └── mock_quote_service.py      # Mock service de OpenAI

scripts/
├── setup_testing.py              # Configuración automática
└── run_tests.py                  # Ejecutor de tests

pytest.ini                        # Configuración de pytest
.env.test                         # Variables para testing
```

### 🎯 Flujo de Testing Validado

#### Test Principal: `test_complete_quote_generation_flow`

1. **Setup**: Levantar Streamlit en puerto 8502
2. **Navigate**: Abrir navegador y ir a la app
3. **Interact**: Click en `[data-testid="stBaseButton-primary"]`
4. **Verify Quote**: Verificar aparición de personaje de Los Simpsons
5. **Verify Analysis**: Verificar contenido en `[data-testid="stMarkdownContainer"]`
6. **Mock Validation**: Confirmar que se usó mock (no API real)

#### Selectores Estables Usados

```python
# Botón principal
main_button = page.locator('[data-testid="stBaseButton-primary"]')

# Contenedor de análisis
analysis_container = page.locator('[data-testid="stMarkdownContainer"]')

# Indicadores de contenido
quote_indicators = [
    page.locator("text=Homer Simpson"),
    page.locator("text=Análisis Filosófico"),
    page.locator("text=Significado Filosófico")
]
```

### 🚀 Integración CI/CD

Los tests están **listos para CI/CD** con:

- **Headless browser**: Sin interfaz gráfica
- **Mock completo**: Sin dependencias externas
- **Timeouts configurados**: Para entornos lentos
- **Reportes estructurados**: Salida compatible con CI

#### Ejemplo GitHub Actions

```yaml
name: QA Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Setup Testing
        run: python scripts/setup_testing.py
      
      - name: Run Tests
        run: python scripts/run_tests.py --type all
```

### 📊 Cobertura y Reportes

```bash
# Generar reporte de cobertura HTML
python scripts/run_tests.py --type coverage

# Ver reporte
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### ✅ Estado del Framework

**Framework QA Automation - ✅ COMPLETAMENTE FUNCIONAL**

- 🎯 **Tests Unitarios**: 14/14 pasando ✅
- 🎭 **Mock de OpenAI**: 100% determinista ✅  
- 🔧 **Configuración**: Automática ✅
- 📋 **Documentación**: Completa ✅
- 🚀 **CI/CD Ready**: Listo ✅

```bash
# Verificación rápida del framework
python -m pytest tests/test_demo_simple.py -v

# Resultado esperado: 6/6 tests pasando
# ✅ Mock service básico
# ✅ Análisis por personaje  
# ✅ Determinismo
# ✅ Simulación de errores
# ✅ Integración lista
```

## ☁️ Deploy en Streamlit Cloud

### 🚀 Configuración Automática con GitHub

1. **Fork este repositorio** en tu cuenta de GitHub

2. **Conecta con Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Haz clic en "New app"
   - Conecta tu repositorio de GitHub
   - Selecciona `streamlit_app.py` como archivo principal

3. **Configura Secrets:**
   - En tu app de Streamlit Cloud, ve a "Settings" → "Secrets"
   - Añade tu configuración:
   ```toml
   OPENAI_API_KEY = "sk-proj-tu-api-key-aqui"
   ```

4. **Deploy Automático:**
   - Cada push a `main` actualizará automáticamente tu app
   - La URL será: `https://tu-usuario-springfield-insights-streamlit-app-xxx.streamlit.app`

### 🔐 Configuración de Secrets

En Streamlit Cloud Settings → Secrets:

```toml
# ✅ Requerido
OPENAI_API_KEY = "tu-api-key-de-openai"

# 🔧 Opcional (con valores por defecto)
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = "250"
OPENAI_TEMPERATURE = "0.8"
```

## 🎯 Uso

1. **Selecciona un personaje** en la barra lateral (o deja "Aleatorio")
2. **Haz clic en "Generar Nueva Reflexión"** 
3. **Explora el análisis** generado por IA
4. **Interactúa** con los botones para copiar, guardar o compartir

## 🏗️ Arquitectura

### Estructura Optimizada para Streamlit Cloud
```
springfield-insights/
├── streamlit_app.py      # 🎯 Aplicación principal (Streamlit Cloud)
├── app_final.py          # 🔧 Versión simple alternativa
├── requirements.txt      # 📦 Dependencias
├── .env.example         # 🔐 Plantilla de configuración
├── .streamlit/          # ⚙️ Configuración de Streamlit
│   └── config.toml
├── config/              # 🛠️ Configuración avanzada
│   └── settings.py
├── services/            # 🔄 Servicios de negocio
├── ui/                  # 🎨 Componentes de interfaz
├── data/                # 📊 Gestión de datos
└── utils/               # 🔧 Utilidades
```

### 🔄 Flujo de Desarrollo

#### Desarrollo Local
```bash
# Desarrollo con hot-reload
streamlit run streamlit_app.py

# Versión simple para testing
streamlit run app_final.py
```

#### Deploy Automático
1. **Commit y push** a GitHub
2. **Streamlit Cloud detecta** cambios automáticamente
3. **Redeploy automático** en segundos
4. **URL actualizada** instantáneamente

## 🤖 Tecnologías

- **🐍 Python 3.9+**
- **🚀 Streamlit**: Framework de aplicaciones web
- **🤖 OpenAI GPT-3.5-Turbo**: Análisis de inteligencia artificial  
- **☁️ Streamlit Cloud**: Hosting y deploy automático
- **🔗 GitHub**: Control de versiones e integración CI/CD
- **🔐 Streamlit Secrets**: Gestión segura de API keys

## 🎓 Valor Académico

**Springfield Insights** demuestra cómo la inteligencia artificial puede ser utilizada para:

- 📚 **Análisis cultural** mediante procesamiento de lenguaje natural
- 🎭 **Crítica social** a través de personajes ficticios
- 🏛️ **Filosofía aplicada** en cultura popular contemporánea
- ☁️ **Deploy moderno** con CI/CD automático

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m 'Añadir nueva funcionalidad increíble'
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abre un Pull Request**

## 📊 Funcionalidades

### ✅ Implementadas
- 🎭 Selección de personajes (Homer, Lisa, Bart, Marge)
- 🤖 Generación de reflexiones con GPT-3.5-Turbo
- 📚 Análisis filosófico contextualizado
- 🎨 Interfaz responsive y moderna
- ☁️ Deploy automático en Streamlit Cloud
- 🔐 Gestión segura de secrets

### 🚧 Próximas Mejoras
- 📊 Dashboard de estadísticas
- 💾 Sistema de favoritos persistente
- 🔗 Compartir en redes sociales
- 📱 Optimización móvil avanzada

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver [LICENSE](LICENSE) para detalles.

---

<div align="center">

**[🚀 Probar la App](https://your-app-name.streamlit.app)** | **[📖 Documentación](https://github.com/tu-usuario/springfield-insights/wiki)** | **[🐛 Reportar Bug](https://github.com/tu-usuario/springfield-insights/issues)**

Hecho con ❤️ y 🤖 para explorar la sabiduría de Springfield

</div>