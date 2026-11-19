# Detector-de-emociones-con-Streamlit_Iza_Lopez
El repositorio alberga una aplicación web con Streamlit que reciba una frase en ingles, la clasifica con el modelo DistilBERT y entrenado usando el dataset en HB llamado dair-ai/emotion

# 🎭 Clasificador de Emociones con Streamlit y DistilBERT

Aplicación web interactiva desarrollada con **Streamlit** y un modelo **DistilBERT** ajustado (*fine-tuned*) para el reconocimiento y clasificación de emociones en texto.

La aplicación permite analizar el contenido emocional de oraciones individuales o en lotes, reportando la emoción dominante, el porcentaje de confianza del modelo, un gráfico de probabilidades para las seis emociones básicas y alertas configurables de umbral de certeza.

---

## 📌 Características Principales

- **Clasificación Multiclase:** Detecta seis emociones fundamentales: *Alegría*, *Tristeza*, *Ira*, *Miedo*, *Amor* y *Sorpresa*.
- **Carga Eficiente:** El modelo y su tokenizador se cargan una única vez en memoria mediante el decorador `@st.cache_resource` de Streamlit.
- **Visualización Completa:** Gráfico interactivo de barras horizontales con la distribución de probabilidades de todas las emociones evaluadas.
- **Validaciones Robustas:** Notificaciones claras si la entrada está vacía o si faltan archivos del modelo en el directorio local.
- **Aviso y Limitaciones del Idioma:** Aclaración explícita de que el modelo fue entrenado en **inglés**, informando al usuario sobre las limitaciones de precisión al ingresar textos en español.
- **Funcionalidades Adicionales:**
  - **Umbral de Confianza:** Deslizador dinámico que advierte cuando la certeza de la predicción es baja.
  - **Frases de Ejemplo:** Botones de acceso rápido para probar oraciones arquetípicas en inglés.
  - **Análisis por Lotes:** Procesamiento masivo de oraciones (mediante cuadro de texto multilínea o subida de archivo `.csv`) con tabla exportable.
  - **Historial de Sesión:** Registro temporal de consultas realizadas durante la sesión utilizando `st.session_state`.

---

## 📂 Estructura del Proyecto

```
ProyectoEmociones/
├── app.py                     # Código de la aplicación web en Streamlit
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación y declaración de uso de IA
├── .gitignore                 # Configuración de archivos excluidos de Git
└── modelo_emociones_distilbert/   # Carpeta con el modelo entrenado (no se sube a GitHub)
    ├── config.json
    ├── model.safetensors
    ├── tokenizer.json
    └── tokenizer_config.json
```

---

## 🛠️ Instalación y Requisitos

### 1. Clonar el repositorio y preparar el entorno

Se recomienda el uso de un entorno virtual con **Python 3.9 o superior**:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias

Instala los paquetes listados en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Verificar el modelo

Asegúrate de que la carpeta `modelo_emociones_distilbert/` esté ubicada en la raíz del proyecto y contenga los archivos de configuración y pesos del modelo (`config.json`, `model.safetensors`, tokenizador).

---

## 🚀 Ejecución de la Aplicación

Para iniciar el servidor local de Streamlit, ejecuta en la terminal:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado en `http://localhost:8501`.

---

## 🌐 Aviso sobre el Idioma y Limitaciones

> ⚠️ **Aviso de Idioma:**  
> El modelo de clasificación DistilBERT utilizado en este proyecto fue ajustado (*fine-tuned*) a partir de un conjunto de datos etiquetado en **idioma inglés**.  
> Por tanto, para obtener resultados consistentes y fiables, **las frases a analizar deben ser ingresadas en inglés**. Si se ingresan textos en español u otros idiomas, la predicción puede presentar sesgos, clasificaciones erróneas o distribuciones de probabilidad con baja certeza, debido a que el espacio vectorial y el vocabulario del tokenizador no corresponden al idioma analizado.

---

## 🤖 Declaración de Uso de Asistentes de IA

En cumplimiento con los lineamientos académicos del proyecto, se declara formalmente el uso de herramientas de Inteligencia Artificial:

### 1. Herramientas utilizadas
- **Asistente de IA (Antigravity / Gemini / Claude)** como copiloto de desarrollo y programación.

### 2. Partes del proyecto en que se utilizaron
- **Desarrollo de la interfaz de usuario:** Generación del andamiaje visual con Streamlit (`app.py`), incluyendo el diseño de las pestañas (*tabs*), la barra lateral de configuración, los botones de frases de prueba y el gráfico de probabilidades con Altair.
- **Estructuración de componentes adicionales:** Creación de la lógica para el procesamiento por lotes (análisis masivo desde CSV o texto multilínea) y gestión del historial de sesión con `st.session_state`.
- **Plantilla de documentación:** Redacción inicial de los comandos de instalación, ejecución y archivo `.gitignore`.

### 3. Verificación y modificaciones realizadas por el equipo
- **Adaptación y verificación de rutas:** Se inspeccionó y adaptó la estructura de la carpeta `modelo_emociones_distilbert` para asegurar la correcta compatibilidad con Hugging Face `transformers.pipeline`.
- **Alineación del idioma y etiquetas:** Se verificó la correspondencia entre los identificadores numéricos de las etiquetas (`id2label`) del `config.json` y los nombres mostrados en pantalla, incorporando emojis y la aclaración de las restricciones del idioma de entrenamiento (inglés).
- **Control de errores y validaciones:** Se probaron y validaron los flujos de excepción (campo vacío, archivo CSV inválido, ausencia de pesos del modelo) para garantizar una experiencia de usuario estable y libre de caídas del servidor.
