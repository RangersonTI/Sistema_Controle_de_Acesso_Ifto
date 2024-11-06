from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.forms import VincularPessoaRfid
from gerenciar_controle_ifto.models import Rfid, Pessoa
from django.http import HttpResponseRedirect

def vincularRfid(request, id):

    pessoa = get_object_or_404(Pessoa, id=id)

    if request.POST:
        form = VincularPessoaRfid(request.POST)

        if form.is_valid():
            print("Passou por validar")
            cod_rfid = form.cleaned_data['rfid_a_vincular']
            pessoa.cod_Rfid = cod_rfid
            pessoa.save()
            print("Pronto :)...  Salvou")
            
            print(type(f"Tipo de erro: {cod_rfid}"))

            rfid = get_object_or_404(Rfid,id=cod_rfid)
            rfid.vinculado = True
            rfid.save()
            print("Vai redirecionar\n")
            HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Vinculação de RFID',
            'nome_usuario_logado' : 'Rangerson'
        }
        return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

    print(request.method)
    print("Bora ve se retorn get novamente")
    form = VincularPessoaRfid(
        initial = {
            'pessoa' : ''+pessoa.nome+' '+pessoa.sobrenome+' '+'('+str(pessoa.id)+')'
        },
        codCargoID = pessoa.cod_Papel_pessoa.id
    )
    context = {
        'form' : form,
        'title' : 'Vinculação de RFID',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

def desvincularRfid(request, id):
    
    pessoa = get_object_or_404(Pessoa, id=id)
    
    if request.method == 'POST':
        form = VincularPessoaRfid(request.POST)
        
        if form.is_valid():
            cod_rfid = form.cleaned_data['rfid_a_vincular']
            pessoa.cod_Rfid = cod_rfid
            pessoa.save()
            
            rfid = get_object_or_404(Rfid,id=cod_rfid)
            rfid.vinculado = True
            rfid.save()

            HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Vinculação de RFID',
            'nome_usuario_logado' : 'Rangerson'
        }

    form = VincularPessoaRfid(
        initial = {
            'pessoa' : ''+pessoa.nome+' '+pessoa.sobrenome+' '+'('+str(pessoa.id)+')'
        },
        codCargoID = pessoa.cod_Papel_pessoa.id
    )
    context = {
        'form' : form,
        'title' : 'Vinculação de RFID',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)