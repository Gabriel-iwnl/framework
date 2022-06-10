from django.contrib import messages
from django.shortcuts import (
    render, redirect, get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseNotAllowed

from visitantes.models import Visitante
from visitantes.forms import (
    VisitanteForm, AutorizaVisitanteForm
)

from django.utils import timezone

@login_required #Com essa função, fazemos a view ser acessível somente após a autenticação
def registrar_visitantes(request):   

    form = VisitanteForm()      #Aqui chamamos a função de registro de visitante localizada em forms

    if request.method == "POST":        #O método POST é sempre utilizado quando precisamos enviar informações pro servidor. Nesse caso estamos enviado os dados de um novo visitante
        form = VisitanteForm(request.POST) #Passamos o corpo para nossa classe VisitanteForm que validará as informações

        if form.is_valid():             #Aqui verificamos se nosso formulário é válido
            visitante = form.save(commit=False)  #Dessa forma o Django retorna um visitante mas que ainda não foi salvo no banco de dados
                                                  #Como a gente quer setar o valor de um atributo, faz total sentido usar essa estratégia      

            visitante.registrado_por = request.user.porteiro #Com o valor do atributo registrado_por setado agora podemos salvar o visitante no banco
            visitante.save()

            messages.success(
                request,
                "Visitante registrado com sucesso"
            )

            return redirect("index")   #Usamos o redirect para redirecionar e evitar que os mesmos dados sejam enviados mais de uma vez ao nosso servidor

    context = {                      #Colocamos todas as variáveis em nosso dicionário de contexto para facilitar acessso
        "nome_pagina": "Registrar visitante",
        "form": form
    }

    return render(request, "registrar_visitante.html", context)

@login_required #Com essa função, fazemos a view ser acessível somente após a autenticação
def informacoes_visitante(request, id):  #Id do visitante a ser buscado no banco de dados

    visitante = get_object_or_404(  #O get_object_or_404 busca a instancia que a gente quer ou retorna um 404
        Visitante,
        id=id
    )
    
    form = AutorizaVisitanteForm() #Aqui a gente chama o método AurotizaVisitanteForm localizada em visitantes forms

    if request.method == "POST":       #Aqui fazemos a mesma verificação contida na função registrar_visitantes
        form = AutorizaVisitanteForm(
            request.POST,
            instance=visitante      #Passando o instance o Django entende que a gente quer atualizar o objeto em questão
        )

        if form.is_valid():          #Aqui verificamos se nosso formulário é válido
            visitante = form.save(commit=False)

            visitante.status = "EM_VISITA"     #Caso o formulário seja válido, já atualizamos o status
            visitante.horario_autorizacao = timezone.now()  #Buscamos o horario atual utilizando a função timezone.now()

            visitante.save()    #Com todos os campos setados podemos salvar o visitante no banco

            messages.success(
                request,
                "Entrada de visitante autorizada com sucesso"
            )

            return redirect("index") #Usamos o redirect para redirecionar e evitar que os mesmos dados sejam enviados mais de uma vez ao nosso servidor

    context = {             #Contexto da view
        "nome_pagina": "Informações de visitante",
        "visitante": visitante,
        "form": form
    }

    return render(request,"informacoes_visitante.html", context)  #Renderizando o template de informações_visitantes

@login_required #Com essa função, fazemos a view ser acessível somente após a autenticação
def finalizar_visita(request, id):

    if request.method == "POST":
        visitante = get_object_or_404(
            Visitante,                  #Como não estamos utilizando um formulário, vamos buscar nosso visitante e atualizar as informações diretamente na instância buscada
            id=id
        )

        visitante.status = "FINALIZADO"     #Mudamos o status pra finalizado
        visitante.horario_saida = timezone.now() #Buscamos a hora atual

        visitante.save()        #Com os elementos que serão atualizados já setados, podemos salvar no banco

        messages.success(
            request,
            "Visita finalizada com sucesso"
        )

        return redirect("index")  #Usamos o redirect para redirecionar e evitar que os mesmos dados sejam enviados mais de uma vez ao nosso servidor

    else:
        return HttpResponseNotAllowed(  #Aqui a gente permite que apenas o método POST acesse a view
            ["POST"],
            "Método não permitido"
        )