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
        admin BOOLEAN NOT NULL,
        token TEXT)
"""

SQL_INSERIR = """
    INSERT INTO pessoa(nome, cpf, data_nascimento, endereco, telefone, email, senha, admin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, admin
    FROM pessoa
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE pessoa
    SET nome=?, cpf=?, data_nascimento=?, endereco=?, telefone=?, email=?
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
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, admin
    FROM pessoa
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, senha, admin
    FROM pessoa
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, admin
    FROM pessoa
    WHERE token=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM pessoa
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, cpf, data_nascimento, endereco, telefone, email, admin
    FROM pessoa
    WHERE nome LIKE ? OR cpf LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM pessoa
    WHERE nome LIKE ? OR cpf LIKE ?
"""

SQL_TORNAR_ADMIN = """
    UPDATE pessoa
    SET admin=1
    WHERE id=?
"""

SQL_REVOGAR_ADMIN = """
    UPDATE pessoa
    SET admin=0
    WHERE id=?
"""
