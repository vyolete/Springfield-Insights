#!/usr/bin/env python3
"""
Script para ejecutar la versión optimizada de Springfield Insights
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta la aplicación optimizada"""
    print("🍩 INICIANDO SPRINGFIELD INSIGHTS OPTIMIZADO")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("app_optimized.py").exists():
        print("❌ Error: app_optimized.py no encontrado")
        print("   Ejecuta desde el directorio springfield_insights/")
        return False
    
    print("✅ Aplicación optimizada encontrada")
    print("🚀 Iniciando Streamlit con configuración optimizada...")
    print("-" * 50)
    
    try:
        # Ejecutar Streamlit con la aplicación optimizada
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_optimized.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.primaryColor", "#FFD700",
            "--theme.backgroundColor", "#FFF8DC",
            "--theme.secondaryBackgroundColor", "#F0E68C",
            "--theme.textColor", "#2F4F4F",
            "--server.maxUploadSize", "10",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar Springfield Insights Optimizado!")
        print("   D'oh! Hasta la próxima...")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando aplicación: {e}")
        print("   Intenta ejecutar manualmente: streamlit run app_optimized.py")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)