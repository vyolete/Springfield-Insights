#!/bin/bash

# ========================================
# 🍩 Springfield Insights - Script de Ejecución
# ========================================

echo "🍩 Iniciando Springfield Insights..."
echo "📍 Directorio: $(pwd)"
echo "🐍 Python: $(python3 --version)"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    echo "💡 Ejecuta este script desde el directorio springfield_insights/"
    exit 1
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Advertencia: No se encuentra archivo .env"
    echo "💡 Copia .env.example a .env y configura tu OPENAI_API_KEY"
    echo ""
fi

# Verificar dependencias principales
echo "🔍 Verificando dependencias..."
python3 -c "import streamlit, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Faltan dependencias"
    echo "💡 Instala con: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencias verificadas"
echo ""

# Limpiar procesos previos de Streamlit (opcional)
echo "🧹 Limpiando procesos previos..."
pkill -f "streamlit run" 2>/dev/null || true

# Configurar variables de entorno para suprimir warnings
export PYTHONWARNINGS="ignore::urllib3.exceptions.NotOpenSSLWarning"

# Ejecutar la aplicación
echo "🚀 Iniciando Springfield Insights..."
echo "🌐 URL Local: http://localhost:8503"
echo "📱 URL Red: http://$(hostname -I | awk '{print $1}'):8503"
echo ""
echo "💡 Para detener: Ctrl+C"
echo "📖 Documentación: README.md"
echo ""

# Ejecutar Streamlit con configuración optimizada
python3 -m streamlit run app.py \
    --server.port 8503 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --server.fileWatcherType none \
    --theme.base "light" \
    --theme.primaryColor "#FF6347" \
    --theme.backgroundColor "#FFF8DC" \
    --theme.secondaryBackgroundColor "#F0F8FF"