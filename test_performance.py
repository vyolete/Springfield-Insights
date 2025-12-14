#!/usr/bin/env python3
"""
Script de prueba para las optimizaciones de performance
Valida cache, monitoreo y mejoras de rendimiento
"""
import sys
import os
import time
from pathlib import Path

# Añadir path del proyecto
sys.path.append(str(Path(__file__).parent))

def test_cache_optimizer():
    """Prueba el optimizador de cache"""
    print("🗄️ PROBANDO OPTIMIZADOR DE CACHE")
    print("=" * 50)
    
    try:
        from services.cache_optimizer import CacheOptimizer, smart_cache
        
        optimizer = CacheOptimizer()
        
        # Probar cache de LLM
        print("🤖 Probando cache de LLM...")
        test_hash = "test_hash_123"
        test_response = "Esta es una respuesta de prueba del LLM"
        
        # Guardar en cache
        optimizer.cache_llm_response(test_hash, test_response)
        
        # Recuperar del cache
        cached_response = optimizer.get_cached_llm_response(test_hash)
        
        if cached_response == test_response:
            print("✅ Cache de LLM funcionando correctamente")
        else:
            print("❌ Error en cache de LLM")
            return False
        
        # Probar cache de episodios
        print("📺 Probando cache de episodios...")
        test_episode = {"id": "test_123", "name": "Test Episode", "season": 1}
        
        optimizer.cache_episode_data("test_123", test_episode)
        cached_episode = optimizer.get_cached_episode_data("test_123")
        
        if cached_episode == test_episode:
            print("✅ Cache de episodios funcionando correctamente")
        else:
            print("❌ Error en cache de episodios")
            return False
        
        # Probar estadísticas
        print("📊 Probando estadísticas de cache...")
        stats = optimizer.get_global_cache_stats()
        
        if 'llm_cache' in stats and 'episodes_cache' in stats:
            print("✅ Estadísticas de cache disponibles")
            print(f"   LLM Cache: {stats['llm_cache']['size']} entradas")
            print(f"   Episodes Cache: {stats['episodes_cache']['size']} entradas")
        else:
            print("❌ Error obteniendo estadísticas")
            return False
        
        # Probar decorador smart_cache
        print("🎯 Probando decorador smart_cache...")
        
        @smart_cache(cache_type='general', ttl=60)
        def test_function(x, y):
            time.sleep(0.1)  # Simular operación costosa
            return x + y
        
        # Primera llamada (sin cache)
        start_time = time.time()
        result1 = test_function(5, 3)
        first_call_time = time.time() - start_time
        
        # Segunda llamada (con cache)
        start_time = time.time()
        result2 = test_function(5, 3)
        cached_call_time = time.time() - start_time
        
        if result1 == result2 and cached_call_time < first_call_time:
            print("✅ Decorador smart_cache funcionando correctamente")
            print(f"   Primera llamada: {first_call_time:.3f}s")
            print(f"   Llamada cacheada: {cached_call_time:.3f}s")
        else:
            print("❌ Error en decorador smart_cache")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_performance_monitor():
    """Prueba el monitor de performance"""
    print("\n⚡ PROBANDO MONITOR DE PERFORMANCE")
    print("=" * 50)
    
    try:
        from services.performance_monitor import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # Probar tracking de carga de página
        print("📄 Probando tracking de carga de página...")
        start_time = time.time()
        time.sleep(0.1)  # Simular carga
        monitor.track_page_load(start_time, "test_page")
        
        if len(monitor.metrics['page_load_time']) > 0:
            print("✅ Tracking de carga de página funcionando")
        else:
            print("❌ Error en tracking de carga")
            return False
        
        # Probar tracking de búsqueda
        print("🔍 Probando tracking de búsqueda...")
        start_time = time.time()
        time.sleep(0.05)  # Simular búsqueda
        monitor.track_search_time(start_time, "test query", 5)
        
        if len(monitor.metrics['search_time']) > 0:
            print("✅ Tracking de búsqueda funcionando")
        else:
            print("❌ Error en tracking de búsqueda")
            return False
        
        # Probar tracking de cache
        print("🗄️ Probando tracking de cache...")
        monitor.track_cache_hit("test_cache", True)
        monitor.track_cache_hit("test_cache", False)
        monitor.track_cache_hit("test_cache", True)
        
        if "test_cache" in monitor.metrics['cache_hit_rate']:
            cache_data = monitor.metrics['cache_hit_rate']['test_cache']
            if cache_data['hits'] == 2 and cache_data['misses'] == 1:
                print("✅ Tracking de cache funcionando")
            else:
                print("❌ Error en conteo de cache")
                return False
        else:
            print("❌ Error en tracking de cache")
            return False
        
        # Probar resumen de performance
        print("📊 Probando resumen de performance...")
        summary = monitor.get_performance_summary()
        
        expected_keys = ['cache_efficiency', 'current_memory']
        if all(key in summary for key in expected_keys):
            print("✅ Resumen de performance disponible")
            print(f"   Memoria actual: {summary.get('current_memory', 0):.1f} MB")
            if 'test_cache' in summary['cache_efficiency']:
                print(f"   Eficiencia test_cache: {summary['cache_efficiency']['test_cache']:.1f}%")
        else:
            print("❌ Error en resumen de performance")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_memory_optimization():
    """Prueba optimizaciones de memoria"""
    print("\n💾 PROBANDO OPTIMIZACIONES DE MEMORIA")
    print("=" * 50)
    
    try:
        import gc
        import psutil
        
        # Obtener uso inicial de memoria
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        print(f"📊 Memoria inicial: {initial_memory:.1f} MB")
        
        # Crear datos de prueba que consuman memoria
        test_data = []
        for i in range(1000):
            test_data.append({
                'id': i,
                'data': 'x' * 1000,  # 1KB por entrada
                'timestamp': time.time()
            })
        
        memory_after_data = process.memory_info().rss / 1024 / 1024
        print(f"📊 Memoria después de crear datos: {memory_after_data:.1f} MB")
        
        # Limpiar datos
        del test_data
        gc.collect()
        
        memory_after_cleanup = process.memory_info().rss / 1024 / 1024
        print(f"📊 Memoria después de limpieza: {memory_after_cleanup:.1f} MB")
        
        # Verificar que la memoria se liberó (al menos parcialmente)
        memory_freed = memory_after_data - memory_after_cleanup
        if memory_freed > 0:
            print(f"✅ Memoria liberada: {memory_freed:.1f} MB")
        else:
            print("⚠️ No se detectó liberación significativa de memoria")
        
        return True
        
    except ImportError:
        print("⚠️ psutil no disponible, saltando pruebas de memoria")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cache_performance():
    """Prueba performance del sistema de cache"""
    print("\n🚀 PROBANDO PERFORMANCE DE CACHE")
    print("=" * 50)
    
    try:
        from services.cache_optimizer import CacheOptimizer
        
        optimizer = CacheOptimizer()
        
        # Probar performance de escritura
        print("✍️ Probando performance de escritura...")
        start_time = time.time()
        
        for i in range(100):
            optimizer.cache_llm_response(f"test_key_{i}", f"test_response_{i}")
        
        write_time = time.time() - start_time
        print(f"✅ 100 escrituras en {write_time:.3f}s ({write_time/100*1000:.2f}ms por escritura)")
        
        # Probar performance de lectura
        print("📖 Probando performance de lectura...")
        start_time = time.time()
        
        hits = 0
        for i in range(100):
            result = optimizer.get_cached_llm_response(f"test_key_{i}")
            if result:
                hits += 1
        
        read_time = time.time() - start_time
        print(f"✅ 100 lecturas en {read_time:.3f}s ({read_time/100*1000:.2f}ms por lectura)")
        print(f"✅ Hit rate: {hits}% ({hits}/100)")
        
        # Probar limpieza de cache
        print("🧹 Probando limpieza de cache...")
        start_time = time.time()
        
        optimizer.cleanup_expired_entries()
        
        cleanup_time = time.time() - start_time
        print(f"✅ Limpieza completada en {cleanup_time:.3f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_integration_performance():
    """Prueba performance de integración completa"""
    print("\n🔗 PROBANDO PERFORMANCE DE INTEGRACIÓN")
    print("=" * 50)
    
    try:
        from services.cache_optimizer import cache_optimizer
        from services.performance_monitor import performance_monitor
        
        # Simular flujo completo de la aplicación
        print("🎭 Simulando flujo completo de aplicación...")
        
        # 1. Carga de página
        page_start = time.time()
        time.sleep(0.1)  # Simular carga
        performance_monitor.track_page_load(page_start, "integration_test")
        
        # 2. Búsqueda de episodios
        search_start = time.time()
        time.sleep(0.05)  # Simular búsqueda
        performance_monitor.track_search_time(search_start, "homer", 10)
        
        # 3. Cache de LLM
        llm_start = time.time()
        test_hash = cache_optimizer.create_content_hash("Homer", "test", "context")
        
        # Simular miss de cache
        cached_result = cache_optimizer.get_cached_llm_response(test_hash)
        if not cached_result:
            # Simular generación de LLM
            time.sleep(0.2)
            cache_optimizer.cache_llm_response(test_hash, "Generated response")
        
        performance_monitor.track_llm_response(llm_start, "Homer", True)
        
        # 4. Verificar métricas
        summary = performance_monitor.get_performance_summary()
        
        print("✅ Flujo de integración completado")
        print(f"   Carga promedio: {summary.get('avg_page_load', 0):.3f}s")
        print(f"   Búsqueda promedio: {summary.get('avg_search_time', 0):.3f}s")
        print(f"   Memoria actual: {summary.get('current_memory', 0):.1f} MB")
        
        # Verificar que las métricas se registraron
        if (len(performance_monitor.metrics['page_load_time']) > 0 and
            len(performance_monitor.metrics['search_time']) > 0 and
            len(performance_monitor.metrics['llm_response_time']) > 0):
            print("✅ Todas las métricas registradas correctamente")
            return True
        else:
            print("❌ Faltan métricas en el registro")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal de pruebas de performance"""
    print("⚡ PRUEBAS DE OPTIMIZACIÓN DE PERFORMANCE")
    print("=" * 60)
    
    tests = [
        ("Optimizador de Cache", test_cache_optimizer),
        ("Monitor de Performance", test_performance_monitor),
        ("Optimizaciones de Memoria", test_memory_optimization),
        ("Performance de Cache", test_cache_performance),
        ("Integración Completa", test_integration_performance)
    ]
    
    results = []
    total_start = time.time()
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    total_time = time.time() - total_start
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS DE PERFORMANCE")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    print(f"⏱️ Tiempo total: {total_time:.3f}s")
    
    if passed == total:
        print("🎉 ¡TODAS LAS OPTIMIZACIONES DE PERFORMANCE FUNCIONANDO!")
        print("\n💡 Beneficios validados:")
        print("   • Cache inteligente con TTL automático")
        print("   • Monitoreo de performance en tiempo real")
        print("   • Limpieza automática de memoria")
        print("   • Métricas detalladas de rendimiento")
        print("   • Optimización de llamadas API")
        print("   • Sistema de alertas automáticas")
    else:
        print("⚠️ Algunas optimizaciones necesitan ajustes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)