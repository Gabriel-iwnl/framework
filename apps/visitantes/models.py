from django.db import models

class Visitante(models.Model): #models.Model representa um modelo padrão do Django já com funcionalidades de interação com o banco de dados

    STATUS_VISITANTE = [
        ("AGUARDANDO", "Aguardando autorização"),  #Lista de possíveis STATUS do usuário, e como será exibida para o usuário final
        ("EM_VISITA", "Em visita"),
        ("FINALIZADO", "Visita finalizada")
    ]

    status = models.CharField(      #Adicionando o Status ao nosso modelo
        verbose_name="Status",
        max_length=10,
        choices=STATUS_VISITANTE,
        default="AGUARDANDO"
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=194
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11
    )

    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
        auto_now=False,
        auto_now_add=False,
    )

    numero_casa = models.PositiveSmallIntegerField(  
        verbose_name="Número da casa a ser visitada",        
    )

    placa_veiculo = models.CharField(
        verbose_name="Placa de veículo",
        max_length=7,
        blank=True,                    #definições de campos não obrigatórios, ou seja, podem ser nulos ou brancos
        null=True,  
    )

    horario_chegada = models.DateTimeField(
        verbose_name="Horário de chegada na portaria",
        auto_now_add=True
    )

    horario_saida = models.DateTimeField(
        verbose_name="Horário de saída do condomínio",
        auto_now=False,
        blank=True,                 #como vamos pegar o horario de saída no final da visita, inicialmente podemos criar eles brancos ou nulos
        null=True,
    )

    horario_autorizacao = models.DateTimeField(
        verbose_name="Horario de autorizacao de entrada",
        auto_now=False,
        blank=True,                 #A autorização de entrada pode demorar um pouco, então inicialmente pode ser branco ou nulo
        null=True,
    )

    morador_responsavel = models.CharField(
        verbose_name="Nome do morador responsável por autorizar a entrada",
        max_length=194, 
        blank=True                  #Em primeiro momento o morador responsável não é registrado, após o contato do porteiro com o morador, podemos registrar o morador responsável
    )

    registrado_por = models.ForeignKey( #O campo ForeignKey evita que a gente precise replicar as informações do Porteiro no registro do visitante, precisando somento do id
        "porteiros.Porteiro",          #Usamos o modelo do Django para vincular o porteiro com o visitante, pra gente saber qual porteiro que liberou a visita
        verbose_name="Porteiro responsável pelo registro",
        on_delete=models.PROTECT
    )

    def get_horario_saida(self):    #O self permite acessar os argumentos da própria classe
        if self.horario_saida:
            return self.horario_saida
                                            #Aqui retorna uma mensagem caso o horário de saída ainda não tenha sido preenchido
        return "Horário de saída não registrado"

    def get_horario_autorizacao(self):
        if self.horario_autorizacao:
            return self.horario_autorizacao
                                                #Aqui retorna uma mensagem caso o horário de autorização ainda não tenha sido preenchido
        return "Visitante aguardando autorização"

    def get_morador_responsavel(self):
        if self.morador_responsavel:
            return self.morador_responsavel
                                                #Aqui retorna uma mensagem caso o morador responsável ainda não tenha autorizado
        return "Visitante aguardando autorização"

    def get_placa_veiculo(self):
        if self.placa_veiculo:
            return self.placa_veiculo
                                            #Aqui retorna uma mensagem caso o veículo não tenha sido registrado
        return "Veiculo não registrado"

    def get_cpf(self):
        if self.cpf:
            cpf = str(self.cpf)
                                        #Esse método a gente formata a aparência do CPF
            cpf_parte_um = cpf[0:3]
            cpf_parte_dois = cpf[3:6]
            cpf_parte_tres = cpf[6:9]
            cpf_parte_quatro = cpf[9:]

            cpf_formatado = f"{cpf_parte_um}.{cpf_parte_dois}.{cpf_parte_tres}-{cpf_parte_quatro}"

            return cpf_formatado

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        db_table = "visitante"      #Nessa linha definimos o nome da tabela que o Django vai criar pra armazenar nossas visitas

    def __str__(self):
        return self.nome_completo   #Aqui a gente transforma a instância do objeto em string e retorna, a fins de exibição