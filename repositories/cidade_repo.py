import json
import sqlite3
from typing import List, Optional
from models.cidade_model import Cidade 
from sql.cidade_sql import *
from util.database import obter_conexao

class CidadeRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_CIDADE)

    @classmethod
    def inserir(cls, cidade: Cidade) -> Optional[Cidade]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR_CIDADE,
                    (cidade.nome, cidade.estado),
                )
                if cursor.rowcount > 0:
                    cidade.id = cursor.lastrowid
                    return cidade
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
    def inserir_cidades_json(cls, arquivo_json: str):
        if CidadeRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                cidades = json.load(arquivo)
                for cidade in cidades:
                    CidadeRepo.inserir(Cidade(**cidade))

    @classmethod
    def obter_todos(cls) -> List[Cidade]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODAS_CIDADES).fetchall()
                cidades = [Cidade(*t) for t in tuplas]
                return cidades
        except sqlite3.Error as ex:
            print(ex)
            return []

    @classmethod
    def alterar(cls, cidade: Cidade) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_CIDADE,
                    (cidade.nome, cidade.estado, cidade.id),
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
                cursor.execute(SQL_EXCLUIR_CIDADE, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Cidade]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UMA_CIDADE, (id,)).fetchone()
                if tupla:
                    cidade = Cidade(*tupla)
                    return cidade
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_estado(cls, estado: str) -> List[Cidade]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_CIDADES_POR_ESTADO, (estado,)).fetchall()
                cidades = [Cidade(*t) for t in tuplas]
                return cidades
        except sqlite3.Error as ex:
            print(ex)
            return []
