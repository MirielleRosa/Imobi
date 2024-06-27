SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS pessoa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        data_nascimento DATE NOT NULL,
        endereco TEXT NOT NULL,
        telefone TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        imagem_perfil TEXT,
        descricao TEXT,
        token TEXT
    );
"""

SQL_INSERIR = """
    INSERT INTO pessoa(nome, cpf, data_nascimento, endereco, telefone, email, senha, imagem_perfil, descricao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, imagem_perfil, descricao
    FROM pessoa
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE pessoa
    SET nome=?, cpf=?, data_nascimento=?, endereco=?, telefone=?, email=?, imagem_perfil=?, descricao=?
    WHERE id=?
"""

SQL_ALTERAR_TOKEN = """
    UPDATE pessoa
    SET token=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM pessoa    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, imagem_perfil, descricao
    FROM pessoa
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, senha, imagem_perfil, descricao
    FROM pessoa
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, senha, imagem_perfil, descricao
    FROM pessoa
    WHERE token=?
"""

SQL_OBTER_POR_TELEFONE = """
    SELECT * FROM pessoa
    WHERE telefone = ?
"""

SQL_OBTER_POR_CPF = """
    SELECT * FROM pessoa
    WHERE cpf = ?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM pessoa
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, imagem_perfil, descricao
    FROM pessoa
    WHERE nome LIKE ? OR cpf LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM pessoa
    WHERE nome LIKE ? OR cpf LIKE ?
"""