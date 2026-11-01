# Proyecto final — EcoMarket
## Fase 1. Arquitectura
Se conserva el RAG del Taller 2 (`src/rag_ejemplo.py`): Chroma, MiniLM multilingüe, Ollama y consultas exactas.
El orquestador `src/agente.py` clasifica la intención con LangChain/Ollama y decide entre RAG y
las herramientas deterministas `verificar_elegibilidad` y `registrar_solicitud`.
Las decisiones sensibles se calculan con reglas Python, nunca mediante texto generado.
La ruta de devoluciones explícitas prevalece sobre la clasificación del modelo.
## Fase 2. Implementación y pruebas
`src/devoluciones.py` consulta pedidos y catálogo existentes, valida exclusiones y plazo,
y registra solicitudes idempotentes en SQLite. `app.py` ofrece interfaz Streamlit.
Las pruebas cubren perecederos, daños, pedidos no entregados, ausencia de fecha real,
confirmación, duplicados y plazo excedido.
**Limitación del dataset original:** `entrega_estimada` no es fecha real de entrega.
El usuario debe aportar fecha real para la simulación. En producción se consultaría al transportista.
## Fase 3. Análisis crítico
Alucinaciones: la lógica de elegibilidad no depende del LLM.
Privacidad: datos ficticios; en producción exigir autenticación/autorización por pedido,
cifrado, retención mínima y auditoría.
Sesgos: evaluar paridad de resultados por tipos de casos y lenguaje, sin inferir características sensibles.
Impacto laboral: el sistema asiste y escala reclamos; no reemplaza la decisión humana.
Seguridad: el prototipo no debe desplegarse públicamente; no verifica identidad,
no firma guías y no integra transportistas.
Monitoreo: medir precisión de clasificación, tasa de escalamiento, errores,
duplicados, latencia y satisfacción, con revisión humana.
## Fase 4. Despliegue
Ejecutar `python -m src.rag_ejemplo --indexar` y luego `streamlit run app.py`.
Ollama debe estar activo y contar con `llama3.2:3b`.
Demostrar una consulta RAG, una devolución excluida, un daño escalado y un
registro de solicitud ficticia. La etiqueta es una referencia interna, no guía válida.
## Decisiones y compromisos
Se elige LangChain por compatibilidad con Taller 2. No se añade fine-tuning porque
los datos de política son escasos y cambiantes. La solución separa documentos recuperados,
datos transaccionales y reglas de negocio para evitar confundir probabilidades del LLM
con hechos verificables.
