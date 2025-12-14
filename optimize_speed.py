#!/usr/bin/env python3
"""
Script para optimizar Springfield Insights para máxima velocidad
Aplica configuración optimizada automáticamente
"""
import os
import shutil
from pathlib import Path

def optimize_for_speed():
    """Aplica optimizaciones de velocidad"""
    print("⚡ OPTIMIZANDO SPRINGFIELD INSIGHTS PARA VELOCIDAD")
    print("=" * 55)
    
    # 1. Backup de configuración actual
    env_file = Path('.env')
    if env_file.exists():
        backup_file = Path('.env.backup')
        shutil.copy2(env_file, backup_file)
        print(f"✅ Backup creado: {backup_file}")
    
    # 2. Aplicar configuración optimizada
    speed_config = Path('.env.speed')
    if speed_config.exists():
        # Leer configuración actual para preservar API key
        current_api_key = None
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY=') and not line.strip().endswith('tu_api_key_aqui'):
                        current_api_key = line.strip().split('=', 1)[1]
                        break
        
        # Aplicar configuración optimizada
        with open(speed_config, 'r') as f:
            content = f.read()
        
        # Reemplazar API key si existe
        if current_api_key:
            content = content.replace('OPENAI_API_KEY=tu_api_key_aqui', f'OPENAI_API_KEY={current_api_key}')
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Configuración optimizada aplicada")
    
    # 3. Mostrar configuración aplicada
    print("\n📊 CONFIGURACIÓN OPTIMIZADA:")
    print("   • Modelo: gpt-3.5-turbo (más rápido que GPT-4)")
    print("   • Max Tokens: 250 (reducido para velocidad)")
    print("   • Temperature: 0.4 (más consistente)")
    print("   • Timeout LLM: 8s (muy agresivo)")
    print("   • Timeout API: 5s (rápido)")
    
    # 4. Instrucciones
    print("\n💡 PRÓXIMOS PASOS:")
    print("   1. Asegúrate de que tu OPENAI_API_KEY esté configurada")
    print("   2. Ejecuta: python3 run_optimized.py")
    print("   3. ¡Disfruta de análisis académicos en ~3 segundos!")
    
    print("\n🔄 PARA REVERTIR:")
    print("   • Restaura desde .env.backup si necesitas la configuración anterior")
    
    print("\n" + "=" * 55)
    print("⚡ OPTIMIZACIÓN COMPLETADA")

if __name__ == "__main__":
    optimize_for_speed()