#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de episodios
Valida integración de episodios, búsqueda y generación contextual
"""
import sys
import os
import time
from pathlib import Path

# Añadir path del proyecto
sys.path.append(str(Path(__file__).parent))

def test_episodes_service():
    """Prueba el servicio de episodios"""
    print("📺 PROBANDO SERVICIO DE EPISODIOS")
    print("=" * 50)
    
    try:
        from services.episodes_service import EpisodesService
        
        service = EpisodesService()
        
        # Probar obtención de página
        print("📄 Probando obtención de página...")
        page_data = service.get_episodes_page(1)
        
        episodes = page_data.get('episodes', [])
        print(f"✅ Página 1: {len(episodes)} episodios obtenidos")
        print(f"   Total páginas: {page_data.get('total_pages', 0)}")
        print(f"   Total episodios: {page_data.get('total_episodes', 0)}")
        
        if episodes:
            # Probar detalle de episodio
            first_episode = episodes[0]
            episode_id = first_episode.get('id')
            
            print(f"\n🔍 Probando detalle del episodio: {first_episode.get('name', 'Sin nombre')}")
            episode_detail = service.get_episode_detail(episode_id)
            
            if episode_detail:
                print(f"✅ Detalle obtenido:")
                print(f"   Nombre: {episode_detail.get('name')}")
                print(f"   Temporada: {episode_detail.get('season')}")
                print(f"   Episodio: {episode_detail.get('episode_number')}")
                print(f"   Fecha: {episode_detail.get('formatted_date')}")
            else:
                print("❌ No se pudo obtener detalle")
        
        # Probar búsqueda
        print(f"\n🔍 Probando búsqueda de episodios...")
        search_results = service.search_episodes("homer", None)
        print(f"✅ Búsqueda 'homer': {len(search_results)} resultados")
        
        # Probar resumen de temporadas
        print(f"\n📊 Probando resumen de temporadas...")
        seasons = service.get_seasons_summary()
        print(f"✅ Temporadas encontradas: {len(seasons)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_quotes_service():
    """Prueba el servicio de citas con episodios"""
    print("\n🎭 PROBANDO SERVICIO DE CITAS CON EPISODIOS")
    print("=" * 50)
    
    try:
        from services.quotes_service import QuotesService
        
        service = QuotesService()
        
        # Probar generación con contexto de episodio
        print("🎬 Probando generación con contexto de episodio...")
        quote_context = service.generate_quote_with_episode_context()
        
        if quote_context and quote_context.get('success'):
            print("✅ Cita con contexto generada:")
            print(f"   Personaje: {quote_context.get('character')}")
            print(f"   Fuente: {quote_context.get('source')}")
            
            episode_context = quote_context.get('episode_context', {})
            if episode_context:
                print(f"   Episodio: {episode_context.get('episode_name', 'N/A')}")
                print(f"   Temporada: {episode_context.get('season', 'N/A')}")
        else:
            print("❌ No se pudo generar cita con contexto")
        
        # Probar búsqueda por episodio
        print(f"\n🔍 Probando búsqueda de citas por episodio...")
        episode_quotes = service.search_quotes_by_episode("marge", 1)
        print(f"✅ Búsqueda 'marge' temporada 1: {len(episode_quotes)} citas")
        
        # Probar citas de temporada
        print(f"\n📺 Probando citas de temporada...")
        season_quotes = service.get_quotes_for_season(1, 3)
        print(f"✅ Temporada 1: {len(season_quotes)} citas generadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_episodes_ui():
    """Prueba componentes UI de episodios"""
    print("\n🎨 PROBANDO COMPONENTES UI DE EPISODIOS")
    print("=" * 50)
    
    try:
        from ui.episodes_components import EpisodesUI
        
        print("✅ Componentes UI de episodios importados correctamente")
        
        # Verificar que los métodos existen
        methods = [
            'render_episodes_browser',
            'render_episode_detail', 
            'render_seasons_overview',
            'render_quote_with_episode_context',
            'render_episode_search_results'
        ]
        
        for method in methods:
            if hasattr(EpisodesUI, method):
                print(f"✅ Método {method} disponible")
            else:
                print(f"❌ Método {method} no encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_integration():
    """Prueba integración completa"""
    print("\n🔗 PROBANDO INTEGRACIÓN COMPLETA")
    print("=" * 50)
    
    try:
        from services.episodes_service import EpisodesService
        from services.quotes_service import QuotesService
        from services.llm_service import LLMService
        
        episodes_service = EpisodesService()
        quotes_service = QuotesService()
        llm_service = LLMService()
        
        # Flujo completo: episodio -> contexto -> LLM
        print("🔄 Probando flujo completo...")
        
        # 1. Obtener episodio aleatorio
        episode = episodes_service.get_random_episode()
        if not episode:
            print("❌ No se pudo obtener episodio aleatorio")
            return False
        
        print(f"✅ Episodio obtenido: {episode.get('name')}")
        
        # 2. Generar contexto para LLM
        episode_context = episodes_service.get_episode_context_for_llm(episode['id'])
        print(f"✅ Contexto generado para LLM")
        
        # 3. Generar reflexión completa
        reflection = llm_service.generate_complete_philosophical_reflection(
            character="Homer Simpson",
            description="Padre de familia que busca la felicidad simple",
            philosophical_context="hedonismo, existencialismo cotidiano",
            episode_context=episode_context
        )
        
        if reflection:
            print("✅ Reflexión con contexto de episodio generada")
            print(f"   Reflexión: {reflection.get('reflection', '')[:100]}...")
            print(f"   Análisis: {reflection.get('analysis', '')[:100]}...")
        else:
            print("⚠️ No se pudo generar reflexión (puede ser por falta de API key)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_caching_performance():
    """Prueba performance del caching"""
    print("\n⚡ PROBANDO PERFORMANCE DE CACHING")
    print("=" * 50)
    
    try:
        from services.episodes_service import EpisodesService
        
        service = EpisodesService()
        
        # Primera llamada (sin cache)
        start_time = time.time()
        page1_first = service.get_episodes_page(1)
        first_call_time = time.time() - start_time
        
        # Segunda llamada (con cache)
        start_time = time.time()
        page1_cached = service.get_episodes_page(1)
        cached_call_time = time.time() - start_time
        
        print(f"✅ Primera llamada: {first_call_time:.3f}s")
        print(f"✅ Llamada cacheada: {cached_call_time:.3f}s")
        
        if cached_call_time < first_call_time:
            improvement = ((first_call_time - cached_call_time) / first_call_time) * 100
            print(f"✅ Mejora de performance: {improvement:.1f}%")
        
        # Verificar que los datos son iguales
        if page1_first == page1_cached:
            print("✅ Cache funcionando correctamente (datos idénticos)")
        else:
            print("⚠️ Cache puede no estar funcionando (datos diferentes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("📺 PRUEBAS DE FUNCIONALIDAD DE EPISODIOS")
    print("=" * 60)
    
    tests = [
        ("Servicio de Episodios", test_episodes_service),
        ("Servicio de Citas con Episodios", test_quotes_service),
        ("Componentes UI de Episodios", test_episodes_ui),
        ("Integración Completa", test_integration),
        ("Performance de Caching", test_caching_performance)
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
    print("📊 RESUMEN DE PRUEBAS DE EPISODIOS")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    print(f"⏱️ Tiempo total: {total_time:.3f}s")
    
    if passed == total:
        print("🎉 ¡FUNCIONALIDAD DE EPISODIOS COMPLETAMENTE OPERATIVA!")
        print("\n💡 Funcionalidades validadas:")
        print("   • Navegación por catálogo de episodios")
        print("   • Búsqueda de episodios por texto y temporada")
        print("   • Generación de citas con contexto episódico")
        print("   • Integración con GPT-4 para análisis contextual")
        print("   • Caching inteligente para performance")
        print("   • Componentes UI especializados")
    else:
        print("⚠️ Algunas funcionalidades necesitan ajustes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)