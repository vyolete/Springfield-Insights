#!/usr/bin/env python3
"""
Ejecutor para la versión FINAL de Springfield Insights
SÚPER SIMPLE - Solo lo que funciona
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("🍩 SPRINGFIELD INSIGHTS - VERSIÓN FINAL")
    print("=" * 45)
    print("✅ SÚPER SIMPLE - Solo lo esencial")
    print("✅ Genera frases y análisis filosófico")
    print("✅ Funciona con OpenAI GPT-3.5")
    print("✅ Sin complejidad innecesaria")
    print("-" * 45)
    
    if not Path("app_final.py").exists():
        print("❌ app_final.py no encontrado")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_final.py",
            "--server.port", "8506"
        ])
    except KeyboardInterrupt:
        print("\n👋 ¡Gracias por usar Springfield Insights!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()