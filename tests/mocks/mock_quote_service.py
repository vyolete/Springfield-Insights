"""
Mock del QuoteService para testing reproducible
"""
import random
from typing import Dict, Any

class MockQuoteService:
    """
    Mock determinista del QuoteService que simula la integración con OpenAI
    sin hacer llamadas reales a la API.
    
    Características:
    - Respuestas deterministas basadas en el input
    - Simula latencia realista
    - Incluye casos de error controlados
    - Compatible con la interfaz original
    """
    
    def __init__(self, simulate_errors: bool = False):
        self.simulate_errors = simulate_errors
        self.call_count = 0
        
        # Análisis predefinidos para testing determinista
        self.mock_analyses = {
            "homer": """1. **Significado Filosófico**: Esta reflexión de Homer Simpson encarna el hedonismo filosófico clásico, sugiriendo que el placer inmediato puede ser una respuesta válida a la complejidad existencial.

2. **Crítica Social**: Satiriza la cultura del consumo instantáneo y la búsqueda de gratificación inmediata como escape de las responsabilidades adultas.

3. **Contexto del Personaje**: Homer actúa como el arquetipo del "everyman" americano, reflejando las contradicciones entre aspiraciones y realidad en la clase trabajadora.

4. **Relevancia Contemporánea**: En la era de la dopamina digital, esta cita resuena con nuestra relación problemática con el placer y la procrastinación.

(Análisis generado por Mock para Testing)""",
            
            "lisa": """1. **Significado Filosófico**: La perspectiva de Lisa Simpson refleja un idealismo kantiano, donde la razón y la moral universal guían las acciones hacia un bien mayor.

2. **Crítica Social**: Critica el anti-intelectualismo contemporáneo y la devaluación del conocimiento en favor del entretenimiento superficial.

3. **Contexto del Personaje**: Lisa representa la voz de la conciencia moral y intelectual, funcionando como contrapunto a la mediocridad circundante.

4. **Relevancia Contemporánea**: Su mensaje resuena en debates actuales sobre educación, cambio climático y justicia social en una sociedad polarizada.

(Análisis generado por Mock para Testing)""",
            
            "bart": """1. **Significado Filosófico**: Bart Simpson encarna la filosofía de la transgresión constructiva, donde la rebeldía juvenil cuestiona estructuras de autoridad obsoletas.

2. **Crítica Social**: Satiriza el sistema educativo rígido y las expectativas sociales que reprimen la creatividad y el pensamiento crítico.

3. **Contexto del Personaje**: Bart funciona como el "trickster" arquetípico, usando el caos para revelar hipocresías institucionales.

4. **Relevancia Contemporánea**: Su actitud resuena con movimientos de desobediencia civil y cuestionamiento de autoridades en la era digital.

(Análisis generado por Mock para Testing)""",
            
            "marge": """1. **Significado Filosófico**: Marge Simpson representa la ética del cuidado de Carol Gilligan, priorizando relaciones y responsabilidad moral sobre reglas abstractas.

2. **Crítica Social**: Critica la invisibilización del trabajo emocional femenino y las expectativas de perfección maternal en la sociedad patriarcal.

3. **Contexto del Personaje**: Marge actúa como el ancla moral de la familia, equilibrando caos y estabilidad con sabiduría práctica.

4. **Relevancia Contemporánea**: Su perspectiva es crucial en debates sobre conciliación familiar, salud mental y roles de género en evolución.

(Análisis generado por Mock para Testing)"""
        }
    
    def generate_analysis(self, quote: str, character: str, context: str) -> str:
        """
        Simula la generación de análisis filosófico de manera determinista
        
        Args:
            quote: La cita a analizar
            character: El personaje que dijo la cita
            context: Contexto de la cita
            
        Returns:
            Análisis filosófico mock determinista
        """
        self.call_count += 1
        
        # Simular error ocasional para testing de manejo de errores
        if self.simulate_errors and self.call_count % 5 == 0:
            raise Exception("Mock API Error: Rate limit exceeded")
        
        # Determinar qué análisis usar basado en el personaje
        character_lower = character.lower()
        
        if "homer" in character_lower:
            base_analysis = self.mock_analyses["homer"]
        elif "lisa" in character_lower:
            base_analysis = self.mock_analyses["lisa"]
        elif "bart" in character_lower:
            base_analysis = self.mock_analyses["bart"]
        elif "marge" in character_lower:
            base_analysis = self.mock_analyses["marge"]
        else:
            # Análisis genérico para personajes no reconocidos
            base_analysis = self.mock_analyses["homer"].replace("Homer Simpson", character)
        
        # Personalizar el análisis con la cita específica
        personalized_analysis = base_analysis.replace(
            "Esta reflexión", 
            f'La cita "{quote[:50]}..." '
        )
        
        return personalized_analysis
    
    def get_call_count(self) -> int:
        """Retorna el número de llamadas realizadas (útil para testing)"""
        return self.call_count
    
    def reset_call_count(self):
        """Resetea el contador de llamadas"""
        self.call_count = 0


def create_mock_quote_service(simulate_errors: bool = False) -> MockQuoteService:
    """
    Factory function para crear instancias del mock service
    
    Args:
        simulate_errors: Si debe simular errores ocasionales
        
    Returns:
        Instancia configurada de MockQuoteService
    """
    return MockQuoteService(simulate_errors=simulate_errors)