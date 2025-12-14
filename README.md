# 🍩 Springfield Insights

**Explorando la filosofía y crítica social de Los Simpsons mediante inteligencia artificial**

## 📋 Descripción

Springfield Insights es una aplicación académica que utiliza GPT-4 para generar análisis filosóficos profundos de citas auténticas de Los Simpsons, demostrando la riqueza intelectual presente en la cultura popular.

## 🚀 Ejecución Rápida

### Prerrequisitos
- Python 3.9+
- Clave API de OpenAI (GPT-4)

### Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd springfield_insights

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY

# 4. Ejecutar aplicación
python run.py
```

## 🎯 Características

- ✅ **12 citas auténticas** de Los Simpsons
- ✅ **Análisis filosófico** generado por GPT-4
- ✅ **Crítica social** contextualizada
- ✅ **Interfaz optimizada** y responsive
- ✅ **Arquitectura modular** y limpia

## 🏗️ Estructura del Proyecto

```
springfield_insights/
├── app.py                    # Aplicación principal
├── run.py                    # Script de ejecución
├── config/
│   └── settings.py           # Configuración
├── services/
│   └── quote_service.py      # Servicio de análisis IA
├── ui/
│   └── components.py         # Componentes de interfaz
├── data/
│   └── quotes_data.py        # Base de datos de citas
├── requirements.txt          # Dependencias
└── README.md                 # Documentación
```

## 🤖 Tecnologías

- **Python 3.9+**: Lenguaje principal
- **Streamlit**: Framework de interfaz web
- **OpenAI GPT-4**: Análisis filosófico
- **Arquitectura modular**: Código limpio y mantenible

## 🎓 Valor Académico

Este proyecto demuestra:

- **Análisis cultural** mediante inteligencia artificial
- **Aplicación práctica** de LLMs en contextos académicos
- **Arquitectura de software** robusta y escalable
- **Interfaz educativa** intuitiva y accesible

## 📊 Funcionalidades

1. **Exploración de Citas**: Acceso a citas auténticas con contexto
2. **Análisis Filosófico**: Generación automática con GPT-4
3. **Crítica Social**: Conexiones con temas contemporáneos
4. **Interfaz Interactiva**: Navegación fluida y responsive

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Requerida
OPENAI_API_KEY=tu-clave-api-de-openai

# Opcionales
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=400
OPENAI_TEMPERATURE=0.7
```

## 📝 Uso

1. Ejecuta `python run.py`
2. Abre tu navegador en la URL mostrada
3. Haz clic en "Obtener Nueva Reflexión Filosófica"
4. Explora el análisis generado por GPT-4

## 🎉 Resultado

Una aplicación completamente funcional que combina:
- Contenido auténtico de Los Simpsons
- Análisis académico riguroso
- Tecnología de IA avanzada
- Experiencia de usuario optimizada

---

**Springfield Insights** - Demostrando que la sabiduría puede encontrarse en los lugares más inesperados. 🍩