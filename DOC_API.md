\# Documentação da API



\## Endpoints



| Método | Endpoint | Finalidade | Resposta esperada |

|---|---|---|---|

| POST | `/auth/login` | Autenticar usuário e gerar JWT | 200 OK |

| POST | `/usuarios` | Criar usuário | 201 Created |

| GET | `/usuarios` | Listar usuários | 200 OK |

| GET | `/usuarios/me` | Consultar dados do usuário autenticado | 200 OK |

| GET | `/usuarios/{id}` | Consultar usuário específico | 200 OK |

| PUT | `/usuarios/{id}` | Atualizar usuário | 200 OK |

| DELETE | `/usuarios/{id}` | Excluir usuário | 204 No Content |



Também podem ser retornados:



\- `401 Unauthorized`: credenciais ou token inválido;

\- `403 Forbidden`: usuário sem permissão;

\- `404 Not Found`: usuário não encontrado;

\- `409 Conflict`: e-mail já cadastrado;

\- `422 Unprocessable Entity`: dados inválidos.



\## Perfis de acesso



\### Administrador

Possui acesso total:

\- Criar usuários;

\- Consultar usuários;

\- Atualizar usuários;

\- Alterar perfis;

\- Excluir usuários.



\### Operador

Possui acesso intermediário:

\- Consultar usuários;

\- Atualizar nome e e-mail.



Não pode:

\- Criar usuários;

\- Excluir usuários;

\- Alterar perfis.



\### Cliente

Possui acesso restrito:

\- Consultar apenas os próprios dados;

\- Atualizar o próprio nome e e-mail.



Não pode:

\- Listar todos os usuários;

\- Consultar outros usuários;

\- Alterar perfil;

\- Excluir usuários.



\## JWT



O login é realizado pelo endpoint:



`POST /auth/login`



O usuário envia e-mail e senha.



Quando as credenciais são válidas, a API gera um token JWT.



O token contém:

\- ID do usuário;

\- Nome;

\- Perfil;

\- Data de emissão;

\- Data de expiração.



O token possui validade de 30 minutos.



Os endpoints protegidos recebem o token pelo cabeçalho:



`Authorization: Bearer TOKEN`



A expiração curta reduz o período em que um token roubado poderia ser utilizado.



\## OAuth 2.0



OAuth 2.0 poderia ser utilizado por aplicações parceiras para acessar a API em nome do usuário.



O fluxo seria:



1\. A aplicação parceira solicita acesso.

2\. O usuário realiza autenticação e autoriza as permissões solicitadas.

3\. A aplicação recebe um token de acesso.

4\. O token é enviado para a API em cada requisição protegida.

5\. A API valida o token e as permissões antes de liberar o recurso.



O token seria utilizado da seguinte forma:



`Authorization: Bearer ACCESS\_TOKEN`



Principais benefícios:



\- Não é necessário compartilhar a senha do usuário com aplicações parceiras;

\- Permite delegar apenas determinadas permissões;

\- Tokens podem ter validade limitada;

\- O acesso pode ser revogado;

\- Melhora a segurança de integrações externas.



OAuth 2.0 não foi implementado no projeto, conforme permitido pelo enunciado.



\## Análise de segurança



| Risco | Mitigação |

|---|---|

| Roubo de token JWT | HTTPS em produção e expiração curta |

| Senha armazenada em texto puro | Hash utilizando bcrypt |

| Acesso indevido a endpoints | Controle de acesso RBAC |

| Vazamento da chave JWT | Armazenamento em variável de ambiente |

| Alteração do token | Assinatura JWT |

| SQL Injection | Uso do SQLAlchemy |

| Exposição de senha na API | Senha não é retornada nas respostas |

| E-mail duplicado | Verificação antes do cadastro e atualização |



\## Considerações de segurança



As senhas são armazenadas utilizando bcrypt.



A chave utilizada para assinar os tokens JWT fica armazenada no arquivo `.env`, que não é enviado ao GitHub.



Durante o desenvolvimento a aplicação utiliza HTTP localmente. Em produção, deve ser utilizado HTTPS para proteger credenciais e tokens durante a transmissão.

