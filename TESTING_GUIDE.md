# 🧪 Guía Técnica de Testing - Springfield Insights

## 📋 Índice

1. [Estrategia de Testing](#estrategia-de-testing)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Mock de OpenAI](#mock-de-openai)
4. [Tests End-to-End](#tests-end-to-end)
5. [Tests Unitarios](#tests-unitarios)
6. [Ejecución en CI/CD](#ejecución-en-cicd)
7. [Troubleshooting](#troubleshooting)

## 🎯 Estrategia de Testing

### Enfoque Elegido: **End-to-End + Mocking**

**¿Por qué E2E en lugar de solo integración?**

- ✅ **Validación completa**: Usuario → UI → Lógica → Mock API
- ✅ **Selectores reales**: Usa `data-testid` como en producción
- ✅ **Navegador real**: Comportamiento idéntico al usuario
- ✅ **Reproducibilidad**: Mock elimina variabilidad externa

### Arquitectura de Testing

```
Usuario (Test) → Playwright → Streamlit App → Mock OpenAI
     ↓              ↓              ↓              ↓
  Clicks reales  Navegador    App real     Respuestas
                 Chromium     corriendo    deterministas
```

## ⚙️ Configuración del Entorno

### 1. Instalación Automática

```bash
# Configuración completa en un comando
python scripts/setup_testing.py
```

### 2. Instalación Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores de Playwright
python -m playwright install chromium
python -m playwright install-deps

# Verificar instalación
python scripts/run_tests.py --check-deps
```

### 3. Dependencias de Testing

```python
# Framework de testing
pytest>=7.4.0
pytest-asyncio>=0.21.0

# End-to-End testing
playwright>=1.40.0

# Mocking y fixtures
pytest-mock>=3.12.0

# Cobertura y reportes
pytest-cov>=4.1.0
pytest-html>=4.1.0
```

## 🎭 Mock de OpenAI

### Diseño del Mock

El mock está diseñado para ser **100% determinista** y **compatible** con la interfaz real:

```python
class MockQuoteService:
    def generate_analysis(self, quote: str, character: str, context: str) -> str:
        # Retorna análisis predefinido basado en el personaje
        # Mismo formato que OpenAI real
        # Cero variabilidad
```

### Características Clave

#### 🎯 Determinismo Completo

```python
# Misma entrada → Misma salida SIEMPRE
service1 = MockQuoteService()
service2 = MockQuoteService()

analysis1 = service1.generate_analysis("test", "Homer", "context")
analysis2 = service2.generate_analysis("test", "Homer", "context")

assert analysis1 == analysis2  # ✅ Siempre True
```

#### 🎭 Análisis por Personaje

```python
# Cada personaje tiene análisis específico y auténtico
homer_analysis = mock.generate_analysis("quote", "Homer Simpson", "context")
# → Contiene "hedonismo filosófico", "everyman americano"

lisa_analysis = mock.generate_analysis("quote", "Lisa Simpson", "context") 
# → Contiene "idealismo kantiano", "anti-intelectualismo"
```

#### ⚡ Sin Latencia

```python
# Respuesta instantánea (vs 2-5 segundos de OpenAI real)
start = time.time()
analysis = mock.generate_analysis("quote", "character", "context")
duration = time.time() - start
assert duration < 0.1  # Menos de 100ms
```

#### 🧪 Simulación de Errores

```python
# Para testing de manejo de errores
mock = MockQuoteService(simulate_errors=True)

# Cada 5ta llamada genera error
for i in range(4):
    analysis = mock.generate_analysis("test", "Homer", "test")  # ✅ OK

# La 5ta llamada falla
with pytest.raises(Exception):
    mock.generate_analysis("test", "Homer", "test")  # ❌ Error simulado
```

### Integración en Tests

#### Método 1: Patch del Servicio Completo

```python
@pytest.mark.asyncio
async def test_with_mock_service(page: Page):
    with patch('services.quote_service.QuoteService') as mock_class:
        # Configurar mock
        mock_service = Mock()
        mock_service.generate_analysis.return_value = "Análisis mock"
        mock_class.return_value = mock_service
        
        # Test usa automáticamente el mock
        await page.click('[data-testid="stBaseButton-primary"]')
        # Verificaciones...
```

#### Método 2: Mock del Cliente OpenAI

```python
@pytest.mark.asyncio  
async def test_with_openai_mock(page: Page):
    with patch('openai.OpenAI') as mock_openai:
        # Configurar respuesta mock
        mock_response = Mock()
        mock_response.choices[0].message.content = "Mock analysis"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test procede normalmente
```

## 🎪 Tests End-to-End

### Flujo Principal Validado

```python
async def test_complete_quote_generation_flow(page: Page):
    """
    Flujo completo: Click → Cita → Análisis → Verificación
    """
    
    # 1. Setup del mock
    with patch('services.quote_service.QuoteService') as mock_service:
        mock_service.return_value.generate_analysis.return_value = MOCK_ANALYSIS
        
        # 2. Interacción con UI
        button = page.locator('[data-testid="stBaseButton-primary"]')
        await button.click()
        
        # 3. Verificación de cita generada
        quote_indicators = [
            page.locator("text=Homer Simpson"),
            page.locator("text=Lisa Simpson"),
            page.locator("text=Análisis Filosófico")
        ]
        
        # Al menos uno debe aparecer
        found = False
        for indicator in quote_indicators:
            try:
                await indicator.wait_for(state="visible", timeout=15000)
                found = True
                break
            except:
                continue
        
        assert found, "No se generó cita de Los Simpsons"
        
        # 4. Verificación de análisis en contenedor correcto
        analysis_container = page.locator('[data-testid="stMarkdownContainer"]')
        await analysis_container.wait_for(state="visible")
        
        # 5. Verificación de estructura del análisis
        required_sections = [
            "Significado Filosófico",
            "Crítica Social",
            "Contexto del Personaje", 
            "Relevancia Contemporánea"
        ]
        
        for section in required_sections:
            section_locator = page.locator(f"text={section}")
            await section_locator.wait_for(state="visible", timeout=5000)
```

### Selectores Estables

#### ✅ Selectores Recomendados

```python
# Botón principal - ESTABLE
main_button = page.locator('[data-testid="stBaseButton-primary"]')

# Contenedor de análisis - ESTABLE  
analysis = page.locator('[data-testid="stMarkdownContainer"]')

# Contenido por texto - SEMI-ESTABLE
character = page.locator("text=Homer Simpson")
```

#### ❌ Selectores a Evitar

```python
# Clases CSS - INESTABLES (cambian con versiones de Streamlit)
button = page.locator('.stButton > button')

# Posición - FRÁGILES
button = page.locator('button:nth-child(2)')

# XPath complejos - DIFÍCILES DE MANTENER
button = page.locator('//div[@class="stButton"]//button[contains(text(), "Reflexión")]')
```

### Gestión de Timeouts

```python
# Configuración de timeouts apropiados
page.set_default_timeout(10000)  # 10 segundos por defecto

# Timeouts específicos para operaciones lentas
await element.wait_for(state="visible", timeout=15000)  # Generación de análisis

# Timeouts cortos para verificaciones rápidas
await element.wait_for(state="visible", timeout=2000)   # Elementos ya cargados
```

## 🔬 Tests Unitarios

### Testing del Mock Service

```python
class TestMockQuoteService:
    def test_deterministic_responses(self):
        """Verificar que las respuestas son deterministas"""
        service1 = MockQuoteService()
        service2 = MockQuoteService()
        
        analysis1 = service1.generate_analysis("test", "Homer", "context")
        analysis2 = service2.generate_analysis("test", "Homer", "context")
        
        assert analysis1 == analysis2
    
    def test_character_specific_analysis(self):
        """Verificar análisis específicos por personaje"""
        service = MockQuoteService()
        
        homer = service.generate_analysis("quote", "Homer Simpson", "context")
        lisa = service.generate_analysis("quote", "Lisa Simpson", "context")
        
        assert "hedonismo filosófico" in homer
        assert "idealismo kantiano" in lisa
        assert homer != lisa
    
    def test_analysis_structure(self):
        """Verificar estructura consistente del análisis"""
        service = MockQuoteService()
        analysis = service.generate_analysis("test", "Homer", "context")
        
        required_sections = [
            "1. **Significado Filosófico**",
            "2. **Crítica Social**",
            "3. **Contexto del Personaje**", 
            "4. **Relevancia Contemporánea**"
        ]
        
        for section in required_sections:
            assert section in analysis
```

## 🚀 Ejecución en CI/CD

### GitHub Actions

```yaml
name: QA Automation Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    
    - name: Setup testing environment
      run: python scripts/setup_testing.py
    
    - name: Run unit tests
      run: python scripts/run_tests.py --type unit
    
    - name: Run E2E tests
      run: python scripts/run_tests.py --type e2e
    
    - name: Generate coverage report
      run: python scripts/run_tests.py --type coverage
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Variables de Entorno para CI

```bash
# En CI/CD, configurar estas variables:
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
OPENAI_API_KEY=sk-test-mock-key  # Mock key, no real
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright  # Cache de navegadores
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Streamlit no inicia en tests

```bash
# Síntoma: Tests fallan con "Connection refused"
# Solución: Verificar puerto y permisos

# Debug
netstat -tulpn | grep 8502  # Verificar si puerto está ocupado
python -c "import streamlit; print(streamlit.__version__)"  # Verificar versión
```

#### 2. Playwright no encuentra elementos

```python
# Síntoma: TimeoutError esperando elementos
# Solución: Aumentar timeouts y verificar selectores

# Debug
await page.screenshot(path="debug.png")  # Capturar estado actual
print(await page.content())  # Ver HTML generado
```

#### 3. Mock no se aplica correctamente

```python
# Síntoma: Tests hacen llamadas reales a OpenAI
# Solución: Verificar patch y orden de imports

# Debug correcto
with patch('services.quote_service.QuoteService') as mock:
    # Configurar mock ANTES de importar/usar el servicio
    mock.return_value.generate_analysis.return_value = "test"
    
    # Ahora usar la funcionalidad
```

#### 4. Tests lentos o inestables

```bash
# Síntomas: Tests tardan mucho o fallan aleatoriamente
# Soluciones:

# 1. Usar headless mode
export PLAYWRIGHT_HEADLESS=true

# 2. Optimizar waits
await page.wait_for_load_state("networkidle")  # Esperar carga completa

# 3. Limpiar estado entre tests
await page.reload()  # Reset de página
```

### Logs y Debug

#### Habilitar logs detallados

```python
# En conftest.py
import logging
logging.basicConfig(level=logging.DEBUG)

# En tests específicos
@pytest.mark.asyncio
async def test_with_debug(page: Page):
    # Habilitar logs de Playwright
    page.on("console", lambda msg: print(f"Console: {msg.text}"))
    page.on("pageerror", lambda err: print(f"Error: {err}"))
    
    # Tu test aquí...
```

#### Capturar evidencia de fallos

```python
@pytest.fixture(autouse=True)
async def capture_on_failure(request, page: Page):
    yield
    
    if request.node.rep_call.failed:
        # Capturar screenshot en caso de fallo
        await page.screenshot(path=f"failure_{request.node.name}.png")
        
        # Guardar HTML
        with open(f"failure_{request.node.name}.html", "w") as f:
            f.write(await page.content())
```

## 📊 Métricas y Reportes

### Cobertura de Código

```bash
# Generar reporte completo
python scripts/run_tests.py --type coverage

# Ver reporte HTML
open htmlcov/index.html
```

### Reportes de Tests

```bash
# Reporte HTML de pytest
pytest --html=report.html --self-contained-html

# Reporte JUnit (para CI)
pytest --junitxml=junit.xml
```

### Métricas de Performance

```python
# En tests, medir tiempos
import time

start = time.time()
await page.click('[data-testid="stBaseButton-primary"]')
await page.locator("text=Análisis Filosófico").wait_for(state="visible")
duration = time.time() - start

assert duration < 10.0, f"Generación tardó {duration}s (máximo: 10s)"
```

---

## 🎯 Resumen Ejecutivo

### ✅ Lo que Tenemos

- **Framework E2E completo** con Playwright
- **Mock determinista** de OpenAI (cero variabilidad)
- **Tests reproducibles** al 100%
- **Selectores estables** usando `data-testid`
- **CI/CD ready** con configuración automática
- **Documentación completa** y scripts de automatización

### 🎪 Flujo Validado

1. **Usuario** hace click en botón principal
2. **Streamlit** procesa la solicitud
3. **Mock OpenAI** genera análisis determinista
4. **UI** muestra cita + análisis en contenedores correctos
5. **Tests** verifican cada paso automáticamente

### 🚀 Próximos Pasos

1. Ejecutar `python scripts/setup_testing.py`
2. Correr `python scripts/run_tests.py`
3. Integrar en pipeline de CI/CD
4. Expandir cobertura según necesidades

**¡Framework listo para producción!** 🎉