"""Orquestador de herramientas: LLM para intención; Python para reglas de negocio."""
import json
import re
from .rag_ejemplo import consultar
from .devoluciones import verificar_elegibilidad, registrar_solicitud

def detectar_intencion(texto):
    """Distingue consultas informativas de solicitudes operativas."""
    t = texto.casefold().strip()

    # Consultas informativas sobre políticas: usar RAG.
    consultas_politica = (
        "politica de devoluciones",
        "política de devoluciones",
        "politica de devolución",
        "política de devolución",
        "condiciones de devolucion",
        "condiciones de devolución",
        "requisitos para devolver",
        "plazo de devolucion",
        "plazo de devolución",
    )

    # Una pregunta general no inicia una devolución.
    if any(x in t for x in consultas_politica):
        if not re.search(
            r"\b(quiero|solicito|necesito|deseo)\s+"
            r"(devolver|retornar|cambiar|un reembolso)",
            t
        ):
            return "rag"

    # Solicitudes operativas explícitas.
    if any(x in t for x in (
        "quiero devolver",
        "solicito devolucion",
        "solicito devolución",
        "necesito devolver",
        "deseo devolver",
        "quiero retornar",
        "quiero un reembolso",
        "quiero cambiar producto",
    )):
        return "devolucion"

    # Consultas sobre pedidos.
    if re.search(r"\bECO-\d{4}\b", texto.upper()):
        return "pedido"

    return "rag"

def clasificar_con_llm(texto):
    """LangChain/Ollama: decisión de herramienta. Ante error, ruta conservadora."""
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    plantilla=ChatPromptTemplate.from_messages([
      ("system","Clasifica la intención. Devuelve SOLO una palabra: devolucion, pedido o rag. "
       "devolucion: solicitar devolución, cambio o reembolso; pedido: consultar estado; "
       "rag: preguntas sobre políticas, catálogo o FAQ. Nunca ejecutes acciones."),
      ("human","{texto}")
    ])
    salida=(plantilla | ChatOllama(model="llama3.2:3b",temperature=0)).invoke({"texto":texto}).content
    valor=salida.strip().lower()
    if valor not in {"devolucion","pedido","rag"}:
        return detectar_intencion(texto)
    return valor

def responder(texto, usar_llm_router=True, **datos):
    ruta=detectar_intencion(texto)
    if usar_llm_router:
        try:
            sugerencia=clasificar_con_llm(texto)
            # El clasificador no puede anular una intención explícita de devolución.
            # Preservar las rutas identificadas explícitamente.
            if ruta == "rag" and sugerencia in {"rag", "pedido"}:
                ruta = sugerencia
        except Exception:
            pass
    if ruta != "devolucion":
        return {"ruta":ruta,"respuesta":consultar(texto)}
    ids=set(re.findall(r"\bECO-\d{4}\b",texto.upper()))
    if len(ids)!=1:
        return {"ruta":ruta,"respuesta":"Indica un único ID de pedido (ECO-XXXX)."}
    pedido_id=ids.pop()
    motivo=datos.get("motivo") or texto
    evaluacion=verificar_elegibilidad(
        pedido_id,motivo,datos.get("sin_uso"),datos.get("empaque_original"),
        datos.get("higiene_abierto"),datos.get("fecha_entrega"))
    resultado={"ruta":ruta,"evaluacion":evaluacion,
               "respuesta":evaluacion["motivo"]}
    if datos.get("confirmar"):
        registro=registrar_solicitud(pedido_id,motivo,evaluacion,True)
        resultado["registro"]=registro
        resultado["respuesta"]+=" "+registro["motivo"]
        if "etiqueta" in registro: resultado["respuesta"]+=" Referencia: "+registro["etiqueta"]
    return resultado
