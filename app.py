import os
from datetime import datetime
import pandas as pd
import streamlit as st
import altair as alt
from transformers import pipeline

# ---------------------------------------------------------
# Configuración inicial de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Detector de Emociones | DistilBERT",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diccionario de metadatos de emociones (traducción, emoji y color)
EMOTION_META = {
    "alegría": {"emoji": "😄", "en": "Joy", "color": "#28a745"},
    "joy": {"emoji": "😄", "en": "Joy", "color": "#28a745"},
    "tristeza": {"emoji": "😢", "en": "Sadness", "color": "#17a2b8"},
    "sadness": {"emoji": "😢", "en": "Sadness", "color": "#17a2b8"},
    "ira": {"emoji": "😡", "en": "Anger", "color": "#dc3545"},
    "anger": {"emoji": "😡", "en": "Anger", "color": "#dc3545"},
    "miedo": {"emoji": "😨", "en": "Fear", "color": "#6f42c1"},
    "fear": {"emoji": "😨", "en": "Fear", "color": "#6f42c1"},
    "amor": {"emoji": "❤️", "en": "Love", "color": "#e83e8c"},
    "love": {"emoji": "❤️", "en": "Love", "color": "#e83e8c"},
    "sorpresa": {"emoji": "😲", "en": "Surprise", "color": "#fd7e14"},
    "surprise": {"emoji": "😲", "en": "Surprise", "color": "#fd7e14"},
}

MODEL_DIR = "modelo_emociones_distilbert"

# ---------------------------------------------------------
# Inicialización de Session State
# ---------------------------------------------------------
if "historial" not in st.session_state:
    st.session_state.historial = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------------------------------------------------
# Carga eficiente del modelo con @st.cache_resource
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def cargar_clasificador_emociones():
    """
    Carga el modelo y tokenizador de forma eficiente una sola vez.
    Verifica la existencia del directorio y archivos indispensables.
    """
    path_to_check = MODEL_DIR
    # Soporte por si está anidado
    if not os.path.exists(path_to_check):
        return None, "No se encontró el directorio del modelo."
    
    if os.path.exists(os.path.join(path_to_check, "modelo_emociones_distilbert", "config.json")):
        path_to_check = os.path.join(path_to_check, "modelo_emociones_distilbert")
    elif not os.path.exists(os.path.join(path_to_check, "config.json")):
        return None, "La carpeta del modelo no contiene el archivo 'config.json'."

    try:
        clasificador = pipeline(
            "text-classification",
            model=path_to_check,
            tokenizer=path_to_check,
            top_k=None,
            truncation=True
        )
        return clasificador, None
    except Exception as e:
        return None, f"Error al inicializar el pipeline: {str(e)}"

# ---------------------------------------------------------
# Verificación de carga del modelo
# ---------------------------------------------------------
with st.spinner("⏳ Cargando el modelo DistilBERT ajustado en memoria..."):
    clasificador, error_msg = cargar_clasificador_emociones()

if clasificador is None:
    st.error("🚨 **Error Crítico: No se pudo cargar el modelo de clasificación.**")
    st.markdown(
        f"""
        **Detalles:** `{error_msg}`  
        Asegúrate de que la carpeta `{MODEL_DIR}/` exista en la raíz del proyecto y contenga:
        - `config.json`
        - `model.safetensors` o `pytorch_model.bin`
        - Archivos del tokenizador (`tokenizer.json`, `tokenizer_config.json`, etc.)
        """
    )
    st.stop()

# ---------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------
def clasificar_texto(texto: str):
    """Ejecuta la inferencia sobre un texto y devuelve el ranking ordenado."""
    resultados = clasificador(texto)[0]
    # Normalizar formato y ordenar descendentemente por score
    ranking = sorted(resultados, key=lambda x: x["score"], reverse=True)
    return ranking

def formatear_emocion(label: str):
    """Devuelve la emoción capitalizada, su emoji y traducción."""
    lbl_clean = label.lower().strip()
    meta = EMOTION_META.get(lbl_clean, {"emoji": "🏷️", "en": lbl_clean, "color": "#6c757d"})
    return f"{meta['emoji']} {lbl_clean.capitalize()} ({meta['en']})", meta

