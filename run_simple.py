#!/usr/bin/env python3
"""
Script para ejecutar la versión SIMPLE y RÁPIDA de Springfield Insights
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta la aplicación simple"""
    print("🍩 INICIANDO SPRINGFIELD INSIGHTS - VERSIÓN SIMPLE")
    print("=" * 55)
    
    # Verificar que estamos en el directorio correcto
    if not Path("app_simple.py").exists():
        print("❌ Error: app_simple.py no encontrado")
        print("   Ejecuta desde el directorio springfield_insights/")
        return False
    
    print("✅ Aplicación simple encontrada")
    print("🚀 Características de esta versión:")
    print("   • Frases REALES de Los Simpsons")
    print("   • Análisis filosófico con GPT-3.5")
    print("   • Imágenes de personajes")
    print("   • Interfaz simple y rápida")
    print("   • Sin complejidad innecesaria")
    print("-" * 55)
    
    try:
        # Ejecutar Streamlit con la aplicación simple
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_simple.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.primaryColor", "#FFD700",
            "--theme.backgroundColor", "#FFF8DC",
            "--theme.secondaryBackgroundColor", "#F0E68C",
            "--theme.textColor", "#2F4F4F",
            "--server.port", "8503"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar Springfield Insights Simple!")
        print("   D'oh! Hasta la próxima...")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando aplicación: {e}")
        print("   Intenta ejecutar manualmente: streamlit run app_simple.py")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)