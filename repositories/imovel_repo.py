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
                        imovel.tipo,
                        imovel.descricao,
                        imovel.endereco,
                        imovel.preco,
                        imovel.area,
                        imovel.quartos,
                        imovel.banheiros,
                        imovel.garagem,
                        imovel.piscina,
                        imovel.imagem_principal,
                        imovel.imagens_secundarias,
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
                        imovel.tipo,
                        imovel.descricao,
                        imovel.endereco,
                        imovel.preco,
                        imovel.area,
                        imovel.quartos,
                        imovel.banheiros,
                        imovel.garagem,
                        imovel.piscina,
                        imovel.imagem_principal,
                        imovel.imagens_secundarias,
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
                    print("Nenhum imóvel encontrado.")
                    return 0  # Return 0 if no results found
        except sqlite3.Error as ex:
            print(f"Erro ao obter quantidade de imóveis: {ex}")
            return None

    @classmethod
    def obter_busca(cls, cidade_nome: str, pagina: int, tamanho_pagina: int, ordem: int) -> List[Imovel]:
        cidade_nome = "%" + cidade_nome + "%"
        offset = (pagina - 1) * tamanho_pagina
        
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                print(f"Query de busca: {SQL_OBTER_BUSCA}")  # Verifique a query sendo executada
                print(f"Parâmetros: {cidade_nome}")  # Verifique os parâmetros sendo passados
                cursor.execute(SQL_OBTER_BUSCA, (cidade_nome,))
                tuplas = cursor.fetchall()
                imoveis = [Imovel(*t) for t in tuplas]
                print(f"Resultado da busca: {imoveis}")  # Log para verificar os resultados (opcional)
                return imoveis
        except sqlite3.Error as ex:
            print(f"Erro ao buscar imóveis: {ex}")
            return []

    @classmethod
    def obter_quantidade_busca(cls, cidade_nome: str) -> Optional[int]:
        cidade_nome = "%" + cidade_nome + "%"
        
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                print(f"Query de quantidade: {SQL_OBTER_QUANTIDADE_BUSCA}")  # Verifique a query sendo executada
                print(f"Parâmetros: {cidade_nome}")  # Verifique os parâmetros sendo passados
                cursor.execute(SQL_OBTER_QUANTIDADE_BUSCA, (cidade_nome,))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"Quantidade de imóveis encontrados: {resultado[0]}")  # Adicione um log para verificar a contagem
                    return resultado[0]
                else:
                    print("Nenhum imóvel encontrado.")
                    return 0  # Return 0 if no results found
        except sqlite3.Error as ex:
            print(f"Erro ao obter quantidade de imóveis: {ex}")
            return None
