"""
Configuración y variables de entorno para Springfield Insights
Implementa gestión segura de credenciales y validación robusta
"""
import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path
import logging

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    
    # Buscar archivo .env en el directorio actual y directorios padre
    env_path = Path('.env')
    if not env_path.exists():
        # Buscar en directorio padre (útil cuando se ejecuta desde subdirectorios)
        parent_env = Path('../.env')
        if parent_env.exists():
            env_path = parent_env
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Variables de entorno cargadas desde: {env_path.absolute()}")
    else:
        print("⚠️  Archivo .env no encontrado. Usando variables del sistema.")
        
except ImportError:
    print("⚠️  python-dotenv no instalado. Usando solo variables del sistema.")

class Settings:
    """
    Configuración centralizada y segura de la aplicación
    Implementa validación robusta y gestión de errores académica
    """
    
    # ========================================
    # CONFIGURACIÓN DE SEGURIDAD
    # ========================================
    
    # API Keys (nunca hardcodeadas)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # ========================================
    # CONFIGURACIÓN DE APIs EXTERNAS
    # ========================================
    
    # URL base de la API de Simpsons
    SIMPSONS_API_BASE_URL: str = os.getenv(
        "SIMPSONS_API_BASE_URL", 
        "https://thesimpsonsquoteapi.glitch.me/quotes"
    )
    
    # ========================================
    # CONFIGURACIÓN DEL MODELO LLM
    # ========================================
    
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Cambiado para velocidad
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "300"))  # Reducido drásticamente
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.5"))  # Optimizado para velocidad
    
    # ========================================
    # CONFIGURACIÓN DE LA APLICACIÓN
    # ========================================
    
    APP_TITLE: str = "Springfield Insights"
    APP_DESCRIPTION: str = "Explorando la filosofía y crítica social de Los Simpsons"
    APP_VERSION: str = "1.0.0"
    
    # ========================================
    # CONFIGURACIÓN DE TIMEOUTS Y RENDIMIENTO (OPTIMIZADA)
    # ========================================
    
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "5"))  # Muy agresivo para APIs
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "10"))  # Timeout muy agresivo para LLM
    
    # ========================================
    # CONFIGURACIÓN DE DESARROLLO
    # ========================================
    
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Valida la configuración completa y retorna reporte detallado
        
        Returns:
            Dict con estado de validación y errores encontrados
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'config_summary': {}
        }
        
        # Validar API Key de OpenAI (crítica)
        if not cls.OPENAI_API_KEY:
            validation_result['is_valid'] = False
            validation_result['errors'].append(
                "OPENAI_API_KEY no configurada. Requerida para análisis filosófico."
            )
        elif len(cls.OPENAI_API_KEY) < 20:
            validation_result['is_valid'] = False
            validation_result['errors'].append(
                "OPENAI_API_KEY parece inválida (muy corta)."
            )
        elif not cls.OPENAI_API_KEY.startswith(('sk-', 'sk-proj-')):
            validation_result['warnings'].append(
                "OPENAI_API_KEY no tiene el formato esperado de OpenAI."
            )
        
        # Validar URL de API de Simpsons
        if not cls.SIMPSONS_API_BASE_URL:
            validation_result['warnings'].append(
                "SIMPSONS_API_BASE_URL no configurada, usando valor por defecto."
            )
        
        # Validar configuración del modelo
        if cls.OPENAI_MAX_TOKENS < 100 or cls.OPENAI_MAX_TOKENS > 4000:
            validation_result['warnings'].append(
                f"OPENAI_MAX_TOKENS ({cls.OPENAI_MAX_TOKENS}) fuera del rango recomendado (100-4000)."
            )
        
        if cls.OPENAI_TEMPERATURE < 0 or cls.OPENAI_TEMPERATURE > 2:
            validation_result['warnings'].append(
                f"OPENAI_TEMPERATURE ({cls.OPENAI_TEMPERATURE}) fuera del rango válido (0-2)."
            )
        
        # Validar timeouts
        if cls.API_TIMEOUT < 5:
            validation_result['warnings'].append(
                f"API_TIMEOUT ({cls.API_TIMEOUT}s) muy bajo, puede causar errores."
            )
        
        if cls.LLM_TIMEOUT < 10:
            validation_result['warnings'].append(
                f"LLM_TIMEOUT ({cls.LLM_TIMEOUT}s) muy bajo para GPT-4."
            )
        
        # Generar resumen de configuración (sin datos sensibles)
        validation_result['config_summary'] = {
            'openai_key_configured': bool(cls.OPENAI_API_KEY),
            'openai_model': cls.OPENAI_MODEL,
            'max_tokens': cls.OPENAI_MAX_TOKENS,
            'temperature': cls.OPENAI_TEMPERATURE,
            'api_timeout': cls.API_TIMEOUT,
            'llm_timeout': cls.LLM_TIMEOUT,
            'debug_mode': cls.DEBUG_MODE,
            'log_level': cls.LOG_LEVEL
        }
        
        return validation_result
    
    @classmethod
    def get_safe_config_display(cls) -> Dict[str, Any]:
        """
        Retorna configuración para mostrar (sin datos sensibles)
        
        Returns:
            Dict con configuración segura para mostrar
        """
        return {
            'app_title': cls.APP_TITLE,
            'app_version': cls.APP_VERSION,
            'openai_model': cls.OPENAI_MODEL,
            'max_tokens': cls.OPENAI_MAX_TOKENS,
            'temperature': cls.OPENAI_TEMPERATURE,
            'api_timeout': f"{cls.API_TIMEOUT}s",
            'llm_timeout': f"{cls.LLM_TIMEOUT}s",
            'debug_mode': cls.DEBUG_MODE,
            'log_level': cls.LOG_LEVEL,
            'openai_key_status': '✅ Configurada' if cls.OPENAI_API_KEY else '❌ No configurada'
        }
    
    @classmethod
    def print_startup_banner(cls):
        """Imprime banner de inicio con información de configuración"""
        
        print("\n" + "="*60)
        print("🍩 SPRINGFIELD INSIGHTS - CONFIGURACIÓN LOCAL")
        print("="*60)
        
        config = cls.get_safe_config_display()
        
        print(f"📱 Aplicación: {config['app_title']} v{config['app_version']}")
        print(f"🤖 Modelo IA: {config['openai_model']}")
        print(f"🔑 API Key: {config['openai_key_status']}")
        print(f"⚙️  Configuración: Tokens={config['max_tokens']}, Temp={config['temperature']}")
        print(f"⏱️  Timeouts: API={config['api_timeout']}, LLM={config['llm_timeout']}")
        print(f"🔧 Debug: {config['debug_mode']}, Log: {config['log_level']}")
        
        # Validar configuración
        validation = cls.validate_config()
        
        if validation['is_valid']:
            print("✅ Configuración válida - Lista para ejecutar")
        else:
            print("❌ Errores de configuración encontrados:")
            for error in validation['errors']:
                print(f"   • {error}")
        
        if validation['warnings']:
            print("⚠️  Advertencias de configuración:")
            for warning in validation['warnings']:
                print(f"   • {warning}")
        
        print("="*60 + "\n")
        
        return validation['is_valid']

# Instancia global de configuración
settings = Settings()

# Función de utilidad para validación rápida
def validate_environment() -> bool:
    """
    Función de utilidad para validación rápida del entorno
    
    Returns:
        True si el entorno está correctamente configurado
    """
    validation = settings.validate_config()
    return validation['is_valid']