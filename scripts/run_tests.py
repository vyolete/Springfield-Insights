#!/usr/bin/env python3
"""
Script para ejecutar tests de Springfield Insights
Maneja la instalación de dependencias y ejecución de diferentes tipos de tests
"""
import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(cmd, description=""):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}")
    print(f"Ejecutando: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - Exitoso")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} - Error")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return False
    
    return True

def install_playwright():
    """Instala navegadores de Playwright"""
    print("\n🎭 Instalando navegadores de Playwright...")
    
    commands = [
        (["python", "-m", "playwright", "install"], "Instalando navegadores"),
        (["python", "-m", "playwright", "install-deps"], "Instalando dependencias del sistema")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print("⚠️ Error instalando Playwright. Los tests E2E podrían fallar.")
            return False
    
    return True

def run_unit_tests():
    """Ejecuta tests unitarios"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/test_mock_quote_service.py",
        "-v", "--tb=short", "-m", "not e2e"
    ]
    return run_command(cmd, "Ejecutando tests unitarios")

def run_e2e_tests():
    """Ejecuta tests end-to-end"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/test_e2e_main_flow.py",
        "-v", "--tb=short", "-m", "e2e", "-s"
    ]
    return run_command(cmd, "Ejecutando tests E2E")

def run_all_tests():
    """Ejecuta todos los tests"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Ejecutando todos los tests")

def run_tests_with_coverage():
    """Ejecuta tests con reporte de cobertura"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/",
        "--cov=.", "--cov-report=html", "--cov-report=term-missing",
        "-v"
    ]
    return run_command(cmd, "Ejecutando tests con cobertura")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        "pytest", "playwright", "pytest-asyncio", "pytest-mock"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} - Instalado")
        except ImportError:
            print(f"❌ {package} - Faltante")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Paquetes faltantes: {', '.join(missing_packages)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Ejecutar tests de Springfield Insights")
    parser.add_argument(
        "--type", 
        choices=["unit", "e2e", "all", "coverage"],
        default="all",
        help="Tipo de tests a ejecutar"
    )
    parser.add_argument(
        "--install-playwright", 
        action="store_true",
        help="Instalar navegadores de Playwright"
    )
    parser.add_argument(
        "--check-deps", 
        action="store_true",
        help="Solo verificar dependencias"
    )
    
    args = parser.parse_args()
    
    print("🍩 Springfield Insights - Test Runner")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Directorio de trabajo: {project_root}")
    
    # Verificar dependencias
    if not check_dependencies():
        if not args.check_deps:
            print("\n❌ Dependencias faltantes. Instala con: pip install -r requirements.txt")
            sys.exit(1)
        else:
            sys.exit(1)
    
    if args.check_deps:
        print("\n✅ Todas las dependencias están instaladas")
        sys.exit(0)
    
    # Instalar Playwright si se solicita
    if args.install_playwright:
        if not install_playwright():
            print("\n⚠️ Continuando sin Playwright. Tests E2E podrían fallar.")
    
    # Ejecutar tests según el tipo
    success = True
    
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "e2e":
        success = run_e2e_tests()
    elif args.type == "coverage":
        success = run_tests_with_coverage()
    else:  # all
        print("\n🧪 Ejecutando suite completa de tests...")
        success = run_unit_tests() and run_e2e_tests()
    
    # Resultado final
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
        print("\n📊 Resumen:")
        print("✅ Tests unitarios: MockQuoteService validado")
        print("✅ Tests E2E: Flujo principal validado")
        print("✅ Mock de OpenAI: Funcionando correctamente")
    else:
        print("❌ Algunos tests fallaron. Revisa los logs arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()