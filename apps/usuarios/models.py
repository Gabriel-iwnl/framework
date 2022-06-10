from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import(BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

class UsuarioManager(BaseUserManager):    #Configurações do nosso UsuarioManager, que herda a classe BaseUserManager do Django, que ajuda na configuração de criacao de usuarios
    
    def create_user(self, email, password=None): #Aqui definimos nossa funcao de criacao de usuarios, sobrescrevendo o método create_user do BaseUserManager
        usuario = self.model(
            email=self.normalize_email(email)
        )

        usuario.is_active = True
        usuario.is_staff = False
        usuario.is_superuser = False

        if password:
            usuario.set_password(password)

        usuario.save()

        return usuario

    def create_superuser(self, email, password): #Método de criacao de super usuário, o legal é notar que reaproveitamos o método create_user para criar um superusuario também
        usuario = self.create_user( 
            email=self.normalize_email(email),
            password=password,
        )

        usuario.is_active = True
        usuario.is_staff = True
        usuario.is_superuser = True

        usuario.set_password(password)

        usuario.save()

        return usuario



class Usuario(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name="E-mail do usuário",  #aqui definimos que os parametros de email do usuário, deixando claro que o email será unico
        max_length=194,
        unique=True,
    )

    is_active = models.BooleanField(
        verbose_name="Usuário está ativo",  #sempre que criarmos um usuário, por padrão, definiremos que ele está ativo
        default=True,
    )

    is_staff = models.BooleanField(
        verbose_name="Usuário é da equipe de desenvolvimento",  #parametros para usuarios que serão usados como admins
        default=False,
    )

    is_superuser = models.BooleanField(
        verbose_name="Usuário é um superusuario",       #parametros para superusuários, default false, por que não é sempre que iremos criar um super usuário
        default=False,
    )

    objects = UsuarioManager() # Aqui mostramos para aplicacao que queremos utilizar a classe UsuarioManager como padrão
    USERNAME_FIELD = "email"    #Definindo o atributo que será utilizado como campo de autenticação

    objects: UsuarioManager()  #

    class Meta:                     
        verbose_name = "Usuário"            
        verbose_name_plural = "Usuários"
        db_table = "usuario"              #Nessa linha definimos o nome da tabela que o Django vai criar pra armazenar nossos usuários

    def __str__(self):
        return self.email       #Aqui a gente transforma a instancia do objeto em string e retorna, a fins de exibição