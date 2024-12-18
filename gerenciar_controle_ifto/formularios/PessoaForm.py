from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User


class CadastrarPessoaForm(forms.Form):
    nome = forms.CharField(label="Nome:")
    sobrenome = forms.CharField(label="Sobrenome:")
    cpf = forms.CharField(label="CPF:")
    data_nascimento = forms.DateTimeField(label="Data de nascimento:",
                                          widget= forms.DateTimeInput(
                                                attrs={'type': 'date'},
                                                format='%d-%m-%Y'
                                            ),
                                        )
    cod_Papel_pessoa = forms.ModelChoiceField(label="Funcao",queryset=Papel_pessoa.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(CadastrarPessoaForm,self).__init__(*args, **kwargs)
        
        self.fields['nome'].widget.attrs = {
            'id' : 'nome'
        }
        self.fields['sobrenome'].widget.attrs = {
            'id' : 'sobrenome'
        }
        self.fields['cpf'].widget.attrs = {
            'id' : 'cpf',
            'maxlength' : 11
        }
        self.fields['data_nascimento'].widget.attrs = {
            'id' : 'data_nascimento',
            'min' : '1900-01-01'
        }
        
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'nome',
            'sobrenome',
            'cpf',
            'data_nascimento',
            'cod_Papel_pessoa',
            
            HTML("""<a href="{% url "visualizar_pessoa" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        nome = self.cleaned_data['nome']
        sobrenome = self.cleaned_data['sobrenome']
        cpf = self.cleaned_data['cpf']
        cpf_validate = CPF()

        if len(nome) <=2:
            self.add_error('nome',"O nome devera ter pelo menos 3 caracteres")

        if len(sobrenome) <=2:
            self.add_error('sobrenome',"O sobrenome devera ter pelo menos 3 caracteres")

        if len(cpf) != 11:
            self.add_error('cpf','CPF incompleto')
        else:
            cpf_pessoa = Pessoa.objects.filter(cpf=cpf)
            if cpf_pessoa:
                self.add_error('cpf', "CPF informado já foi cadastrado no sistema")
            else:
                cpf_p1 = cpf[:3]
                cpf_p2 = cpf[3:6]
                cpf_p3 = cpf[6:9]
                cpf_p4 = cpf[9:]
                cpf_particionado = "{}.{}.{}-{}".format(cpf_p1,cpf_p2,cpf_p3,cpf_p4)

                if not(cpf_validate.validate(cpf_particionado)):
                    self.add_error('cpf', "CPF informado é invalido")

class EditarPessoaForm(forms.Form):
    id = forms.IntegerField()
    nome = forms.CharField(label="Nome:")
    sobrenome = forms.CharField(label="Sobrenome:")
    cpf = forms.CharField(label="CPF:")
    data_nascimento = forms.DateTimeField(label="Data de nascimento:",
                                          widget= forms.DateTimeInput(
                                                attrs={'type': 'date'},
                                                format='%d-%m-%Y'
                                            ),
                                        )
    cod_Papel_pessoa = forms.ModelChoiceField(label="Funcao",queryset=Papel_pessoa.objects.all())
    
    def __init__(self, *args, cod_cargoID=None, vinculado=False, **kwargs):
        super(EditarPessoaForm,self).__init__(*args, **kwargs)

        self.fields['id'].widget.attrs = {
            'readonly' : True
        }
        self.fields['nome'].widget.attrs = {
            'id' : 'nome'
        }
        self.fields['sobrenome'].widget.attrs = {
            'id' : 'sobrenome'
        }
        self.fields['cpf'].widget.attrs = {
            'id' : 'cpf',
            'maxlength' : 11
        }
        self.fields['data_nascimento'].widget.attrs = {
            'id' : 'data_nascimento',
            'min' : '1900-01-01'
        }
        
        if cod_cargoID is not None:
            cod_cargo =Papel_pessoa.objects.filter(id=cod_cargoID)
            if vinculado == False:
                others_options = Papel_pessoa.objects.exclude(id=cod_cargoID)
                self.fields['cod_Papel_pessoa'].queryset = cod_cargo | others_options
            else:
                self.fields['cod_Papel_pessoa'].queryset = cod_cargo
        
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'id',
            'nome',
            'sobrenome',
            'cpf',
            'data_nascimento',
            'cod_Papel_pessoa',
            
            HTML("""<a href="{% url "visualizar_pessoa" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        id = self.cleaned_data['id']
        nome = self.cleaned_data['nome']
        sobrenome = self.cleaned_data['sobrenome']
        cpf = self.cleaned_data['cpf']
        cpf_validate = CPF()
        
        print(id)

        if len(nome) <=2:
            self.add_error('nome',"O nome devera ter pelo menos 3 caracteres")

        if len(sobrenome) <=2:
            self.add_error('nome',"O sobrenome devera ter pelo menos 3 caracteres")

        if len(cpf) != 11:
            self.add_error('cpf','CPF incompleto')
        else:
            cpf_pessoa = Pessoa.objects.filter(cpf=cpf).exclude(id=id)
            if cpf_pessoa:
                self.add_error('cpf', "CPF informado já foi cadastrado no sistema")
            else:
                cpf_p1 = cpf[:3]
                cpf_p2 = cpf[3:6]
                cpf_p3 = cpf[6:9]
                cpf_p4 = cpf[9:]
                cpf_particionado = "{}.{}.{}-{}".format(cpf_p1,cpf_p2,cpf_p3,cpf_p4)

                if not(cpf_validate.validate(cpf_particionado)):
                    self.add_error('cpf', "CPF informado é invalido")

class VincularPessoaRfid(forms.Form):
    id = forms.IntegerField(label="ID Pessoa:", required=False)
    pessoa= forms.CharField(label="Pessoa:", required=False)
    rfid_a_vincular = forms.CharField(label="RFID:")

    def __init__(self, *args, **kwargs):
        super(VincularPessoaRfid, self).__init__(*args, **kwargs)
        
        self.fields['id'].widget.attrs = {
            'readonly' : True
        }

        self.fields['pessoa'].widget.attrs = {
            'readonly' : 'True',
        }
        
        self.fields['rfid_a_vincular'].widget.attrs = {
            'id' : 'rfid_a_vincular',
            'readonly' : 'True',
            'placeholder' : 'Clique em "Ler Rfid" para ler a Tag'
        }

        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'id',
            'pessoa',
            'rfid_a_vincular',

            HTML("""<a href="{% url "visualizar_pessoa" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>
                    <button type='button' class="btn btn-danger", onclick="leitura_rfid_vinculacao()", id="botao_ler_rfid">Ler RFID</button>
                    """),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )


    def clean(self):
        id_pessoa = self.cleaned_data['id']
        rfid_a_vincular = self.cleaned_data['rfid_a_vincular']

        if rfid_a_vincular == "" or rfid_a_vincular=="Nenhum card" or rfid_a_vincular=="undefined":
            self.add_error('rfid_a_vincular', "O leitor não identificou a informação da Tag. Favor, tentar novamente.")

        try:
            a_vincular = Rfid.objects.filter(tag_rfid_value=rfid_a_vincular).first()
            
            if a_vincular.vinculado:
                self.add_error('rfid_a_vincular', "A Tag-Rfid informada já foi vinculado à uma pessoa")
            else:
                pessoa = Pessoa.objects.get(id=id_pessoa)
                
                if not(a_vincular.cod_corRFID_funcao.cod_cargo.id == pessoa.cod_Papel_pessoa.id):
                    self.add_error('rfid_a_vincular', "A Tag-Rfid informada não pertence a mesma função da pessoa ")
        except:
            if not(rfid_a_vincular == "" or rfid_a_vincular=="Nenhum card" or rfid_a_vincular=="undefined"):
                self.add_error('rfid_a_vincular', "A Tag-Rfid informada não foi encontrada. Favor, cadastra-la no sistema.")

class BuscarPessoaForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarPessoaForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Busque por Nome ou CPF',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-group mb-2'
        self.helper.layout = Layout(
            'campo',
            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )