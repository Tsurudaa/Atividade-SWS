import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY não configurada. "
        "Defina a variável no arquivo .env."
    )


ALGORITHM = "HS256"
TEMPO_EXPIRACAO_MINUTOS = 30


def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")

    salt = bcrypt.gensalt()

    hash_bytes = bcrypt.hashpw(
        senha_bytes,
        salt
    )

    return hash_bytes.decode("utf-8")


def verificar_senha(
    senha: str,
    senha_hash: str
) -> bool:
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8")
    )


def criar_token_jwt(
    usuario_id: int,
    nome: str,
    perfil: str
) -> str:

    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "nome": nome,
        "perfil": perfil,
        "iat": agora,
        "exp": agora + timedelta(
            minutes=TEMPO_EXPIRACAO_MINUTOS
        )
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decodificar_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )