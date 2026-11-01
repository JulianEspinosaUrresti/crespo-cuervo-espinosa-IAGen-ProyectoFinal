from datetime import date
from src.devoluciones import verificar_elegibilidad, registrar_solicitud
def test_perecedero():
    assert verificar_elegibilidad("ECO-1003","no lo quiero")["estado"]=="no_elegible"
def test_danado_escalamiento():
    assert verificar_elegibilidad("ECO-1003","llegó dañado")["estado"]=="escalar"
def test_no_entregado():
    assert verificar_elegibilidad("ECO-1001","no lo quiero")["estado"]=="no_elegible"
def test_no_inventar_fecha():
    assert verificar_elegibilidad("ECO-1009","no lo quiero",True,True)["estado"]=="requiere_datos"
def test_elegible_y_duplicado(tmp_path):
    ev=verificar_elegibilidad("ECO-1009","cambié de opinión",True,True,
                             fecha_entrega="2026-10-30",hoy=date(2026,11,1))
    assert ev["estado"]=="pre_elegible"
    db=tmp_path/"solicitudes.db"
    assert registrar_solicitud("ECO-1009","cambié de opinión",ev,False,db)["estado"]=="requiere_confirmacion"
    assert registrar_solicitud("ECO-1009","cambié de opinión",ev,True,db)["estado"]=="registrado"
    assert registrar_solicitud("ECO-1009","cambié de opinión",ev,True,db)["estado"]=="duplicado"
def test_fuera_plazo():
    assert verificar_elegibilidad("ECO-1009","no lo quiero",True,True,
       fecha_entrega="2026-10-01",hoy=date(2026,11,1))["estado"]=="no_elegible"
