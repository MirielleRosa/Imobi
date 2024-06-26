from datetime import datetime
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from dtos.entrar_dto import EntrarDTO
from dtos.nova_pessoa_dto import NovaPessoaDTO
from util.ler_html import ler_html
from models.pessoa_model import Pessoa
from repositories.pessoa_repo import PessoaRepo
from util.auth import conferir_senha, gerar_token, obter_hash_senha, obter_pessoa_logada
from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response



@router.get("/")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    # imoveis = ImoveisRepo.obter_todos()
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
            # "imoveis": imoveis,
        },
    )

@router.get("/cadastro")
def get_cadastro(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
        },
    )

@router.get("/entrar")
def get_entrar(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    return templates.TemplateResponse(
        "pages/entrar.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
        },
    )

@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmacao_senha: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(...),
    endereco: str = Form(...),
    data_nascimento: str = Form(...)
):
    if senha != confirmacao_senha:
        return JSONResponse(
            content=create_validation_errors(
                {"senha": senha, "confirmacao_senha": confirmacao_senha},
                ["senha", "confirmacao_senha"],
                ["As senhas não coincidem.", "As senhas não coincidem."]
            ),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Data de nascimento inválida. Use o formato AAAA-MM-DD.")

    pessoa_data = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "telefone": telefone,
        "email": email,
        "senha": obter_hash_senha(senha),
    }

    # Verificar se o email já existe
    if PessoaRepo.obter_por_email(email):
        raise HTTPException(status_code=400, detail="Email já está em uso.")
    
    # Verificar se o telefone já existe
    if PessoaRepo.obter_por_telefone(telefone):
        raise HTTPException(status_code=400, detail="Telefone já está em uso.")
    
    # Verificar se o CPF já existe
    if PessoaRepo.obter_por_cpf(cpf):
        raise HTTPException(status_code=400, detail="CPF já está em uso.")
    
    # Inserir a nova pessoa
    nova_pessoa = PessoaRepo.inserir(Pessoa(**pessoa_data))
    if not nova_pessoa or not nova_pessoa.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar corretor.")
    
    return {"redirect": {"url": "/cadastro_realizado"}}



@router.get("/cadastro_realizado")
def get_cadastro_realizado(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    return templates.TemplateResponse(
        "pages/cadastro_confirmado.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
        },
    )

@router.get("/entrar")
def get_entrar(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    return templates.TemplateResponse(
        "entrar.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
        },
    )

@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(
    email: str = Form(...),
    senha: str = Form(...),
    return_url: str = Query("/perfil")
):
    pessoa_entrou = PessoaRepo.obter_por_email(email)
    if (
        (not pessoa_entrou)
        or (not pessoa_entrou.senha)
        or (not conferir_senha(senha, pessoa_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                {"email": email, "senha": senha},
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    token = gerar_token()
    if not PessoaRepo.alterar_token(pessoa_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do corretor no banco de dados."
        )
    
    response = JSONResponse(content={"redirect": {"url": return_url}})
    adicionar_mensagem_sucesso(response, "Entrada efetuada com sucesso.")
    adicionar_cookie_auth(response, token)
    return response

