# Proyecto Final — EcoMarket

**Maestría en Inteligencia Artificial — IA Generativa**

**Integrantes:** David Crespo, Jhon Jairo Cuervo y Julian Espinosa

## Fase 1. Arquitectura de la solución

### 1.1. Descripción

EcoMarket es un prototipo académico de agente de inteligencia artificial generativa para atención al cliente, consultas documentales y evaluación preliminar de devoluciones.

El proyecto extiende el sistema desarrollado en el Taller 2, conservando su arquitectura de recuperación aumentada por generación (RAG) e incorporando herramientas deterministas para operaciones sujetas a reglas de negocio.

### 1.2. Componentes

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| Interfaz | Streamlit | Recibir consultas y mostrar respuestas |
| Orquestador | Python y LangChain | Clasificar y dirigir consultas |
| LLM | Llama 3.2 3B mediante Ollama | Interpretar consultas y generar respuestas |
| Recuperación | RAG y Chroma | Recuperar información documental |
| Embeddings | MiniLM multilingüe | Representar documentos mediante vectores |
| Herramientas | Python | Evaluar reglas comerciales |
| Persistencia | SQLite | Registrar solicitudes y controlar duplicados |

### 1.3. Flujo de funcionamiento

1. El usuario ingresa una consulta en Streamlit.
2. El orquestador identifica la intención de la solicitud.
3. Las devoluciones explícitas se dirigen prioritariamente a la ruta determinista.
4. Las consultas documentales utilizan recuperación de información mediante RAG.
5. Las herramientas Python verifican condiciones comerciales cuando corresponde.
6. El sistema presenta una respuesta y la trazabilidad disponible.

### 1.4. Justificación tecnológica

**Ollama y Llama 3.2 3B**

Permiten ejecutar el modelo generativo localmente, reduciendo la dependencia de servicios externos. Esta elección resulta apropiada para un prototipo académico con recursos limitados.

Como contrapartida, el rendimiento depende del hardware y el modelo puede presentar errores de interpretación.

**RAG con Chroma y MiniLM multilingüe**

Permite consultar información documental sin modificar los parámetros del modelo generativo.

Se prefiere RAG frente a fine-tuning para incorporar políticas y documentación, porque facilita actualizar el conocimiento mediante documentos sin volver a entrenar el LLM.

**Python y reglas deterministas**

Las decisiones de elegibilidad se calculan mediante condiciones explícitas y verificables.

Esto reduce el riesgo de que una respuesta generada autorice una devolución sin cumplir las políticas comerciales.

**SQLite**

Proporciona persistencia local sencilla y permite controlar registros duplicados.

Es apropiado para el alcance académico. Para un sistema comercial con múltiples usuarios concurrentes sería necesario evaluar una infraestructura de datos más robusta.

### 1.5. Costos y escalabilidad

El prototipo evita costos recurrentes por llamadas a una API externa de generación, aunque requiere recursos locales de procesamiento, memoria, almacenamiento y energía.

La arquitectura modular permite considerar futuras integraciones con servicios de inventario, logística y atención al cliente.

Para producción sería necesario evaluar concurrencia, tiempos de respuesta, disponibilidad, monitoreo, seguridad y costos operativos.

---

## Fase 2. Implementación y pruebas

### 2.1. Implementación

El proyecto se organiza mediante los siguientes módulos:

- `src/agente.py`: orquestación de consultas.
- `src/rag_ejemplo.py`: recuperación documental.
- `src/devoluciones.py`: evaluación y registro de devoluciones.
- `app.py`: interfaz de usuario.
- `data/`: pedidos, inventario, políticas y casos ficticios.
- `tests/`: pruebas automatizadas.
- `resultados/`: evidencias locales de evaluación y reporte publicado de pytest.

### 2.2. Gestión de devoluciones

La lógica de negocio contempla:

- Identificación del pedido.
- Consulta del producto asociado.
- Exclusiones por categoría.
- Verificación de condiciones y plazos.
- Tratamiento de pedidos no entregados.
- Escalamiento de casos especiales.
- Registro de solicitudes ficticias.
- Prevención de duplicados.

La elegibilidad preliminar no representa una autorización definitiva.

### 2.3. Limitación de fechas

El dataset original contiene el atributo `entrega_estimada`, que no equivale a una fecha real de entrega.

