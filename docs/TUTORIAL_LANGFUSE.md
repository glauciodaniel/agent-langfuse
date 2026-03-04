# Tutorial: Rodando o Projeto + Integração com Langfuse

Este tutorial guia você passo a passo para rodar o projeto "O Analista Junior" e configurar o Langfuse para tracking das interações com LLM.

---

## Parte 1: Rodando o Projeto

### Pré-requisitos

- Python 3.10+
- Git
- Chave de API da OpenAI

### Passo 1: Criar ambiente virtual

```bash
# Na pasta do projeto
cd c:\projects\fiap\itau\ai-agents\aula1-agent

# Criar e ativar ambiente virtual
python -m venv venv

# Windows CMD
venv\Scripts\activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Git Bash / Linux / Mac
source venv/Scripts/activate
```

### Passo 2: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Configurar variáveis de ambiente

O arquivo `.env` já está configurado no seu projeto. Verifique se a `OPENAI_API_KEY` está correta.

### Passo 4: Executar o agente

```bash
python main.py
```

Você verá algo como:

```
============================================================
   O ANALISTA JUNIOR - Agente Financeiro Cognitivo
============================================================

Ola! Sou seu assistente financeiro junior.
Posso consultar precos, comparar acoes e simular investimentos.

Modelo: gpt-4
✅ Langfuse conectado: http://localhost:3000
Session ID: cli-20260304-143052-a1b2c3d4

Voce:
```

### Exemplos de perguntas:

- "Qual o preço da Petrobras?"
- "Compare PETR4 e VALE3"
- "Me dê um resumo do mercado"

---

## Parte 2: Instalando o Langfuse (Auto-hospedado)

O Langfuse é uma plataforma open-source para observabilidade de LLMs.

### Opção A: Langfuse Cloud (Recomendado para testes)

1. Acesse **https://cloud.langfuse.com**
2. Crie uma conta gratuita
3. Crie um projeto
4. Copie as API Keys

### Opção B: Self-hosted com Docker

#### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose

#### Passo 1: Clonar o Langfuse

```bash
# Em um diretório separado do projeto
cd c:\projects\fiap\itau\ai-agents

# Clonar o repositório do Langfuse
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

#### Passo 2: Iniciar com Docker Compose

```bash
docker compose up -d
```

Isso irá iniciar:

- **Langfuse Web** (porta 3000) - Interface web
- **PostgreSQL** (porta 5432) - Banco de dados

#### Passo 3: Acessar o Langfuse

1. Abra o navegador em: **http://localhost:3000**
2. Clique em **Sign up** para criar uma conta local
3. Crie sua conta (ex: email: `admin@local.dev`, senha: `admin123`)

#### Passo 4: Criar API Keys no Langfuse

1. Após fazer login, vá em **Settings** (ícone de engrenagem)
2. Clique em **API Keys**
3. Clique em **Create new API key**
4. Copie:
   - **Secret Key** (sk-lf-...)
   - **Public Key** (pk-lf-...)

> ⚠️ **Guarde essas chaves!** Você só verá a Secret Key uma vez.

---

## Parte 3: Configurando o Projeto

A integração com Langfuse **já está implementada** no projeto. Você só precisa configurar as variáveis de ambiente.

### Passo 1: Atualizar o .env

Edite o arquivo `.env` e configure as variáveis do Langfuse:

```env
# =============================================================================
# LANGFUSE - Observabilidade de LLM (opcional)
# =============================================================================

# Habilitar/desabilitar tracking (true/false)
LANGFUSE_ENABLED=true

# Host do Langfuse (local ou cloud)
LANGFUSE_HOST=http://localhost:3000
# Para Langfuse Cloud use: https://cloud.langfuse.com

