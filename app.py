import streamlit as st
from src.agente import responder
st.set_page_config(page_title="EcoMarket | Agente académico")
st.title("EcoMarket — Agente de IA")
st.caption("Prototipo académico con datos ficticios. Las etiquetas no son válidas para envío.")
pregunta=st.text_input("Consulta",placeholder="Quiero devolver el pedido ECO-1009")
with st.expander("Datos para solicitar una devolución"):
    motivo=st.text_input("Motivo")
    fecha=st.text_input("Fecha REAL de entrega (AAAA-MM-DD); no usar fecha estimada")
    sin_uso=st.selectbox("¿Sin uso?",["Sin confirmar","Sí","No"])
    empaque=st.selectbox("¿Empaque original?",["Sin confirmar","Sí","No"])
    higiene=st.selectbox("¿Producto de higiene abierto?",["Sin confirmar","Sí","No"])
    confirmar=st.checkbox("Confirmo registrar solicitud ficticia, sujeta a validación humana")
def conv(v): return {"Sin confirmar":None,"Sí":True,"No":False}[v]
if st.button("Enviar",type="primary") and pregunta:
    with st.spinner("Consultando..."):
        try:
            resultado=responder(pregunta,motivo=motivo,fecha_entrega=fecha or None,
                sin_uso=conv(sin_uso),empaque_original=conv(empaque),
                higiene_abierto=conv(higiene),confirmar=confirmar)
            st.write(resultado["respuesta"])
            with st.expander("Trazabilidad"):
                st.json(resultado)
        except Exception as exc:
            st.error(f"No se pudo completar la consulta: {exc}")
