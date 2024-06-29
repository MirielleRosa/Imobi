from ast import parse
from datetime import date, datetime
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.cidade_model import Cidade
from models.imovel_model import Imovel
from models.pessoa_model import Pessoa
from repositories.cidade_repo import CidadeRepo
from repositories.imovel_repo import ImovelRepo
from repositories.pessoa_repo import PessoaRepo
from util.auth import checar_autorizacao, obter_pessoa_logada
from util.cookies import adicionar_mensagem_sucesso
import uuid
import util.firebaseconfig as firebaseconfig
from util.templates import obter_jinja_templates
from pathlib import Path

UPLOAD_DIR = Path("static/img")
router = APIRouter()
templates = obter_jinja_templates("templates/pessoa")

@router.get("/perfil")
def get_perfil(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("pages/perfil.html", {"request": request, "pessoa": pessoa_logada})


@router.post("/alterar_perfil")
async def post_alterar_perfil(
    request: Request,
    imagem: UploadFile = File(None),
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)

    form_data = await request.form()
    dados = {key: form_data[key] for key in form_data}

    try:
        # Verifique se uma nova imagem foi recebida
        if imagem and imagem.filename:
            file_name = f"{uuid.uuid4()}.png"
            image_path = f"imagens_perfil/{file_name}"

            with open(file_name, "wb") as buffer:
                buffer.write(await imagem.read())

            firebaseconfig.storage.child(image_path).put(file_name)

            image_url = firebaseconfig.storage.child(image_path).get_url(None)

            os.remove(file_name)
        else:
            image_url = pessoa_logada.imagem_perfil  # Mantém a URL da imagem existente

        data_nascimento_str = dados.get("data_nascimento")
        if data_nascimento_str:
            try:
                # Convertendo a string data_nascimento_str para um objeto date
                data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Erro ao converter data de nascimento: {str(e)}")

            # Atualizando os dados do perfil
            alterar_perfil = Pessoa(
                id=pessoa_logada.id,
                nome=dados.get("nome"),
                cpf=dados.get("cpf"),
                data_nascimento=data_nascimento,
                endereco=dados.get("endereco"),
                telefone=dados.get("telefone"),
                email=dados.get("email"),
                senha=pessoa_logada.senha,  # Manter a senha atual
                imagem_perfil=image_url,  # Usar a URL da nova imagem ou a existente
                descricao=dados.get("descricao")
            )

            print(alterar_perfil)

            # Atualizar os dados do perfil no banco de dados
            PessoaRepo.alterar(alterar_perfil)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")

    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/imoveis")
def get_imoveis(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    imoveis = ImovelRepo.obter_todos() 
    return templates.TemplateResponse("pages/imoveis.html", {"request": request, "pessoa": pessoa_logada, "imoveis": imoveis})


@router.get("/cadastro_imovel")
def get_cadastro_imovel(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    cidades = CidadeRepo.obter_todos()
    return templates.TemplateResponse("pages/cadastro_imovel.html", {"request": request, "pessoa": pessoa_logada, "cidades": cidades})

@router.post("/post_cadastro_cidade", response_class=JSONResponse)
async def post_cadastro_cidade(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    
    form_data = await request.form()
    nome = form_data.get("nome")
    estado = form_data.get("estado")
    
    nova_cidade = Cidade(nome=nome, estado=estado)  

    try:
        cidade_inserida = CidadeRepo.inserir(nova_cidade)
        if cidade_inserida:
            return RedirectResponse(url="/cadastro_imovel", status_code=status.HTTP_303_SEE_OTHER)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao cadastrar a cidade!")
    except Exception as e:
        print(f"Erro ao inserir cidade no banco de dados: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao cadastrar cidade")


@router.post("/post_cadastro_imovel")
async def post_cadastro_imovel(
    request: Request,
    imagem: UploadFile = File(...),
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)
    
    form_data = await request.form()
    dados = {key: form_data[key] for key in form_data}
    
    try:
        cidade_id = dados.get("cidade_id")
        if not cidade_id:
            raise HTTPException(status_code=400, detail="Cidade não selecionada ou inválida.")
        
        file_name = f"{uuid.uuid4()}.png"
        image_path = f"imagens_imoveis/{file_name}"
        
        with open(file_name, "wb") as buffer:
            buffer.write(await imagem.read())
        
        firebaseconfig.storage.child(image_path).put(file_name)
        
        image_url = firebaseconfig.storage.child(image_path).get_url(None)
        
        os.remove(file_name)

        novo_imovel = Imovel(
            titulo=dados.get("titulo"),
            descricao=dados.get("descricao"),
            endereco=dados.get("endereco"),
            preco=dados.get("preco"),
            area=dados.get("area"),
            quartos=dados.get("quartos"),
            banheiros=dados.get("banheiros"),
            imagem=image_url, 
            pessoa_id=pessoa_logada.id,
            cidade_id=cidade_id
        )

        imovel_inserido = ImovelRepo.inserir(novo_imovel)
        if not imovel_inserido:
            raise HTTPException(status_code=400, detail="Erro ao cadastrar imóvel.")

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")

    return RedirectResponse(url="/imoveis", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/sair", response_class=RedirectResponse)
async def get_sair(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)
    if pessoa_logada:
        PessoaRepo.alterar_token(pessoa_logada.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="auth_token", value=" ", httponly=True, expires=0)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso.")
    return response
