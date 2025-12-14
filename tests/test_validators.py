"""
Tests unitarios para el módulo de validadores
"""
import unittest
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import QuoteValidator, ErrorHandler

class TestQuoteValidator(unittest.TestCase):
    """Tests para la clase QuoteValidator"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.validator = QuoteValidator()
    
    def test_validate_quote_structure_valid(self):
        """Test para estructura válida de cita"""
        valid_quote = {
            'quote': 'D\'oh! This is a valid quote.',
            'character': 'Homer Simpson'
        }
        
        result = self.validator.validate_quote_structure(valid_quote)
        self.assertTrue(result)
    
    def test_validate_quote_structure_missing_fields(self):
        """Test para estructura con campos faltantes"""
        invalid_quote = {
            'quote': 'Missing character field'
        }
        
        result = self.validator.validate_quote_structure(invalid_quote)
        self.assertFalse(result)
    
    def test_validate_quote_structure_wrong_type(self):
        """Test para estructura con tipos incorrectos"""
        invalid_quote = {
            'quote': 123,  # Debería ser string
            'character': 'Homer Simpson'
        }
        
        result = self.validator.validate_quote_structure(invalid_quote)
        self.assertFalse(result)
    
    def test_validate_quote_content_valid(self):
        """Test para contenido válido de cita"""
        result = self.validator.validate_quote_content(
            "This is a perfectly valid quote with enough content.",
            "Homer Simpson"
        )
        self.assertTrue(result)
    
    def test_validate_quote_content_too_short(self):
        """Test para cita muy corta"""
        result = self.validator.validate_quote_content(
            "Short",  # Muy corta
            "Homer Simpson"
        )
        self.assertFalse(result)
    
    def test_validate_quote_content_too_long(self):
        """Test para cita muy larga"""
        long_quote = "A" * 600  # Excede el límite
        result = self.validator.validate_quote_content(
            long_quote,
            "Homer Simpson"
        )
        self.assertFalse(result)
    
    def test_validate_character_name_valid(self):
        """Test para nombre de personaje válido"""
        result = self.validator._validate_character_name("Homer Simpson")
        self.assertTrue(result)
    
    def test_validate_character_name_too_short(self):
        """Test para nombre muy corto"""
        result = self.validator._validate_character_name("H")
        self.assertFalse(result)
    
    def test_validate_api_key_valid(self):
        """Test para API key válida"""
        valid_key = "sk-1234567890abcdef1234567890abcdef"
        result = self.validator.validate_api_key(valid_key)
        self.assertTrue(result)
    
    def test_validate_api_key_invalid(self):
        """Test para API key inválida"""
        invalid_key = "short"
        result = self.validator.validate_api_key(invalid_key)
        self.assertFalse(result)
    
    def test_sanitize_text(self):
        """Test para sanitización de texto"""
        dirty_text = "  Text with\x00control\x1fcharacters  and   extra   spaces  "
        clean_text = self.validator.sanitize_text(dirty_text)
        
        expected = "Text with control characters and extra spaces"
        self.assertEqual(clean_text, expected)

class TestErrorHandler(unittest.TestCase):
    """Tests para la clase ErrorHandler"""
    
    def test_handle_timeout_error(self):
        """Test para manejo de errores de timeout"""
        timeout_error = Exception("Connection timeout occurred")
        result = ErrorHandler.handle_api_error(timeout_error)
        
        self.assertIn("tiempo", result.lower())
    
    def test_handle_connection_error(self):
        """Test para manejo de errores de conexión"""
        connection_error = Exception("Network connection failed")
        result = ErrorHandler.handle_api_error(connection_error)
        
        self.assertIn("conexión", result.lower())
    
    def test_handle_api_key_error(self):
        """Test para manejo de errores de API key"""
        auth_error = Exception("Invalid API key provided")
        result = ErrorHandler.handle_api_error(auth_error)
        
        self.assertIn("autenticación", result.lower())
    
    def test_handle_generic_error(self):
        """Test para manejo de errores genéricos"""
        generic_error = Exception("Some unexpected error")
        result = ErrorHandler.handle_api_error(generic_error)
        
        self.assertIn("inesperado", result.lower())

if __name__ == '__main__':
    # Ejecutar tests
    unittest.main(verbosity=2)