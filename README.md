## Projeto Corretora de Imóveis

## Descrição do Projeto

O Projeto Corretora de Imóveis é uma aplicação web desenvolvida para resolver problemas relacionados à autenticação de usuário e gerenciamento de entidades com relacionamento de 1 para N (um para muitos). A aplicação visa facilitar o gerenciamento de imóveis por corretores, permitindo que cada corretor cadastre e gerencie seus próprios imóveis. Além disso, a aplicação fornece uma vitrine de imóveis para todos os corretores cadastrados.

## Funcionalidades Principais

1. **Autenticação de Usuário**
   - Cadastro de corretores (administradores).
   - Login de corretores para acessar o sistema.

2. **Cadastro de Entidades**
   - Cadastro de cidades.
   - Cadastro de imóveis vinculados a corretores.
   - Possibilidade de corretores cadastrarem novas cidades ao cadastrar um imóvel.

3. **Gerenciamento de Imóveis**
   - Cada corretor pode cadastrar múltiplos imóveis.
   - Cada corretor pode visualizar, editar e excluir apenas seus próprios imóveis.
   - A tela principal exibe todos os imóveis cadastrados por todos os corretores.

## Relacionamentos Entre Entidades

- **Corretores e Imóveis**: Relacionamento de 1 para N.
  - Cada corretor pode cadastrar vários imóveis.
  - Cada imóvel pertence a um único corretor.

## Detalhamento das Funcionalidades

### Cadastro de Corretores

- **Campos**:
  - Nome
  - Email
  - Senha
- **Funcionalidades**:
  - Formulário de registro.
  - Login com autenticação.

### Cadastro de Cidades

- **Campos**:
  - Nome da cidade
- **Funcionalidades**:
  - Formulário para adicionar novas cidades.
  - Listagem de cidades cadastradas.

### Cadastro de Imóveis

- **Campos**:
  - Título do imóvel
  - Descrição
  - Preço
  - Localização (cidade)
  - Corretor responsável
- **Funcionalidades**:
  - Formulário para adicionar novos imóveis.
  - Listagem de imóveis cadastrados pelo corretor logado.
  - Edição e exclusão de imóveis.
  - Possibilidade de adicionar nova cidade caso a cidade desejada não esteja cadastrada.

### Vitrine de Imóveis

- **Funcionalidades**:
  - Exibição de todos os imóveis cadastrados por todos os corretores.
  - Filtro por cidade, preço, etc.