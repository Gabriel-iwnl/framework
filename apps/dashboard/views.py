from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from visitantes.models import Visitante

from django.utils import timezone

@login_required #Com essa função, fazemos a view ser acessível somente após a autenticação
def index(request):                 #Aqui realizamos as buscas no banco de dados

    todos_visitantes = Visitante.objects.order_by(     #Buscamos todos os visitantes e guardamos na variável todos_visitantes
        "-horario_chegada"                              # o "-" na frente é pra dizer pro Django que queremos os dados sendo listados em forma descendente
    )

    visitantes_aguardando = todos_visitantes.filter(    #Buscamos todos os visitantes que estão aguardando e guardamos na variável visitantes_aguardando
        status="AGUARDANDO"
    )

    visitantes_em_visita = todos_visitantes.filter(     #Buscamos todos os visitantes em visita e guardamos os dados na variável visitantes_em_visita
        status="EM_VISITA"
    )

    visitantes_finalizado = todos_visitantes.filter(    #Buscamos todos as visitas finalizadas e guardamos na variável visitantes_finalizado
        status="FINALIZADO"
    )

    hora_atual = timezone.now()     #Aqui a gente pega o tempo atual e passa o mês pra variavel mes_atual
    mes_atual = hora_atual.month

    visitantes_mes = todos_visitantes.filter(
        horario_chegada__month=mes_atual    #Utilizando o field lookups conseguimos acessar só o mes desse campo, bas utilizar __ e o nome da propriedade
    )

    context = {
        "nome_pagina": "Início da dashboard",                       #Colocamos todas as variáveis buscadas em nosso dicionário de contexto para conseguir acessar ela no template
        "todos_visitantes": todos_visitantes,
        "visitantes_aguardando": visitantes_aguardando.count(),
        "visitantes_em_visita": visitantes_em_visita.count(),
        "visitantes_finalizado": visitantes_finalizado.count(),
        "visitantes_mes": visitantes_mes.count(),
    }

    return render(request,"index.html", context)