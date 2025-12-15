"""
Pruebas unitarias para el MockQuoteService
Valida que el mock funciona correctamente de manera aislada
"""
import pytest
from tests.mocks.mock_quote_service import MockQuoteService, create_mock_quote_service

class TestMockQuoteService:
    """
    Suite de pruebas para validar el comportamiento del MockQuoteService
    
    Estas pruebas aseguran que:
    1. El mock genera respuestas deterministas
    2. Las respuestas son diferentes por personaje
    3. El manejo de errores funciona correctamente
    4. La interfaz es compatible con QuoteService real
    """
    
    def test_mock_service_initialization(self):
        """Test 1: Verificar inicialización correcta del mock"""
        service = MockQuoteService()
        
        assert service.call_count == 0
        assert not service.simulate_errors
        assert len(service.mock_analyses) == 4  # homer, lisa, bart, marge
    
    def test_mock_service_with_error_simulation(self):
        """Test 2: Verificar inicialización con simulación de errores"""
        service = MockQuoteService(simulate_errors=True)
        
        assert service.simulate_errors
        assert service.call_count == 0
    
    def test_generate_analysis_homer(self):
        """Test 3: Verificar análisis específico para Homer"""
        service = MockQuoteService()
        
        quote = "D'oh! Life is like a box of donuts."
        character = "Homer Simpson"
        context = "Homer reflecting on life"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Verificar que el análisis contiene elementos esperados
        assert "Significado Filosófico" in analysis
        assert "Crítica Social" in analysis
        assert "Contexto del Personaje" in analysis
        assert "Relevancia Contemporánea" in analysis
        assert "hedonismo filosófico" in analysis
        assert "Mock para Testing" in analysis
        
        # Verificar que se incrementó el contador
        assert service.call_count == 1
    
    def test_generate_analysis_lisa(self):
        """Test 4: Verificar análisis específico para Lisa"""
        service = MockQuoteService()
        
        quote = "The truth will set you free, but first it will make you miserable."
        character = "Lisa Simpson"
        context = "Lisa discussing intellectual honesty"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Verificar contenido específico de Lisa
        assert "idealismo kantiano" in analysis
        assert "anti-intelectualismo" in analysis
        assert "conciencia moral" in analysis
        assert service.call_count == 1
    
    def test_generate_analysis_bart(self):
        """Test 5: Verificar análisis específico para Bart"""
        service = MockQuoteService()
        
        quote = "I didn't do it, nobody saw me do it, you can't prove anything!"
        character = "Bart Simpson"
        context = "Bart avoiding responsibility"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Verificar contenido específico de Bart
        assert "transgresión constructiva" in analysis
        assert "sistema educativo" in analysis
        assert "trickster" in analysis
        assert service.call_count == 1
    
    def test_generate_analysis_marge(self):
        """Test 6: Verificar análisis específico para Marge"""
        service = MockQuoteService()
        
        quote = "I just think they're neat."
        character = "Marge Simpson"
        context = "Marge expressing simple appreciation"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Verificar contenido específico de Marge
        assert "ética del cuidado" in analysis
        assert "trabajo emocional" in analysis
        assert "ancla moral" in analysis
        assert service.call_count == 1
    
    def test_generate_analysis_unknown_character(self):
        """Test 7: Verificar comportamiento con personaje desconocido"""
        service = MockQuoteService()
        
        quote = "Excellent..."
        character = "Mr. Burns"
        context = "Burns plotting something"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Debería usar análisis base de Homer pero personalizado
        assert "Significado Filosófico" in analysis
        assert "Mr. Burns" in analysis
        assert service.call_count == 1
    
    def test_deterministic_responses(self):
        """Test 8: Verificar que las respuestas son deterministas"""
        service1 = MockQuoteService()
        service2 = MockQuoteService()
        
        quote = "Mmm... beer."
        character = "Homer Simpson"
        context = "Homer enjoying beer"
        
        analysis1 = service1.generate_analysis(quote, character, context)
        analysis2 = service2.generate_analysis(quote, character, context)
        
        # Las respuestas deberían ser idénticas (deterministas)
        assert analysis1 == analysis2
    
    def test_call_counter_functionality(self):
        """Test 9: Verificar funcionamiento del contador de llamadas"""
        service = MockQuoteService()
        
        assert service.get_call_count() == 0
        
        # Hacer varias llamadas
        for i in range(3):
            service.generate_analysis("test", "Homer", "test")
            assert service.get_call_count() == i + 1
        
        # Reset counter
        service.reset_call_count()
        assert service.get_call_count() == 0
    
    def test_error_simulation(self):
        """Test 10: Verificar simulación de errores"""
        service = MockQuoteService(simulate_errors=True)
        
        # Las primeras 4 llamadas deberían funcionar
        for i in range(4):
            analysis = service.generate_analysis("test", "Homer", "test")
            assert "Significado Filosófico" in analysis
        
        # La quinta llamada debería generar error
        with pytest.raises(Exception) as exc_info:
            service.generate_analysis("test", "Homer", "test")
        
        assert "Mock API Error" in str(exc_info.value)
        assert "Rate limit exceeded" in str(exc_info.value)
    
    def test_factory_function(self):
        """Test 11: Verificar función factory"""
        # Sin errores
        service1 = create_mock_quote_service()
        assert not service1.simulate_errors
        
        # Con errores
        service2 = create_mock_quote_service(simulate_errors=True)
        assert service2.simulate_errors
    
    def test_quote_personalization(self):
        """Test 12: Verificar personalización con cita específica"""
        service = MockQuoteService()
        
        quote = "This is a very specific test quote for personalization"
        character = "Homer Simpson"
        context = "Testing personalization"
        
        analysis = service.generate_analysis(quote, character, context)
        
        # Verificar que la cita se incorpora al análisis
        assert "This is a very specific test quote" in analysis
    
    def test_interface_compatibility(self):
        """Test 13: Verificar compatibilidad de interfaz con QuoteService real"""
        service = MockQuoteService()
        
        # Verificar que tiene los métodos esperados
        assert hasattr(service, 'generate_analysis')
        assert callable(service.generate_analysis)
        
        # Verificar signature del método principal
        import inspect
        sig = inspect.signature(service.generate_analysis)
        params = list(sig.parameters.keys())
        
        expected_params = ['quote', 'character', 'context']
        assert all(param in params for param in expected_params)
    
    def test_analysis_structure_consistency(self):
        """Test 14: Verificar estructura consistente de análisis"""
        service = MockQuoteService()
        
        characters = ["Homer Simpson", "Lisa Simpson", "Bart Simpson", "Marge Simpson"]
        
        for character in characters:
            analysis = service.generate_analysis("test quote", character, "test context")
            
            # Verificar estructura consistente
            required_sections = [
                "1. **Significado Filosófico**",
                "2. **Crítica Social**", 
                "3. **Contexto del Personaje**",
                "4. **Relevancia Contemporánea**"
            ]
            
            for section in required_sections:
                assert section in analysis, f"Sección '{section}' faltante para {character}"
            
            # Verificar que termina con indicador de mock
            assert "Mock para Testing" in analysis