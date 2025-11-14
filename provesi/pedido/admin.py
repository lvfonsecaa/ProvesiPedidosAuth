from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "owner_id", "fechaCreacion", "estadoActual", "direccion", "total")
    list_filter = ("estadoActual",)
    search_fields = ("id", "owner_id", "direccion")
