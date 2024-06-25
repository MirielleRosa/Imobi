SQL_CRIAR_TABELA_CIDADE = """
CREATE TABLE IF NOT EXISTS cidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    estado TEXT NOT NULL
);
"""

SQL_INSERIR_CIDADE = """
INSERT INTO cidade (nome, estado)
VALUES (?, ?);
"""

SQL_OBTER_TODAS_CIDADES = """
SELECT * FROM cidade;
"""

SQL_ALTERAR_CIDADE = """
UPDATE cidade
SET nome = ?, estado = ?
WHERE id = ?;
"""

SQL_EXCLUIR_CIDADE = """
DELETE FROM cidade WHERE id = ?;
"""

SQL_OBTER_UMA_CIDADE = """
SELECT * FROM cidade WHERE id = ?;
"""

SQL_OBTER_CIDADES_POR_ESTADO = """
SELECT * FROM cidade WHERE estado = ?;
"""
SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM cidade
"""