# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a **Springfield Insights**! 

## 🚀 Formas de Contribuir

### 🐛 Reportar Bugs
- Usa el [template de bug report](https://github.com/vyolete/Springfield-Insights/issues/new?template=bug_report.md)
- Incluye pasos detallados para reproducir el problema
- Añade capturas de pantalla si es posible

### ✨ Sugerir Funcionalidades
- Usa el [template de feature request](https://github.com/vyolete/Springfield-Insights/issues/new?template=feature_request.md)
- Explica claramente el caso de uso
- Considera el impacto en la experiencia del usuario

### 🔧 Contribuir Código

#### Configuración del Entorno
```bash
# 1. Fork el repositorio
# 2. Clona tu fork
git clone https://github.com/tu-usuario/Springfield-Insights.git
cd Springfield-Insights

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura variables de entorno
cp .env.example .env
# Añade tu OPENAI_API_KEY

# 5. Ejecuta la app
streamlit run streamlit_app.py
```

#### Flujo de Trabajo
1. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

2. **Desarrolla** tu funcionalidad:
   - Sigue las convenciones de código existentes
   - Añade comentarios claros
   - Mantén los commits pequeños y descriptivos

3. **Prueba** tu código:
   ```bash
   # Verifica que la app funcione
   streamlit run streamlit_app.py
   
   # Verifica sintaxis
   python -m py_compile streamlit_app.py
   ```

4. **Commit** tus cambios:
   ```bash
   git commit -m "✨ Añadir [descripción de la funcionalidad]"
   ```

5. **Push** y crea un **Pull Request**:
   ```bash
   git push origin feature/nombre-descriptivo
   ```

## 📋 Estándares de Código

### 🐍 Python
- Usa **PEP 8** para el estilo de código
- Añade **docstrings** a funciones y clases
- Mantén las líneas bajo **88 caracteres**

### 📝 Commits
Usa el formato de **Conventional Commits**:
- `✨ feat:` Nueva funcionalidad
- `🐛 fix:` Corrección de bug
- `📚 docs:` Cambios en documentación
- `🎨 style:` Cambios de formato/estilo
- `♻️ refactor:` Refactorización de código
- `⚡ perf:` Mejoras de rendimiento
- `✅ test:` Añadir o corregir tests

### 🎨 UI/UX
- Mantén la **consistencia visual**
- Usa **emojis** apropiados para mejorar la UX
- Asegúrate de que sea **responsive**

## 🔍 Revisión de Código

### Criterios de Aceptación
- [ ] El código funciona correctamente
- [ ] Sigue los estándares de código
- [ ] No rompe funcionalidades existentes
- [ ] Incluye documentación si es necesario
- [ ] Es compatible con Streamlit Cloud

### Proceso de Review
1. **Automated checks** deben pasar
2. **Manual review** por maintainers
3. **Testing** en diferentes entornos
4. **Merge** cuando todo esté aprobado

## 🎯 Áreas de Contribución

### 🚀 Funcionalidades Prioritarias
- [ ] Sistema de favoritos persistente
- [ ] Compartir en redes sociales
- [ ] Dashboard de estadísticas
- [ ] Optimización móvil
- [ ] Modo offline

### 🐛 Bugs Conocidos
- Revisa los [issues abiertos](https://github.com/vyolete/Springfield-Insights/issues)
- Prioriza bugs marcados como `good first issue`

### 📚 Documentación
- Mejorar README
- Añadir ejemplos de uso
- Crear tutoriales
- Traducir a otros idiomas

## 💬 Comunicación

### 📞 Canales
- **Issues**: Para bugs y feature requests
- **Discussions**: Para preguntas generales
- **Pull Requests**: Para contribuciones de código

### 🤝 Código de Conducta
- Sé **respetuoso** y **constructivo**
- **Ayuda** a otros contributors
- **Celebra** la diversidad de ideas
- **Mantén** un ambiente positivo

## 🏆 Reconocimiento

Los contributors serán reconocidos en:
- 📝 **README.md** (sección de contributors)
- 🎉 **Release notes** cuando aplique
- 💫 **Hall of Fame** en la documentación

---

¡Gracias por hacer **Springfield Insights** mejor para todos! 🍩✨