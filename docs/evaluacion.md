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