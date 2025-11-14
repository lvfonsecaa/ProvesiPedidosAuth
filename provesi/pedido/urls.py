from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/estado/',         views.pedido_estado_view,          name='pedido-estado'),
    path('<int:pk>/direccion/',      views.pedido_direccion_update_view, name='pedido-direccion'),
    path('<int:pk>/direccion/editar/', views.pedido_direccion_form_view,   name='pedido-direccion-form'),
]
