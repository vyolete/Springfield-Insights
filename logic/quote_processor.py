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
        Obtiene contexto de personaje y genera reflexión filosófica completa
        Implementa nueva estrategia robusta sin dependencia de citas preexistentes
        
        Returns:
            Dict con la estructura: {
                'quote': str,           # Reflexión generada por LLM
                'character': str,       # Personaje de Los Simpsons
                'image': str,          # URL de imagen
                'analysis': str,       # Análisis filosófico profundo
                'success': bool,       # Estado de la operación
                'source': str,         # Fuente de los datos ('api' o 'fallback')
                'error_message': str   # Mensaje de error (opcional)
            }
        """
        try:
            # Obtener contexto del personaje (API o fallback)
            character_context = self.simpsons_service.get_random_quote()
            
            if not character_context or not character_context.get('success'):
                return self._create_error_response("D'oh! No se pudo obtener información de Springfield")
            
            # Extraer información del contexto
            character = character_context.get('character', 'Habitante de Springfield')
            description = character_context.get('description', 'Personaje de Los Simpsons')
            philosophical_context = character_context.get('philosophical_context', 'reflexión existencial')
            image_url = character_context.get('image', '')
            source = character_context.get('source', 'unknown')
            
            logger.info(f"🎭 Generando contenido para: {character} (fuente: {source})")
            
            # Obtener contexto de episodio si está disponible
            episode_context = character_context.get('episode_context')
            
            # Generar reflexión filosófica completa usando el LLM
            generated_content = self.llm_service.generate_complete_philosophical_reflection(
                character=character,
                description=description,
                philosophical_context=philosophical_context,
                episode_context=episode_context
            )
            
            if not generated_content:
                return self._create_error_response("Moe dice que el generador de sabiduría está roto...")
            
            # Validar contenido generado
            if not self._validate_generated_content(generated_content):
                return self._create_error_response("El contenido generado no cumple los estándares académicos")
            
            return {
                'quote': generated_content.get('reflection', ''),
                'character': character,
                'image': image_url,
                'analysis': generated_content.get('analysis', ''),
                'success': True,
                'source': source,
                'generation_method': 'llm_complete'
            }
            
        except Exception as e:
            logger.error(f"Error en QuoteProcessor.get_analyzed_quote: {e}")
            return self._create_error_response(f"¡Ay, caramba! Error interno: {str(e)}")
    
    def _validate_generated_content(self, content: Dict[str, Any]) -> bool:
        """
        Valida que el contenido generado por LLM sea académicamente apropiado
        
        Args:
            content: Contenido generado por el LLM
            
        Returns:
            True si el contenido es válido
        """
        if not isinstance(content, dict):
            return False
        
        # Verificar campos requeridos
        required_fields = ['reflection', 'analysis']
        if not all(field in content for field in required_fields):
            return False
        
        # Verificar longitud mínima para calidad académica
        reflection = content.get('reflection', '')
        analysis = content.get('analysis', '')
        
        if len(reflection.strip()) < 50:  # Reflexión muy corta
            return False
        
        if len(analysis.strip()) < 100:  # Análisis muy superficial
            return False
        
        # Verificar que no contenga placeholders o errores comunes
        problematic_phrases = [
            '[placeholder]', 'lorem ipsum', 'TODO', 'FIXME',
            'error', 'failed to generate', 'unable to create'
        ]
        
        full_text = (reflection + ' ' + analysis).lower()
        if any(phrase in full_text for phrase in problematic_phrases):
            return False
        
        return True
    
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