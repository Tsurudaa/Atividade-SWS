from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt

from .auth import decodificar_token
from .database import get_db
from .models import Usuario


security = HTTPBearer()


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credenciais.credentials

    try:
        payload = decodificar_token(token)

        usuario_id = int(payload.get("sub"))

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário do token não encontrado."
        )

    return usuario


def somente_admin(
    usuario: Usuario = Depends(get_usuario_atual)
):
    if usuario.perfil != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido somente para administradores."
        )

    return usuario


def admin_ou_operador(
    usuario: Usuario = Depends(get_usuario_atual)
):
    if usuario.perfil not in ["admin", "operador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido somente para administradores ou operadores."
        )

    return usuario