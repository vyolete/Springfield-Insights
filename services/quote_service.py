"""
Servicio para generación de análisis filosóficos de citas de Los Simpsons
"""
import streamlit as st
from openai import OpenAI
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class QuoteService:
    """Servicio para generar análisis filosóficos usando GPT-4"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
    
    @st.cache_data(ttl=3600)
    def generate_analysis(_self, quote: str, character: str, context: str) -> str:
        """
        Genera análisis filosófico usando GPT-3.5-Turbo
        """
        try:
            prompt = _self._build_analysis_prompt(quote, character, context)
            
            response = _self.client.chat.completions.create(
                model=_self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": _self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.7,
                timeout=15
            )
            
            # Incrementar contador de análisis
            if 'analyses_generated' not in st.session_state:
                st.session_state.analyses_generated = 0
            st.session_state.analyses_generated += 1
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback Mock para modo Demo
            import random
            err_str = str(e)
            if "insufficient_quota" in err_str or "429" in err_str or "404" in err_str or "model_not_found" in err_str:
                mock_analyses = [
                    f"""1. **Significado Filosófico**: La afirmación de {character} resuena con un nihilismo optimista, sugiriendo que en un universo indiferente, la subjetividad del individuo es la única fuente de sentido.
                    
2. **Crítica Social**: Satiriza la obsesión moderna con la productividad y el significado, exponiendo la fragilidad de nuestras construcciones sociales ante la realidad absurda.

3. **Contexto del Personaje**: Refleja la visión única de {character}, quien a menudo actúa como un espejo distorsionado de nuestras propias inseguridades y contradicciones.

4. **Relevancia Contemporánea**: En la era digital, esta reflexión nos invita a cuestionar las narrativas de éxito impuestas y buscar una autenticidad más allá del consumo.

(Nota: Análisis generado en Modo Demo debido a límites de API)""",
                    f"""1. **Significado Filosófico**: Este planteamiento evoca el absurdismo de Camus. {character} confronta la irracionalidad del mundo no con desesperación, sino con una aceptación irónica.

2. **Crítica Social**: Una crítica mordaz al conformismo de la clase media y a las instituciones que perpetúan ciclos de alienación bajo la promesa de estabilidad.

3. **Contexto del Personaje**: {character} demuestra aquí su rol como el 'tonto sabio', revelando verdades incómodas a través de una aparente simplicidad o cinismo.

4. **Relevancia Contemporánea**: Nos recuerda la importancia de mantener un pensamiento crítico frente a la saturación informativa y la posverdad.

(Nota: Análisis generado en Modo Demo debido a límites de API)"""
                ]
                logger.warning(f"Usando Mock Analysis por error API: {e}")
                return random.choice(mock_analyses)

            logger.error(f"Error generando análisis: {e}")
            return f"Error generando análisis: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        """Prompt del sistema para GPT-4"""
        return """Eres un experto en filosofía especializado en análisis cultural de Los Simpsons. 
        Tu tarea es generar análisis académicos rigurosos pero accesibles que exploren la 
        profundidad filosófica y crítica social presente en las citas de la serie.
        
        Mantén un equilibrio entre rigor académico y claridad, usando referencias filosóficas 
        apropiadas y conectando con temas contemporáneos relevantes."""
    
    def _build_analysis_prompt(self, quote: str, character: str, context: str) -> str:
        """Construye el prompt específico para el análisis"""
        return f"""Analiza esta cita de Los Simpsons desde una perspectiva filosófica profunda:

Cita: "{quote}"
Personaje: {character}
Contexto: {context}

Proporciona un análisis académico riguroso de 200-250 palabras que incluya:

1. **Significado Filosófico**: Identifica corrientes filosóficas específicas (existencialismo, nihilismo, hedonismo, etc.) y conceptos clave presentes en la cita.

2. **Crítica Social**: Analiza qué aspectos de la sociedad contemporánea satiriza o critica esta reflexión, incluyendo referencias a instituciones, valores culturales o comportamientos sociales.

3. **Contexto del Personaje**: Explica cómo esta cita refleja la cosmovisión particular de {character} y su rol como arquetipo social en la serie.

4. **Relevancia Contemporánea**: Conecta el mensaje con problemas actuales de la sociedad, política, tecnología o cultura.

5. **Profundidad Académica**: Incluye referencias a pensadores o teorías filosóficas relevantes cuando sea apropiado.

Mantén un equilibrio entre rigor académico y accesibilidad, usando un lenguaje claro pero sofisticado."""