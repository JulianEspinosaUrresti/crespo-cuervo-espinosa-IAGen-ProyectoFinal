# Evaluación comparativa — EcoMarket

## 1. Objetivo

Evaluar la calidad de las respuestas generadas por el agente EcoMarket mediante una comparación de variantes de prompts, considerando exactitud factual, abstención ante información insuficiente, pertinencia de las fuentes y ausencia de afirmaciones inventadas.

## 2. Metodología

Se analizaron dos conjuntos de evaluación, denominados V2 y V3.

Cada conjunto contiene 12 preguntas evaluadas con dos variantes, para un total de 24 respuestas por conjunto y 48 registros de evaluación.

La revisión humana clasificó las respuestas como:

- **Correcto:** respuesta adecuada según los datos ficticios y criterios establecidos.
- **Parcial:** respuesta con información pertinente, pero incompleta o con problemas de precisión.
- **Incorrecto:** respuesta que no cumple los criterios de evaluación.

La métrica utilizada fue:

**Porcentaje de respuestas correctas = (respuestas correctas / respuestas evaluadas) × 100.**

Las respuestas parciales no se contabilizaron como correctas.

### Diseño y justificación de las variantes de prompts

El sistema EcoMarket utiliza ingeniería de prompts para orientar las respuestas del modelo Llama 3.2 3B, ejecutado localmente mediante Ollama y LangChain.

Las variantes comparten un prompt de sistema que establece el rol de agente de atención al cliente, el uso exclusivo del contexto documental y los pedidos verificados, la prohibición de inventar información y la obligación de reconocer cuando los datos son insuficientes.

**Variante base**

Incorpora la instrucción adicional de responder de forma amable y breve. Se utiliza como referencia para comparar el efecto de incorporar reglas más específicas.

**Variante mejorada**

Añade instrucciones explícitas para gestionar pedidos retrasados, distinguir devoluciones ordinarias de reclamaciones por daños, evitar solicitar identificadores innecesarios y abstenerse cuando no exista información verificable.

Esta variante aplica principios de especificidad, restricciones y contextualización propios de la ingeniería de prompts.

**Variante corregida**

Organiza las instrucciones adicionales en seis reglas prioritarias para situaciones concretas: pedidos retrasados, devoluciones, productos dañados, tarifas de envío, referencias documentales y consultas generales.

Su diseño busca reducir ambigüedades mediante instrucciones estructuradas, comportamientos esperados y restricciones explícitas.

**Estrategia de prompting**

Las tres variantes utilizan instrucciones de rol, contexto documental y restricciones de respuesta. No incorporan ejemplos completos de entrada y salida dentro del prompt; por tanto, su diseño corresponde principalmente a una estrategia *zero-shot* contextualizada y no a *few-shot prompting*.

El contexto se construye mediante recuperación documental con ChromaDB, mientras que los pedidos se consultan por identificador exacto.

La temperatura del modelo se configura en cero para favorecer respuestas más consistentes, aunque esto no garantiza determinismo absoluto ni elimina las alucinaciones.

**Interpretación experimental**

En V2, las variantes base y mejorada obtuvieron un 66,7 % de respuestas correctas.

En V3, la variante mejorada obtuvo un 66,7 % y la corregida alcanzó un 83,3 %, equivalente a una diferencia de 16,7 puntos porcentuales.

Sin embargo, la variante corregida presentó una respuesta incorrecta, por lo que el aumento de respuestas correctas no demuestra una eliminación del riesgo de alucinaciones.

Los resultados sugieren que estructurar instrucciones puede mejorar determinados comportamientos del agente, pero su efectividad depende de la consulta, el contexto recuperado y la capacidad del modelo para cumplir las restricciones.

Dado el tamaño reducido de la muestra y las limitaciones metodológicas documentadas, no se atribuye causalidad concluyente a los cambios del prompt.

## 3. Resultados experimentales

| Evaluación | Variante | Correctas | Parciales | Incorrectas | Porcentaje correcto |
|---|---|---:|---:|---:|---:|
| V2 | Base | 8 | 4 | 0 | 66,7 % |
| V2 | Mejorado | 8 | 4 | 0 | 66,7 % |
| V3 | Corregido | 10 | 1 | 1 | 83,3 % |
| V3 | Mejorado | 8 | 4 | 0 | 66,7 % |

**Fuentes de evidencia:**

- `resultados/comparacion_v2_evaluada.csv`
- `resultados/comparacion_v3_evaluada.csv`

## 4. Análisis crítico

### 4.1. Comparación V2

Las variantes base y mejorada alcanzaron un 66,7 % de respuestas correctas.

Este resultado indica que las modificaciones del prompt no se tradujeron en una mejora cuantitativa de la exactitud bajo los criterios utilizados.

### 4.2. Comparación V3

La variante corregida obtuvo un 83,3 % de respuestas correctas, mientras que la mejorada alcanzó un 66,7 %.

La diferencia observada fue de aproximadamente 16,7 puntos porcentuales.

Sin embargo, la variante corregida también presentó una respuesta incorrecta, mientras que la mejorada presentó cuatro respuestas parciales y ninguna incorrecta.

Por tanto, el porcentaje de respuestas correctas debe interpretarse junto con la distribución de errores.

### 4.3. Recuperación documental y generación

El uso de RAG permite proporcionar contexto documental al modelo de lenguaje, pero no garantiza que la información recuperada sea pertinente ni que las respuestas generadas sean completamente fieles a las fuentes.

Se identificó, entre los ejemplos revisados, un problema de atribución de fuentes: utilizar una política de devoluciones para respaldar información sobre el estado logístico de un pedido.

Este comportamiento evidencia la necesidad de diferenciar las fuentes operacionales de los documentos normativos.

### 4.4. Limitaciones metodológicas

- La muestra comprende 12 preguntas por variante en cada conjunto.
- No se demuestra significancia estadística de las diferencias.
- No se ha establecido que todas las variantes se ejecutaran bajo condiciones idénticas.
- Las evaluaciones dependen de criterios de revisión humana.
- Los resultados no representan el rendimiento de un sistema desplegado en producción.

## 5. Recomendaciones

1. Fortalecer la selección y atribución de fuentes documentales.
2. Mantener reglas deterministas para evaluar devoluciones.
3. Separar consultas de pedidos, preguntas frecuentes y políticas comerciales.
4. Ampliar la cantidad y diversidad de casos de prueba.
5. Repetir los experimentos bajo condiciones controladas.
6. Mantener validación humana para decisiones sensibles.

## 6. Conclusión

La evaluación evidencia que una mayor especificidad del prompt no garantiza, por sí sola, mejores resultados.

La variante V3 corregida obtuvo el mayor porcentaje de respuestas correctas, aunque presentó una respuesta incorrecta.

El proyecto demuestra la utilidad de combinar modelos de lenguaje, recuperación documental y reglas deterministas, manteniendo mecanismos de trazabilidad y supervisión humana.

Los resultados corresponden a un prototipo académico basado en datos ficticios y no constituyen una validación para producción.