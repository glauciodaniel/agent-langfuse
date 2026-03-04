# 🏗️ Arquitetura do Projeto - O Analista Júnior

## 📊 Visão Geral

Este documento explica a arquitetura do agente cognitivo e como os componentes interagem.

---

## 🔄 Fluxo de Dados Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIO (CLI)                            │
│                         main.py                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 1. Pergunta
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENTE (Cérebro)                            │
│                         agent.py                                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  run_agent(query)                                      │    │
│  │  • Cria mensagens com System Prompt                    │    │
│  │  • Invoca LLM com bind_tools                           │    │
│  │  • Processa resposta                                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                             │                                    │
│                             ▼                                    │
│                    ┌────────────────┐                           │
│                    │  Tool Calls?   │                           │
│                    └────────┬───────┘                           │
│                             │                                    │
│              ┌──────────────┴──────────────┐                   │
│              │ SIM                          │ NÃO               │
│              ▼                              ▼                    │
│    ┌──────────────────┐         ┌──────────────────┐          │
│    │  Executar Tool   │         │ Retornar Resposta│          │
│    └──────────────────┘         └──────────────────┘          │
└──────────────┬────────────────────────────────────────────────┘
               │
               │ 2. Chamar Tool
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FERRAMENTAS                                 │
│                         tools.py                                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  @tool(args_schema=StockPriceInput)                    │    │
│  │  def stock_price_tool(ticker: str) -> str              │    │
│  │      • Valida entrada com Pydantic                     │    │
│  │      • Chama função do mock                            │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────┬──────────────────────────────────────────────────┘
               │
               │ 3. Buscar Preço
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DADOS (Mock)                                │
│                      market_mock.py                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  MOCK_STOCK_PRICES = {                                 │    │
│  │      'PETR4': 38.50,                                   │    │
│  │      'VALE3': 60.20,                                   │    │
│  │      ...                                               │    │
│  │  }                                                     │    │
│  │                                                        │    │
│  │  def get_stock_price(ticker: str) -> str              │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────┬──────────────────────────────────────────────────┘
               │
               │ 4. Retornar Resultado
               ▼
         (Volta para agent.py)
               │
               │ 5. Re-invocar LLM com resultado
               ▼
         (LLM formula resposta final)
               │
               │ 6. Resposta Final
               ▼
         (Volta para main.py)
               │
               │ 7. Exibir para usuário
               ▼
           USUÁRIO
```

---

## 🧩 Componentes Detalhados

### 1. `market_mock.py` - Camada de Dados

**Responsabilidade:** Simular fonte de dados externa

```python
MOCK_STOCK_PRICES = {...}  # Dados fixos
get_stock_price(ticker)    # Função de busca
```

**Por que existe:**
- Isola a lógica de dados
- Facilita substituição por API real no futuro
- Permite testes sem dependências externas

---

### 2. `tools.py` - Camada de Ferramentas

**Responsabilidade:** Adaptar funções Python para o formato LangChain Tool

```python
class StockPriceInput(BaseModel):  # Schema Pydantic
    ticker: str

@tool(args_schema=StockPriceInput)  # Decorador LangChain
def stock_price_tool(ticker: str):
    return get_stock_price(ticker)
```

**Por que existe:**
- Cria contrato explícito para o LLM
- Valida entrada automaticamente
- Gera JSON Schema que o LLM entende

---

### 3. `agent.py` - Camada de Lógica (Cérebro)

**Responsabilidade:** Implementar o loop ReAct

```python
def run_agent(query: str):
    1. Criar mensagens com System Prompt
    2. Invocar LLM com bind_tools
    3. Verificar tool_calls na resposta
    4. Se houver: executar tools e re-invocar
    5. Se não: retornar resposta
```

**Por que existe:**
- Orquestra a interação entre LLM e Tools
- Implementa o padrão ReAct manualmente
- Permite visualizar cada etapa (didático)

---

### 4. `main.py` - Camada de Interface

**Responsabilidade:** Interagir com o usuário

```python
def run_cli():
    while True:
        query = input("Você: ")
        answer, logs = run_agent(query)
        print_logs(logs)
        print(f"Agente: {answer}")
