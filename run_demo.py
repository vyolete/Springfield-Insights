#!/usr/bin/env python3
"""
Script para ejecutar la versión DEMO de Springfield Insights
Funciona sin IA - Perfecto para demostraciones
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta la aplicación demo"""
    print("🍩 INICIANDO SPRINGFIELD INSIGHTS - VERSIÓN DEMO")
    print("=" * 55)
    
    # Verificar que estamos en el directorio correcto
    if not Path("app_demo.py").exists():
        print("❌ Error: app_demo.py no encontrado")
        print("   Ejecuta desde el directorio springfield_insights/")
        return False
    
    print("✅ Aplicación demo encontrada")
    print("🎭 Características de la versión DEMO:")
    print("   • ✅ Funciona SIN OpenAI (sin IA)")
    print("   • ✅ Análisis predefinidos de alta calidad")
    print("   • ✅ Frases REALES de Los Simpsons")
    print("   • ✅ Imágenes funcionando perfectamente")
    print("   • ✅ Experiencia completa sin configuración")
    print("   • ✅ Perfecto para demostraciones académicas")
    print("   • ✅ NUNCA se cuelga ni falla")
    print("-" * 55)
    
    try:
        # Ejecutar Streamlit con la aplicación demo
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_demo.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.primaryColor", "#FFD700",
            "--theme.backgroundColor", "#FFF8DC",
            "--theme.secondaryBackgroundColor", "#F0E68C",
            "--theme.textColor", "#2F4F4F",
            "--server.port", "8504"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar Springfield Insights Demo!")
        print("   D'oh! Hasta la próxima...")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando aplicación: {e}")
        print("   Intenta ejecutar manualmente: streamlit run app_demo.py")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)