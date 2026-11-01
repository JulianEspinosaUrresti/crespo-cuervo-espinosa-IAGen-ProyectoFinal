# EcoMarket — Proyecto Final (extensión del Taller 2)
**Todos los pedidos, políticas, solicitudes y etiquetas son ficticios.**
El código original del Taller 2 permanece disponible.
## Instalación
Python 3.11 recomendado.
```bash
python -m venv .venv
# activar entorno
pip install -r requirements.txt
ollama pull llama3.2:3b
python -m src.rag_ejemplo --indexar
streamlit run app.py
```
Ollama debe estar ejecutándose. Primera indexación descarga el modelo de embeddings.
## Pruebas
```bash
python -m pytest -q
```
## Demostración
- `¿Qué dice la política de devoluciones?` (RAG)
- `Quiero devolver ECO-1003` (perecedero excluido)
- `ECO-1003 llegó dañado, quiero devolverlo` (escalamiento humano)
- `Quiero devolver ECO-1009` (requiere datos y fecha real de entrega)
- Con fecha real ficticia reciente, sin uso, empaque original y confirmación,
  registrar una solicitud y mostrar referencia simulada.
## Documentación
Ver `docs/proyecto_final.md`. No publicar esta demo sin autenticación y controles de producción.
