#!/usr/bin/env python3
"""
Script de diagnóstico de performance para Springfield Insights
Identifica cuellos de botella en el análisis académico
"""
import time
import sys
import logging
from pathlib import Path

# Configurar path
sys.path.append(str(Path(__file__).parent))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_llm_performance():
    """Prueba específica de performance del LLM"""
    print("\n🤖 DIAGNÓSTICO DE PERFORMANCE LLM")
    print("=" * 50)
    
    try:
        from services.llm_service import LLMService
        from config.settings import settings
        
        # Verificar configuración
        print(f"✅ Modelo: {settings.OPENAI_MODEL}")
        print(f"✅ Max Tokens: {settings.OPENAI_MAX_TOKENS}")
        print(f"✅ Temperature: {settings.OPENAI_TEMPERATURE}")
        print(f"✅ Timeout: {settings.LLM_TIMEOUT}s")
        
        if not settings.OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY no configurada")
            return False
        
        print(f"✅ API Key: {'*' * 10}{settings.OPENAI_API_KEY[-4:]}")
        
        # Inicializar servicio
        llm_service = LLMService()
        print("✅ LLMService inicializado")
        
        # Test 1: Análisis simple (método original)
        print("\n📊 Test 1: Análisis filosófico simple")
        start_time = time.time()
        
        simple_analysis = llm_service.generate_philosophical_analysis(
            "La vida es como una caja de donuts, nunca sabes cuál va a estar relleno.",
            "Homer Simpson"
        )
        
        simple_time = time.time() - start_time
        print(f"⏱️ Tiempo análisis simple: {simple_time:.2f}s")
        
        if simple_analysis:
            print(f"✅ Análisis generado: {len(simple_analysis)} caracteres")
        else:
            print("❌ Error generando análisis simple")
            return False
        
        # Test 2: Reflexión completa (método optimizado)
        print("\n📊 Test 2: Reflexión filosófica completa")
        start_time = time.time()
        
        complete_reflection = llm_service.generate_complete_philosophical_reflection(
            character="Homer Simpson",
            description="Padre de familia trabajador de planta nuclear",
            philosophical_context="Reflexiones sobre la vida cotidiana y el trabajo"
        )
        
        complete_time = time.time() - start_time
        print(f"⏱️ Tiempo reflexión completa: {complete_time:.2f}s")
        
        if complete_reflection:
            print(f"✅ Reflexión generada:")
            print(f"   - Reflexión: {len(complete_reflection.get('reflection', ''))} caracteres")
            print(f"   - Análisis: {len(complete_reflection.get('analysis', ''))} caracteres")
        else:
            print("❌ Error generando reflexión completa")
            return False
        
        # Test 3: Cache performance
        print("\n📊 Test 3: Performance de cache")
        start_time = time.time()
        
        # Segunda llamada (debería usar cache)
        cached_reflection = llm_service.generate_complete_philosophical_reflection(
            character="Homer Simpson",
            description="Padre de familia trabajador de planta nuclear",
            philosophical_context="Reflexiones sobre la vida cotidiana y el trabajo"
        )
        
        cache_time = time.time() - start_time
        print(f"⏱️ Tiempo con cache: {cache_time:.2f}s")
        
        if cache_time < 1.0:
            print("✅ Cache funcionando correctamente")
        else:
            print("⚠️ Cache podría no estar funcionando")
        
        # Resumen
        print(f"\n📊 RESUMEN DE PERFORMANCE:")
        print(f"   • Análisis simple: {simple_time:.2f}s")
        print(f"   • Reflexión completa: {complete_time:.2f}s")
        print(f"   • Con cache: {cache_time:.2f}s")
        
        # Diagnóstico
        if complete_time > 20:
            print("🚨 PROBLEMA DETECTADO: Reflexión completa muy lenta (>20s)")
            print("   Posibles causas:")
            print("   - Timeout muy alto en configuración")
            print("   - Prompt demasiado complejo")
            print("   - Problemas de conectividad")
            print("   - Modelo GPT-4 sobrecargado")
        elif complete_time > 10:
            print("⚠️ ADVERTENCIA: Reflexión completa lenta (>10s)")
            print("   Considera optimizar prompts o usar GPT-3.5-turbo")
        else:
            print("✅ Performance LLM aceptable")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test LLM: {e}")
        return False

