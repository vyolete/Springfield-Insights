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
        
        # Variables de entorno con soporte para Streamlit secrets
        self.OPENAI_API_KEY = self._get_secret_or_env("OPENAI_API_KEY")
        
        # Configuración del modelo OpenAI
        self.OPENAI_MODEL = self._get_secret_or_env("OPENAI_MODEL", "gpt-3.5-turbo")
        self.OPENAI_MAX_TOKENS = int(self._get_secret_or_env("OPENAI_MAX_TOKENS", "400"))
        self.OPENAI_TEMPERATURE = float(self._get_secret_or_env("OPENAI_TEMPERATURE", "0.7"))
    
    def _get_secret_or_env(self, key: str, default: str = None):
        """Obtiene valor de Streamlit secrets o variables de entorno"""
        try:
            import streamlit as st
            return st.secrets[key]
        except (KeyError, FileNotFoundError, ImportError):
            return os.getenv(key, default)

# Instancia global de configuración
settings = Settings()