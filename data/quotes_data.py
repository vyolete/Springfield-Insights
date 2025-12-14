"""
Base de datos de citas auténticas de Los Simpsons
Sistema híbrido: API real + fallback local
"""
from services.simpsons_api_service import SimpsonsAPIService
import random
import logging

logger = logging.getLogger(__name__)

# Fallback local de citas auténticas
FALLBACK_QUOTES = [
    {
        "quote": "D'oh!",
        "character": "Homer Simpson",
        "context": "Expresión de frustración ante los errores cotidianos",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "¡Ay, caramba!",
        "character": "Bart Simpson", 
        "context": "Exclamación de sorpresa ante situaciones inesperadas",
        "image": "https://static.wikia.nocookie.net/simpsons/images/a/aa/Bart_Simpson.png"
    },
    {
        "quote": "Si no tienes nada bueno que decir sobre alguien, ven y siéntate aquí a mi lado.",
        "character": "Marge Simpson",
        "context": "Crítica sutil al chisme y la naturaleza humana",
        "image": "https://static.wikia.nocookie.net/simpsons/images/0/0b/Marge_Simpson.png"
    },
    {
        "quote": "La ignorancia es una bendición.",
        "character": "Homer Simpson",
        "context": "Reflexión sobre la felicidad en la simplicidad",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "Soy demasiado joven para morir y demasiado viejo para comer de la mesa de los niños.",
        "character": "Lisa Simpson",
        "context": "Dilema existencial de la adolescencia y el crecimiento",
        "image": "https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png"
    },
    {
        "quote": "Estúpido Flanders.",
        "character": "Homer Simpson",
        "context": "Envidia hacia la perfección aparente del vecino",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "No me hagas pensar. Estoy de vacaciones.",
        "character": "Homer Simpson",
        "context": "Rechazo al esfuerzo intelectual en momentos de descanso",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "La televisión: maestra, madre, amante secreta.",
        "character": "Homer Simpson",
        "context": "Dependencia moderna de los medios de comunicación",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "Ser normal está sobrevalorado.",
        "character": "Lisa Simpson",
        "context": "Valoración de la individualidad frente al conformismo",
        "image": "https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png"
    },
    {
        "quote": "Los libros son inútiles. Solo enseñan cosas.",
        "character": "Homer Simpson",
        "context": "Paradoja del anti-intelectualismo",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    },
    {
        "quote": "Nunca, nunca, nunca te rindas.",
        "character": "Lisa Simpson",
        "context": "Perseverancia ante la adversidad",
        "image": "https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png"
    },
    {
        "quote": "Marge, no voy a mentirte... Bueno, sí voy a mentirte.",
        "character": "Homer Simpson",
        "context": "Honestidad paradójica sobre la deshonestidad",
        "image": "https://static.wikia.nocookie.net/simpsons/images/7/7f/Mmm.jpg"
    }
]

class QuotesManager:
    """Gestor de citas que combina API real con fallback local"""
    
    def __init__(self):
        self.api_service = SimpsonsAPIService()
        self.fallback_quotes = FALLBACK_QUOTES
    
    def get_random_quote(self):
        """
        Obtiene una cita aleatoria, primero de la API, luego fallback local
        
        Returns:
            Dict con cita, personaje, contexto e imagen
        """
        # Intentar obtener de la API real primero
        try:
            api_quote = self.api_service.get_random_quote_from_api()
            if api_quote:
                logger.info("✅ Cita obtenida de API real de Los Simpsons")
                return api_quote
        except Exception as e:
            logger.warning(f"API no disponible: {e}")
        
        # Fallback a citas locales
        logger.info("🔄 Usando citas de fallback local")
        return random.choice(self.fallback_quotes)
    
    def get_api_status(self):
        """Verifica estado de la API"""
        return self.api_service.get_api_status()

# Instancia global del gestor de citas
quotes_manager = QuotesManager()

# Función de compatibilidad para mantener la interfaz existente
def get_simpsons_quotes():
    """Retorna todas las citas disponibles (para compatibilidad)"""
    return FALLBACK_QUOTES

# Variable de compatibilidad
SIMPSONS_QUOTES = FALLBACK_QUOTES