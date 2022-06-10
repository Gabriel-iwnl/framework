from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views

from dashboard.views import index
from visitantes.views import (
    registrar_visitantes, informacoes_visitante, finalizar_visita
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "login/",                           #String que representa a URL no navegador
        auth_views.LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    path(
        "logout/",                      #String que representa a URL no navegador
        auth_views.LogoutView.as_view(
            template_name="logout.html"
        ),
        name="logout"
    ),

    path(
        "",
        index,
        name="index",
    ),

    path(
        "registrar-visitante/",         #String que representa a URL no navegador
        registrar_visitantes,           #Função de view que será retornada
        name="registrar_visitante",
    ),

    path(
        "visitantes/<int:id>/",         #String que representa a URL no navegador
        informacoes_visitante,          #Função de view que será retornada
        name="informacoes_visitante",
    ),

    path(
        "visitantes/<int:id>/finalizar-visita/",        #String que representa a URL no navegador
        finalizar_visita,                               #Função de view que será retornada
        name="finalizar_visita"
    )
]
