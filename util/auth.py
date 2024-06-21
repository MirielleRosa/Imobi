import secrets
from typing import Optional
import bcrypt
from fastapi import HTTPException, Request, status
from models.pessoa_model import Pessoa
from repositories.pessoa_repo import PessoaRepo


async def obter_pessoa_logado(request: Request) -> Optional[Pessoa]:
    try:
        token = request.cookies["auth_token"]
        if token.strip() == "":
            return None
        pessoa = PessoaRepo.obter_por_token(token)
        return pessoa
    except KeyError:
        return None