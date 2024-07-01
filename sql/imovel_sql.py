SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS imovel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    endereco TEXT NOT NULL,
    preco REAL NOT NULL,
    area INTEGER NOT NULL,
    quartos INTEGER NOT NULL,
    banheiros INTEGER NOT NULL,
    garagem INTEGER NOT NULL,
    piscina BOOLEAN NOT NULL,
    ar_condicionado BOOLEAN NOT NULL,
    churrasqueira BOOLEAN NOT NULL,
    jardim BOOLEAN NOT NULL,
    portaria BOOLEAN NOT NULL,
    academia BOOLEAN NOT NULL,
    imagem_principal TEXT,
    imagens_secundarias TEXT,
    pessoa_id INTEGER NOT NULL,
    cidade_id INTEGER NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoa(id),
    FOREIGN KEY (cidade_id) REFERENCES cidade(id)
);
"""

SQL_INSERIR_IMOVEL = """
INSERT INTO imovel (
    titulo, tipo, descricao, endereco, preco, area, quartos, banheiros, garagem, piscina, 
    ar_condicionado, churrasqueira, jardim, portaria, academia, 
    imagem_principal, imagens_secundarias, pessoa_id, cidade_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

SQL_ALTERAR_IMOVEL = """
UPDATE imovel
SET titulo = ?, tipo = ?, descricao = ?, endereco = ?, preco = ?, area = ?, quartos = ?, banheiros = ?, garagem = ?, piscina = ?, 
    ar_condicionado = ?, churrasqueira = ?, jardim = ?, portaria = ?, academia = ?, 
    imagem_principal = ?, imagens_secundarias = ?, pessoa_id = ?, cidade_id = ?
WHERE id = ?;
"""



SQL_OBTER_TODOS_IMOVEIS = """
SELECT imovel.*, cidade.nome AS nome_cidade, cidade.estado, pessoa.nome AS nome_corretor, pessoa.imagem_perfil AS imagem_corretor
FROM imovel
JOIN cidade ON imovel.cidade_id = cidade.id
JOIN pessoa ON imovel.pessoa_id = pessoa.id;
"""

SQL_OBTER_TODOS_IMOVEIS_DO_CORRETOR = """
SELECT * FROM imovel WHERE pessoa_id = ?;
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM imovel
"""


SQL_OBTER_UM_IMOVEL = """
SELECT imovel.*, cidade.nome AS nome_cidade, cidade.estado, pessoa.nome AS nome_corretor, pessoa.imagem_perfil AS imagem_corretor, 
pessoa.email AS email_corretor, pessoa.telefone AS telefone_corretor, pessoa.descricao AS descricao_corretor
FROM imovel
JOIN cidade ON imovel.cidade_id = cidade.id
JOIN pessoa ON imovel.pessoa_id = pessoa.id
WHERE imovel.id = ?;
"""

SQL_EXCLUIR_IMOVEL = """
DELETE FROM imovel WHERE id = ?;
"""

SQL_OBTER_BUSCA = """
SELECT imovel.id, imovel.titulo, imovel.tipo, imovel.descricao, imovel.endereco,
       imovel.preco, imovel.area, imovel.quartos, imovel.banheiros, imovel.garagem,
       imovel.piscina, imovel.ar_condicionado, imovel.churrasqueira, imovel.jardim,
       imovel.portaria, imovel.academia, imovel.imagem_principal, imovel.imagens_secundarias,
       imovel.pessoa_id, imovel.cidade_id,
       cidade.nome AS cidade_nome, cidade.estado,
       pessoa.nome AS nome_corretor, pessoa.imagem_perfil AS imagem_corretor
FROM imovel
JOIN cidade ON imovel.cidade_id = cidade.id
LEFT JOIN pessoa ON imovel.pessoa_id = pessoa.id
WHERE cidade.nome LIKE ?;
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
SELECT COUNT(*) 
FROM imovel
JOIN cidade ON imovel.cidade_id = cidade.id
WHERE cidade.nome LIKE ?;
"""