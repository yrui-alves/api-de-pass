import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL", "")

if not BASE_API_URL:
    import warnings
    warnings.warn(
        "A variável de ambiente BASE_API_URL não está definida. "
        "Configure-a no arquivo .env antes de fazer requisições.",
        stacklevel=1,
    )

app = FastAPI(
    title="API de Passe Booyah",
    description="Wrapper da API externa de envio de Passe Booyah (Free Fire). "
                "Utilize os endpoints abaixo para enviar passes e consultar saldo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request models ────────────────────────────────────────────────────────────

class SendPassRequest(BaseModel):
    key: str = Field(..., description="Sua API Key")
    uid: str = Field(..., description="Client ID do jogador Free Fire")
    mensagem: str | None = Field(None, description="Mensagem personalizada do presente")


class BalanceRequest(BaseModel):
    key: str = Field(..., description="Sua API Key")


# ── Response models ───────────────────────────────────────────────────────────

class SendPassResponse(BaseModel):
    status: str = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de retorno")
    ClientID: str = Field(..., description="Client ID do jogador")
    Nickname: str = Field(..., description="Nickname do jogador")
    Conta_utilizada: str = Field(..., description="Conta utilizada para envio")
    Diamantes_Antes: int = Field(..., description="Saldo de diamantes antes do envio")
    Diamantes_Depois: int = Field(..., description="Saldo de diamantes após o envio")
    Mensagem_Do_Presente: str = Field(..., description="Mensagem do presente enviado")


class BalanceResponse(BaseModel):
    status: str = Field(..., description="Status da operação")
    usuario: str = Field(..., description="Nome do usuário")
    saldo: float = Field(..., description="Saldo disponível")
    saldo_formatado: str = Field(..., description="Saldo formatado em reais")
    passes_disponiveis: int = Field(..., description="Quantidade de passes disponíveis")
    custo_por_passe: float = Field(..., description="Custo por passe em reais")
    ilimitado: bool = Field(..., description="Indica se a conta tem passes ilimitados")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post(
    "/api/v1/send-pass",
    response_model=SendPassResponse,
    tags=["Passe Booyah"],
    summary="Enviar Passe Booyah",
    description="Envia um Passe Booyah para um jogador Free Fire informando a API Key, "
                "o Client ID do jogador e, opcionalmente, uma mensagem personalizada.",
)
async def send_pass(body: SendPassRequest):
    payload = {"key": body.key, "uid": body.uid}
    if body.mensagem is not None:
        payload["mensagem"] = body.mensagem

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_API_URL}/api/v1/send-pass",
                json=payload,
                timeout=30,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail={"codigo": "API_ERROR", "mensagem": str(exc)})

    if response.status_code == 200:
        return response.json()

    error_map = {
        400: ("SALDO_INSUFICIENTE", "Saldo insuficiente para enviar passe"),
        401: ("KEY_INVALIDA", "API Key não encontrada"),
        403: ("KEY_DESATIVADA", "API Key desativada"),
    }
    codigo, mensagem_erro = error_map.get(
        response.status_code, ("API_ERROR", "Erro na API externa")
    )
    http_status = response.status_code if response.status_code in error_map else 502
    raise HTTPException(status_code=http_status, detail={"codigo": codigo, "mensagem": mensagem_erro})


@app.post(
    "/api/v1/balance",
    response_model=BalanceResponse,
    tags=["Saldo"],
    summary="Consultar Saldo",
    description="Consulta o saldo disponível na conta associada à API Key informada.",
)
async def balance(body: BalanceRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_API_URL}/api/v1/balance",
                json={"key": body.key},
                timeout=30,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail={"codigo": "API_ERROR", "mensagem": str(exc)})

    if response.status_code == 200:
        return response.json()

    error_map = {
        401: ("KEY_INVALIDA", "API Key não encontrada"),
        403: ("KEY_DESATIVADA", "API Key desativada"),
        404: ("USUARIO_NAO_ENCONTRADO", "Usuário não encontrado"),
    }
    codigo, mensagem_erro = error_map.get(
        response.status_code, ("API_ERROR", "Erro na API externa")
    )
    http_status = response.status_code if response.status_code in error_map else 502
    raise HTTPException(status_code=http_status, detail={"codigo": codigo, "mensagem": mensagem_erro})
