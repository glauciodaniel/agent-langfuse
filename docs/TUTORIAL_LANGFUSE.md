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
╔══════════════════════════════════════════════════════════════╗
║           O ANALISTA JÚNIOR - Assistente Financeiro          ║
╚══════════════════════════════════════════════════════════════╝

Olá! Eu sou o Analista Júnior, seu assistente para mercado financeiro.
Digite 'sair' para encerrar.

Você:
```

### Exemplos de perguntas:

- "Qual o preço da Petrobras?"
- "Compare PETR4 e VALE3"
- "Me dê um resumo do mercado"

---

## Parte 2: Instalando o Langfuse (Auto-hospedado)

O Langfuse é uma plataforma open-source para observabilidade de LLMs. Vamos cloná-lo em um diretório separado.

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose

### Passo 1: Clonar o Langfuse

```bash
# Voltar para o diretório pai
cd c:\projects\fiap\itau\ai-agents

# Clonar o repositório do Langfuse
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

### Passo 2: Iniciar com Docker Compose

```bash
docker compose up -d
```

Isso irá iniciar:

- **Langfuse Web** (porta 3000) - Interface web
- **PostgreSQL** (porta 5432) - Banco de dados

### Passo 3: Acessar o Langfuse

1. Abra o navegador em: **http://localhost:3000**
2. Clique em **Sign up** para criar uma conta local
3. Crie sua conta (ex: email: `admin@local.dev`, senha: `admin123`)

### Passo 4: Criar API Keys no Langfuse

1. Após fazer login, vá em **Settings** (ícone de engrenagem)
2. Clique em **API Keys**
3. Clique em **Create new API key**
4. Copie:
   - **Secret Key** (sk-lf-...)
   - **Public Key** (pk-lf-...)

> ⚠️ **Guarde essas chaves!** Você só verá a Secret Key uma vez.

---

## Parte 3: Integrando Langfuse no Projeto

### Passo 1: Instalar a dependência do Langfuse

```bash
cd c:\projects\fiap\itau\ai-agents\aula1-agent

# Ativar ambiente virtual (se não estiver)
venv\Scripts\activate

# Instalar langfuse
pip install langfuse
```

### Passo 2: Adicionar ao requirements.txt

Adicione no final do arquivo `requirements.txt`:

```
# Langfuse - Observabilidade e tracking de LLM
langfuse>=2.0.0
```

### Passo 3: Atualizar o .env

Adicione as seguintes variáveis no final do seu arquivo `.env`:

```env
# =============================================================================
# LANGFUSE - Observabilidade de LLM
# =============================================================================

# Host do Langfuse (local ou cloud)
LANGFUSE_HOST=http://localhost:3000

# Chaves de API do Langfuse (obtidas no passo anterior)
LANGFUSE_SECRET_KEY=sk-lf-COLE_SUA_SECRET_KEY_AQUI
LANGFUSE_PUBLIC_KEY=pk-lf-COLE_SUA_PUBLIC_KEY_AQUI

# Habilitar/desabilitar tracking (true/false)
LANGFUSE_ENABLED=true
```

### Passo 4: Atualizar o config.py

Crie ou atualize para incluir as configurações do Langfuse. Adicione estas linhas no arquivo `core/config.py`:

**Dentro da classe `Settings`**, adicione os novos atributos:

```python
# Langfuse
langfuse_enabled: bool = False
langfuse_host: str = "http://localhost:3000"
langfuse_secret_key: str = ""
langfuse_public_key: str = ""
```

**No método `from_env()`**, adicione:

```python
langfuse_enabled=os.getenv("LANGFUSE_ENABLED", "false").lower() == "true",
langfuse_host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
```

### Passo 5: Criar módulo de observabilidade

Crie o arquivo `core/observability.py`:

