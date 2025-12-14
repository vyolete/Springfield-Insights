#!/usr/bin/env python3
"""
Script de ejecución local para Springfield Insights
Implementa validación completa del entorno antes de ejecutar la aplicación
"""
import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    """Imprime banner de inicio"""
    print("\n" + "="*60)
    print("🍩 SPRINGFIELD INSIGHTS - EJECUCIÓN LOCAL")
    print("="*60)
    print("Validación académica del entorno y ejecución segura")
    print("="*60 + "\n")

def check_python_version():
    """Verifica versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ requerido. Versión actual: {sys.version}")
        print("   Instala Python 3.8+ desde https://python.org")
        return False
    
    if sys.version_info < (3, 10):
        print(f"⚠️  Python 3.10+ recomendado. Versión actual: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print("   La aplicación funcionará pero algunas características pueden estar limitadas")
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Verifica dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        'streamlit',
        'openai', 
        'requests',
        'python-dotenv',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Manejar casos especiales de nombres de módulos
            if package == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(missing_packages)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_environment_file():
    """Verifica archivo de configuración"""
    print("\n🔧 Verificando configuración...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  Archivo .env no encontrado")
            print("   Copiando desde .env.example...")
            
            # Copiar plantilla
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                content = src.read()
                dst.write(content)
            
            print("✅ Archivo .env creado desde plantilla")
            print("🔑 IMPORTANTE: Configura tu OPENAI_API_KEY en .env")
            return False
        else:
            print("❌ Ni .env ni .env.example encontrados")
            return False
    
    print("✅ Archivo .env encontrado")
    
    # Verificar variables críticas
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key or openai_key == 'tu-clave-api-de-openai-aqui':
            print("⚠️  OPENAI_API_KEY no configurada correctamente")
            print("   Edita .env y configura tu clave real de OpenAI")
            return False
        
        print("✅ OPENAI_API_KEY configurada")
        
    except ImportError:
        print("⚠️  python-dotenv no disponible, usando variables del sistema")
    
    return True

def run_environment_validation():
    """Ejecuta validación completa del entorno"""
    print("\n🔍 Ejecutando validación completa del entorno...")
    
    try:
        # Importar y ejecutar validador
        sys.path.append(str(Path.cwd()))
        from config.environment_validator import validate_environment_startup
        
        can_run, results = validate_environment_startup()
        
        if can_run:
            print("\n🎉 ¡Validación exitosa! La aplicación puede ejecutarse.")
            return True
        else:
            print("\n❌ Validación falló. Revisa los errores arriba.")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante validación: {e}")
        print("   La aplicación intentará ejecutarse de todas formas...")
        return True  # Permitir ejecución con advertencia

def run_streamlit():
    """Ejecuta la aplicación Streamlit"""
    print("\n🚀 Iniciando Springfield Insights...")
    print("   Presiona Ctrl+C para detener la aplicación")
    print("   La aplicación se abrirá en tu navegador automáticamente")
    print("-" * 60)
    
    try:
        # Ejecutar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.primaryColor", "#FFD700",
            "--theme.backgroundColor", "#FFF8DC"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar Springfield Insights!")
        print("   D'oh! Hasta la próxima...")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando Streamlit: {e}")
        print("   Intenta ejecutar manualmente: streamlit run app.py")

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones previas
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        print("\n💡 Instala las dependencias y vuelve a ejecutar este script")
        sys.exit(1)
    
    if not check_environment_file():
        print("\n💡 Configura el archivo .env y vuelve a ejecutar este script")
        sys.exit(1)
    
    # Validación completa
    if not run_environment_validation():
        response = input("\n¿Quieres intentar ejecutar de todas formas? (y/N): ")
        if response.lower() != 'y':
            print("👋 Configuración cancelada")
            sys.exit(1)
    
    # Ejecutar aplicación
    run_streamlit()

if __name__ == "__main__":
    main()