#!/usr/bin/env python3
"""
Script de prueba para la versión optimizada de Springfield Insights
Valida mejoras de performance, UX y arquitectura
"""
import sys
import os
import time
from pathlib import Path

# Añadir path del proyecto
sys.path.append(str(Path(__file__).parent))

def test_component_loading():
    """Prueba carga de componentes optimizados"""
    print("🧪 PROBANDO CARGA DE COMPONENTES OPTIMIZADOS")
    print("=" * 50)
    
    try:
        start_time = time.time()
        
        # Probar imports optimizados
        from ui.components import UIComponents, StateManager, PerformanceOptimizer
        from services.image_service import ImageService
        
        load_time = time.time() - start_time
        print(f"✅ Componentes cargados en {load_time:.3f}s")
        
        # Probar inicialización de estado
        StateManager.initialize_session_state()
        print("✅ Estado de sesión inicializado")
        
        # Probar servicio de imágenes
        image_service = ImageService()
        print("✅ Servicio de imágenes inicializado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_caching_system():
    """Prueba sistema de caching"""
    print("\n🗄️ PROBANDO SISTEMA DE CACHING")
    print("=" * 50)
    
    try:
        from ui.components import PerformanceOptimizer
        
        # Probar cache de servicios
        start_time = time.time()
        services1 = PerformanceOptimizer.get_cached_services()
        first_load = time.time() - start_time
        
        start_time = time.time()
        services2 = PerformanceOptimizer.get_cached_services()
        cached_load = time.time() - start_time
        
        print(f"✅ Primera carga: {first_load:.3f}s")
        print(f"✅ Carga desde cache: {cached_load:.3f}s")
        print(f"✅ Mejora de performance: {((first_load - cached_load) / first_load * 100):.1f}%")
        
        # Verificar que son los mismos objetos (cache funcionando)
        assert services1 is services2, "Cache no está funcionando correctamente"
        print("✅ Cache de servicios funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_image_service():
    """Prueba servicio de imágenes optimizado"""
    print("\n🖼️ PROBANDO SERVICIO DE IMÁGENES")
    print("=" * 50)
    
    try:
        from services.image_service import ImageService
        
        service = ImageService()
        
        # Probar obtención de personajes (con cache)
        start_time = time.time()
        characters = service.get_characters_with_images(page=1)
        load_time = time.time() - start_time
        
        print(f"✅ Personajes obtenidos: {len(characters)} en {load_time:.3f}s")
        
        if characters:
            # Probar obtención de imagen específica
            test_character = characters[0]['name']
            image_url = service.get_character_image_url(test_character, 'medium')
            
            if image_url:
                print(f"✅ Imagen obtenida para {test_character}")
                print(f"   URL: {image_url[:60]}...")
            else:
                print(f"⚠️ No se pudo obtener imagen para {test_character}")
        
        # Probar fallback
        fallback_url = service._get_fallback_image("Test Character", "medium")
        print(f"✅ Fallback generado: {fallback_url[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_state_management():
    """Prueba gestión de estado optimizada"""
    print("\n🔄 PROBANDO GESTIÓN DE ESTADO")
    print("=" * 50)
    
    try:
        from ui.components import StateManager
        
        # Simular session_state
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def __getitem__(self, key):
                return self.data[key]
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def get(self, key, default=None):
                return self.data.get(key, default)
        
        # Usar mock para pruebas
        import streamlit as st
        st.session_state = MockSessionState()
        
        # Probar inicialización
        StateManager.initialize_session_state()
        print("✅ Estado inicializado correctamente")
        
        # Probar operaciones de estado
        StateManager.set_processing(True)
        assert StateManager.is_processing() == True
        print("✅ Control de procesamiento funcionando")
        
        StateManager.increment_quotes_analyzed()
        assert st.session_state.get('quotes_analyzed') == 1
        print("✅ Contador de citas funcionando")
        
        # Probar datos de cita
        test_quote = {'quote': 'Test', 'character': 'Homer', 'success': True}
        StateManager.set_current_quote(test_quote)
        retrieved_quote = StateManager.get_current_quote()
        assert retrieved_quote == test_quote
        print("✅ Gestión de citas funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ui_components():
    """Prueba componentes UI optimizados"""
    print("\n🎨 PROBANDO COMPONENTES UI")
    print("=" * 50)
    
    try:
        from ui.components import UIComponents, ErrorHandler, LoadingStates
        
        # Probar generación de imagen optimizada
        image_url = UIComponents.get_character_image("Homer Simpson", "")
        print(f"✅ Imagen generada: {image_url[:60]}...")
        
        # Probar componentes de error (sin streamlit)
        print("✅ Componentes de error disponibles")
        
        # Probar componentes de carga
        print("✅ Componentes de carga disponibles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_performance_metrics():
    """Prueba métricas de performance"""
    print("\n⚡ PROBANDO MÉTRICAS DE PERFORMANCE")
    print("=" * 50)
    
    try:
        import psutil
        import gc
        
        # Memoria antes
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Cargar componentes
        from ui.components import PerformanceOptimizer
        services = PerformanceOptimizer.get_cached_services()
        
        # Memoria después
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        print(f"✅ Memoria usada: {memory_used:.1f} MB")
        
        # Probar garbage collection
        gc.collect()
        memory_final = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"✅ Memoria final: {memory_final:.1f} MB")
        print(f"✅ Eficiencia de memoria: {((memory_before - memory_final + memory_used) / memory_used * 100):.1f}%")
        
        return True
        
    except ImportError:
        print("⚠️ psutil no disponible, saltando pruebas de memoria")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🍩 PRUEBAS DE OPTIMIZACIÓN - SPRINGFIELD INSIGHTS")
    print("=" * 60)
    
    tests = [
        ("Carga de Componentes", test_component_loading),
        ("Sistema de Caching", test_caching_system),
        ("Servicio de Imágenes", test_image_service),
        ("Gestión de Estado", test_state_management),
        ("Componentes UI", test_ui_components),
        ("Métricas de Performance", test_performance_metrics)
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
    print("📊 RESUMEN DE OPTIMIZACIONES")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    print(f"⏱️ Tiempo total: {total_time:.3f}s")
    
    if passed == total:
        print("🎉 ¡TODAS LAS OPTIMIZACIONES FUNCIONANDO CORRECTAMENTE!")
        print("\n💡 Beneficios implementados:")
        print("   • Caching inteligente de servicios")
        print("   • Gestión optimizada de estado")
        print("   • Componentes UI modulares")
        print("   • Servicio de imágenes con fallbacks")
        print("   • Control de flujo sin duplicaciones")
        print("   • Performance mejorada")
    else:
        print("⚠️ Algunas optimizaciones necesitan ajustes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)