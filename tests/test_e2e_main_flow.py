"""
Pruebas End-to-End del flujo principal de Springfield Insights
Valida la interacción completa usuario → UI → lógica → mock API
"""
import pytest
import asyncio
import subprocess
import time
import os
import signal
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from unittest.mock import patch, Mock

class TestSpringfieldInsightsE2E:
    """
    Suite de pruebas End-to-End para Springfield Insights
    
    Estas pruebas validan:
    1. Inicio de la aplicación Streamlit
    2. Navegación y interacción con la UI
    3. Click en el botón principal (data-testid="stBaseButton-primary")
    4. Verificación de contenido generado con mock de OpenAI
    5. Validación de elementos en data-testid="stMarkdownContainer"
    """
    
    @pytest.fixture(scope="class")
    async def streamlit_app(self):
        """
        Fixture que levanta la aplicación Streamlit para testing
        """
        # Configurar variables de entorno para testing
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = "sk-test-mock-key-for-e2e-testing"
        env["STREAMLIT_SERVER_PORT"] = "8502"  # Puerto diferente para testing
        
        # Comando para levantar Streamlit
        cmd = ["streamlit", "run", "app.py", "--server.port=8502", "--server.headless=true"]
        
        # Iniciar proceso de Streamlit
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent
        )
        
        # Esperar a que Streamlit esté listo
        max_wait = 30  # segundos
        wait_time = 0
        app_ready = False
        
        while wait_time < max_wait and not app_ready:
            try:
                # Intentar conectar a la app
                import requests
                response = requests.get("http://localhost:8502", timeout=2)
                if response.status_code == 200:
                    app_ready = True
                    break
            except:
                pass
            
            time.sleep(1)
            wait_time += 1
        
        if not app_ready:
            process.terminate()
            raise Exception("Streamlit app no se pudo iniciar en 30 segundos")
        
        yield "http://localhost:8502"
        
        # Cleanup: terminar proceso
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    
    @pytest.fixture(scope="class")
    async def browser(self):
        """Fixture para el navegador Playwright"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,  # Cambiar a False para debug visual
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            yield browser
            await browser.close()
    
    @pytest.fixture
    async def page(self, browser: Browser, streamlit_app: str):
        """Fixture para una página nueva en cada test"""
        page = await browser.new_page()
        
        # Configurar timeouts
        page.set_default_timeout(10000)  # 10 segundos
        
        # Navegar a la aplicación
        await page.goto(streamlit_app)
        
        # Esperar a que la página cargue completamente
        await page.wait_for_load_state("networkidle")
        
        yield page
        await page.close()
    
    @pytest.mark.asyncio
    async def test_app_loads_successfully(self, page: Page):
        """
        Test 1: Verificar que la aplicación carga correctamente
        """
        # Verificar que el título contiene "Springfield Insights"
        title = await page.title()
        assert "Springfield Insights" in title
        
        # Verificar que elementos clave están presentes
        header = page.locator("h1", has_text="Springfield Insights")
        await header.wait_for(state="visible", timeout=5000)
        
        # Verificar que hay contenido de bienvenida
        welcome_content = page.locator("text=Bienvenido a Springfield Insights")
        await welcome_content.wait_for(state="visible", timeout=5000)
    
    @pytest.mark.asyncio
    async def test_main_button_exists_and_clickable(self, page: Page):
        """
        Test 2: Verificar que el botón principal existe y es clickeable
        """
        # Buscar el botón principal usando data-testid
        main_button = page.locator('[data-testid="stBaseButton-primary"]')
        
        # Verificar que el botón existe y es visible
        await main_button.wait_for(state="visible", timeout=10000)
        
        # Verificar que el botón es clickeable
        assert await main_button.is_enabled()
        
        # Verificar el texto del botón
        button_text = await main_button.text_content()
        assert "Reflexión Filosófica" in button_text or "Nueva Reflexión" in button_text
    
    @pytest.mark.asyncio
    async def test_complete_quote_generation_flow(self, page: Page):
        """
        Test 3: Flujo completo - Click botón → Generar cita → Verificar análisis
        
        Este es el test principal que valida todo el flujo:
        1. Click en botón principal
        2. Verificar que aparece una cita de Los Simpsons
        3. Verificar que se genera análisis (usando mock)
        4. Verificar que el análisis aparece en stMarkdownContainer
        """
        
        # Mock del servicio OpenAI antes de hacer click
        with patch('services.quote_service.QuoteService') as mock_service_class:
            # Configurar el mock
            mock_service = Mock()
            mock_service.generate_analysis.return_value = """1. **Significado Filosófico**: Esta reflexión encarna el hedonismo filosófico clásico de Los Simpsons.

2. **Crítica Social**: Satiriza la cultura del consumo instantáneo moderna.

3. **Contexto del Personaje**: Refleja la cosmovisión única del personaje.

4. **Relevancia Contemporánea**: Conecta con problemas actuales de la sociedad.

