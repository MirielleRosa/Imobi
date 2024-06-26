import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status, File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
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



router = APIRouter()

router = APIRouter()
templates = obter_jinja_templates("templates/pessoa")

@router.get("/perfil")
def get_perfil(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("pages/perfil.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/imoveis")
def get_imoveis(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("pages/imoveis.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/cadastro_imovel")
def get_cadastro_imovel(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    cidades = CidadeRepo.obter_todos()
    return templates.TemplateResponse("pages/cadastro_imovel.html", {"request": request, "pessoa": pessoa_logada, "cidades": cidades})

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

UPLOAD_DIR = Path("static/img")

@router.post("/post_cadastro_imovel", response_class=JSONResponse)
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
        image_path = f"images/{file_name}"
        
        # Salva o arquivo temporariamente
        with open(file_name, "wb") as buffer:
            buffer.write(await imagem.read())
        
        # Faz o upload da imagem para o Firebase Storage
        firebaseconfig.storage.child(image_path).put(file_name)
        
        # Obtém a URL da imagem
        image_url = firebaseconfig.storage.child(image_path).get_url(None)
        
        # Remove o arquivo temporário
        os.remove(file_name)

        novo_imovel = Imovel(
            titulo=dados.get("titulo"),
            descricao=dados.get("descricao"),
            endereco=dados.get("endereco"),
            preco=dados.get("preco"),
            area=dados.get("area"),
            quartos=dados.get("quartos"),
            banheiros=dados.get("banheiros"),
            imagem=image_url,  # Salva a URL da imagem
            pessoa_id=pessoa_logada.id,
            cidade_id=cidade_id
        )

        print(novo_imovel)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")

    imovel_inserido = ImovelRepo.inserir(novo_imovel)
    if not imovel_inserido:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar imóvel.")

    return {"redirect": {"url": "/imoveis", "message": "Cadastro de imóvel realizado com sucesso."}}