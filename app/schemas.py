from typing import Literal

from pydantic import BaseModel, EmailStr, ConfigDict


PerfilUsuario = Literal["admin", "operador", "cliente"]


class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: PerfilUsuario = "cliente"


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str

    model_config = ConfigDict(from_attributes=True)

class UsuarioAtualizar(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    perfil: PerfilUsuario | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResposta(BaseModel):
    access_token: str
    token_type: str