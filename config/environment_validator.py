"""
Validador de entorno para Springfield Insights
Implementa validaciones previas a la ejecución siguiendo buenas prácticas académicas
"""
import requests
import openai
from typing import Dict, Any, Tuple
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class EnvironmentValidator:
    """
    Validador completo del entorno de ejecución
    Verifica APIs, configuración y dependencias antes del inicio
    """
    
    def __init__(self):
        self.validation_results = {
            'environment': {'status': 'pending', 'details': []},
            'simpsons_api': {'status': 'pending', 'details': []},
            'openai_api': {'status': 'pending', 'details': []},
            'overall': {'status': 'pending', 'can_run': False}
        }
    
    def validate_complete_environment(self) -> Dict[str, Any]:
        """
        Ejecuta validación completa del entorno
        
        Returns:
            Dict con resultados detallados de todas las validaciones
        """
        print("🔍 Iniciando validación completa del entorno...")
        print("-" * 50)
        
        # 1. Validar configuración básica
        self._validate_basic_configuration()
        
        # 2. Validar API de Simpsons
        self._validate_simpsons_api()
        
        # 3. Validar API de OpenAI
        self._validate_openai_api()
        
        # 4. Determinar estado general
        self._determine_overall_status()
        
        # 5. Mostrar resumen
        self._print_validation_summary()
        
        return self.validation_results
    
    def _validate_basic_configuration(self):
        """Valida la configuración básica del entorno"""
        
        print("📋 Validando configuración básica...")
        
        try:
            # Usar el validador de settings
            config_validation = settings.validate_config()
            
            if config_validation['is_valid']:
                self.validation_results['environment']['status'] = 'success'
                self.validation_results['environment']['details'].append(
                    "✅ Configuración básica válida"
                )
            else:
                self.validation_results['environment']['status'] = 'error'
                for error in config_validation['errors']:
                    self.validation_results['environment']['details'].append(f"❌ {error}")
            
            # Agregar advertencias si las hay
            for warning in config_validation.get('warnings', []):
                self.validation_results['environment']['details'].append(f"⚠️  {warning}")
                
        except Exception as e:
            self.validation_results['environment']['status'] = 'error'
            self.validation_results['environment']['details'].append(
                f"❌ Error validando configuración: {str(e)}"
            )
        
        # Mostrar resultados
        for detail in self.validation_results['environment']['details']:
            print(f"   {detail}")
    
    def _validate_simpsons_api(self):
        """Valida conectividad con fuentes de datos de Los Simpsons"""
        
        print("\n🍩 Validando fuentes de datos de Los Simpsons...")
        
        # Importar el servicio para usar su lógica robusta
        try:
            from services.simpsons_api import SimpsonsAPIService
            simpsons_service = SimpsonsAPIService()
            
            # Verificar estado de APIs
            api_status = simpsons_service.get_api_status()
            
            accessible_apis = sum(1 for status in api_status.values() if status['accessible'])
            total_apis = len(api_status)
            
            if accessible_apis > 0:
                self.validation_results['simpsons_api']['status'] = 'success'
                self.validation_results['simpsons_api']['details'].extend([
                    f"✅ {accessible_apis}/{total_apis} endpoints de API accesibles",
                    "✅ Sistema de fallback local disponible",
                    "✅ Generación de contenido filosófico habilitada"
                ])
                
                # Mostrar detalles de APIs
                for endpoint, status in api_status.items():
                    if status['accessible']:
                        self.validation_results['simpsons_api']['details'].append(
                            f"   ✅ {endpoint}: Accesible"
                        )
                    else:
                        self.validation_results['simpsons_api']['details'].append(
                            f"   ⚠️  {endpoint}: {status.get('error', 'No accesible')}"
                        )
            
            elif accessible_apis == 0:
                # Todas las APIs fallan, pero tenemos fallback
                self.validation_results['simpsons_api']['status'] = 'warning'
                self.validation_results['simpsons_api']['details'].extend([
                    "⚠️  APIs externas no accesibles",
                    "✅ Sistema de fallback local activado",
                    "✅ Personajes predefinidos disponibles",
                    "💡 La aplicación funcionará con datos locales"
                ])
            
            # Probar generación de contenido
            try:
                test_context = simpsons_service.get_random_quote()
                if test_context and test_context.get('success'):
                    character = test_context.get('character', 'Desconocido')
                    source = test_context.get('source', 'unknown')
                    
                    self.validation_results['simpsons_api']['details'].append(
                        f"🎭 Prueba exitosa: {character} (fuente: {source})"
                    )
                else:
                    self.validation_results['simpsons_api']['status'] = 'error'
                    self.validation_results['simpsons_api']['details'].append(
                        "❌ Error en sistema de fallback local"
                    )
                    
            except Exception as e:
                self.validation_results['simpsons_api']['status'] = 'error'
                self.validation_results['simpsons_api']['details'].append(
                    f"❌ Error probando generación: {str(e)}"
                )
                
        except ImportError as e:
            self.validation_results['simpsons_api']['status'] = 'error'
            self.validation_results['simpsons_api']['details'].append(
                f"❌ Error importando servicio: {str(e)}"
            )
        except Exception as e:
            self.validation_results['simpsons_api']['status'] = 'error'
            self.validation_results['simpsons_api']['details'].append(
                f"❌ Error inesperado: {str(e)}"
            )
        
        # Mostrar resultados
        for detail in self.validation_results['simpsons_api']['details']:
            print(f"   {detail}")
    
    def _validate_openai_api(self):
        """Valida conectividad con la API de OpenAI (sin consumir tokens)"""
        
        print("\n🤖 Validando API de OpenAI...")
        
        if not settings.OPENAI_API_KEY:
            self.validation_results['openai_api']['status'] = 'error'
            self.validation_results['openai_api']['details'].append(
                "❌ OPENAI_API_KEY no configurada"
            )
            for detail in self.validation_results['openai_api']['details']:
                print(f"   {detail}")
            return
        
        try:
            # Configurar cliente OpenAI
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Intentar listar modelos (operación de bajo costo)
            models = client.models.list()
            
            # Verificar que GPT-4 esté disponible
            available_models = [model.id for model in models.data]
            gpt4_available = any('gpt-4' in model for model in available_models)
            
            if gpt4_available:
                self.validation_results['openai_api']['status'] = 'success'
                self.validation_results['openai_api']['details'].extend([
                    "✅ API de OpenAI accesible",
                    "✅ Clave API válida",
                    f"✅ GPT-4 disponible",
                    f"📊 Modelos disponibles: {len(available_models)}"
                ])
            else:
                self.validation_results['openai_api']['status'] = 'warning'
                self.validation_results['openai_api']['details'].extend([
                    "✅ API de OpenAI accesible",
                    "✅ Clave API válida", 
                    "⚠️  GPT-4 no encontrado en modelos disponibles",
                    "💡 La aplicación intentará usar el modelo configurado"
                ])
                
        except openai.AuthenticationError:
            self.validation_results['openai_api']['status'] = 'error'
            self.validation_results['openai_api']['details'].append(
                "❌ Clave API inválida o expirada"
            )
            
        except openai.RateLimitError:
            self.validation_results['openai_api']['status'] = 'warning'
            self.validation_results['openai_api']['details'].extend([
                "⚠️  Límite de rate alcanzado",
                "💡 La API funciona pero está temporalmente limitada"
            ])
            
        except openai.APIConnectionError:
            self.validation_results['openai_api']['status'] = 'error'
            self.validation_results['openai_api']['details'].append(
                "❌ Error de conexión con OpenAI - Verifica tu conexión"
            )
            
        except Exception as e:
            self.validation_results['openai_api']['status'] = 'error'
            self.validation_results['openai_api']['details'].append(
                f"❌ Error inesperado: {str(e)}"
            )
        
        # Mostrar resultados
        for detail in self.validation_results['openai_api']['details']:
            print(f"   {detail}")
    
    def _determine_overall_status(self):
        """Determina el estado general basado en validaciones individuales"""
        
        # Contar estados
        success_count = 0
        error_count = 0
        warning_count = 0
        
        for component in ['environment', 'simpsons_api', 'openai_api']:
            status = self.validation_results[component]['status']
            if status == 'success':
                success_count += 1
            elif status == 'error':
                error_count += 1
            elif status == 'warning':
                warning_count += 1
        
        # Determinar si puede ejecutarse
        can_run = (
            self.validation_results['environment']['status'] in ['success', 'warning'] and
            self.validation_results['openai_api']['status'] in ['success', 'warning']
        )
        
        # Determinar estado general
        if error_count == 0:
            if warning_count == 0:
                overall_status = 'success'
            else:
                overall_status = 'warning'
        else:
            overall_status = 'error'
        
        self.validation_results['overall'] = {
            'status': overall_status,
            'can_run': can_run,
            'success_count': success_count,
            'warning_count': warning_count,
            'error_count': error_count
        }
    
    def _print_validation_summary(self):
        """Imprime resumen final de validación"""
        
        print("\n" + "="*50)
        print("📊 RESUMEN DE VALIDACIÓN")
        print("="*50)
        
        overall = self.validation_results['overall']
        
        # Estado general
        if overall['status'] == 'success':
            print("🎉 ¡Entorno completamente válido!")
        elif overall['status'] == 'warning':
            print("⚠️  Entorno válido con advertencias")
        else:
            print("❌ Errores críticos encontrados")
        
        # Estadísticas
        print(f"✅ Componentes exitosos: {overall['success_count']}")
        if overall['warning_count'] > 0:
            print(f"⚠️  Componentes con advertencias: {overall['warning_count']}")
        if overall['error_count'] > 0:
            print(f"❌ Componentes con errores: {overall['error_count']}")
        
        # Capacidad de ejecución
        if overall['can_run']:
            print("\n🚀 ¡La aplicación puede ejecutarse!")
            print("   Ejecuta: streamlit run app.py")
        else:
            print("\n🛑 La aplicación NO puede ejecutarse")
            print("   Corrige los errores antes de continuar")
        
        print("="*50)
    
    def get_startup_recommendations(self) -> list:
        """
        Genera recomendaciones basadas en la validación
        
        Returns:
            Lista de recomendaciones para el usuario
        """
        recommendations = []
        
        # Recomendaciones basadas en errores
        if self.validation_results['environment']['status'] == 'error':
            recommendations.append(
                "🔧 Revisa el archivo .env y asegúrate de que todas las variables estén configuradas"
            )
        
        if self.validation_results['openai_api']['status'] == 'error':
            recommendations.extend([
                "🔑 Verifica tu OPENAI_API_KEY en https://platform.openai.com/api-keys",
                "💳 Asegúrate de tener créditos disponibles en tu cuenta OpenAI"
            ])
        
        if self.validation_results['simpsons_api']['status'] == 'error':
            recommendations.append(
                "🌐 Verifica tu conexión a internet para acceder a la API de Simpsons"
            )
        
        # Recomendaciones generales
        if not recommendations:
            recommendations.extend([
                "🎯 Todo listo para usar Springfield Insights",
                "📚 Explora las diferentes pestañas: Explorar, Favoritos, Analytics",
                "💡 Guarda tus citas favoritas para análisis posteriores"
            ])
        
        return recommendations

def validate_environment_startup() -> Tuple[bool, Dict[str, Any]]:
    """
    Función de utilidad para validación rápida en startup
    
    Returns:
        Tuple con (puede_ejecutarse, resultados_detallados)
    """
    validator = EnvironmentValidator()
    results = validator.validate_complete_environment()
    
    return results['overall']['can_run'], results