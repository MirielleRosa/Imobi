import secrets
from typing import Optional
import bcrypt
from fastapi import HTTPException, Request, status
from models.pessoa_model import Pessoa
from repositories.pessoa_repo import PessoaRepo

async def obter_pessoa_logada(request: Request) -> Optional[Pessoa]:
    try:
        token = request.cookies["auth_token"]
        if token.strip() == "":
            return None
        pessoa = PessoaRepo.obter_por_token(token)
        return pessoa
    except KeyError:
        return None
    
async def atualizar_cookie_autenticacao(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == status.HTTP_303_SEE_OTHER:
        return response
    pessoa = await obter_pessoa_logada(request)
    if pessoa:
        token = request.cookies["auth_token"]
        response.set_cookie(
            key="auth_token",
            value=token,
            max_age=1800,
            httponly=True,
            samesite="lax",
        )
    return response
    
async def detectar_cookie_autenticacao(request: Request, call_next):
    pessoa = await obter_pessoa_logada(request)
    request.pessoa = pessoa
    response = await call_next(request)
    return response

def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""

def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False


def gerar_token(length: int = 32) -> str:
    try:
        return secrets.token_hex(length)
    except ValueError:
        return ""


def checar_autorizacao(pessoa_logada: Pessoa):
    if not pessoa_logada:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