```

**Por que existe:**
- Separa interface da lógica de negócio
- Fornece feedback visual do processo
- Facilita debug e aprendizado

---

## 🔀 Padrão ReAct em Ação

### Exemplo: "Quanto está a Petrobras?"

```
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 1: REASONING (Raciocínio)                            │
├─────────────────────────────────────────────────────────────┤
│ LLM recebe: "Quanto está a Petrobras?"                     │
│ LLM pensa: "Preciso buscar o preço de PETR4"              │
│ LLM gera: tool_call(name="stock_price_tool", args={"ticker":"PETR4"}) │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 2: ACTION (Ação)                                     │
├─────────────────────────────────────────────────────────────┤
│ Agente executa: stock_price_tool("PETR4")                  │
│ Tool chama: get_stock_price("PETR4")                       │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 3: OBSERVATION (Observação)                          │
├─────────────────────────────────────────────────────────────┤
│ Tool retorna: "R$ 38.50"                                   │
│ Agente cria: ToolMessage(content="R$ 38.50")              │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ ETAPA 4: REASONING (Raciocínio Final)                      │
├─────────────────────────────────────────────────────────────┤
│ LLM recebe: Pergunta + Tool Result                         │
│ LLM pensa: "Tenho o preço, vou formular resposta"         │
│ LLM gera: "O preço atual da Petrobras (PETR4) é R$ 38,50" │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Decisões de Design

### Por que NÃO usar AgentExecutor?

**AgentExecutor é legado e abstrai demais o processo.**

Neste projeto educacional:
- ✅ Implementamos o loop manualmente
- ✅ Cada etapa é visível e compreensível
- ✅ Logs detalhados para aprendizado

### Por que Pydantic?

**Pydantic cria um contrato type-safe entre LLM e código.**

```python
# Sem Pydantic (ruim)
@tool
def stock_price_tool(ticker):  # LLM não sabe o que enviar
    ...

# Com Pydantic (bom)
class StockPriceInput(BaseModel):
    ticker: str = Field(description="...")  # LLM sabe exatamente

@tool(args_schema=StockPriceInput)
def stock_price_tool(ticker: str):
    ...
```

### Por que Temperature=0?

**Para tool calling, queremos determinismo.**

- `temperature=0`: Sempre a mesma decisão (preciso)
- `temperature>0`: Variação nas respostas (criativo)

Para um agente que precisa decidir quando usar tools, precisão é crucial.

---

## 📦 Dependências e Versões

```
langchain-core  ─┐
                 ├─► Abstrações base (Tool, Message, LCEL)
langchain-openai ┘

pydantic ─────────► Validação de schemas

python-dotenv ────► Gerenciamento de .env
```

---

## 🔄 Extensibilidade

### Como adicionar uma nova Tool?

1. **Criar função em `market_mock.py`** (ou novo arquivo)
2. **Criar schema Pydantic em `tools.py`**
3. **Decorar com `@tool` em `tools.py`**
4. **Adicionar à lista `tools` em `agent.py`**

Exemplo: Tool de cálculo de variação percentual

```python
# tools.py
class VariationInput(BaseModel):
    ticker: str
    days: int = Field(description="Número de dias para calcular variação")

@tool(args_schema=VariationInput)
def calculate_variation(ticker: str, days: int) -> str:
    """Calcula a variação percentual de uma ação."""
    # Implementação...
    return f"Variação de {days} dias: +5.2%"

# agent.py
tools = [stock_price_tool, calculate_variation]  # Adicionar aqui
```

---

## 🎓 Conceitos Avançados (Próximas Aulas)

### Aula 2: Memória
- Adicionar `ConversationBufferMemory`
- Manter contexto entre perguntas

### Aula 3: LangGraph
- Substituir loop manual por grafo de estados
- Fluxos condicionais complexos

### Aula 4: RAG
- Adicionar `VectorStore`
- Buscar em documentos financeiros

---

## 📚 Referências

- [LangChain Tool Calling](https://python.langchain.com/docs/how_to/tool_calling/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

---

**Arquitetura criada para fins educacionais - Bootcamp FIAP + Itaú** 🚀
