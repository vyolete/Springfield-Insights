#!/usr/bin/env python3
"""
🍩 Springfield Insights - Launcher Limpio
Ejecuta la aplicación con configuración optimizada y warnings suprimidos
"""

import os
import sys
import warnings
import subprocess
from pathlib import Path

def setup_environment():
    """Configura el entorno para ejecución limpia"""
    
    # Suprimir warnings específicos
    warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
    os.environ["PYTHONWARNINGS"] = "ignore::urllib3.exceptions.NotOpenSSLWarning"
    
    # Configurar variables de Streamlit
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

def check_requirements():
    """Verifica que los requisitos estén instalados"""
    
    print("🔍 Verificando dependencias...")
    
    try:
        import streamlit
        import openai
        print("✅ Dependencias principales verificadas")
        return True
    except ImportError as e:
        print(f"❌ Error: Falta dependencia - {e}")
        print("💡 Instala con: pip install -r requirements.txt")
        return False

def check_config():
    """Verifica la configuración"""
    
    # Verificar archivo .env
    if not Path(".env").exists():
        print("⚠️  Advertencia: No se encuentra archivo .env")
        print("💡 Copia .env.example a .env y configura tu OPENAI_API_KEY")
        return False
    
    # Verificar app.py
    if not Path("app.py").exists():
        print("❌ Error: No se encuentra app.py")
        print("💡 Ejecuta desde el directorio springfield_insights/")
        return False
    
    return True

def run_app():
    """Ejecuta la aplicación Streamlit"""
    
    print("\n🍩 Springfield Insights")
    print("=" * 50)
    print("🎭 Explorando la filosofía de Los Simpsons")
    print("🤖 Análisis con GPT-4")
    print("🌐 API oficial de Los Simpsons")
    print("=" * 50)
    
    # Configurar comando
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8503",
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false",
        "--server.fileWatcherType", "none",
        "--theme.base", "light",
        "--theme.primaryColor", "#FF6347",
        "--theme.backgroundColor", "#FFF8DC",
        "--theme.secondaryBackgroundColor", "#F0F8FF"
    ]
    
    print("\n🚀 Iniciando aplicación...")
    print("🌐 URL: http://localhost:8503")
    print("💡 Para detener: Ctrl+C")
    print("\n" + "=" * 50 + "\n")
    
    try:
        # Ejecutar Streamlit
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Aplicación detenida por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error ejecutando la aplicación: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    
    # Configurar entorno
    setup_environment()
    
    # Verificar requisitos
    if not check_requirements():
        sys.exit(1)
    
    # Verificar configuración
    if not check_config():
        print("\n⚠️  Continuando con advertencias...")
    
    # Ejecutar aplicación
    success = run_app()
    
    if success:
        print("\n✅ Aplicación ejecutada exitosamente")
    else:
        print("\n❌ Error en la ejecución")
        sys.exit(1)

if __name__ == "__main__":
    main()