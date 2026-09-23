# API REST Segura para Gestão de Usuários

Projeto acadêmico desenvolvido em Python com FastAPI para gerenciamento de usuários.

A aplicação possui:

- CRUD de usuários;
- Login com JWT;
- Senhas protegidas com bcrypt;
- Controle de acesso por perfil;
- Perfis `admin`, `operador` e `cliente`;
- Banco de dados SQLite;
- Interface web simples em HTML, CSS e JavaScript;
- Documentação automática pelo Swagger.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT
- bcrypt
- HTML
- CSS
- JavaScript

## Como executar

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd api-usuarios
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows, ative com:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`.

Exemplo:

```env
SECRET_KEY=sua-chave-secreta
ADMIN_EMAIL=admin@exemplo.com
ADMIN_PASSWORD=Admin123!
ADMIN_NAME=Administrador
```

Para gerar uma chave segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Depois execute:

```bash
uvicorn app.main:app --reload
```

A interface estará disponível em:

```text
http://127.0.0.1:8000
```

A documentação Swagger estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Perfis de acesso

- **Administrador:** acesso total ao sistema.
- **Operador:** pode consultar e atualizar usuários.
- **Cliente:** pode visualizar e editar apenas os próprios dados.

## Autenticação

Após o login, a API gera um token JWT com validade de 30 minutos.

Os endpoints protegidos utilizam:

```http
Authorization: Bearer TOKEN
```

## Observação

O projeto foi desenvolvido para fins acadêmicos e execução local.