# 🍩 Springfield Insights

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

**Explorando la filosofía y crítica social de Los Simpsons mediante inteligencia artificial**

## 🚀 Demo en Vivo

**[▶️ Abrir Springfield Insights](https://your-app-name.streamlit.app)**

## 📋 Descripción

Springfield Insights es una aplicación académica que utiliza **GPT-3.5-Turbo** para generar análisis filosóficos profundos de Los Simpsons, demostrando la riqueza intelectual presente en la cultura popular. Optimizada para **Streamlit Cloud** con integración automática de GitHub.

## ✨ Características

- 🤖 **Análisis con GPT-3.5-Turbo**: Interpretaciones filosóficas auténticas
- 🎭 **Personajes Únicos**: Reflexiones fieles a Homer, Lisa, Bart y Marge
- 🏛️ **Rigor Académico**: Enfoque en crítica social y contexto filosófico
- ☁️ **Deploy Automático**: Integración completa con Streamlit Cloud y GitHub
- 🎨 **Interfaz Moderna**: Diseño responsive y experiencia optimizada
- 🔄 **CI/CD Automático**: Cada push actualiza la app automáticamente

## 🛠️ Instalación Local

### Prerrequisitos
- Python 3.9+
- Cuenta de OpenAI con API Key

### Pasos Rápidos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/springfield-insights.git
cd springfield-insights

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
cp .env.example .env
# Edita .env y añade tu OPENAI_API_KEY

# 4. Ejecutar aplicación
streamlit run streamlit_app.py
```

## ☁️ Deploy en Streamlit Cloud

### 🚀 Configuración Automática con GitHub

1. **Fork este repositorio** en tu cuenta de GitHub

2. **Conecta con Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Haz clic en "New app"
   - Conecta tu repositorio de GitHub
   - Selecciona `streamlit_app.py` como archivo principal

3. **Configura Secrets:**
   - En tu app de Streamlit Cloud, ve a "Settings" → "Secrets"
   - Añade tu configuración:
   ```toml
   OPENAI_API_KEY = "sk-proj-tu-api-key-aqui"
   ```

4. **Deploy Automático:**
   - Cada push a `main` actualizará automáticamente tu app
   - La URL será: `https://tu-usuario-springfield-insights-streamlit-app-xxx.streamlit.app`

### 🔐 Configuración de Secrets

En Streamlit Cloud Settings → Secrets:

```toml
# ✅ Requerido
OPENAI_API_KEY = "tu-api-key-de-openai"

# 🔧 Opcional (con valores por defecto)
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = "250"
OPENAI_TEMPERATURE = "0.8"
```

## 🎯 Uso

1. **Selecciona un personaje** en la barra lateral (o deja "Aleatorio")
2. **Haz clic en "Generar Nueva Reflexión"** 
3. **Explora el análisis** generado por IA
4. **Interactúa** con los botones para copiar, guardar o compartir

## 🏗️ Arquitectura

### Estructura Optimizada para Streamlit Cloud
```
springfield-insights/
├── streamlit_app.py      # 🎯 Aplicación principal (Streamlit Cloud)
├── app_final.py          # 🔧 Versión simple alternativa
├── requirements.txt      # 📦 Dependencias
├── .env.example         # 🔐 Plantilla de configuración
├── .streamlit/          # ⚙️ Configuración de Streamlit
│   └── config.toml
├── config/              # 🛠️ Configuración avanzada
│   └── settings.py
├── services/            # 🔄 Servicios de negocio
├── ui/                  # 🎨 Componentes de interfaz
├── data/                # 📊 Gestión de datos
└── utils/               # 🔧 Utilidades
```

### 🔄 Flujo de Desarrollo

#### Desarrollo Local
```bash
# Desarrollo con hot-reload
streamlit run streamlit_app.py

# Versión simple para testing
streamlit run app_final.py
```

#### Deploy Automático
1. **Commit y push** a GitHub
2. **Streamlit Cloud detecta** cambios automáticamente
3. **Redeploy automático** en segundos
4. **URL actualizada** instantáneamente

## 🤖 Tecnologías

- **🐍 Python 3.9+**
- **🚀 Streamlit**: Framework de aplicaciones web
- **🤖 OpenAI GPT-3.5-Turbo**: Análisis de inteligencia artificial  
- **☁️ Streamlit Cloud**: Hosting y deploy automático
- **🔗 GitHub**: Control de versiones e integración CI/CD
- **🔐 Streamlit Secrets**: Gestión segura de API keys

## 🎓 Valor Académico

**Springfield Insights** demuestra cómo la inteligencia artificial puede ser utilizada para:

- 📚 **Análisis cultural** mediante procesamiento de lenguaje natural
- 🎭 **Crítica social** a través de personajes ficticios
- 🏛️ **Filosofía aplicada** en cultura popular contemporánea
- ☁️ **Deploy moderno** con CI/CD automático

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m 'Añadir nueva funcionalidad increíble'
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abre un Pull Request**

## 📊 Funcionalidades

### ✅ Implementadas
- 🎭 Selección de personajes (Homer, Lisa, Bart, Marge)
- 🤖 Generación de reflexiones con GPT-3.5-Turbo
- 📚 Análisis filosófico contextualizado
- 🎨 Interfaz responsive y moderna
- ☁️ Deploy automático en Streamlit Cloud
- 🔐 Gestión segura de secrets

### 🚧 Próximas Mejoras
- 📊 Dashboard de estadísticas
- 💾 Sistema de favoritos persistente
- 🔗 Compartir en redes sociales
- 📱 Optimización móvil avanzada

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver [LICENSE](LICENSE) para detalles.

---

<div align="center">

**[🚀 Probar la App](https://your-app-name.streamlit.app)** | **[📖 Documentación](https://github.com/tu-usuario/springfield-insights/wiki)** | **[🐛 Reportar Bug](https://github.com/tu-usuario/springfield-insights/issues)**

Hecho con ❤️ y 🤖 para explorar la sabiduría de Springfield

</div>