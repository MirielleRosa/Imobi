from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.pessoa_model import Pessoa
from repositories.pessoa_repo import PessoaRepo
from util.auth import checar_autorizacao, obter_pessoa_logada
from util.cookies import adicionar_mensagem_sucesso


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/perfil")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("perfil.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/imoveis")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("imoveis.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/cadastro_imovel")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("cadastro_imovel.html", {"request": request, "pessoa": pessoa_logada})

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