def test_api_performance():
    """Prueba performance de APIs externas"""
    print("\n🌐 DIAGNÓSTICO DE PERFORMANCE APIs")
    print("=" * 50)
    
    try:
        from services.simpsons_api import SimpsonsAPIService
        
        api_service = SimpsonsAPIService()
        
        # Test API status
        print("📡 Probando estado de API...")
        start_time = time.time()
        
        status = api_service.get_api_status()
        api_time = time.time() - start_time
        
        print(f"⏱️ Tiempo API status: {api_time:.2f}s")
        print(f"📊 Estado API: {status}")
        
        # Test quote generation
        print("\n🎭 Probando generación de cita...")
        start_time = time.time()
        
        quote = api_service.get_random_quote()
        quote_time = time.time() - start_time
        
        print(f"⏱️ Tiempo generación cita: {quote_time:.2f}s")
        
        if quote and quote.get('success'):
            print(f"✅ Cita generada: {quote.get('character', 'Unknown')}")
        else:
            print("⚠️ Usando datos fallback")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test API: {e}")
        return False

def test_full_workflow():
    """Prueba el flujo completo de la aplicación"""
    print("\n🔄 DIAGNÓSTICO DE FLUJO COMPLETO")
    print("=" * 50)
    
    try:
        from logic.quote_processor import QuoteProcessor
        
        processor = QuoteProcessor()
        
        print("🎯 Ejecutando flujo completo...")
        start_time = time.time()
        
        result = processor.get_analyzed_quote()
        total_time = time.time() - start_time
        
        print(f"⏱️ Tiempo total: {total_time:.2f}s")
        
        if result and result.get('success'):
            print("✅ Flujo completo exitoso")
            print(f"   - Personaje: {result.get('character', 'Unknown')}")
            print(f"   - Reflexión: {len(result.get('quote', ''))} caracteres")
            print(f"   - Análisis: {len(result.get('analysis', ''))} caracteres")
            print(f"   - Fuente: {result.get('source', 'unknown')}")
        else:
            print(f"❌ Error en flujo: {result.get('error_message', 'Unknown')}")
            return False
        
        # Diagnóstico de tiempo
        if total_time > 30:
            print("🚨 FLUJO MUY LENTO (>30s)")
            print("   Recomendaciones:")
            print("   - Verificar conexión a internet")
            print("   - Reducir max_tokens en configuración")
            print("   - Considerar usar GPT-3.5-turbo")
        elif total_time > 15:
            print("⚠️ FLUJO LENTO (>15s)")
            print("   Considera optimizaciones adicionales")
        else:
            print("✅ Flujo con performance aceptable")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en flujo completo: {e}")
        return False

def test_cache_efficiency():
    """Prueba la eficiencia del sistema de cache"""
    print("\n🗄️ DIAGNÓSTICO DE CACHE")
    print("=" * 50)
    
    try:
        from services.cache_optimizer import cache_optimizer
        
        # Obtener estadísticas
        stats = cache_optimizer.get_global_cache_stats()
        
        print("📊 Estadísticas de Cache:")
        for cache_name, cache_stats in stats.items():
            hit_rate = cache_stats.get('hit_rate', 0)
            size = cache_stats.get('size', 0)
            max_size = cache_stats.get('max_size', 0)
            
            print(f"   • {cache_name}:")
            print(f"     - Hit Rate: {hit_rate:.1f}%")
            print(f"     - Tamaño: {size}/{max_size}")
            
            if hit_rate < 50 and cache_stats.get('hits', 0) + cache_stats.get('misses', 0) > 10:
                print(f"     ⚠️ Baja eficiencia de cache")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en diagnóstico de cache: {e}")
        return False

def main():
    """Ejecuta diagnóstico completo"""
    print("🔍 DIAGNÓSTICO COMPLETO DE PERFORMANCE")
    print("=" * 60)
    print("Identificando cuellos de botella en Springfield Insights...")
    
    total_start = time.time()
    
    # Ejecutar tests
    tests = [
        ("API Performance", test_api_performance),
        ("Cache Efficiency", test_cache_efficiency),
        ("LLM Performance", test_llm_performance),
        ("Full Workflow", test_full_workflow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen final
    total_time = time.time() - total_start
    
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"⏱️ Tiempo total de diagnóstico: {total_time:.2f}s")
    print(f"📊 Tests pasados: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES:")
    
    if not results.get("LLM Performance", False):
        print("   🤖 Problema con LLM - Verificar API key y configuración")
    
    if not results.get("Full Workflow", False):
        print("   🔄 Problema en flujo completo - Revisar logs de error")
    
    if passed == total:
        print("   🎉 ¡Todos los tests pasaron! La aplicación debería funcionar bien.")
    else:
        print("   🔧 Hay problemas que requieren atención.")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()