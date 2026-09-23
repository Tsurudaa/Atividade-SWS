from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, Usuario
from .schemas import (
    UsuarioCriar,
    UsuarioResposta,
    UsuarioAtualizar,
    LoginRequest,
    TokenResposta
)

from .auth import (
    gerar_hash_senha,
    verificar_senha,
    criar_token_jwt
)

from .dependencies import (
    get_usuario_atual,
    somente_admin,
    admin_ou_operador
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API de Gestão de Usuários",
    description="API REST segura com autenticação JWT e controle de acesso.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "API de Gestão de Usuários funcionando!"
    }


@app.post(
    "/auth/login",
    response_model=TokenResposta
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == dados.email)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )

    token = criar_token_jwt(
        usuario_id=usuario.id,
        nome=usuario.nome,
        perfil=usuario.perfil
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post(
    "/usuarios",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    dados: UsuarioCriar,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(somente_admin)
):
    usuario_existente = (
        db.query(Usuario)
        .filter(Usuario.email == dados.email)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este e-mail."
        )

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@app.get(
    "/usuarios",
    response_model=list[UsuarioResposta]
)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(admin_ou_operador)
):
    usuarios = db.query(Usuario).all()
    return usuarios


@app.get(
    "/usuarios/me",
    response_model=UsuarioResposta
)
def meus_dados(
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    return usuario_atual


@app.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResposta
)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    if (
        usuario_atual.perfil == "cliente"
        and usuario_atual.id != usuario_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clientes só podem consultar os próprios dados."
        )

    return usuario


@app.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResposta
)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioAtualizar,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    if usuario_atual.perfil == "cliente":
        if usuario_atual.id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clientes só podem atualizar os próprios dados."
            )

        if dados.perfil is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clientes não podem alterar o próprio perfil."
            )

    elif usuario_atual.perfil == "operador":
        if dados.perfil is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operadores não podem alterar perfis de acesso."
            )

    if dados.email is not None:
        email_existente = (
            db.query(Usuario)
            .filter(
                Usuario.email == dados.email,
                Usuario.id != usuario_id
            )
            .first()
        )

        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um usuário com este e-mail."
            )

        usuario.email = dados.email

    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.perfil is not None:
        usuario.perfil = dados.perfil

    db.commit()
    db.refresh(usuario)

    return usuario


@app.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(somente_admin)
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    db.delete(usuario)
    db.commit()

    return None