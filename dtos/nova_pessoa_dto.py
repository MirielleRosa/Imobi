from pydantic import BaseModel, validator
from datetime import date, datetime, timedelta
from util.validators import *

class NovaPessoaDTO(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    endereco: str
    telefone: str
    email: str
    senha: str
    confirmacao_senha: str

    @validator("email")
    def validar_email(cls, v):
        msg = is_email(v, "E-mail")
        if msg:
            raise ValueError(msg)
        msg = is_email_unique(v, "E-mail")
        if msg:
            raise ValueError(msg)
        return v

    @validator("telefone")
    def validar_telefone(cls, v):
        msg = is_phone_number(v, "Telefone")
        if msg:
            raise ValueError(msg)
        msg = is_phone_unique(v, "Telefone")
        if msg:
            raise ValueError(msg)
        return v

    @validator("cpf")
    def validar_cpf(cls, v):
        msg = is_cpf(v, "CPF")
        if msg:
            raise ValueError(msg)
        msg = is_cpf_unique(v, "CPF")
        if msg:
            raise ValueError(msg)
        return v

    @validator("data_nascimento")
    def validar_data_nascimento(cls, v):
        msg = is_not_empty(v, "Data de Nascimento")
        if not msg:
            msg = is_date_valid(v, "Data de Nascimento")
        if not msg:
            data_minima = date.today() - timedelta(days=125 * 365)
            data_v = datetime.strptime(v, "%Y-%m-%d").date()
            msg = is_date_between(
                data_v, "Data de Nascimento", data_minima, date.today()
            )
        if msg:
            raise ValueError(msg)
        return v

    @validator("endereco")
    def validar_endereco(cls, v):
        msg = is_size_between(v, "Endereço", 8, 128)
        if msg:
            raise ValueError(msg)
        return v

    @validator("senha")
    def validar_senha(cls, v):
        msg = is_not_empty(v, "Senha")
        if not msg:
            msg = is_password(v, "Senha")
        if msg:
            raise ValueError(msg.strip())
        return v

    @validator("confirmacao_senha")
    def validar_confirmacao_senha(cls, v, values):
        msg = is_not_empty(v, "Confirmação de Senha")
        if "senha" in values:
            msg = is_matching_fields(
                v, "Confirmação de Senha", values["senha"], "Senha"
            )
        else:
            msg = "Senha não informada."
        if msg:
            raise ValueError(msg)
        return v
