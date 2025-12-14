"""
Análisis y métricas de citas y análisis filosóficos
"""
import re
from typing import Dict, List, Any, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class QuoteAnalytics:
    """Analizador de patrones y métricas en citas y análisis"""
    
    def __init__(self):
        self.philosophical_keywords = [
            'existencial', 'moral', 'ético', 'filosófico', 'ontológico',
            'epistemológico', 'fenomenológico', 'dialéctico', 'hermenéutico',
            'nihilismo', 'humanismo', 'racionalismo', 'empirismo',
            'pragmatismo', 'utilitarismo', 'deontología', 'virtud'
        ]
        
        self.social_critique_keywords = [
            'capitalismo', 'consumismo', 'alienación', 'burocracia',
            'poder', 'autoridad', 'clase social', 'desigualdad',
            'corrupción', 'medios', 'propaganda', 'ideología',
            'conformismo', 'individualismo', 'colectivismo'
        ]
        
        self.emotional_indicators = [
            'ironía', 'sarcasmo', 'humor', 'melancolía', 'nostalgia',
            'esperanza', 'desesperanza', 'optimismo', 'pesimismo',
            'cinismo', 'ingenuidad', 'sabiduría', 'ignorancia'
        ]
    
    def analyze_quote_complexity(self, quote: str) -> Dict[str, Any]:
        """
        Analiza la complejidad lingüística y conceptual de una cita
        
        Args:
            quote: Texto de la cita a analizar
            
        Returns:
            Diccionario con métricas de complejidad
        """
        words = quote.split()
        sentences = re.split(r'[.!?]+', quote)
        
        # Métricas básicas
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        
        # Complejidad léxica
        unique_words = len(set(word.lower().strip('.,!?;:') for word in words))
        lexical_diversity = unique_words / max(word_count, 1)
        
        # Longitud promedio de palabras
        avg_word_length = sum(len(word.strip('.,!?;:')) for word in words) / max(word_count, 1)
        
        # Detectar estructuras complejas
        complex_structures = {
            'subordinate_clauses': len(re.findall(r'\b(que|cuando|donde|como|si|aunque|porque|para que|a fin de que)\b', quote.lower())),
            'conjunctions': len(re.findall(r'\b(y|o|pero|sin embargo|no obstante|además|por tanto|así que)\b', quote.lower())),
            'questions': len(re.findall(r'\?', quote)),
            'exclamations': len(re.findall(r'!', quote))
        }
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'lexical_diversity': round(lexical_diversity, 3),
            'avg_word_length': round(avg_word_length, 2),
            'complexity_score': self._calculate_complexity_score(
                avg_words_per_sentence, lexical_diversity, avg_word_length, complex_structures
            ),
            'structural_elements': complex_structures
        }
    
    def analyze_philosophical_content(self, analysis: str) -> Dict[str, Any]:
        """
        Analiza el contenido filosófico de un análisis generado
        
        Args:
            analysis: Texto del análisis filosófico
            
        Returns:
            Diccionario con métricas filosóficas
        """
        analysis_lower = analysis.lower()
        
        # Detectar corrientes filosóficas mencionadas
        philosophical_matches = [
            keyword for keyword in self.philosophical_keywords
            if keyword in analysis_lower
        ]
        
        # Detectar crítica social
        social_critique_matches = [
            keyword for keyword in self.social_critique_keywords
            if keyword in analysis_lower
        ]
        
        # Detectar tono emocional
        emotional_matches = [
            keyword for keyword in self.emotional_indicators
            if keyword in analysis_lower
        ]
        
        # Analizar estructura del análisis
        sections = self._identify_analysis_sections(analysis)
        
        # Calcular profundidad conceptual
        conceptual_depth = self._calculate_conceptual_depth(
            philosophical_matches, social_critique_matches, sections
        )
        
        return {
            'philosophical_schools': philosophical_matches,
            'social_critique_elements': social_critique_matches,
            'emotional_tone_indicators': emotional_matches,
            'analysis_sections': sections,
            'conceptual_depth_score': conceptual_depth,
            'academic_rigor_score': self._calculate_academic_rigor(analysis),
            'accessibility_score': self._calculate_accessibility(analysis)
        }
    
    def analyze_character_patterns(self, quotes_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analiza patrones por personaje en múltiples citas
        
        Args:
            quotes_data: Lista de datos de citas con análisis
            
        Returns:
            Diccionario con patrones por personaje
        """
        character_stats = {}
        
        for quote_data in quotes_data:
            character = quote_data.get('character', 'Unknown')
            quote = quote_data.get('quote', '')
            analysis = quote_data.get('analysis', '')
            
            if character not in character_stats:
                character_stats[character] = {
                    'quote_count': 0,
                    'total_words': 0,
                    'philosophical_themes': [],
                    'social_themes': [],
                    'complexity_scores': [],
                    'quotes': []
                }
            
            # Actualizar estadísticas
            stats = character_stats[character]
            stats['quote_count'] += 1
            stats['total_words'] += len(quote.split())
            stats['quotes'].append(quote)
            
            # Analizar contenido filosófico
            if analysis:
                phil_analysis = self.analyze_philosophical_content(analysis)
                stats['philosophical_themes'].extend(phil_analysis['philosophical_schools'])
                stats['social_themes'].extend(phil_analysis['social_critique_elements'])
            
            # Analizar complejidad
            complexity = self.analyze_quote_complexity(quote)
            stats['complexity_scores'].append(complexity['complexity_score'])
        
        # Procesar estadísticas finales
        for character, stats in character_stats.items():
            stats['avg_words_per_quote'] = stats['total_words'] / max(stats['quote_count'], 1)
            stats['avg_complexity'] = sum(stats['complexity_scores']) / max(len(stats['complexity_scores']), 1)
            stats['top_philosophical_themes'] = [
                item[0] for item in Counter(stats['philosophical_themes']).most_common(3)
            ]
            stats['top_social_themes'] = [
                item[0] for item in Counter(stats['social_themes']).most_common(3)
            ]
        
        return character_stats
    
    def generate_insights_report(self, quotes_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Genera un reporte completo de insights
        
        Args:
            quotes_data: Lista de datos de citas con análisis
            
        Returns:
            Reporte completo de insights
        """
        if not quotes_data:
            return {'error': 'No hay datos para analizar'}
        
        # Análisis general
        total_quotes = len(quotes_data)
        characters = list(set(q.get('character', 'Unknown') for q in quotes_data))
        
        # Análisis de complejidad promedio
        complexity_scores = []
        for quote_data in quotes_data:
            quote = quote_data.get('quote', '')
            if quote:
                complexity = self.analyze_quote_complexity(quote)
                complexity_scores.append(complexity['complexity_score'])
        
        avg_complexity = sum(complexity_scores) / max(len(complexity_scores), 1)
        
        # Análisis filosófico agregado
        all_philosophical_themes = []
        all_social_themes = []
        
        for quote_data in quotes_data:
            analysis = quote_data.get('analysis', '')
            if analysis:
                phil_analysis = self.analyze_philosophical_content(analysis)
                all_philosophical_themes.extend(phil_analysis['philosophical_schools'])
                all_social_themes.extend(phil_analysis['social_critique_elements'])
        
        # Patrones por personaje
        character_patterns = self.analyze_character_patterns(quotes_data)
        
        return {
            'summary': {
                'total_quotes_analyzed': total_quotes,
                'unique_characters': len(characters),
                'average_complexity_score': round(avg_complexity, 2),
                'most_complex_character': self._find_most_complex_character(character_patterns),
                'most_philosophical_character': self._find_most_philosophical_character(character_patterns)
            },
            'thematic_analysis': {
                'top_philosophical_themes': [
                    item[0] for item in Counter(all_philosophical_themes).most_common(5)
                ],
                'top_social_critique_themes': [
                    item[0] for item in Counter(all_social_themes).most_common(5)
                ],
                'philosophical_theme_distribution': dict(Counter(all_philosophical_themes)),
                'social_theme_distribution': dict(Counter(all_social_themes))
            },
            'character_insights': character_patterns,
            'recommendations': self._generate_recommendations(character_patterns, all_philosophical_themes)
        }
    
    def _calculate_complexity_score(self, avg_words_per_sentence: float, 
                                  lexical_diversity: float, avg_word_length: float,
                                  complex_structures: Dict[str, int]) -> float:
        """Calcula un score de complejidad normalizado"""
        
        # Normalizar métricas (0-1)
        sentence_complexity = min(avg_words_per_sentence / 20, 1)  # 20 palabras = máximo
        diversity_score = lexical_diversity  # Ya está normalizado
        word_length_score = min(avg_word_length / 8, 1)  # 8 caracteres = máximo
        
        # Score de estructuras complejas
        structure_score = min(sum(complex_structures.values()) / 10, 1)  # 10 = máximo
        
        # Promedio ponderado
        complexity_score = (
            sentence_complexity * 0.3 +
            diversity_score * 0.3 +
            word_length_score * 0.2 +
            structure_score * 0.2
        )
        
        return round(complexity_score, 3)
    
    def _identify_analysis_sections(self, analysis: str) -> Dict[str, bool]:
        """Identifica secciones típicas en el análisis"""
        
        analysis_lower = analysis.lower()
        
        return {
            'has_philosophical_section': any(
                phrase in analysis_lower 
                for phrase in ['filosófico', 'filosofía', 'corriente', 'pensamiento']
            ),
            'has_social_critique': any(
                phrase in analysis_lower 
                for phrase in ['social', 'sociedad', 'crítica', 'satiriza']
            ),
            'has_character_analysis': any(
                phrase in analysis_lower 
                for phrase in ['personaje', 'carácter', 'personalidad', 'visión']
            ),
            'has_contemporary_relevance': any(
                phrase in analysis_lower 
                for phrase in ['actual', 'contemporáneo', 'hoy', 'relevante']
            )
        }
    
    def _calculate_conceptual_depth(self, philosophical_matches: List[str],
                                  social_critique_matches: List[str],
                                  sections: Dict[str, bool]) -> float:
        """Calcula la profundidad conceptual del análisis"""
        
        depth_score = 0
        
        # Puntos por diversidad temática
        depth_score += min(len(set(philosophical_matches)) * 0.2, 1)
        depth_score += min(len(set(social_critique_matches)) * 0.2, 1)
        
        # Puntos por completitud de secciones
        section_completeness = sum(sections.values()) / len(sections)
        depth_score += section_completeness * 0.6
        
        return round(min(depth_score, 1), 3)
    
    def _calculate_academic_rigor(self, analysis: str) -> float:
        """Calcula el rigor académico del análisis"""
        
        rigor_indicators = [
            r'\b(según|de acuerdo con|como señala|plantea que)\b',  # Referencias
            r'\b(por tanto|así pues|en consecuencia|por consiguiente)\b',  # Conectores lógicos
            r'\b(evidencia|demuestra|sugiere|indica)\b',  # Lenguaje académico
            r'\b(concepto|teoría|paradigma|marco teórico)\b'  # Terminología académica
        ]
        
        rigor_score = 0
        for pattern in rigor_indicators:
            matches = len(re.findall(pattern, analysis.lower()))
            rigor_score += min(matches * 0.1, 0.25)  # Máximo 0.25 por categoría
        
        return round(min(rigor_score, 1), 3)
    
    def _calculate_accessibility(self, analysis: str) -> float:
        """Calcula qué tan accesible es el análisis"""
        
        words = analysis.split()
        
        # Penalizar palabras muy técnicas o largas
        complex_words = [w for w in words if len(w) > 12]
        complexity_penalty = len(complex_words) / max(len(words), 1)
        
        # Premiar estructura clara
        sentences = re.split(r'[.!?]+', analysis)
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # Score base alto, reducir por complejidad
        accessibility = 1 - (complexity_penalty * 0.5) - (max(0, avg_sentence_length - 15) * 0.01)
        
        return round(max(accessibility, 0), 3)
    
    def _find_most_complex_character(self, character_patterns: Dict[str, Any]) -> str:
        """Encuentra el personaje con citas más complejas en promedio"""
        
        if not character_patterns:
            return "N/A"
        
        most_complex = max(
            character_patterns.items(),
            key=lambda x: x[1].get('avg_complexity', 0)
        )
        
        return most_complex[0]
    
    def _find_most_philosophical_character(self, character_patterns: Dict[str, Any]) -> str:
        """Encuentra el personaje más filosófico"""
        
        if not character_patterns:
            return "N/A"
        
        most_philosophical = max(
            character_patterns.items(),
            key=lambda x: len(x[1].get('philosophical_themes', []))
        )
        
        return most_philosophical[0]
    
    def _generate_recommendations(self, character_patterns: Dict[str, Any],
                                philosophical_themes: List[str]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        
        recommendations = []
        
        if not character_patterns:
            return ["Analiza más citas para obtener recomendaciones personalizadas"]
        
        # Recomendación basada en diversidad
        unique_characters = len(character_patterns)
        if unique_characters < 3:
            recommendations.append(
                "Explora citas de más personajes para obtener una perspectiva más amplia"
            )
        
        # Recomendación basada en temas filosóficos
        unique_themes = len(set(philosophical_themes))
        if unique_themes < 3:
            recommendations.append(
                "Busca citas que aborden diferentes corrientes filosóficas"
            )
        
        # Recomendación del personaje más complejo
        most_complex = self._find_most_complex_character(character_patterns)
        if most_complex != "N/A":
            recommendations.append(
                f"Las citas de {most_complex} muestran mayor complejidad conceptual"
            )
        
        return recommendations