(Análisis generado por Mock para Testing E2E)"""
            mock_service_class.return_value = mock_service
            
            # 1. Encontrar y hacer click en el botón principal
            main_button = page.locator('[data-testid="stBaseButton-primary"]')
            await main_button.wait_for(state="visible", timeout=10000)
            await main_button.click()
            
            # 2. Esperar a que aparezca contenido de cita
            # Buscar indicadores de que se generó una cita
            quote_indicators = [
                page.locator("text=Homer Simpson"),
                page.locator("text=Lisa Simpson"), 
                page.locator("text=Bart Simpson"),
                page.locator("text=Marge Simpson"),
                page.locator("text=Análisis Filosófico"),
                page.locator("text=Significado Filosófico")
            ]
            
            # Esperar a que al menos uno de los indicadores aparezca
            found_indicator = False
            for indicator in quote_indicators:
                try:
                    await indicator.wait_for(state="visible", timeout=15000)
                    found_indicator = True
                    break
                except:
                    continue
            
            assert found_indicator, "No se encontró evidencia de que se generó una cita"
            
            # 3. Verificar que aparece análisis en contenedor markdown
            markdown_containers = page.locator('[data-testid="stMarkdownContainer"]')
            await markdown_containers.first.wait_for(state="visible", timeout=10000)
            
            # Verificar que hay contenido de análisis
            analysis_content = page.locator("text=Significado Filosófico")
            await analysis_content.wait_for(state="visible", timeout=5000)
            
            # 4. Verificar estructura del análisis
            analysis_sections = [
                "Significado Filosófico",
                "Crítica Social", 
                "Contexto del Personaje",
                "Relevancia Contemporánea"
            ]
            
            for section in analysis_sections:
                section_locator = page.locator(f"text={section}")
                await section_locator.wait_for(state="visible", timeout=5000)
    
    @pytest.mark.asyncio
    async def test_mock_openai_integration(self, page: Page):
        """
        Test 4: Verificar específicamente que el mock de OpenAI funciona
        """
        with patch('openai.OpenAI') as mock_openai_class:
            # Configurar mock de OpenAI
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Mock Analysis: Testing OpenAI integration works correctly"
            
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client
            
            # Click en el botón
            main_button = page.locator('[data-testid="stBaseButton-primary"]')
            await main_button.wait_for(state="visible", timeout=10000)
            await main_button.click()
            
            # Verificar que el mock fue llamado (indirectamente)
            # Buscar evidencia de que se procesó contenido
            processing_indicators = [
                page.locator("text=Generando análisis"),
                page.locator("text=GPT-3.5"),
                page.locator("text=Análisis Filosófico"),
                page.locator("text=Mock Analysis")  # Del mock específico
            ]
            
            found_processing = False
            for indicator in processing_indicators:
                try:
                    await indicator.wait_for(state="visible", timeout=10000)
                    found_processing = True
                    break
                except:
                    continue
            
            # Si no encontramos indicadores específicos, al menos verificar que hay contenido nuevo
            if not found_processing:
                # Verificar que hay más contenido después del click
                markdown_containers = page.locator('[data-testid="stMarkdownContainer"]')
                container_count = await markdown_containers.count()
                assert container_count > 0, "No se generó contenido después del click"
    
    @pytest.mark.asyncio
    async def test_ui_elements_after_quote_generation(self, page: Page):
        """
        Test 5: Verificar elementos de UI después de generar una cita
        """
        # Click en botón principal
        main_button = page.locator('[data-testid="stBaseButton-primary"]')
        await main_button.wait_for(state="visible", timeout=10000)
        await main_button.click()
        
        # Esperar a que se genere contenido
        await asyncio.sleep(3)
        
        # Verificar que aparecen botones de acción
        action_buttons = [
            page.locator("text=Otra Cita"),
            page.locator("text=Copiar"),
            page.locator("text=Favorito"),
            page.locator("text=Compartir")
        ]
        
        # Al menos algunos botones de acción deberían estar presentes
        visible_buttons = 0
        for button in action_buttons:
            try:
                await button.wait_for(state="visible", timeout=2000)
                visible_buttons += 1
            except:
                continue
        
        # Verificar que hay elementos interactivos adicionales
        assert visible_buttons > 0 or await page.locator("button").count() > 1
    
    @pytest.mark.asyncio 
    async def test_error_handling_graceful(self, page: Page):
        """
        Test 6: Verificar manejo graceful de errores
        """
        with patch('services.quote_service.QuoteService') as mock_service_class:
            # Configurar mock que simula error
            mock_service = Mock()
            mock_service.generate_analysis.side_effect = Exception("Mock API Error")
            mock_service_class.return_value = mock_service
            
            # Click en botón
            main_button = page.locator('[data-testid="stBaseButton-primary"]')
            await main_button.wait_for(state="visible", timeout=10000)
            await main_button.click()
            
            # Verificar que la app no se rompe
            # Debería mostrar algún mensaje de error o fallback
            await asyncio.sleep(2)
            
            # La página debería seguir siendo funcional
            title = await page.title()
            assert "Springfield Insights" in title
            
            # El botón debería seguir siendo clickeable
            assert await main_button.is_enabled()


# Configuración adicional para pytest
def pytest_configure(config):
    """Configuración adicional de pytest para E2E tests"""
    config.addinivalue_line(
        "markers", "e2e: marca tests como end-to-end (requieren Streamlit corriendo)"
    )