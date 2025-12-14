"""
Script de setup para Springfield Insights
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 10):
        print("❌ Error: Se requiere Python 3.10 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def create_directories():
    """Crea directorios necesarios"""
    directories = ['logs', 'data', '.streamlit']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio '{directory}' creado/verificado")

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crea archivo .env si no existe"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return
    
    print("📝 Creando archivo .env...")
    
    # Solicitar API key al usuario
    api_key = input("Ingresa tu OpenAI API Key (o presiona Enter para configurar después): ").strip()
    
    env_content = f"""# Configuración de Springfield Insights
# OpenAI API Key (requerida)
OPENAI_API_KEY={api_key if api_key else 'tu-api-key-aqui'}

# Configuración opcional
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    
    if not api_key:
        print("⚠️  Recuerda configurar tu OPENAI_API_KEY en el archivo .env")

def create_streamlit_config():
    """Crea configuración de Streamlit"""
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    
    if config_file.exists():
        print("✅ Configuración de Streamlit ya existe")
        return
    
    print("📝 Creando configuración de Streamlit...")
    
    config_content = """[theme]
primaryColor = "#FFD700"
backgroundColor = "#FFF8DC"
secondaryBackgroundColor = "#F0E68C"
textColor = "#2F4F4F"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
"""
    
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✅ Configuración de Streamlit creada")

def run_tests():
    """Ejecuta tests básicos"""
    print("🧪 Ejecutando tests básicos...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ])
        print("✅ Tests ejecutados correctamente")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Tests fallaron, pero la instalación puede continuar")
        return False
    except FileNotFoundError:
        print("⚠️  pytest no encontrado, saltando tests")
        return False

def main():
    """Función principal de setup"""
    print("🍩 Springfield Insights - Setup")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Setup fallido en instalación de dependencias")
        sys.exit(1)
    
    # Crear archivos de configuración
    create_env_file()
    create_streamlit_config()
    
    # Ejecutar tests (opcional)
    run_tests()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completado exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Configura tu OPENAI_API_KEY en el archivo .env")
    print("2. Ejecuta la aplicación con: streamlit run app.py")
    print("3. Abre tu navegador en: http://localhost:8501")
    print("\n🔧 Para desarrollo:")
    print("- Ejecutar tests: python -m pytest tests/")
    print("- Ver logs: tail -f logs/springfield_insights_*.log")

if __name__ == "__main__":
    main()