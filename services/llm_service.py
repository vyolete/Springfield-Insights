"""
Servicio para integración con GPT-4 y generación de análisis filosóficos
"""
import openai
from typing import Optional, Dict, Any
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Servicio para generar análisis filosóficos usando GPT-4"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
    
    def generate_philosophical_analysis(self, quote: str, character: str) -> Optional[str]:
        """
        Genera un análisis filosófico y contextual de una cita de Los Simpsons
        
        Args:
            quote: La cita a analizar
            character: El personaje que pronuncia la cita
            
        Returns:
            Análisis filosófico como string, o None si hay error
        """
        try:
            prompt = self._build_analysis_prompt(quote, character)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                timeout=settings.LLM_TIMEOUT
            )
            
            if response.choices and len(response.choices) > 0:
                analysis = response.choices[0].message.content.strip()
                return analysis
            
            logger.error("Respuesta vacía del modelo LLM")
            return None
            
        except openai.error.OpenAIError as e:
            logger.error(f"Error de OpenAI: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en LLMService: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """
        Prompt del sistema que define el comportamiento del LLM
        
        Returns:
            Prompt del sistema como string
        """
        return """Eres un experto en filosofía, crítica social y análisis cultural especializado en Los Simpsons. 
        Tu tarea es analizar citas de la serie desde una perspectiva académica, identificando:
        
        1. El significado filosófico subyacente
        2. La crítica social implícita
        3. El contexto cultural y moral
        4. La relevancia contemporánea
        
        Mantén un tono académico pero accesible, respetando la personalidad del personaje que pronuncia la cita.
        Utiliza un lenguaje claro y estructurado, evitando jerga excesivamente técnica."""
    
    def _build_analysis_prompt(self, quote: str, character: str) -> str:
        """
        Construye el prompt específico para analizar una cita
        
        Args:
            quote: La cita a analizar
            character: El personaje que la pronuncia
            
        Returns:
            Prompt formateado para el análisis
        """
        return f"""Analiza la siguiente cita de Los Simpsons desde una perspectiva filosófica y social:

Cita: "{quote}"
Personaje: {character}

Proporciona un análisis que incluya:

1. **Significado Filosófico**: ¿Qué conceptos o corrientes filosóficas refleja esta cita?

2. **Crítica Social**: ¿Qué aspectos de la sociedad contemporánea critica o satiriza?

3. **Contexto del Personaje**: ¿Cómo refleja esta cita la personalidad y visión del mundo de {character}?

4. **Relevancia Actual**: ¿Por qué esta reflexión sigue siendo relevante hoy?

Mantén un equilibrio entre rigor académico y accesibilidad, respetando el tono irónico característico de la serie."""
    
    def validate_analysis(self, analysis: str) -> bool:
        """
        Valida que el análisis generado tenga contenido útil
        
        Args:
            analysis: El análisis a validar
            
        Returns:
            True si el análisis es válido, False en caso contrario
        """
        if not analysis or not isinstance(analysis, str):
            return False
        
        # Verificar longitud mínima
        if len(analysis.strip()) < 100:
            return False
        
        # Verificar que contenga palabras clave esperadas
        keywords = ['filosófico', 'social', 'crítica', 'personaje', 'relevante']
        analysis_lower = analysis.lower()
        
        return any(keyword in analysis_lower for keyword in keywords)