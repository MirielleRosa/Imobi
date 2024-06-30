from datetime import datetime
import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jsonschema import ValidationError

from dtos.entrar_dto import EntrarDTO
from dtos.nova_pessoa_dto import NovaPessoaDTO
from repositories.imovel_repo import ImovelRepo
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
    imoveis = ImovelRepo.obter_todos()
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
            "imoveis": imoveis,
        },
    )

@router.get("/imovel/{id:int}")
async def get_imovel(request: Request, id: int, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    imovel = ImovelRepo.obter_um(id)
    return templates.TemplateResponse(
        "pages/imovel.html",
        {
            "request": request, 
            "pessoa": pessoa_logada,
            "imovel": imovel,
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

@router.get("/sobre")
def get_cadastro(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    return templates.TemplateResponse(
        "pages/sobre.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
        },
    )

@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(pessoa: NovaPessoaDTO):
    pessoa_data = pessoa.model_dump(exclude={"confirmacao_senha"})
    pessoa_data["senha"] = obter_hash_senha(pessoa_data["senha"])

    # Verificar se o email já existe
    if PessoaRepo.obter_por_email(pessoa_data["email"]):
        raise HTTPException(status_code=400, detail="Email já está em uso.")
    
    # Verificar se o telefone já existe
    if PessoaRepo.obter_por_telefone(pessoa_data["telefone"]):
        raise HTTPException(status_code=400, detail="Telefone já está em uso.")
    
    # Verificar se o CPF já existe
    if PessoaRepo.obter_por_cpf(pessoa_data["cpf"]):
        raise HTTPException(status_code=400, detail="CPF já está em uso.")
    
    # Inserir a nova pessoa
    nova_pessoa = PessoaRepo.inserir(Pessoa(**pessoa_data))
    if not nova_pessoa or not nova_pessoa.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar corretor.")
    
    return {"redirect": {"url": "cadastro_realizado"}}

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

@router.get("/buscar")
async def get_buscar(
    request: Request,
    q: str,  # Certifique-se de que este parâmetro está sendo passado na URL
    p: int = 1,
    tp: int = 6,
    o: int = 1,
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    imoveis = ImovelRepo.obter_busca(q, p, tp, o)
    qtde_imoveis = ImovelRepo.obter_quantidade_busca(q)
    qtde_paginas = math.ceil(qtde_imoveis / float(tp))

    return templates.TemplateResponse(
        "pages/buscar.html",
        {
            "request": request,
            "pessoa": pessoa_logada,
            "imoveis": imoveis,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "ordem": o,
        },
    )


@router.get("/entrar", response_class=HTMLResponse)
def get_entrar(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    if pessoa_logada:
        return RedirectResponse("/perfil", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            "pages/entrar.html",
            {
                "request": request,
                "pessoa": pessoa_logada,
            },
        )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO, return_url: str = Query("/perfil")):
    pessoa_entrou = PessoaRepo.obter_por_email(entrar_dto.email)
    if (
        (not pessoa_entrou)
        or (not pessoa_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, pessoa_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
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