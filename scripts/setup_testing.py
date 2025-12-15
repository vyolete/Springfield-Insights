#!/usr/bin/env python3
"""
Script de configuración para el entorno de testing de Springfield Insights
Instala dependencias y configura Playwright automáticamente
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description="", check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}")
    print(f"Ejecutando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        print(f"✅ {description} - Exitoso")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} no es compatible")
        print("Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_requirements():
    """Instala las dependencias del requirements.txt"""
    print("\n📦 Instalando dependencias de Python...")
    
    # Actualizar pip primero
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      "Actualizando pip"):
        return False
    
    # Instalar requirements
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Instalando dependencias"):
        return False
    
    return True

def setup_playwright():
    """Configura Playwright para tests E2E"""
    print("\n🎭 Configurando Playwright...")
    
    # Instalar navegadores
    commands = [
        ([sys.executable, "-m", "playwright", "install", "chromium"], 
         "Instalando navegador Chromium"),
        ([sys.executable, "-m", "playwright", "install-deps"], 
         "Instalando dependencias del sistema")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc, check=False):
            print("⚠️ Error configurando Playwright. Tests E2E podrían no funcionar.")
            return False
    
    return True

def verify_installation():
    """Verifica que todo esté instalado correctamente"""
    print("\n🔍 Verificando instalación...")
    
    # Verificar paquetes Python
    packages_to_check = [
        ("pytest", "pytest"),
        ("playwright", "playwright"),
        ("pytest_asyncio", "pytest-asyncio"),
        ("pytest_mock", "pytest-mock")
    ]
    
    all_good = True
    
    for import_name, package_name in packages_to_check:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - Instalado correctamente")
        except ImportError:
            print(f"❌ {package_name} - Error de importación")
            all_good = False
    
    # Verificar Playwright
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "--version"], 
            capture_output=True, text=True, check=True
        )
        print(f"✅ Playwright - {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ Playwright - No funciona correctamente")
        all_good = False
    
    return all_good

def create_test_env_file():
    """Crea archivo .env.test para testing"""
    print("\n📝 Creando archivo de configuración para tests...")
    
    test_env_content = """# Configuración para testing de Springfield Insights
# Este archivo es usado automáticamente por los tests

# Mock API Key para testing (no es una key real)
OPENAI_API_KEY=sk-test-mock-api-key-for-testing-only

# Configuración de Streamlit para testing
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_PORT=8502

# Configuración de logging para tests
LOG_LEVEL=WARNING
"""
    
    try:
        with open(".env.test", "w") as f:
            f.write(test_env_content)
        print("✅ Archivo .env.test creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env.test: {e}")
        return False

def show_usage_instructions():
    """Muestra instrucciones de uso"""
    print("\n" + "=" * 60)
    print("🎉 ¡Configuración de testing completada!")
    print("=" * 60)
    
    print("\n📋 Comandos disponibles:")
    print("\n1. Ejecutar todos los tests:")
    print("   python scripts/run_tests.py")
    
    print("\n2. Solo tests unitarios (rápidos):")
    print("   python scripts/run_tests.py --type unit")
    
    print("\n3. Solo tests E2E (requieren Streamlit):")
    print("   python scripts/run_tests.py --type e2e")
    
    print("\n4. Tests con reporte de cobertura:")
    print("   python scripts/run_tests.py --type coverage")
    
    print("\n5. Verificar dependencias:")
    print("   python scripts/run_tests.py --check-deps")
    
    print("\n📁 Estructura de tests creada:")
    print("   tests/")
    print("   ├── conftest.py           # Configuración global")
    print("   ├── test_mock_quote_service.py  # Tests unitarios")
    print("   ├── test_e2e_main_flow.py       # Tests E2E")
    print("   └── mocks/")
    print("       └── mock_quote_service.py   # Mock de OpenAI")
    
    print("\n🔧 Configuración:")
    print("   ├── pytest.ini           # Configuración de pytest")
    print("   ├── .env.test            # Variables para testing")
    print("   └── scripts/")
    print("       ├── run_tests.py     # Ejecutor de tests")
    print("       └── setup_testing.py # Este script")
    
    print("\n🎯 Características del framework:")
    print("   ✅ Mock completo de OpenAI (sin llamadas reales)")
    print("   ✅ Tests E2E con Playwright")
    print("   ✅ Selectores estables (data-testid)")
    print("   ✅ 100% reproducible")
    print("   ✅ Listo para CI/CD")

def main():
    """Función principal"""
    print("🍩 Springfield Insights - Configuración de Testing")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Directorio del proyecto: {project_root}")
    
    # Verificaciones y configuración paso a paso
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependencias", install_requirements),
        ("Configurar Playwright", setup_playwright),
        ("Crear configuración de test", create_test_env_file),
        ("Verificar instalación", verify_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"\n❌ Error en: {step_name}")
            print("La configuración no se completó correctamente.")
            sys.exit(1)
    
    # Mostrar instrucciones finales
    show_usage_instructions()

if __name__ == "__main__":
    main()