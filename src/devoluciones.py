"""Herramientas deterministas. Datos y etiquetas EXCLUSIVAMENTE ficticios."""
import json
import re
import sqlite3
from datetime import date
from pathlib import Path
from .rag_ejemplo import BASE, cargar_json

DB_DEV = BASE / "data" / "devoluciones.sqlite3"

def iniciar_db(db_path=None):
    ruta = str(db_path or DB_DEV)
    con = sqlite3.connect(ruta)
    con.execute("""CREATE TABLE IF NOT EXISTS solicitudes (
        pedido_id TEXT PRIMARY KEY, motivo TEXT NOT NULL,
        estado TEXT NOT NULL, etiqueta TEXT, creado TEXT NOT NULL)""")
    con.commit()
    return con

def verificar_elegibilidad(pedido_id, motivo, sin_uso=None, empaque_original=None,
                          higiene_abierto=None, fecha_entrega=None, hoy=None):
    """Evaluación preliminar: no reemplaza validación humana."""
    pedido_id = pedido_id.strip().upper()
    pedidos = {p["id"]:p for p in cargar_json("pedidos.json")}
    productos = {p["id"]:p for p in cargar_json("inventario.json")}
    if pedido_id not in pedidos:
        return {"estado":"no_encontrado","motivo":"Pedido no registrado en datos ficticios."}
    pedido = pedidos[pedido_id]
    producto = productos[pedido["producto_id"]]
    if pedido["estado"] != "Entregado":
        return {"estado":"no_elegible","motivo":"El pedido no figura como entregado."}
    motivo_norm = motivo.casefold()
    if any(t in motivo_norm for t in ("defect", "dañ", "roto", "equivoc", "incorrect")):
        return {"estado":"escalar","motivo":"Incidencia que requiere evaluación humana."}
    if producto["categoria"] == "perecedero":
        return {"estado":"no_elegible","motivo":"Perecederos excluidos de devolución ordinaria."}
    if producto["categoria"] == "higiene" and higiene_abierto is not False:
        return {"estado":"requiere_datos" if higiene_abierto is None else "no_elegible",
                "motivo":"Confirmar si el producto de higiene está abierto; abierto no es elegible."}
    if sin_uso is None or empaque_original is None:
        return {"estado":"requiere_datos","motivo":"Confirmar que está sin uso y con empaque original."}
    if not sin_uso or not empaque_original:
        return {"estado":"no_elegible","motivo":"No cumple condiciones de estado y empaque."}
    # El Taller 2 solo registra entrega_estimada, NO fecha efectiva de entrega.
    if fecha_entrega is None:
        return {"estado":"requiere_datos","motivo":"Falta fecha real de entrega; entrega_estimada no sirve para validar el plazo."}
    try:
        fecha = date.fromisoformat(fecha_entrega)
        actual = hoy or date.today()
        dias = (actual-fecha).days
    except ValueError:
        return {"estado":"requiere_datos","motivo":"Fecha de entrega inválida (AAAA-MM-DD)."}
    if dias < 0:
        return {"estado":"requiere_datos","motivo":"La fecha real de entrega no puede ser futura."}
    if dias > 15:
        return {"estado":"no_elegible","motivo":"Supera los 15 días para devolución ordinaria."}
    return {"estado":"pre_elegible","motivo":"Cumple reglas preliminares; pendiente de validación humana.",
            "producto":producto["nombre"],"dias":dias}

def registrar_solicitud(pedido_id, motivo, evaluacion, confirmar=False, db_path=None):
    """Registro idempotente. No emite etiqueta de transporte real."""
    if not confirmar:
        return {"estado":"requiere_confirmacion","motivo":"Confirmación explícita necesaria."}
    if evaluacion.get("estado") != "pre_elegible":
        return {"estado":"bloqueado","motivo":"No existe pre-elegibilidad verificada."}
    if not re.fullmatch(r"ECO-\d{4}",pedido_id):
        return {"estado":"bloqueado","motivo":"Identificador inválido."}
    con=iniciar_db(db_path)
    try:
        existente=con.execute("SELECT estado,etiqueta FROM solicitudes WHERE pedido_id=?",(pedido_id,)).fetchone()
        if existente:
            return {"estado":"duplicado","etiqueta":existente[1],"motivo":"Solicitud previamente registrada."}
        etiqueta=f"SIMULADA-DEV-{pedido_id}"
        con.execute("INSERT INTO solicitudes VALUES (?,?,?,?,?)",
                    (pedido_id,motivo,"pendiente_validacion_humana",etiqueta,date.today().isoformat()))
        con.commit()
        return {"estado":"registrado","etiqueta":etiqueta,
                "motivo":"Etiqueta interna ficticia; no es guía de envío válida ni aprobación."}
    finally:
        con.close()
