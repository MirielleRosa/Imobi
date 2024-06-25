import sqlite3
from typing import List, Optional
from models.imovel_model import Imovel
from sql.imovel_sql import *
from util.database import obter_conexao

class ImovelRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, imovel: Imovel) -> Optional[Imovel]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR_IMOVEL,
                    (
                        imovel.titulo,
                        imovel.descricao,
                        imovel.endereco,
                        imovel.preco,
                        imovel.area,
                        imovel.quartos,
                        imovel.banheiros,
                        imovel.imagem,
                        imovel.pessoa_id,
                        imovel.cidade_id,
                    ),
                )
                if cursor.rowcount > 0:
                    imovel.id = cursor.lastrowid
                    return imovel
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Imovel]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_IMOVEIS).fetchall()
                imoveis = [Imovel(*t) for t in tuplas]
                return imoveis
        except sqlite3.Error as ex:
            print(ex)
            return []

    @classmethod
    def alterar(cls, imovel: Imovel) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_IMOVEL,
                    (
                        imovel.titulo,
                        imovel.descricao,
                        imovel.endereco,
                        imovel.preco,
                        imovel.area,
                        imovel.quartos,
                        imovel.banheiros,
                        imovel.imagem,
                        imovel.pessoa_id,
                        imovel.cidade_id,
                        imovel.id,
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
                cursor.execute(SQL_EXCLUIR_IMOVEL, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Imovel]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM_IMOVEL, (id,)).fetchone()
                if tupla:
                    imovel = Imovel(*tupla)
                    return imovel
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
