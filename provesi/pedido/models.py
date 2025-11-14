from django.db import models

class EstadoPedido(models.TextChoices):
    TRANSITO = "Transito"
    ALISTAMIENTO = "Alistamiento"
    POR_VERIFICAR = "Por Verificar"
    REHAZADO_X_VERIFICAR = "Rechazado por Verificar"
    VERIFICADO = "Verificado"
    CREADO = "Creado"
    EMPACADP_X_DESPACHAR = "Empacado por Despachar"
    DESPACHADO = "Despachado"
    DESPACHADO_X_FACTURAR = "Despachado por Facturar"
    FACTURADO = "Facturado"
    ENTREGADO = "Entregado"
    DEVUELTO = "Devuelto"
    PRODUCCION = "Produccion"
    BORDADO = "Bordado"
    DROPSHIPPING = "Dropshipping"
    COMPRA = "Compra"
    ANULADO = "Anulado"

class Pedido(models.Model):
    owner_id = models.CharField(
        max_length=128,
        db_index=True,
        editable=False,
    )

    fechaCreacion = models.DateTimeField(auto_now_add=True)
    estadoActual = models.CharField(
        max_length=50,
        choices=EstadoPedido.choices,
        default=EstadoPedido.ALISTAMIENTO,
    )
    direccion = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} — {self.estadoActual}"
