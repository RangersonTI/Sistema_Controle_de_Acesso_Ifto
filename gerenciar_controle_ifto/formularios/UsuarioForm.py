from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 
            
# PARA USUARIOS (CADASTRAR E EDITAR)

class CadastrarUsuarioForm(forms.Form):
    nome = forms.CharField(label="Nome:")   
    sobrenome = forms.CharField(label="Sobrenome:")
    email = forms.EmailField(label="Email:")
    usuario = forms.CharField(label="Usuario:")
    senha = forms.CharField(required=False,label="Senha:", 
                            widget=forms.PasswordInput(
                                render_value=False
                            ))
    ativo = forms.BooleanField(label="Ativo", required=False)

    def __init__(self, *args,**kwargs):
        super(CadastrarUsuarioForm, self).__init__(*args, **kwargs)
        
        self.fields['ativo'].widget.attrs = {
            'checked' : True
        }
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'nome',
            'sobrenome',
            'email',
            'usuario',
            'senha',
            'ativo',
            HTML("""<a href="{% url "visualizar_usuario" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        email = self.cleaned_data['email']
        usuario = self.cleaned_data['usuario']
        senha = self.cleaned_data['senha']
        
        
        email_exist = User.objects.filter(email=email).first()
        usuario_exist = User.objects.filter(username=usuario).first()

        if email_exist:
            self.add_error('email', "O email informado já foi utilizado em um outro usuário")
        else:
            if len(usuario) <5:
                self.add_error('usuario',"O nome de'usuário' deverá ter pelo menos 5 caracteres")
        
        if usuario_exist:
            self.add_error('usuario',"O usuário informado já foi utilizado em outro usuário")
            
        if len(senha) <=0 or len(senha)>=0:
            pass
        else:
            self.add_error('senha',"A 'senha' deverá ter pelo menos 8 caracteres")

        if usuario.upper() == senha.upper():
            self.add_error('senha',"A 'senha' não pode ser igual ao nome de usuário")
            
            
class EditarUsuarioForm(forms.Form):
    id = forms.IntegerField(required=False)
    nome = forms.CharField(label="Nome:")   
    sobrenome = forms.CharField(label="Sobrenome:")
    email = forms.EmailField(label="Email:")
    usuario = forms.CharField(label="Usuario:")
    senha = forms.CharField(required=False,label="Senha:", 
                            widget=forms.PasswordInput(
                                render_value=False
                            ))
    ativo = forms.BooleanField(label="Ativo", required=False)

    def __init__(self, *args,**kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)
        
        self.fields['ativo'].widget.attrs = {
            'checked' : True
        }
        
        self.fields['id'].widget.attrs = {
            'readonly' : True
        }
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'id',
            'nome',
            'sobrenome',
            'email',
            'usuario',
            'senha',
            'ativo',
            HTML("""<a href="{% url "visualizar_usuario" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        id = self.cleaned_data['id']
        email = self.cleaned_data['email']
        usuario = self.cleaned_data['usuario']
        senha = self.cleaned_data['senha']

        email_exist = User.objects.filter(email=email).exclude(id=id)
        usuario_exist = User.objects.filter(username=usuario).exclude(id=id)

        if email_exist:
            self.add_error('email', "O email informado já foi utilizado em um outro usuário")

        if usuario_exist:
            self.add_error('usuario',"O usuario informado já foi utilizado em outro usuario")

        if len(usuario) <5:
            self.add_error('usuario',"O nome de'usuário' deverá ter pelo menos 5 caracteres")

        if len(senha) <=0 or len(senha)>=8:
            pass
        else:
            self.add_error('senha',"A 'senha' deverá ter pelo menos 8 caracteres")

        if usuario.upper() == senha.upper():
            self.add_error('senha',"A 'senha' não pode ser igual ao nome de usuário")

class BuscarUsuarioForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarUsuarioForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Busque por Nome, Sobrenome, email, usuario ou Ativo/N.Ativo',
            'title' : 'Busque por Nome, Sobrenome, email, usuario ou Ativo(%at)/N.Ativo(%nat)'
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-group mb-2'
        self.helper.layout = Layout(
            'campo',
            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )