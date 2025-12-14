"""
Servicio OPTIMIZADO para integración con GPT-4 y generación de análisis filosóficos
"""
from openai import OpenAI
from typing import Optional, Dict, Any
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Servicio para generar análisis filosóficos usando GPT-4"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
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
            
            response = self.client.chat.completions.create(
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
            
        except Exception as e:
            logger.error(f"Error en LLMService: {e}")
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
        OPTIMIZADO: Cache inteligente, timeouts reducidos, prompts más eficientes
        
        Args:
            character: Nombre del personaje de Los Simpsons
            description: Descripción del personaje
            philosophical_context: Contexto filosófico del personaje
            episode_context: Contexto del episodio (opcional)
            
        Returns:
            Dict con 'reflection' y 'analysis', o None si hay error
        """
        import time
        start_time = time.time()
        
        try:
            # Crear hash del contenido para cache
            from services.cache_optimizer import cache_optimizer
            from services.performance_monitor import performance_monitor
            import hashlib
            
            content_for_hash = f"{character}|{description}|{philosophical_context}|{episode_context or ''}"
            content_hash = hashlib.md5(content_for_hash.encode()).hexdigest()
            
            # Intentar obtener del cache primero
            cached_response = cache_optimizer.get_cached_llm_response(content_hash)
            if cached_response:
                logger.info(f"⚡ LLM cache hit for {character}")
                performance_monitor.track_llm_response(start_time, character, True)
                return self._parse_complete_response(cached_response)
            
            # Si no está en cache, generar nueva respuesta con configuración ultra-optimizada
            prompt = self._build_optimized_reflection_prompt(character, description, philosophical_context, episode_context)
            
            # Configuración ULTRA-OPTIMIZADA para máxima velocidad
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Cambiar a GPT-3.5 para velocidad
                messages=[
                    {
                        "role": "system",
                        "content": self._get_optimized_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=300,  # Reducir drásticamente para velocidad
                temperature=0.5,  # Temperatura baja para consistencia
                timeout=10  # Timeout muy agresivo
            )
            
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content.strip()
                
                # Cachear la respuesta
                cache_optimizer.cache_llm_response(content_hash, content, ttl=86400)  # 24 horas
                logger.info(f"🎭 LLM response generated and cached for {character} in {time.time() - start_time:.2f}s")
                
                performance_monitor.track_llm_response(start_time, character, True)
                return self._parse_complete_response(content)
            
            logger.error("Respuesta vacía del modelo LLM para generación completa")
            performance_monitor.track_llm_response(start_time, character, False)
            return None
            
        except Exception as e:
            logger.error(f"Error generando reflexión completa: {e}")
            performance_monitor.track_llm_response(start_time, character, False)
            return None
    
    def _get_optimized_system_prompt(self) -> str:
        """
        Prompt del sistema ULTRA-OPTIMIZADO para máxima velocidad
        
        Returns:
            Prompt mínimo y eficiente
        """
        return """Experto en Los Simpsons. Genera:
REFLEXIÓN: 2 oraciones del personaje sobre vida/sociedad
ANÁLISIS: 100-150 palabras sobre filosofía y crítica social

Formato:
REFLEXIÓN: [texto]
ANÁLISIS: [texto]

Sé conciso, auténtico y académico."""
    
    def _build_optimized_reflection_prompt(self, character: str, description: str, philosophical_context: str, episode_context: Optional[Dict[str, str]] = None) -> str:
        """
        Construye prompt OPTIMIZADO para velocidad y eficiencia
        
        Args:
            character: Nombre del personaje
            description: Descripción del personaje  
            philosophical_context: Contexto filosófico
            episode_context: Contexto del episodio (opcional)
            
        Returns:
            Prompt conciso y eficiente
        """
        # Prompt base optimizado
        base_prompt = f"""Personaje: {character}
Contexto: {description} - {philosophical_context}"""

        # Contexto de episodio simplificado
        if episode_context:
            episode_name = episode_context.get('episode_name', '')
            synopsis = episode_context.get('synopsis', '')[:100]  # Limitar sinopsis
            base_prompt += f"""
Episodio: "{episode_name}" - {synopsis}"""

        # Instrucciones ultra-concisas
        task_prompt = f"""

{character}: Genera reflexión (2 oraciones) + análisis (100 palabras) sobre vida/sociedad{"del episodio" if episode_context else ""}."""

        return base_prompt + task_prompt
    
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