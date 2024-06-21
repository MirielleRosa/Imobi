from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Pessoa:
    id: Optional[int] = None
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    admin: Optional[bool] = True
    token: Optional[str] = None
