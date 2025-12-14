"""
Configuración de logging para Springfield Insights
"""
import logging
import os
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
    """
    Configura el sistema de logging de la aplicación
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, también guarda logs en archivo
    """
    
    # Crear directorio de logs si no existe
    if log_to_file:
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # Configurar formato de logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar logging básico
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format
    )
    
    # Configurar handler para archivo si se requiere
    if log_to_file:
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_filename = os.path.join("logs", f"springfield_insights_{timestamp}.log")
        
        # Crear file handler
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Crear formatter
        formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(formatter)
        
        # Agregar handler al logger raíz
        logging.getLogger().addHandler(file_handler)
    
    # Configurar loggers específicos
    configure_specific_loggers()

def configure_specific_loggers():
    """Configura loggers específicos para diferentes módulos"""
    
    # Logger para servicios externos (menos verboso)
    external_logger = logging.getLogger('services')
    external_logger.setLevel(logging.WARNING)
    
    # Logger para requests (menos verboso)
    requests_logger = logging.getLogger('urllib3')
    requests_logger.setLevel(logging.WARNING)
    
    # Logger para OpenAI (menos verboso)
    openai_logger = logging.getLogger('openai')
    openai_logger.setLevel(logging.WARNING)
    
    # Logger principal de la aplicación
    app_logger = logging.getLogger('springfield_insights')
    app_logger.setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico
    
    Args:
        name: Nombre del módulo
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(f'springfield_insights.{name}')