```python
"""
Módulo de observabilidade com Langfuse.

Fornece integração com Langfuse para tracking de:
- Chamadas ao LLM
- Uso de ferramentas
- Latência e custos
"""

from typing import Optional
from functools import lru_cache

from core.config import get_settings


@lru_cache(maxsize=1)
def get_langfuse_handler():
    """
    Retorna o callback handler do Langfuse para LangChain.

    Returns:
        CallbackHandler configurado ou None se desabilitado
    """
    settings = get_settings()

    if not settings.langfuse_enabled:
        return None

    if not settings.langfuse_secret_key or not settings.langfuse_public_key:
        print("⚠️  Langfuse habilitado mas chaves não configuradas")
        return None

    try:
        from langfuse.callback import CallbackHandler

        handler = CallbackHandler(
            secret_key=settings.langfuse_secret_key,
            public_key=settings.langfuse_public_key,
            host=settings.langfuse_host,
        )

        print("✅ Langfuse conectado:", settings.langfuse_host)
        return handler

    except ImportError:
        print("⚠️  Langfuse não instalado. Execute: pip install langfuse")
        return None
    except Exception as e:
        print(f"⚠️  Erro ao conectar Langfuse: {e}")
        return None
```

### Passo 6: Integrar no agent.py

Atualize o arquivo `core/agent.py` para usar o Langfuse:

**1. Adicione o import no topo:**

```python
from core.observability import get_langfuse_handler
```

**2. Na função `run_agent()`, modifique a chamada ao LLM:**

Altere de:

```python
response = llm.invoke(messages)
```

Para:

```python
# Obter handler do Langfuse (se configurado)
langfuse_handler = get_langfuse_handler()
callbacks = [langfuse_handler] if langfuse_handler else None

# Invocar modelo com callbacks
response = llm.invoke(messages, config={"callbacks": callbacks})
```

---

## Parte 4: Testando a Integração

### Passo 1: Verificar se o Langfuse está rodando

```bash
# Verificar containers
docker ps

# Deve mostrar langfuse-web e langfuse-db
```

### Passo 2: Executar o agente

```bash
cd c:\projects\fiap\itau\ai-agents\aula1-agent
python main.py
```

Você deve ver:

```
✅ Langfuse conectado: http://localhost:3000
```

### Passo 3: Fazer algumas perguntas

```
Você: Quanto está a Petrobras?
Você: Compare PETR4 e VALE3
Você: sair
```

### Passo 4: Visualizar no Langfuse

1. Abra **http://localhost:3000**
2. Vá em **Traces** no menu lateral
3. Você verá todas as chamadas registradas com:
   - Input/Output de cada chamada
   - Tokens utilizados
   - Latência
   - Custo estimado

---

## Parte 5: Troubleshooting

### Langfuse não conecta

1. Verifique se o Docker está rodando: `docker ps`
2. Verifique as chaves no `.env`
3. Tente acessar http://localhost:3000 no navegador

### Erro "Connection refused"

```bash
# Reiniciar os containers
cd c:\projects\fiap\itau\ai-agents\langfuse
docker compose restart
```

### Traces não aparecem

1. Verifique se `LANGFUSE_ENABLED=true` no `.env`
2. Verifique se as chaves estão corretas
3. Espere alguns segundos e atualize a página

### Parar o Langfuse

```bash
cd c:\projects\fiap\itau\ai-agents\langfuse
docker compose down
```

---

## Resumo de Arquivos Modificados

| Arquivo                 | Ação                            |
| ----------------------- | ------------------------------- |
| `requirements.txt`      | Adicionar `langfuse>=2.0.0`     |
| `.env`                  | Adicionar variáveis do Langfuse |
| `core/config.py`        | Adicionar atributos do Langfuse |
| `core/observability.py` | **Criar** novo arquivo          |
| `core/agent.py`         | Integrar callback handler       |

---

## Recursos Adicionais

- [Documentação do Langfuse](https://langfuse.com/docs)
- [Langfuse + LangChain](https://langfuse.com/docs/integrations/langchain)
- [Langfuse Self-Hosting](https://langfuse.com/docs/deployment/self-host)

---

Pronto! Agora você tem observabilidade completa do seu agente com Langfuse! 🎉

- [Documentação do Langfuse](https://langfuse.com/docs)
- [Langfuse + LangChain](https://langfuse.com/docs/integrations/langchain)
- [Langfuse Self-Hosting](https://langfuse.com/docs/deployment/self-host)

---

Pronto! Agora você tem observabilidade completa do seu agente com Langfuse! 🎉
