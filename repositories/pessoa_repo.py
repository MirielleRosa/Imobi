import json
import sqlite3
from typing import List, Optional
from models.pessoa_model import Pessoa
from sql.pessoa_sql import *
from util.database import obter_conexao

class PessoaRepo:
    
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, pessoa: Pessoa) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        pessoa.nome,
                        pessoa.cpf,
                        pessoa.data_nascimento,
                        pessoa.endereco,
                        pessoa.telefone,
                        pessoa.email,
                        pessoa.senha,
                        pessoa.admin,
                    ),
                )
                if cursor.rowcount > 0:
                    pessoa.id = cursor.lastrowid
                    return pessoa
        except sqlite3.Error as ex:
            print(ex)
            return None