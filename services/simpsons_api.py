"""
Servicio para consumir la API de citas de Los Simpsons
"""
import requests
from typing import Dict, Optional, Any
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class SimpsonsAPIService:
    """Servicio para obtener citas de Los Simpsons desde la API pública"""
    
    def __init__(self):
        self.base_url = settings.SIMPSONS_API_BASE_URL
        self.timeout = settings.API_TIMEOUT
    
    def get_random_quote(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene una cita aleatoria de Los Simpsons
        
        Returns:
            Dict con la estructura: {
                'quote': str,
                'character': str,
                'image': str,
                'characterDirection': str
            }
        """
        try:
            response = requests.get(
                self.base_url,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # La API devuelve una lista, tomamos el primer elemento
            if isinstance(data, list) and len(data) > 0:
                quote_data = data[0]
                
                # Validar estructura esperada
                required_fields = ['quote', 'character']
                if all(field in quote_data for field in required_fields):
                    return quote_data
                else:
                    logger.error(f"Estructura de datos inesperada: {quote_data}")
                    return None
            
            logger.error(f"Formato de respuesta inesperado: {data}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar la API de Simpsons: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en SimpsonsAPIService: {e}")
            return None
    
    def validate_quote_data(self, quote_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de la cita tengan la estructura correcta
        
        Args:
            quote_data: Diccionario con los datos de la cita
            
        Returns:
            True si la estructura es válida, False en caso contrario
        """
        if not isinstance(quote_data, dict):
            return False
        
        required_fields = ['quote', 'character']
        return all(
            field in quote_data and 
            isinstance(quote_data[field], str) and 
            quote_data[field].strip()
            for field in required_fields
        )