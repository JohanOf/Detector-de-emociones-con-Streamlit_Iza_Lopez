# 📑 Frases de Demostración para Evaluación del Modelo

Este documento contiene un conjunto estructurado de oraciones de prueba clasificadas en cuatro categorías clave. Su objetivo es evaluar el desempeño del modelo **DistilBERT**, validar las alertas del **umbral de confianza**, identificar patrones de fallo y evidenciar las **limitaciones de idioma**.

---

## 1. Frases Correctas (Alta Confianza)

> **Objetivo:** Demostrar la capacidad del modelo para reconocer emociones explícitas en inglés, donde el vocabulario es directo y no hay ambigüedades.

| N° | Frase de Prueba (Inglés) | Emoción Esperada | Justificación Técnica |
|---|---|---|---|
| **1** | `I just won the championship and I have never felt this happy before!` | 😄 Alegría (*Joy*) | Términos clave unívocos de victoria y felicidad (*won*, *championship*, *happy*). |
| **2** | `I feel so empty, lonely and hopeless since you walked out of my life.` | 😢 Tristeza (*Sadness*) | Fuerte concentración léxica de duelo y desolación (*empty*, *lonely*, *hopeless*). |
| **3** | `I can't stand your constant lies anymore, it makes my blood boil!` | 😡 Ira (*Anger*) | Expresiones idiomáticas de hostilidad y rechazo directo (*can't stand*, *blood boil*). |
| **4** | `I was walking alone in the dark alley and suddenly heard someone running behind me.` | 😨 Miedo (*Fear*) | Contexto clásico de amenaza física inminente y suspenso (*dark alley*, *running behind me*). |
| **5** | `Thank you for always supporting me, you are the most precious person in the world to me.` | ❤️ Amor (*Love*) | Indicadores explícitos de apego, ternura y gratitud profunda (*precious*, *supporting*). |

---

## 2. Frases Incorrectas (Errores por Sarcasmo, Modismos o Negaciones)

> **Objetivo:** Evidenciar las limitaciones del modelo ante fenómenos lingüísticos complejos como modismos (*slang*), sarcasmo contextual y trampas de palabras clave.

| N° | Frase de Prueba (Inglés) | Sentido Real | Error Típico del Modelo | Causa del Fallo |
|---|---|---|---|---|
| **1** | `I am totally killing it at work today!` | 😄 Alegría / Éxito | 😨 Miedo o 😡 Ira | **Trampa léxica:** Confusión por la palabra literal *"killing"*, ignorando el modismo positivo. |
| **2** | `Oh fantastic, my car broke down in the rain on my way to the interview.` | 😡 Ira / Frustración | 😄 Alegría (*Joy*) | **Sarcasmo:** Falsa pista generada por el adjetivo de apertura *"fantastic"*. |
| **3** | `I am definitely not crying because I am sad, don't worry.` | 😢 Tristeza reprimida | 😄 Alegría o Indeciso | **Negación:** Dificultad para modelar el alcance real de *"not"* frente a palabras emocionales como *"crying"* y *"sad"*. |
| **4** | `This horror movie is insanely good, I loved how terrified it made me.` | 😄 Satisfacción / ❤️ Amor | 😨 Miedo (*Fear*) | **Dominancia léxica:** Palabras como *"horror"* y *"terrified"* superan la señal afectiva de *"loved"* y *"insanely good"*. |
| **5** | `You really have a unique talent for ruining every single family dinner.` | 😡 Ira / Desprecio | 😄 Alegría (*Joy*) | **Sarcasmo sutil:** Los tokens *"unique"* y *"talent"* sesgan erróneamente la atención hacia positividad. |

---

## 3. Frases Difíciles / Ambiguas (Evaluación del Umbral de Confianza)

> **Objetivo:** Evaluar oraciones donde coexisten dos o más emociones, provocando que las probabilidades se dispersen y se active la advertencia de **Baja Confianza** (`< Umbral %`).

| N° | Frase de Prueba (Inglés) | Emociones en Conflicto | Comportamiento Esperado en la App |
|---|---|---|---|
| **1** | `After that exam I feel like my life is over.` | 😢 Tristeza vs. 😨 Miedo | Probabilidades repartidas entre depresión y pánico por el futuro; activa aviso de umbral bajo. |
| **2** | `I just opened the acceptance letter and I'm trembling, I don't know whether to laugh or scream.` | 😲 Sorpresa vs. 😄 Alegría vs. 😨 Miedo | Ninguna emoción supera el 40-50% de probabilidad; genera alerta de incertidumbre. |
| **3** | `I finally said goodbye to him; it hurts like hell, but I know it was the right decision.` | 😢 Tristeza vs. ❤️ Amor / Alivio | Tensión entre dolor de pérdida y tranquilidad; distribución de pesos dividida. |
| **4** | `I didn't expect anyone to show up at my door at 3 AM.` | 😲 Sorpresa vs. 😨 Miedo | Frontera entre lo imprevisto y la sensación de peligro; el modelo muestra indecisión. |
| **5** | `He bought me a car out of nowhere and I honestly feel weird about it.` | 😲 Sorpresa vs. ❤️ Amor vs. 😨 Desconfianza | La sorpresa positiva choca con la incomodidad expresada (*feel weird*). |

---

## 4. Frases en Español (Demostración de la Limitación de Idioma)

> **Objetivo:** Demostrar que el modelo fue entrenado en inglés y que ingresar frases en español degrada la capacidad del tokenizador y arroja predicciones arbitrarias o erradas.

| N° | Frase de Prueba (Español) | Sentido Emocional Real | Efecto en el Modelo DistilBERT en Inglés |
|---|---|---|---|
| **1** | `Extraño jugar a la pelota con mis amigos los fines de semana.` | 😢 Tristeza / Nostalgia | El tokenizador fragmenta palabras (*Ex-tra-ño*, *pe-lo-ta*), asignando etiquetas al azar (frecuentemente *Joy* o *Surprise*). |
| **2** | `Estoy profundamente enamorado de ti desde el primer día.` | ❤️ Amor | El modelo no reconoce la raíz morfológica de *"enamorado"*, provocando una distribución de baja confianza y predicción inconsistente. |
| **3** | `Siento un miedo terrible cada vez que tiembla la tierra.` | 😨 Miedo | Aunque reconoce vagamente *"terrible"*, la estructura sintáctica en español desorienta el mecanismo de autoatención. |
| **4** | `Qué rabia me da perder el autobús por solo un minuto.` | 😡 Ira / Impotencia | La palabra *"rabia"* no existe en el vocabulario anglosajón del modelo, lo que conduce a clasificaciones aleatorias. |
| **5** | `No puedo creer que organizaron todo esto a mis espaldas, ¡qué gran sorpresa!` | 😲 Sorpresa / 😄 Alegría | La palabra clave en inglés (*surprise*) difiere morfológicamente de *"sorpresa"*, impidiendo una correlación semántica adecuada. |
