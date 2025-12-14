#!/usr/bin/env python3
"""
Script de ejecución para Springfield Insights
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta Springfield Insights"""
    
    print("🍩 SPRINGFIELD INSIGHTS")
    print("=" * 40)
    print("✅ Versión modular y limpia")
    print("✅ GPT-4 para análisis profundos")
    print("=" * 40)
    
    # Verificar archivo .env
    if not Path(".env").exists():
        print("⚠️  Archivo .env no encontrado")
        if Path(".env.example").exists():
            print("💡 Copia .env.example a .env y configura tu OPENAI_API_KEY")
        return
    
    print("🚀 Iniciando aplicación...")
    print("   Presiona Ctrl+C para detener")
    print("-" * 40)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 ¡Gracias por usar Springfield Insights!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()