Por tanto, el prototipo solicita la fecha real cuando es necesaria para evaluar el plazo de devolución.

En producción, esta información debería obtenerse de un sistema logístico confiable.

### 2.4. Validación automatizada

Se ejecutó la suite de pruebas mediante pytest.

**Resultado observado:**

- 14 pruebas ejecutadas.
- 14 pruebas aprobadas.
- 0 pruebas fallidas.

Las pruebas verifican aspectos como pedidos, recuperación de contexto, productos perecederos, devoluciones, ausencia de fechas, escalamiento y solicitudes duplicadas.

**Evidencia:** [Reporte de pruebas automatizadas](../resultados/pytest_resultado.txt)

### 2.5. Alcance de la validación

Los resultados demuestran que los casos incluidos en la suite automatizada se ejecutaron satisfactoriamente.

No constituyen evidencia suficiente para afirmar que el modelo generativo está libre de alucinaciones, que el sistema soporta múltiples usuarios concurrentes o que su desempeño es adecuado para producción.

---

## Fase 3. Análisis crítico

### 3.1. Fortalezas

**Separación de responsabilidades:** el modelo generativo se utiliza para interpretar consultas y elaborar respuestas, mientras las reglas comerciales se ejecutan mediante Python.

**Recuperación contextual:** RAG permite utilizar documentos relevantes sin requerir fine-tuning.

**Trazabilidad:** la aplicación permite observar información sobre la ruta de procesamiento.

**Reproducibilidad:** el repositorio contiene código, dependencias, datos ficticios y pruebas automatizadas.

### 3.2. Limitaciones

**Alucinaciones:** el LLM puede producir información incorrecta o no respaldada por los documentos recuperados.

**Dependencia del contexto:** documentos incompletos, fragmentos poco relevantes o consultas ambiguas pueden afectar las respuestas.

**Latencia:** la ejecución local depende de los recursos computacionales disponibles.

**Cobertura:** los pedidos, productos y casos de prueba representan un escenario académico reducido.

**Integración:** no existe conexión con sistemas reales de logística, pagos o gestión comercial.

### 3.3. Sesgos

El sistema debe evaluarse con diferentes formulaciones lingüísticas, niveles de detalle y tipos de solicitudes.

La evaluación debería verificar si consultas equivalentes reciben tratamientos consistentes.

No se dispone de evidencia suficiente para afirmar que el modelo está libre de sesgos.

### 3.4. Privacidad y seguridad

El prototipo utiliza datos ficticios.

En un entorno real sería necesario incorporar autenticación, autorización por pedido, cifrado, políticas de retención, auditoría y controles frente a instrucciones maliciosas incorporadas en documentos recuperados.

También sería necesario restringir el acceso a información personal y evitar que el agente revele datos de otros clientes.

### 3.5. Impacto laboral

El agente puede apoyar tareas repetitivas de atención al cliente, como consultar pedidos y orientar solicitudes.

Sin embargo, las reclamaciones complejas y las decisiones comerciales sensibles deben permanecer bajo supervisión humana.

Su incorporación requeriría capacitación, definición de responsabilidades y mecanismos claros de escalamiento.

### 3.6. Mejoras futuras

Se proponen las siguientes mejoras, que no forman parte de las funcionalidades verificadas del prototipo:

1. Integración con sistemas reales de pedidos y logística.
2. Autenticación y autorización por usuario.
3. Evaluación cuantitativa de calidad de recuperación y respuestas.
4. Medición de latencia y consumo de recursos.
5. Pruebas de concurrencia y escalabilidad.
6. Monitoreo y auditoría de interacciones.

---

## Conclusiones

El proyecto EcoMarket demuestra cómo integrar un modelo de lenguaje basado en Transformers, recuperación aumentada por generación y herramientas deterministas para resolver consultas de comercio electrónico.

Su principal decisión arquitectónica consiste en separar la generación de lenguaje de las operaciones sujetas a reglas comerciales.

Las 14 pruebas automatizadas aprobadas proporcionan evidencia de funcionamiento para los casos implementados.

El proyecto constituye un prototipo académico reproducible y extensible. Para su utilización comercial serían necesarias validaciones adicionales de seguridad, precisión, desempeño y escalabilidad.