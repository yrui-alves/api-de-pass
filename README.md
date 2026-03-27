# API de Passe Booyah

Wrapper em **Python + FastAPI** que consome uma API externa de envio de Passe Booyah (Free Fire).  
A documentação interativa é gerada automaticamente pelo FastAPI e fica disponível em `/docs` (Swagger UI) e `/redoc`.

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
# Edite o arquivo .env e preencha BASE_API_URL com a URL da API externa

# 4. Inicie o servidor
uvicorn main:app --reload
```

---

## Documentação

| URL | Descrição |
|-----|-----------|
| `http://localhost:8000/docs` | Swagger UI (interativa) |
| `http://localhost:8000/redoc` | ReDoc |

---

## Endpoints

### `POST /api/v1/send-pass` — Enviar Passe Booyah

Envia um Passe Booyah para um jogador Free Fire.

**Parâmetros (JSON body):**

| Parâmetro | Tipo   | Obrigatório | Descrição                          |
|-----------|--------|-------------|------------------------------------|
| key       | string | Sim         | Sua API Key                        |
| uid       | string | Sim         | Client ID do jogador Free Fire     |
| mensagem  | string | Não         | Mensagem personalizada do presente |

**Exemplo:**
```json
{
  "key": "ap_sua_chave_aqui",
  "uid": "123456789",
  "mensagem": "Bom aproveite ao Passe Booyah!"
}
```

---

### `POST /api/v1/balance` — Consultar Saldo

Consulta o saldo disponível na conta associada à API Key.

**Parâmetros (JSON body):**

| Parâmetro | Tipo   | Obrigatório | Descrição   |
|-----------|--------|-------------|-------------|
| key       | string | Sim         | Sua API Key |

**Exemplo:**
```json
{
  "key": "ap_sua_chave_aqui"
}
```

---

## Variáveis de Ambiente

| Variável      | Descrição                            |
|---------------|--------------------------------------|
| BASE_API_URL  | URL base da API externa (sem `/` no final) |

Copie `.env.example` para `.env` e preencha os valores.
