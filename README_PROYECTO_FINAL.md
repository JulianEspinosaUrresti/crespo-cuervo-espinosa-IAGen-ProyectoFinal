# EcoMarket — Proyecto Final de IA Generativa

# David Crespo - Jhon Jairo Cuervo - Julian Espinosa

**Extensión del Taller 2 — Maestría en Inteligencia Artificial**

## 1. Descripción del proyecto

EcoMarket es un prototipo académico de un agente de inteligencia artificial generativa orientado a la atención de clientes de un comercio electrónico de productos sostenibles.

El sistema integra un modelo de lenguaje de gran tamaño (LLM), recuperación aumentada por generación (RAG) y reglas de negocio implementadas en Python.

Permite consultar información sobre pedidos, inventario y políticas comerciales, así como evaluar solicitudes ficticias de devolución.

**Importante:** Todos los pedidos, productos, políticas, solicitudes y etiquetas utilizados son ficticios. El sistema no procesa devoluciones reales ni genera autorizaciones de envío.

## 2. Objetivo

Diseñar e implementar un agente de IA generativa que apoye la atención al cliente de EcoMarket, integrando información estructurada, documentación comercial y validaciones deterministas para proporcionar respuestas contextualizadas y trazables.

## 3. Arquitectura de la solución

El prototipo utiliza los siguientes componentes:

| Componente | Tecnología | Función |
|---|---|---|
| Interfaz | Streamlit | Interacción con el usuario |
| Modelo generativo | Llama 3.2 3B mediante Ollama | Generación de respuestas |
| Recuperación documental | RAG | Consulta de información relevante |
| Embeddings | Modelo de embeddings local | Representación vectorial de documentos |
| Base documental | Archivos JSON y Markdown | Información de EcoMarket |
| Lógica de negocio | Python | Validación de pedidos y devoluciones |
| Persistencia local | SQLite | Registro y control de solicitudes |
| Pruebas | pytest | Validación automatizada |

El sistema combina respuestas generativas con reglas deterministas para evitar que decisiones sensibles, como la elegibilidad de devoluciones, dependan exclusivamente del LLM.

## 4. Funcionalidades principales

- Consultas sobre productos e inventario.
- Consultas sobre estados de pedidos.
- Recuperación de información mediante RAG.
- Evaluación preliminar de devoluciones.
- Exclusión de productos perecederos según las reglas del prototipo.
- Escalamiento de casos que requieren intervención humana.
- Prevención de solicitudes duplicadas.
- Generación de referencias internas ficticias.
- Visualización de trazabilidad de las respuestas.

## 5. Instalación

Se recomienda Python 3.11 y disponer de Ollama instalado y ejecutándose.

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Descargar el modelo generativo:

```bash
ollama pull llama3.2:3b
```

Construir el índice documental:

```bash
python -m src.rag_ejemplo --indexar
```

La primera indexación puede descargar el modelo de embeddings.

Ejecutar la aplicación:

```bash
streamlit run app.py
```

La interfaz estará disponible normalmente en:

http://localhost:8501

## 6. Pruebas automatizadas

Ejecutar:

```bash
python -m pytest -v
```

En la ejecución documentada se obtuvieron:

**14 pruebas aprobadas, 0 fallidas.**

Las pruebas incluyen validaciones de pedidos, contexto documental, productos perecederos, devoluciones, fechas, escalamiento y duplicados.

Evidencia:

[resultados/pytest_resultado.txt](resultados/pytest_resultado.txt)

Estos resultados corresponden a las pruebas automatizadas incluidas en el repositorio y no representan una validación integral de calidad del modelo generativo.

## 7. Ejemplos de demostración

**Consulta sobre pedidos**

¿Qué debo hacer si mi pedido de EcoMarket está retrasado?

**Consulta documental**

¿Cuál es la política de devoluciones de EcoMarket?

**Solicitud de devolución**

Quiero devolver el producto del pedido ECO-1012.

**Producto excluido**

Quiero devolver el pedido ECO-1003.

Los identificadores anteriores corresponden exclusivamente a datos ficticios de evaluación.

## 8. Seguridad y uso responsable

El sistema incorpora las siguientes consideraciones:

- Separación entre generación de lenguaje y reglas deterministas.
- Validación humana para decisiones que requieren autorización.
- Prevención de solicitudes duplicadas.
- Uso exclusivo de datos ficticios.
- Restricciones para evitar autorizaciones de devolución no verificadas.
- Trazabilidad de las rutas de procesamiento.

## 9. Limitaciones

El prototipo presenta las siguientes limitaciones:

- Depende de la disponibilidad local de Ollama.
- La calidad de las respuestas generativas depende del modelo y del contexto recuperado.
- El conjunto de documentos y pedidos es reducido y ficticio.
- No existe integración con sistemas reales de comercio electrónico.
- No se han establecido métricas de rendimiento en producción.
- Las solicitudes de devolución requieren validación humana.

## 10. Conclusiones

El proyecto demuestra la integración de modelos de lenguaje, recuperación documental y lógica determinista en un caso práctico de comercio electrónico.

La arquitectura permite separar consultas informativas de operaciones sujetas a reglas comerciales, mejorando la trazabilidad y reduciendo el riesgo de decisiones generativas no verificadas.

El resultado constituye un prototipo académico funcional, no una plataforma comercial lista para producción.

## 11. Repositorio

El código, la documentación y las pruebas están disponibles en:

https://github.com/JulianEspinosaUrresti/crespo-cuervo-espinosa-IAGen-ProyectoFinal

El proyecto conserva la continuidad académica con el Taller 2.