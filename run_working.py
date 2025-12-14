#!/usr/bin/env python3
"""
Script para ejecutar la versión FUNCIONAL de Springfield Insights
Basada en la versión original que funcionaba correctamente
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta la aplicación funcional"""
    print("🍩 INICIANDO SPRINGFIELD INSIGHTS - VERSIÓN FUNCIONAL")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("app_working.py").exists():
        print("❌ Error: app_working.py no encontrado")
        print("   Ejecuta desde el directorio springfield_insights/")
        return False
    
    print("✅ Aplicación funcional encontrada")
    print("🎭 Características de esta versión:")
    print("   • ✅ Basada en la versión original que funcionaba")
    print("   • ✅ Genera reflexiones con GPT-3.5 (rápido)")
    print("   • ✅ Muestra el texto generado por IA correctamente")
    print("   • ✅ Análisis filosófico riguroso")
    print("   • ✅ Interfaz simple y estable")
    print("   • ✅ Sin complejidad innecesaria")
    print("-" * 60)
    
    try:
        # Ejecutar Streamlit con la aplicación funcional
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_working.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.primaryColor", "#FFD700",
            "--theme.backgroundColor", "#FFF8DC",
            "--theme.secondaryBackgroundColor", "#F0E68C",
            "--theme.textColor", "#2F4F4F",
            "--server.port", "8505"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar Springfield Insights Funcional!")
        print("   D'oh! Hasta la próxima...")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando aplicación: {e}")
        print("   Intenta ejecutar manualmente: streamlit run app_working.py")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)