# ---------------------------------------------------------
# Barra Lateral (Configuraciones, Info y Estadísticas)
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    
    umbral_confianza = st.slider(
        "Umbral de Confianza Mínimo (%)",
        min_value=10,
        max_value=95,
        value=50,
        step=5,
        help="Si la probabilidad de la emoción principal es menor a este porcentaje, el sistema emitirá una advertencia de baja certeza."
    )

    st.markdown("---")
    st.subheader("🌐 Información del Modelo")
    st.caption("**Arquitectura:** DistilBERT Fine-Tuned")
    st.caption("**Clases:** 6 emociones (tristeza, alegría, amor, ira, miedo, sorpresa)")
    
    st.info(
        "**Idioma de entrenamiento:** 🇬🇧 **Inglés (English)**\n\n"
        "⚠️ **Limitación del idioma:** El modelo fue entrenado exclusivamente con textos en inglés. "
        "Para obtener la máxima precisión, **ingresa frases en inglés**. "
        "Si ingresas oraciones en español u otro idioma, la clasificación puede ser errónea o impredecible debido a la distribución del vocabulario aprendido."
    )

    st.markdown("---")
    st.subheader("📜 Historial de Sesión")
    if st.session_state.historial:
        st.write(f"Total analizadas: **{len(st.session_state.historial)}**")
        if st.button("🗑️ Borrar Historial", use_container_width=True):
            st.session_state.historial = []
            st.rerun()
    else:
        st.caption("No hay análisis registrados todavía en esta sesión.")

# ---------------------------------------------------------
# Encabezado Principal de la Aplicación
# ---------------------------------------------------------
st.title("🎭 Clasificador de Emociones con DistilBERT")
st.markdown(
    """
    Esta aplicación utiliza un modelo **DistilBERT** ajustado (*fine-tuned*) para clasificar el tono emocional 
    de un texto en una de las seis emociones básicas: **alegría, tristeza, ira, miedo, amor o sorpresa**.
    """
)

# Banner informativo de restricción de idioma
st.warning(
    "🇬🇧 **Aviso importante sobre el idioma:** El modelo fue entrenado con frases en **inglés**. "
    "Por favor formula tus oraciones en **inglés** para garantizar una predicción certera.",
    icon="⚠️"
)

# ---------------------------------------------------------
# Pestañas: Análisis Individual, Análisis por Lotes e Historial
# ---------------------------------------------------------
tab_individual, tab_lotes, tab_historial = st.tabs([
    "🔍 Análisis Individual", 
    "📁 Análisis por Lotes (Batch)", 
    "📋 Historial de Sesión"
])

