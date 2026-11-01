
from src.rag_ejemplo import consultar


def test_estado_pedido_cita_fuente_correcta():
    respuesta = consultar(
        "¿Cuál es el estado del pedido ECO-1004?"
    )

    assert "Retrasado" in respuesta
    assert "No hay fecha confirmada" in respuesta
    assert "pedidos.json" in respuesta
    assert "politica_devoluciones.md" not in respuesta.lower()
