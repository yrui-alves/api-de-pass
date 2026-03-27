import os
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL", "")

if not BASE_API_URL:
    raise RuntimeError(
        "A variável de ambiente BASE_API_URL não está definida. "
        "Copie .env.example para .env e preencha o valor."
    )

app = FastAPI(
    title="API de Passe Booyah",
    description=(
        "Wrapper da API de envio de Passe Booyah (Free Fire). "
        "Permite enviar passes e consultar saldo via endpoints REST documentados. "
        "Documentação interativa disponível em `/docs` (Swagger UI) e `/redoc`."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ────────────────────────────────────────────────


class SendPassRequest(BaseModel):
    key: str = Field(..., description="Sua API Key")
    uid: str = Field(..., description="Client ID do jogador Free Fire")
    mensagem: Optional[str] = Field(None, description="Mensagem personalizada do presente")


class SendPassResponse(BaseModel):
    status: str = Field(..., description="Status da operação")
    message: str = Field(..., description="Mensagem de retorno")
    ClientID: str = Field(..., description="Client ID do jogador")
    Nickname: str = Field(..., description="Nickname do jogador")
    Conta_utilizada: str = Field(..., description="Conta utilizada para envio")
    Diamantes_Antes: int = Field(..., description="Saldo de diamantes antes do envio")
    Diamantes_Depois: int = Field(..., description="Saldo de diamantes após o envio")
    Mensagem_Do_Presente: str = Field(..., description="Mensagem do presente enviado")


class BalanceRequest(BaseModel):
    key: str = Field(..., description="Sua API Key")


class BalanceResponse(BaseModel):
    status: str = Field(..., description="Status da operação")
    usuario: str = Field(..., description="Nome do usuário")
    saldo: float = Field(..., description="Saldo disponível em reais")
    saldo_formatado: str = Field(..., description="Saldo formatado (ex: R$ 25.00)")
    passes_disponiveis: int = Field(..., description="Quantidade de passes disponíveis")
    custo_por_passe: float = Field(..., description="Custo por passe em reais")
    ilimitado: bool = Field(..., description="Indica se o plano é ilimitado")


# ── Endpoints ────────────────────────────────────────────────────────────────


@app.post(
    "/api/v1/send-pass",
    response_model=SendPassResponse,
    tags=["Passe Booyah"],
    summary="Enviar Passe Booyah",
    description=(
        "Envia um Passe Booyah para um jogador Free Fire pelo Client ID informado. "
        "Requer uma API Key válida e com saldo suficiente."
    ),
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
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                status_code=502,
                content={"status": "API_ERROR", "message": f"Erro ao conectar à API externa: {exc}"},
            )

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return response.json()


@app.post(
    "/api/v1/balance",
    response_model=BalanceResponse,
    tags=["Saldo"],
    summary="Consultar Saldo",
    description=(
        "Consulta o saldo disponível na conta associada à API Key informada, "
        "incluindo a quantidade de passes disponíveis e o custo por passe."
    ),
)
async def balance(body: BalanceRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_API_URL}/api/v1/balance",
                json={"key": body.key},
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                status_code=502,
                content={"status": "API_ERROR", "message": f"Erro ao conectar à API externa: {exc}"},
            )

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return response.json()
