# API de Passe Booyah

Wrapper em **Python + FastAPI** que consome a API externa de envio de Passe Booyah para o Free Fire.

A documentação interativa é gerada automaticamente pelo FastAPI e fica disponível em:

- **Swagger UI** → `/docs`
- **ReDoc** → `/redoc`

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/yrui-alves/api-de-pass.git
cd api-de-pass

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env e defina BASE_API_URL com o domínio da API externa

# 4. Inicie o servidor
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

---

## Endpoints

### `POST /api/v1/send-pass` — Enviar Passe Booyah

| Parâmetro | Tipo   | Obrigatório | Descrição                              |
|-----------|--------|-------------|----------------------------------------|
| key       | string | Sim         | Sua API Key                            |
| uid       | string | Sim         | Client ID do jogador Free Fire         |
| mensagem  | string | Não         | Mensagem personalizada do presente     |

**Resposta de sucesso (200):**
```json
{
  "status": "PASSE_ENVIADO",
  "message": "Passe Booyah enviado com sucesso!",
  "ClientID": "123456789",
  "Nickname": "JogadorXYZ",
  "Conta_utilizada": "conta@email.com",
  "Diamantes_Antes": 1000,
  "Diamantes_Depois": 400,
  "Mensagem_Do_Presente": "Bom aproveito ao Passe Booyah!"
}
```

---

### `POST /api/v1/balance` — Consultar Saldo

| Parâmetro | Tipo   | Obrigatório | Descrição   |
|-----------|--------|-------------|-------------|
| key       | string | Sim         | Sua API Key |

**Resposta de sucesso (200):**
```json
{
  "status": "OK",
  "usuario": "SeuNome",
  "saldo": 25.00,
  "saldo_formatado": "R$ 25.00",
  "passes_disponiveis": 10,
  "custo_por_passe": 2.50,
  "ilimitado": false
}
```

---

## Variáveis de ambiente

| Variável      | Descrição                              |
|---------------|----------------------------------------|
| BASE_API_URL  | URL base da API externa (sem barra final) |
