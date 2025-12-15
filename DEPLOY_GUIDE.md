# 🚀 Guía de Deploy en Streamlit Cloud

## Pasos para Deploy Automático

### 1. Preparar Repositorio en GitHub

```bash
# Subir código a GitHub
git add .
git commit -m "Preparar para Streamlit Cloud deploy"
git push origin main
```

### 2. Conectar con Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en "New app"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Repository**: tu-usuario/springfield-insights
   - **Branch**: main
   - **Main file path**: streamlit_app.py

### 3. Configurar Secrets

En Settings → Secrets, añade:

```toml
OPENAI_API_KEY = "tu-api-key-aqui"
```

### 4. Deploy Automático

- La app se desplegará automáticamente
- URL: `https://tu-usuario-springfield-insights-streamlit-app-xxx.streamlit.app`
- Cada push a main actualizará la app

## ✅ Verificación

- [ ] Repositorio en GitHub
- [ ] App conectada en Streamlit Cloud  
- [ ] Secrets configurados
- [ ] Deploy exitoso
- [ ] URL funcionando

## 🔧 Troubleshooting

**Error de API Key**: Verifica secrets en Streamlit Cloud
**Error de dependencias**: Revisa requirements.txt
**Error de sintaxis**: Ejecuta tests localmente

## 📱 Resultado

Tu app estará disponible 24/7 en Streamlit Cloud con deploy automático.