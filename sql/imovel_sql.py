SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS imovel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    endereco TEXT NOT NULL,
    preco REAL NOT NULL,
    area INTEGER NOT NULL,
    quartos INTEGER NOT NULL,
    banheiros INTEGER NOT NULL,
    imagem TEXT,
    pessoa_id INTEGER NOT NULL,
    cidade_id INTEGER NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoa(id),
    FOREIGN KEY (cidade_id) REFERENCES cidade(id)
);
"""

SQL_INSERIR_IMOVEL = """
INSERT INTO imovel (titulo, descricao, endereco, preco, area, quartos, banheiros, imagem, pessoa_id, cidade_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

SQL_ALTERAR_IMOVEL = """
UPDATE imovel
SET titulo = ?, descricao = ?, endereco = ?, preco = ?, area = ?, quartos = ?, banheiros = ?, imagem = ?, pessoa_id = ?, cidade_id = ?
WHERE id = ?;
"""

SQL_OBTER_TODOS_IMOVEIS = """
SELECT * FROM imovel;
"""

SQL_OBTER_UM_IMOVEL = """
SELECT imovel.*, cidade.nome AS nome_cidade, cidade.estado
FROM imovel
JOIN cidade ON imovel.cidade_id = cidade.id
WHERE imovel.id = ?;
"""

SQL_EXCLUIR_IMOVEL = """
DELETE FROM imovel WHERE id = ?;
"""
