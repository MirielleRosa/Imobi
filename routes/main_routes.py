import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ler_html import ler_html
from models.pessoa_model import Pessoa
from util.auth import obter_pessoa_logado

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/html/{arquivo}")
def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )

@router.get("/cadastro")
def get_cadastro(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logado)
):
    return templates.TemplateResponse(
        "cadastro.html",
        {
            "request": request,
            "pessoa": obter_pessoa_logado,
        },
    )

@router.get("/entrar")
def get_entrar(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logado)
):
    return templates.TemplateResponse(
        "entrar.html",
        {
            "request": request,
            "pessoa": obter_pessoa_logado,
        },
    )