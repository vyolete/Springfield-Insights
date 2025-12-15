"""
Configuración global de pytest para Springfield Insights
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Añadir el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def mock_openai_api_key():
    """Mock de API key para testing"""
    return "sk-test-mock-api-key-for-testing"

@pytest.fixture(scope="session")
def test_env_vars(mock_openai_api_key):
    """Configurar variables de entorno para testing"""
    os.environ["OPENAI_API_KEY"] = mock_openai_api_key
    yield
    # Cleanup
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

@pytest.fixture
def mock_openai_client():
    """Mock completo del cliente OpenAI"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = """1. **Significado Filosófico**: Esta reflexión de Homer Simpson encarna el hedonismo filosófico clásico, sugiriendo que el placer inmediato puede ser una respuesta válida a la complejidad existencial.

2. **Crítica Social**: Satiriza la cultura del consumo instantáneo y la búsqueda de gratificación inmediata como escape de las responsabilidades adultas.

3. **Contexto del Personaje**: Homer actúa como el arquetipo del "everyman" americano, reflejando las contradicciones entre aspiraciones y realidad en la clase trabajadora.

4. **Relevancia Contemporánea**: En la era de la dopamina digital, esta cita resuena con nuestra relación problemática con el placer y la procrastinación.

(Análisis generado por Mock para Testing)"""
    
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    
    return mock_client

@pytest.fixture
def mock_streamlit_secrets():
    """Mock de Streamlit secrets"""
    with patch('streamlit.secrets') as mock_secrets:
        mock_secrets.__getitem__.return_value = "sk-test-mock-api-key"
        yield mock_secrets