# Chaves de API do Langfuse (obtenha no painel do Langfuse)
LANGFUSE_SECRET_KEY=sk-lf-sua-secret-key-aqui
LANGFUSE_PUBLIC_KEY=pk-lf-sua-public-key-aqui
```

> ⚠️ **Importante:** Não deixe espaços antes das variáveis!

### Passo 2: Instalar o cliente Langfuse

```bash
pip install langfuse
```

### Passo 3: Executar o agente

```bash
python main.py
```

Você deve ver:

```
✅ Langfuse conectado: http://localhost:3000
Session ID: cli-20260304-143052-a1b2c3d4
```

---

## Parte 4: Visualizando os Traces

### Passo 1: Fazer algumas perguntas

```
Voce: Qual o preço da Petrobras?
Voce: Compare PETR4 e VALE3
Voce: sair
```

### Passo 2: Acessar o Dashboard

1. Abra **http://localhost:3000** (ou cloud.langfuse.com)
2. Vá em **Traces** no menu lateral
3. Você verá todos os traces registrados

### O que você verá no Langfuse:

| Campo          | Descrição                         |
| -------------- | --------------------------------- |
| **Trace**      | Cada chamada ao `run_agent`       |
| **Session ID** | Agrupa traces da mesma sessão CLI |
| **Input**      | Pergunta do usuário               |
| **Output**     | Resposta do agente                |
| **Latência**   | Tempo de execução                 |
| **Tokens**     | Tokens consumidos (se disponível) |

### Filtrando por Sessão

No Langfuse, você pode filtrar por `session_id` para ver todas as interações de uma mesma sessão do CLI.

---

## Parte 5: Arquitetura da Integração

### Arquivos envolvidos

```
core/
├── observability.py    # Módulo de integração com Langfuse
├── config.py           # Configurações (inclui Langfuse)
└── agent.py            # Usa o decorator @langfuse_observe

adapters/
└── cli.py              # Gera session_id único por sessão
```

### Fluxo de dados

```
.env (configurações)
    ↓
core/config.py (carrega variáveis LANGFUSE_*)
    ↓
core/observability.py (configura cliente Langfuse)
    ↓
@langfuse_observe decorator em run_agent()
    ↓
Langfuse Server (recebe telemetria)
```

### Código principal

**observability.py** - Decorator para observabilidade:

```python
from langfuse import observe

def langfuse_observe(name: str = None):
    """Decorator que usa @observe do Langfuse se habilitado."""
    def decorator(func):
        if not settings.langfuse_enabled:
            return func
        return observe(name=name)(func)
    return decorator
```

**agent.py** - Função decorada:

```python
@langfuse_observe(name="run_agent")
def run_agent(query: str, memory=None, session_id=None):
    # Atualiza contexto do trace com session_id
    if session_id:
        update_trace_context(session_id=session_id)
    # ... resto da lógica
```

**cli.py** - Geração de session_id:

```python
session_id = f"cli-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
response = run_agent(user_input, memory=memory, session_id=session_id)
```

---

## Parte 6: Troubleshooting

### Langfuse não conecta

1. Verifique se o Docker está rodando: `docker ps`
2. Verifique as chaves no `.env` (sem espaços!)
3. Tente acessar http://localhost:3000 no navegador

### Erro "Connection refused"

```bash
# Reiniciar os containers
cd c:\projects\fiap\itau\ai-agents\langfuse
docker compose restart
```

### Traces não aparecem

1. Verifique se `LANGFUSE_ENABLED=true` no `.env`
2. Verifique se as chaves estão corretas (sem espaços)
3. Espere alguns segundos e atualize a página
4. Verifique se aparece "✅ Langfuse conectado" no terminal

### Session não agrupa traces

Verifique se o `session_id` está sendo passado corretamente:

```python
response = run_agent(user_input, memory=memory, session_id=session_id)
```

### Parar o Langfuse

```bash
cd c:\projects\fiap\itau\ai-agents\langfuse
docker compose down
```

---

## Parte 7: Resumo

### Arquivos Modificados/Criados

| Arquivo                 | Descrição                        |
| ----------------------- | -------------------------------- |
| `requirements.txt`      | Adicionado `langfuse>=2.0.0`     |
| `.env`                  | Variáveis `LANGFUSE_*`           |
| `core/config.py`        | Atributos de configuração        |
| `core/observability.py` | **Criado** - Integração Langfuse |
| `core/agent.py`         | Decorator `@langfuse_observe`    |
| `adapters/cli.py`       | Gera `session_id` único          |

### Funcionalidades

- ✅ Tracking automático de chamadas ao agente
- ✅ Session ID para agrupar conversas
- ✅ Flush automático dos dados
- ✅ Habilitação via variável de ambiente
- ✅ Suporte a self-hosted e cloud

---

## Recursos Adicionais

- [Documentação do Langfuse](https://langfuse.com/docs)
- [Langfuse Python SDK](https://langfuse.com/docs/sdk/python)
- [Langfuse Self-Hosting](https://langfuse.com/docs/deployment/self-host)
- [Decorator @observe](https://langfuse.com/docs/sdk/python/decorators)

---

Pronto! Agora você tem observabilidade completa do seu agente com Langfuse! 🎉
