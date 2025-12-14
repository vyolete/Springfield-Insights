"""
Validadores y control de errores para Springfield Insights
"""
import re
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class QuoteValidator:
    """Validador para datos de citas y análisis"""
    
    def __init__(self):
        # Patrones para validación
        self.min_quote_length = 10
        self.max_quote_length = 500
        self.min_character_length = 2
        self.max_character_length = 50
    
    def validate_quote_structure(self, quote_data: Dict[str, Any]) -> bool:
        """
        Valida la estructura básica de los datos de una cita
        
        Args:
            quote_data: Diccionario con datos de la cita
            
        Returns:
            True si la estructura es válida, False en caso contrario
        """
        if not isinstance(quote_data, dict):
            logger.error("quote_data no es un diccionario")
            return False
        
        required_fields = ['quote', 'character']
        
        for field in required_fields:
            if field not in quote_data:
                logger.error(f"Campo requerido '{field}' no encontrado")
                return False
            
            if not isinstance(quote_data[field], str):
                logger.error(f"Campo '{field}' no es string")
                return False
        
        return True
    
    def validate_quote_content(self, quote: str, character: str) -> bool:
        """
        Valida el contenido de una cita y personaje
        
        Args:
            quote: Texto de la cita
            character: Nombre del personaje
            
        Returns:
            True si el contenido es válido, False en caso contrario
        """
        # Validar cita
        if not self._validate_quote_text(quote):
            return False
        
        # Validar personaje
        if not self._validate_character_name(character):
            return False
        
        return True
    
    def _validate_quote_text(self, quote: str) -> bool:
        """
        Valida el texto de una cita
        
        Args:
            quote: Texto de la cita a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        if not quote or not isinstance(quote, str):
            logger.error("Cita vacía o no es string")
            return False
        
        quote = quote.strip()
        
        # Validar longitud
        if len(quote) < self.min_quote_length:
            logger.error(f"Cita muy corta: {len(quote)} caracteres")
            return False
        
        if len(quote) > self.max_quote_length:
            logger.error(f"Cita muy larga: {len(quote)} caracteres")
            return False
        
        # Validar que no sea solo espacios o caracteres especiales
        if not re.search(r'[a-zA-Z]', quote):
            logger.error("Cita no contiene letras")
            return False
        
        return True
    
    def _validate_character_name(self, character: str) -> bool:
        """
        Valida el nombre de un personaje
        
        Args:
            character: Nombre del personaje a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        if not character or not isinstance(character, str):
            logger.error("Nombre de personaje vacío o no es string")
            return False
        
        character = character.strip()
        
        # Validar longitud
        if len(character) < self.min_character_length:
            logger.error(f"Nombre de personaje muy corto: {len(character)} caracteres")
            return False
        
        if len(character) > self.max_character_length:
            logger.error(f"Nombre de personaje muy largo: {len(character)} caracteres")
            return False
        
        # Validar que contenga al menos una letra
        if not re.search(r'[a-zA-Z]', character):
            logger.error("Nombre de personaje no contiene letras")
            return False
        
        return True
    
    def validate_api_key(self, api_key: Optional[str]) -> bool:
        """
        Valida que una API key tenga formato correcto
        
        Args:
            api_key: La API key a validar
            
        Returns:
            True si es válida, False en caso contrario
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        api_key = api_key.strip()
        
        # Validar longitud mínima (las API keys suelen ser largas)
        if len(api_key) < 20:
            return False
        
        # Validar que no contenga espacios
        if ' ' in api_key:
            return False
        
        return True
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitiza texto para mostrar en la interfaz
        
        Args:
            text: Texto a sanitizar
            
        Returns:
            Texto sanitizado
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remover caracteres de control
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

class ErrorHandler:
    """Manejador centralizado de errores"""
    
    @staticmethod
    def handle_api_error(error: Exception, context: str = "") -> str:
        """
        Maneja errores de API y devuelve mensaje amigable
        
        Args:
            error: La excepción capturada
            context: Contexto adicional del error
            
        Returns:
            Mensaje de error amigable para el usuario
        """
        error_msg = str(error).lower()
        
        if "timeout" in error_msg:
            return "La consulta tardó demasiado tiempo. Por favor, inténtalo de nuevo."
        
        if "connection" in error_msg or "network" in error_msg:
            return "Problema de conexión. Verifica tu conexión a internet."
        
        if "api key" in error_msg or "authentication" in error_msg:
            return "Error de autenticación. Verifica tu configuración de API."
        
        if "rate limit" in error_msg:
            return "Demasiadas consultas. Espera un momento antes de intentar de nuevo."
        
        # Error genérico
        logger.error(f"Error en {context}: {error}")
        return "Ocurrió un error inesperado. Por favor, inténtalo de nuevo."
    
    @staticmethod
    def log_error(error: Exception, context: str = "", user_id: str = None):
        """
        Registra errores en el log del sistema
        
        Args:
            error: La excepción a registrar
            context: Contexto donde ocurrió el error
            user_id: ID del usuario (opcional)
        """
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'user_id': user_id
        }
        
        logger.error(f"Error registrado: {error_info}")