#!/usr/bin/env python3
"""
Test rápido para verificar si OpenAI funciona y si hay créditos
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

# Cargar variables de entorno
load_dotenv()

def test_openai_connection():
    """Prueba la conexión y créditos de OpenAI"""
    
    print("🔍 VERIFICANDO CONEXIÓN Y CRÉDITOS DE OPENAI")
    print("=" * 50)
    
    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada en .env")
        print("   Crea un archivo .env con:")
        print("   OPENAI_API_KEY=tu_api_key_aqui")
        return False
    
    print(f"✅ API Key encontrada: ...{api_key[-4:]}")
    
    try:
        # Inicializar cliente
        client = OpenAI(api_key=api_key)
        print("✅ Cliente OpenAI inicializado")
        
        # Test simple y rápido
        print("\n🧪 Probando llamada simple...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Di solo 'Hola' en una palabra"}
            ],
            max_tokens=5,
            timeout=10
        )
        
        elapsed = time.time() - start_time
        
        if response.choices:
            result = response.choices[0].message.content.strip()
            print(f"✅ Respuesta recibida en {elapsed:.2f}s: '{result}'")
            print("✅ OpenAI funciona correctamente")
            print("✅ Tienes créditos disponibles")
            return True
        else:
            print("❌ Respuesta vacía de OpenAI")
            return False
            
    except Exception as e:
        error_str = str(e).lower()
        
        print(f"❌ Error: {e}")
        
        # Diagnóstico específico del error
        if "insufficient_quota" in error_str or "quota" in error_str:
            print("\n🚨 PROBLEMA: SIN CRÉDITOS")
            print("   • Tu cuenta de OpenAI no tiene créditos")
            print("   • Necesitas añadir créditos en https://platform.openai.com/billing")
            print("   • O usar una API key diferente con créditos")
            
        elif "invalid_api_key" in error_str or "unauthorized" in error_str:
            print("\n🚨 PROBLEMA: API KEY INVÁLIDA")
            print("   • La API key no es válida")
            print("   • Verifica en https://platform.openai.com/api-keys")
            print("   • Asegúrate de copiar la key completa")
            
        elif "timeout" in error_str:
            print("\n🚨 PROBLEMA: TIMEOUT")
            print("   • La conexión está muy lenta")
            print("   • Verifica tu conexión a internet")
            print("   • Intenta de nuevo en unos minutos")
            
        else:
            print("\n🚨 PROBLEMA DESCONOCIDO")
            print("   • Error no identificado")
            print("   • Verifica tu conexión a internet")
            print("   • Revisa el estado de OpenAI en https://status.openai.com/")
        
        return False

def suggest_solutions():
    """Sugiere soluciones alternativas"""
    
    print("\n💡 SOLUCIONES ALTERNATIVAS")
    print("=" * 35)
    
    print("\n🔄 OPCIÓN 1: Usar versión sin IA")
    print("   • Crear versión que solo muestre frases sin análisis")
    print("   • Mostrar contexto predefinido")
    print("   • No requiere OpenAI")
    
    print("\n💳 OPCIÓN 2: Añadir créditos")
    print("   • Ir a https://platform.openai.com/billing")
    print("   • Añadir $5-10 USD")
    print("   • Usar la aplicación normalmente")
    
    print("\n🆓 OPCIÓN 3: Usar API key gratuita")
    print("   • Crear nueva cuenta en OpenAI")
    print("   • Usar créditos gratuitos iniciales")
    print("   • Configurar nueva API key")
    
    print("\n🎭 OPCIÓN 4: Versión demo")
    print("   • Crear versión con análisis predefinidos")
    print("   • Simular funcionalidad de IA")
    print("   • Perfecta para demostraciones")

if __name__ == "__main__":
    success = test_openai_connection()
    
    if not success:
        suggest_solutions()
        
        print("\n" + "=" * 50)
        print("🎯 RECOMENDACIÓN: Crear versión demo sin IA")
        print("=" * 50)
    else:
        print("\n🎉 ¡Todo funciona! La aplicación debería trabajar correctamente.")