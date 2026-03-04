# O Analista Junior

**Agente Cognitivo Financeiro com Padrao ReAct**

Projeto educacional do Bootcamp FIAP + Itau de GenAI. Este agente demonstra as melhores praticas de arquitetura para construcao de agentes de IA.

---

## Arquitetura

O projeto segue principios de **Clean Architecture** e **Separacao de Responsabilidades**:

```
financial_analyst/
├── core/                    # Cerebro do agente
│   ├── agent.py             # Loop ReAct (logica principal)
│   ├── memory.py            # Gerenciamento de memoria
│   └── config.py            # Configuracoes centralizadas
│
├── domain/                  # Dominio de negocios
│   ├── market_data.py       # Dados mockados do mercado
│   └── tools.py             # Ferramentas LangChain
│
├── prompts/                 # Prompts versionados
│   └── system_prompt.txt    # Prompt do sistema (editavel)
│
├── adapters/                # Interfaces de entrada
│   └── cli.py               # Interface de linha de comando
│
├── common/                  # Codigo compartilhado
│   ├── exceptions.py        # Excecoes customizadas
│   └── types.py             # Tipos e dataclasses
│
├── tests/                   # Testes organizados
│   ├── test_market_data.py
│   ├── test_memory.py
│   └── test_tools.py
│
├── main.py                  # Ponto de entrada (3 linhas!)
├── requirements.txt
└── env.example
```

---

## Principios de Arquitetura

| Principio | Aplicacao |
|-----------|-----------|
| **Single Responsibility** | Cada modulo tem uma unica funcao |
| **Prompts Externalizados** | Prompt em arquivo .txt, facil de versionar |
| **Configuracao Centralizada** | Um unico lugar (config.py + .env) |
| **Tipos Explicitos** | Dataclasses ao inves de dicts |
| **Excecoes Hierarquicas** | Tratamento granular de erros |
| **Adapters Desacoplados** | CLI separado da logica core |

---

## Instalacao

```bash
# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencias
pip install -r requirements.txt

# Configuracao
cp env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

---

## Uso

```bash
# Executar o agente
python main.py

# Rodar testes (sem API)
python tests/test_market_data.py
python tests/test_memory.py
python tests/test_tools.py
```

---

## Ferramentas Disponiveis

| Ferramenta | Descricao |
|------------|-----------|
| `stock_price_tool` | Consulta preco de uma acao |
| `compare_stocks_tool` | Compara duas acoes |
| `market_summary_tool` | Resumo do mercado |
| `calculate_returns_tool` | Simula investimentos |
| `list_available_stocks_tool` | Lista acoes disponiveis |

---

## Configuracoes (.env)

| Variavel | Padrao | Descricao |
|----------|--------|-----------|
| `OPENAI_API_KEY` | - | Chave da API (obrigatorio) |
| `OPENAI_MODEL` | gpt-3.5-turbo | Modelo LLM |
| `OPENAI_TEMPERATURE` | 0 | Criatividade (0-1) |
| `OPENAI_MAX_RETRIES` | 3 | Tentativas em erro |
| `OPENAI_TIMEOUT` | 30 | Timeout em segundos |
| `AGENT_MAX_ITERATIONS` | 5 | Max iteracoes ReAct |
| `AGENT_MEMORY_MAX_MESSAGES` | 20 | Limite de memoria |

---

## Exemplos

```
Voce: Quanto esta a Petrobras?
[ACAO] Usando: stock_price_tool
  -> Args: {'ticker': 'PETR4'}
[OBSERVACAO] Dados obtidos
Analista: O preco da Petrobras (PETR4) e R$ 38,50.

Voce: Compare com a Vale
[ACAO] Usando: compare_stocks_tool
  -> Args: {'ticker1': 'PETR4', 'ticker2': 'VALE3'}
Analista: [Comparacao detalhada...]
```

---

## Comandos CLI

| Comando | Descricao |
|---------|-----------|
| `sair` | Encerra |
| `limpar` | Limpa memoria |
| `memoria` | Status da memoria |
| `config` | Mostra configuracoes |

---

## Conceitos Didaticos

1. **Padrao ReAct**: Loop de Reasoning + Acting
2. **Tool Calling**: LLM decidindo usar ferramentas
3. **Memoria de Conversacao**: Buffer Memory com limite
4. **Clean Architecture**: Separacao clara de camadas
5. **Type Safety**: Pydantic e dataclasses
6. **Error Handling**: Excecoes hierarquicas

---

## Acoes Disponiveis (Mock)

| Ticker | Empresa | Setor |
|--------|---------|-------|
| PETR4 | Petrobras | Petroleo |
| VALE3 | Vale | Mineracao |
| ITUB4 | Itau | Bancos |
| BBDC4 | Bradesco | Bancos |
| WEGE3 | WEG | Industria |
| ABEV3 | Ambev | Bebidas |
| MGLU3 | Magazine Luiza | Varejo |
| B3SA3 | B3 | Financeiro |

---

## Proximas Aulas

- **Aula 2**: LangGraph para fluxos complexos
- **Aula 3**: RAG (Retrieval-Augmented Generation)
- **Aula 4**: Deploy em producao

---

## Licenca

Projeto educacional - Use livremente para aprender!
