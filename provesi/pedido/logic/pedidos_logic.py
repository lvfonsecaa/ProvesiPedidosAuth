from ..models import Pedido

def get_pedido_estado(pk: int):
    pedido = Pedido.objects.get(pk=pk)
    return {"id": pedido.id, "estadoActual": pedido.estadoActual}

def update_pedido_direccion(pk: int, nueva_dir: str) -> bool:
    updated = Pedido.objects.filter(pk=pk).update(direccion=nueva_dir)
    return updated == 1