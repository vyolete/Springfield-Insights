"""
Orquestador principal que coordina la obtención de citas y generación de análisis
"""
from typing import Optional, Dict, Any
import logging
from services.simpsons_api import SimpsonsAPIService
from services.llm_service import LLMService
from utils.validators import QuoteValidator

logger = logging.getLogger(__name__)

class QuoteProcessor:
    """Orquestador que coordina la obtención y análisis de citas"""
    
    def __init__(self):
        self.simpsons_service = SimpsonsAPIService()
        self.llm_service = LLMService()
        self.validator = QuoteValidator()
    
    def get_analyzed_quote(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene una cita aleatoria y genera su análisis filosófico
        
        Returns:
            Dict con la estructura: {
                'quote': str,
                'character': str,
                'image': str (opcional),
                'analysis': str,
                'success': bool,
                'error_message': str (opcional)
            }
        """
        try:
            # Obtener cita de la API
            quote_data = self.simpsons_service.get_random_quote()
            
            if not quote_data:
                return self._create_error_response("No se pudo obtener una cita de la API")
            
            # Validar datos de la cita
            if not self.validator.validate_quote_structure(quote_data):
                return self._create_error_response("Estructura de cita inválida")
            
            # Extraer información
            quote_text = quote_data.get('quote', '').strip()
            character = quote_data.get('character', '').strip()
            image_url = quote_data.get('image', '')
            
            # Validar contenido
            if not self.validator.validate_quote_content(quote_text, character):
                return self._create_error_response("Contenido de cita inválido")
            
            # Generar análisis filosófico
            analysis = self.llm_service.generate_philosophical_analysis(quote_text, character)
            
            if not analysis:
                return self._create_error_response("No se pudo generar el análisis filosófico")
            
            # Validar análisis
            if not self.llm_service.validate_analysis(analysis):
                return self._create_error_response("Análisis generado inválido")
            
            return {
                'quote': quote_text,
                'character': character,
                'image': image_url,
                'analysis': analysis,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error en QuoteProcessor.get_analyzed_quote: {e}")
            return self._create_error_response(f"Error interno: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Crea una respuesta de error estandarizada
        
        Args:
            error_message: Mensaje de error descriptivo
            
        Returns:
            Dict con estructura de error
        """
        return {
            'quote': '',
            'character': '',
            'image': '',
            'analysis': '',
            'success': False,
            'error_message': error_message
        }
    
    def retry_analysis(self, quote: str, character: str, max_retries: int = 2) -> Optional[str]:
        """
        Reintenta generar análisis en caso de fallo
        
        Args:
            quote: Texto de la cita
            character: Personaje que la pronuncia
            max_retries: Número máximo de reintentos
            
        Returns:
            Análisis generado o None si falla
        """
        for attempt in range(max_retries + 1):
            try:
                analysis = self.llm_service.generate_philosophical_analysis(quote, character)
                
                if analysis and self.llm_service.validate_analysis(analysis):
                    return analysis
                
                logger.warning(f"Intento {attempt + 1} falló, reintentando...")
                
            except Exception as e:
                logger.error(f"Error en intento {attempt + 1}: {e}")
        
        return None
    
    def get_quote_summary(self, quote_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Genera un resumen de la cita para mostrar en la interfaz
        
        Args:
            quote_data: Datos completos de la cita
            
        Returns:
            Dict con resumen formateado
        """
        if not quote_data.get('success', False):
            return {
                'title': 'Error',
                'subtitle': quote_data.get('error_message', 'Error desconocido'),
                'preview': ''
            }
        
        quote_preview = quote_data.get('quote', '')[:100]
        if len(quote_data.get('quote', '')) > 100:
            quote_preview += '...'
        
        return {
            'title': f"Cita de {quote_data.get('character', 'Desconocido')}",
            'subtitle': quote_preview,
            'preview': quote_data.get('analysis', '')[:200] + '...'
        }