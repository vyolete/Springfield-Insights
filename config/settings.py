"""
Configuración y variables de entorno para Springfield Insights
"""
import os
from typing import Optional

class Settings:
    """Configuración centralizada de la aplicación"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # URLs de APIs
    SIMPSONS_API_BASE_URL: str = "https://thesimpsonsquoteapi.glitch.me/quotes"
    
    # Configuración del modelo LLM
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 500
    OPENAI_TEMPERATURE: float = 0.7
    
    # Configuración de la aplicación
    APP_TITLE: str = "Springfield Insights"
    APP_DESCRIPTION: str = "Explorando la filosofía y crítica social de Los Simpsons"
    
    # Timeouts
    API_TIMEOUT: int = 10
    LLM_TIMEOUT: int = 30
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida que las configuraciones críticas estén presentes"""
        if not cls.OPENAI_API_KEY:
            return False
        return True

# Instancia global de configuración
settings = Settings()