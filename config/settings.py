"""
Configuración centralizada para Springfield Insights
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración centralizada de la aplicación"""
    
    def __init__(self):
        # Configuración de la aplicación
        self.APP_TITLE = "Springfield Insights"
        self.APP_VERSION = "1.0.0"
        
        # Variables de entorno
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        # Configuración del modelo OpenAI
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
        self.OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "400"))
        self.OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Instancia global de configuración
settings = Settings()