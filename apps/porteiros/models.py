from django.db import models

class Porteiro(models.Model): #models.Model representa um modelo padrão do Django já com funcionalidades de interação com o banco de dados

    usuario = models.OneToOneField(  # 1 usuário para 1 porteiro e vice versa
        "usuarios.Usuario",
        verbose_name="Usuário",
        on_delete=models.PROTECT   #protegemos esse tipo de usuário, apenas admins tem o poder de excluir
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=194,
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    telefone = models.CharField(
        verbose_name="Telefone de contato",
        max_length=11,
    )

    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
        auto_now=False,
        auto_now_add=False,
    )

    class Meta:
        verbose_name = "Porteiro"
        verbose_name_plural = "Porteiros"
        db_table = "porteiro"              #Nessa linha definimos o nome da tabela que o Django vai criar pra armazenar nossos porteiros

    def __str__(self):
        return self.nome_completo           #Aqui a gente transforma a instância do objeto em string e retorna, a fins de exibição
