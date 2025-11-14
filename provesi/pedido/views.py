from django.shortcuts import render
import json

from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from provesi.auth0backend import getRole
from .logic.pedidos_logic import (
    get_pedido_estado,
    update_pedido_direccion,
)


@login_required
def pedido_estado_view(request, pk: int):
    """
    Devuelve el estado actual del pedido.
    Cualquier usuario autenticado puede consultarlo.
    """
    data = get_pedido_estado(pk)
    return JsonResponse(data)


@csrf_exempt
@login_required
@require_http_methods(["PATCH", "POST"])
def pedido_direccion_update_view(request, pk: int):
    """
    Actualiza la dirección de un pedido.
    Solo usuarios con rol ADMIN pueden hacerlo.
    (En esta opción desactivamos CSRF para simplificar el laboratorio.)
    """

    role = getRole(request)
    print("ROL EN UPDATE:", role)
    print("METHOD:", request.method)
    print("BODY RAW:", request.body)

    if role != "ADMIN":
        return HttpResponseForbidden("No tiene permisos para modificar el pedido.")

    # Leer JSON del body
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {"detail": "Cuerpo de la petición inválido. Se esperaba JSON."},
            status=400,
        )

    nueva_dir = body.get("direccion")
    if not nueva_dir:
        return JsonResponse(
            {"detail": "El campo 'direccion' es obligatorio."},
            status=400,
        )

    # Actualizar dirección
    updated = update_pedido_direccion(pk, nueva_dir)

    if not updated:
        return JsonResponse(
            {"detail": "Pedido no encontrado."},
            status=404,
        )

    return JsonResponse(
        {
            "id": pk,
            "direccion": nueva_dir,
            "mensaje": "Dirección actualizada correctamente.",
        }
    )


@csrf_exempt
@login_required
def pedido_direccion_form_view(request, pk: int):
    """
    Muestra el formulario HTML para editar la dirección.
    También restringido a rol ADMIN.
    (CSRF desactivado solo para simplificar el lab.)
    """
    role = getRole(request)
    print("ROL FORM:", role)

    if role != "ADMIN":
        return HttpResponseForbidden("No tiene permisos para modificar el pedido.")

    return render(request, "pedido/editar_direccion.html", {"pedido_id": pk})