# =========================================================
# TAB 1: ANÁLISIS INDIVIDUAL
# =========================================================
with tab_individual:
    st.subheader("1. Frases de Ejemplo en Inglés")
    st.caption("Haz clic en cualquiera de los botones para cargar una frase de prueba representativa:")

    ejemplos = [
        ("😄 Alegría", "I just received the job offer I had been dreaming of for months!", "Alegría / Joy"),
        ("😢 Tristeza", "I feel completely lost and heartbroken after receiving the bad news.", "Tristeza / Sadness"),
        ("😡 Ira", "I am sick and tired of people disrespecting my personal boundaries!", "Ira / Anger"),
        ("😨 Miedo", "I heard strange footsteps outside my bedroom door in the dark.", "Miedo / Fear"),
        ("❤️ Amor", "I am so deeply grateful to have you in my life, I love you.", "Amor / Love"),
        ("😲 Sorpresa", "I had absolutely no idea you prepared a surprise party for me!", "Sorpresa / Surprise"),
    ]

    cols_ejemplos = st.columns(3)
    for i, (nombre_btn, frase_ejemplo, label_desc) in enumerate(ejemplos):
        with cols_ejemplos[i % 3]:
            if st.button(nombre_btn, use_container_width=True, help=f"Probar: {label_desc}"):
                st.session_state.input_text = frase_ejemplo

    st.markdown("---")
    st.subheader("2. Ingreso de Texto para Análisis")

    # Formulario para análisis individual
    with st.form("form_analisis_individual"):
        texto_usuario = st.text_area(
            "Escribe o pega una frase en inglés:",
            value=st.session_state.input_text,
            height=110,
            placeholder="Ejemplo: I am so excited about starting my new university project tomorrow!",
            help="Ingresa el texto que deseas que el modelo clasifique (recomendado en inglés)."
        )
        col_btn, _ = st.columns([1, 4])
        with col_btn:
            btn_analizar = st.form_submit_button("🚀 Analizar Emoción", use_container_width=True)

    if btn_analizar:
        texto_limpio = texto_usuario.strip()

        # Validación 1: Frase vacía
        if not texto_limpio:
            st.warning("⚠️ **El campo de texto está vacío.** Por favor ingresa una frase antes de hacer clic en 'Analizar Emoción'.")
        else:
            with st.spinner("Analizando texto con DistilBERT..."):
                ranking = clasificar_texto(texto_limpio)
                top_pred = ranking[0]
                emocion_top = top_pred["label"]
                prob_top = top_pred["score"] * 100
                nombre_formateado, meta_top = formatear_emocion(emocion_top)

                # Guardar en el historial de sesión
                st.session_state.historial.insert(0, {
                    "Fecha / Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Frase": texto_limpio,
                    "Emoción": f"{meta_top['emoji']} {emocion_top.capitalize()}",
                    "Confianza (%)": round(prob_top, 2)
                })

            st.markdown("### 🎯 Resultado Principal")
            
            # Métricas en columnas
            col_m1, col_m2, col_m3 = st.columns([2, 1.5, 2.5])
            with col_m1:
                st.metric(
                    label="Emoción Detectada",
                    value=f"{meta_top['emoji']} {emocion_top.capitalize()}",
                    help=f"Traducción en inglés: {meta_top['en']}"
                )
            with col_m2:
                st.metric(
                    label="Nivel de Confianza",
                    value=f"{prob_top:.2f}%"
                )
            with col_m3:
                # Verificación del umbral de confianza
                if prob_top < umbral_confianza:
                    st.warning(
                        f"⚠️ **Confianza Baja (< {umbral_confianza}%):** El modelo no tiene una certeza contundente sobre esta predicción. Puede haber ambigüedad o vocabulario atípico."
                    )
                else:
                    st.success(
                        f"✅ **Confianza Aceptable (≥ {umbral_confianza}%):** La predicción supera el umbral establecido en la configuración."
                    )

            st.markdown("---")
            st.subheader("📊 Distribución Completa de Probabilidades (6 Emociones)")

            # Preparación del DataFrame para visualización
            df_prob = pd.DataFrame([
                {
                    "Emoción": f"{EMOTION_META.get(r['label'].lower(), {}).get('emoji', '')} {r['label'].capitalize()}",
                    "Probabilidad": r["score"] * 100,
                    "Probabilidad_Texto": f"{r['score'] * 100:.2f}%"
                }
                for r in ranking
            ])

            # Gráfico de barras ordenado con Altair
            chart = alt.Chart(df_prob).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
                x=alt.X("Probabilidad:Q", title="Probabilidad (%)", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Emoción:N", sort="-x", title="Emoción"),
                color=alt.Color("Probabilidad:Q", scale=alt.Scale(scheme="blues"), legend=None),
                tooltip=["Emoción", alt.Tooltip("Probabilidad:Q", format=".2f", title="Confianza (%)")]
            ).properties(height=260)

            text = chart.mark_text(
                align="left",
                baseline="middle",
                dx=5,
                color="black"
            ).encode(
                text=alt.Text("Probabilidad_Texto:N")
            )

            st.altair_chart(chart + text, use_container_width=True)

