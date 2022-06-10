from django import forms                       #Da mesma forma que uma classe model é mapeada pros campos do banco de dados, os campos forms são mapeados para elementos HTML
from visitantes.models import Visitante

class VisitanteForm(forms.ModelForm):    #Essa classe é responsável em criar um formulário para resgistro de visitantes
    class Meta:
        model = Visitante
        fields = [
            "nome_completo", "cpf", "data_nascimento",      #Lista dos campos que a gente quer exibir
            "numero_casa", "placa_veiculo"
        ]
        error_messages = {                      #Dicionário de mensagens de possíveis erros no formulário
            "nome_completo": {
                "required": "O nome completo do visitante é obrigatório"
            },
            "cpf": {
                "required": "O CPF do visitante é obrigatório"
            },
            "data_nascimento": {
                "required": "A data de nascimento do visitante é obrigatória",
                "invalid": "Por favor, informe um formato válido para a data de nascimento (DD/MM/AAAA)"
            },
            "numero_casa": {
                "required": "O número da casa que será visitada é obrigatório"
            }
        }

class AutorizaVisitanteForm(forms.ModelForm):
    morador_responsavel = forms.CharField(required=True)  #Aqui a gente obriga o formulário a ter um morador responsável

    class Meta:
        model = Visitante
        fields = [ 
            "morador_responsavel"       #Para autorizar um visitante, nesse momento, já temos os outros dados do próprio, agora precisamos do morador responsável
        ]
        error_messages = {
            "morador_responsavel": {
                "required": "Por favor, informe o nome do morador responsável pela entrada do visitante"
            }
        }