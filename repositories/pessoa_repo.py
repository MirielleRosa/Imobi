import json
import sqlite3
from typing import List, Optional
from models.pessoa_model import Pessoa
from sql.pessoa_sql import *
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

    @classmethod
    def obter_todos(cls) -> List[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                pessoas = [pessoas(*t) for t in tuplas]
                return pessoas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, pessoa: Pessoa) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        pessoa.nome,
                        pessoa.cpf,
                        pessoa.data_nascimento,
                        pessoa.endereco,
                        pessoa.email,
                        pessoa.telefone,
                        pessoa.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                pessoa = Pessoa(*tupla)
                return pessoa
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_pessoa_json(cls, arquivo_json: str):
        if PessoaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                pessoas = json.load(arquivo)
                for pessoa in pessoas:
                    PessoaRepo.inserir(Pessoa(**pessoa))

    @classmethod
    def obter_busca(cls, termo: str, pagina: int, tamanho_pagina: int) -> List[Pessoa]:
        termo = "%" + termo + "%"
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(
                    SQL_OBTER_BUSCA, (termo, termo, tamanho_pagina, offset)
                ).fetchall()
                pessoas = [pessoas(*t) for t in tuplas]
                return pessoas
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_busca(cls, termo: str) -> Optional[int]:
        termo = "%" + termo + "%"
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_QUANTIDADE_BUSCA, (termo, termo)
                ).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def tornar_admin(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_TORNAR_ADMIN, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def revogar_admin(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_REVOGAR_ADMIN, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                if tupla:
                    pessoa = Pessoa(*tupla)
                    return pessoa
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar_token(cls, id: int, token: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_TOKEN, (token, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                if tupla:
                    pessoa = Pessoa(*tupla)
                    return pessoa
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_por_telefone(cls, telefone: str) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_TELEFONE, (telefone,)).fetchone()
                if tupla:
                    pessoa = Pessoa(*tupla)
                    return pessoa
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_por_cpf(cls, cpf: str) -> Optional[Pessoa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_CPF, (cpf,)).fetchone()
                if tupla:
                    pessoa = Pessoa(*tupla)
                    return pessoa
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None