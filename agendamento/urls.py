from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("medicos/", views.medicos_list, name="medicos_list"),
    path("medicos/<int:medico_id>/", views.medico_detail, name="medico_detail"),
    path(
        "medicos/<int:medico_id>/horarios/<str:data>/",
        views.horarios_disponiveis,
        name="horarios_disponiveis",
    ),
    path("consultas/", views.consultas_list, name="consultas_list"),
]
