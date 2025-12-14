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
    
    def generate_complete_philosophical_reflection(self, character: str, description: str, philosophical_context: str, episode_context: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """
        Genera una reflexión filosófica completa al estilo del personaje
        Nueva funcionalidad para crear contenido original académico con contexto de episodio
        
        Args:
            character: Nombre del personaje de Los Simpsons
            description: Descripción del personaje
            philosophical_context: Contexto filosófico del personaje
            episode_context: Contexto del episodio (opcional)
            
        Returns:
            Dict con 'reflection' y 'analysis', o None si hay error
        """
        try:
            prompt = self._build_complete_reflection_prompt(character, description, philosophical_context, episode_context)
            
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_complete_generation_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens * 2,  # Más tokens para contenido completo
                temperature=self.temperature,
                timeout=settings.LLM_TIMEOUT
            )
            
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content.strip()
                return self._parse_complete_response(content)
            
            logger.error("Respuesta vacía del modelo LLM para generación completa")
            return None
            
        except Exception as e:
            logger.error(f"Error generando reflexión completa: {e}")
            return None
    
    def _get_complete_generation_system_prompt(self) -> str:
        """
        Prompt del sistema para generación completa de contenido filosófico
        
        Returns:
            Prompt especializado para generación de contenido original
        """
        return """Eres un experto en filosofía y crítica social especializado en Los Simpsons. 
        Tu tarea es generar contenido filosófico original que capture la esencia de los personajes.
        
        Debes crear:
        1. Una reflexión filosófica auténtica al estilo del personaje
        2. Un análisis académico profundo de esa reflexión
        
        IMPORTANTE:
        - La reflexión debe sonar como algo que el personaje realmente diría
        - El análisis debe ser riguroso y académicamente sólido
        - Mantén el equilibrio entre humor inteligente y profundidad filosófica
        - Usa un lenguaje accesible pero académicamente apropiado
        
        Formato de respuesta:
        REFLEXIÓN: [La reflexión del personaje]
        ANÁLISIS: [El análisis filosófico académico]"""
    
    def _build_complete_reflection_prompt(self, character: str, description: str, philosophical_context: str, episode_context: Optional[Dict[str, str]] = None) -> str:
        """
        Construye el prompt para generar reflexión completa con contexto de episodio
        
        Args:
            character: Nombre del personaje
            description: Descripción del personaje  
            philosophical_context: Contexto filosófico
            episode_context: Contexto del episodio (opcional)
            
        Returns:
            Prompt formateado para generación completa
        """
        base_prompt = f"""Genera una reflexión filosófica original para {character} de Los Simpsons.

CONTEXTO DEL PERSONAJE:
- Nombre: {character}
- Descripción: {description}
- Contexto filosófico: {philosophical_context}"""

        # Añadir contexto de episodio si está disponible
        if episode_context:
            episode_section = f"""

CONTEXTO DEL EPISODIO:
- Episodio: {episode_context.get('episode_name', 'Desconocido')}
- Temporada: {episode_context.get('season', 'N/A')} • Episodio: {episode_context.get('episode_number', 'N/A')}
- Sinopsis: {episode_context.get('synopsis', 'No disponible')}
- Fecha de emisión: {episode_context.get('airdate', 'Desconocida')}

INSTRUCCIONES ESPECIALES:
La reflexión debe relacionarse con los temas y situaciones específicas del episodio "{episode_context.get('episode_name', '')}", 
incorporando elementos de la trama y el contexto narrativo en el análisis filosófico."""
            
            base_prompt += episode_section

        task_section = f"""

TAREA:
1. Crea una reflexión de 2-3 oraciones que {character} podría decir sobre la vida, la sociedad o la condición humana
2. La reflexión debe ser auténtica al personaje pero con profundidad filosófica
3. {"Si hay contexto de episodio, relaciona la reflexión con los temas del episodio" if episode_context else ""}
4. Genera un análisis académico que explore:
   - Los conceptos filosóficos presentes
   - La crítica social implícita
   - La relevancia contemporánea
   - El estilo característico del personaje
   {"- La conexión con la narrativa y temas del episodio específico" if episode_context else ""}

EJEMPLO DE ESTRUCTURA:
REFLEXIÓN: [Una reflexión auténtica del personaje{" relacionada con el episodio" if episode_context else ""}]
ANÁLISIS: [Análisis académico profundo de 250-350 palabras{"que incluya referencias al episodio" if episode_context else ""}]

Asegúrate de que tanto la reflexión como el análisis sean originales, académicamente rigurosos y fieles al espíritu de Los Simpsons."""

        return base_prompt + task_section
    
    def _parse_complete_response(self, content: str) -> Optional[Dict[str, str]]:
        """
        Parsea la respuesta del LLM para extraer reflexión y análisis
        
        Args:
            content: Contenido completo de la respuesta
            
        Returns:
            Dict con 'reflection' y 'analysis' separados
        """
        try:
            # Buscar marcadores de sección
            if "REFLEXIÓN:" in content and "ANÁLISIS:" in content:
                parts = content.split("ANÁLISIS:")
                reflection_part = parts[0].replace("REFLEXIÓN:", "").strip()
                analysis_part = parts[1].strip()
                
                return {
                    'reflection': reflection_part,
                    'analysis': analysis_part
                }
            
            # Fallback: dividir por párrafos si no hay marcadores
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            if len(paragraphs) >= 2:
                return {
                    'reflection': paragraphs[0],
                    'analysis': '\n\n'.join(paragraphs[1:])
                }
            
            # Último recurso: usar todo como reflexión
            return {
                'reflection': content[:200] + "..." if len(content) > 200 else content,
                'analysis': content
            }
            
        except Exception as e:
            logger.error(f"Error parseando respuesta completa: {e}")
            return None
    
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