# =========================================================
# TAB 2: ANÁLISIS POR LOTES (BATCH)
# =========================================================
with tab_lotes:
    st.subheader("📁 Procesamiento de Múltiples Frases")
    st.markdown(
        "Puedes ingresar varias frases simultáneas mediante un **archivo CSV** o pegando una lista de frases "
        "**(una por línea)**. Recuerda que las frases deben estar en **inglés** para una clasificación óptima."
    )

    modo_lote = st.radio(
        "Selecciona el método de entrada por lotes:",
        options=["Pegar texto (una frase por línea)", "Subir archivo CSV"],
        horizontal=True
    )

    frases_a_procesar = []

    if modo_lote == "Pegar texto (una frase por línea)":
        lote_texto = st.text_area(
            "Pega tus frases aquí (una por línea):",
            height=150,
            placeholder="I love spending time with my family.\nI feel so terrified of thunder.\nThis delay makes me furious."
        )
        if st.button("⚡ Procesar Frases Ingresadas"):
            lineas = [line.strip() for line in lote_texto.split("\n") if line.strip()]
            if not lineas:
                st.warning("⚠️ No has ingresado ninguna frase para procesar.")
            else:
                frases_a_procesar = lineas

    else:
        archivo_csv = st.file_uploader("Sube un archivo CSV con una columna de frases en inglés:", type=["csv"])
        if archivo_csv is not None:
            try:
                df_cargado = pd.read_csv(archivo_csv)
                columna_seleccionada = st.selectbox("Selecciona la columna que contiene las frases:", options=df_cargado.columns)
                if st.button("⚡ Procesar Columna de CSV"):
                    frases_a_procesar = df_cargado[columna_seleccionada].dropna().astype(str).tolist()
            except Exception as e:
                st.error(f"Error al leer el archivo CSV: {str(e)}")

    if frases_a_procesar:
        with st.spinner(f"Clasificando {len(frases_a_procesar)} frases con el modelo..."):
            resultados_lote = []
            barra_progreso = st.progress(0)
            total = len(frases_a_procesar)

            for idx, frase in enumerate(frases_a_procesar):
                preds = clasificar_texto(frase)
                top = preds[0]
                lbl = top["label"].lower().strip()
                meta = EMOTION_META.get(lbl, {"emoji": "🏷️", "en": lbl})
                prob = top["score"] * 100
                confianza_baja = "Sí" if prob < umbral_confianza else "No"

                resultados_lote.append({
                    "Frase": frase,
                    "Emoción": f"{meta['emoji']} {lbl.capitalize()}",
                    "Emoción (EN)": meta["en"],
                    "Confianza (%)": round(prob, 2),
                    "Alerta Umbral": confianza_baja
                })
                barra_progreso.progress((idx + 1) / total)

            df_resultados = pd.DataFrame(resultados_lote)
            st.success(f"✅ Se procesaron exitosamente {len(frases_a_procesar)} frases.")

            st.dataframe(df_resultados, use_container_width=True)

            # Botón para descargar resultados en CSV
            csv_data = df_resultados.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Descargar Resultados en CSV",
                data=csv_data,
                file_name="resultados_clasificacion_emociones.csv",
                mime="text/csv",
                use_container_width=True
            )

# =========================================================
# TAB 3: HISTORIAL DE SESIÓN
# =========================================================
with tab_historial:
    st.subheader("📋 Historial de Consultas de la Sesión")
    st.markdown(
        "Registro de todas las oraciones analizadas individualmente durante la sesión actual, "
        "con su emoción detectada, nivel de confianza y marca de tiempo."
    )

    if st.session_state.historial:
        df_hist = pd.DataFrame(st.session_state.historial)

        col_h1, col_h2, col_h3 = st.columns([2, 1.5, 1.5])
        with col_h1:
            st.metric("Total de consultas registradas", len(df_hist))
        with col_h2:
            csv_hist = df_hist.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Descargar Historial (CSV)",
                data=csv_hist,
                file_name="historial_consultas_emociones.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_h3:
            if st.button("🗑️ Limpiar Historial", key="btn_limpiar_tab_historial", use_container_width=True):
                st.session_state.historial = []
                st.rerun()

        st.markdown("---")
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info(
            "ℹ️ Aún no has realizado análisis en esta sesión. "
            "Cada vez que evalúes una frase en la pestaña **'🔍 Análisis Individual'**, se registrará automáticamente en este panel."
        )
