# ⚡ Quick Start - O Analista Júnior

## 🚀 3 Comandos para Começar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar API Key (edite o arquivo .env depois)
cp env.example .env

# 3. Executar
python main.py
```

---

## 📝 Estrutura do Projeto

```
financial_analyst/
│
├── 🧠 CORE (Código Principal)
│   ├── market_mock.py      # Dados simulados (R$ 38.50, etc)
│   ├── tools.py            # Ferramenta LangChain (@tool decorator)
│   ├── agent.py            # Cérebro do agente (loop ReAct)
│   └── main.py             # Interface CLI (você roda este)
│
├── ⚙️ CONFIG
│   ├── requirements.txt    # Dependências Python
│   ├── env.example         # Template de configuração
│   └── .gitignore          # Arquivos ignorados pelo Git
│
├── 🧪 TESTES
│   └── test_agent.py       # Script de testes automatizados
│
└── 📚 DOCUMENTAÇÃO
    ├── README.md           # Visão geral completa
    ├── INSTRUCOES.md       # Guia passo a passo detalhado
    ├── ARQUITETURA.md      # Explicação técnica da arquitetura
    └── QUICK_START.md      # Este arquivo (início rápido)
```

---

## 🎯 Ações Disponíveis

| Ticker | Empresa         | Preço    |
|--------|-----------------|----------|
| PETR4  | Petrobras       | R$ 38,50 |
| VALE3  | Vale            | R$ 60,20 |
| ITUB4  | Itaú Unibanco   | R$ 32,10 |
| BBDC4  | Bradesco        | R$ 14,85 |
| WEGE3  | WEG             | R$ 42,30 |
| ABEV3  | Ambev           | R$ 11,95 |

---

## 💬 Exemplos de Perguntas

### ✅ Com Tool (consulta preços)
```
Você: Quanto está a Petrobras?
🤖: O preço atual da Petrobras (PETR4) é R$ 38,50.
```

### ✅ Sem Tool (conhecimento geral)
```
Você: O que é um CDB?
🤖: CDB significa Certificado de Depósito Bancário...
```

---

## 🔧 Comandos Úteis

```bash
# Testar o agente automaticamente
python test_agent.py

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/Scripts/activate  # Git Bash
venv\Scripts\activate         # CMD

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

---

## 🐛 Problemas Comuns

| Erro | Solução |
|------|---------|
| `OPENAI_API_KEY não encontrada` | Crie arquivo `.env` com sua chave |
| `No module named 'langchain_core'` | Execute `pip install -r requirements.txt` |
| `Ticker não encontrado` | Use apenas: PETR4, VALE3, ITUB4, BBDC4, WEGE3, ABEV3 |

---

## 📖 Próximos Passos

1. ✅ Execute `python main.py` e teste o agente
2. 📚 Leia `INSTRUCOES.md` para entender os conceitos
3. 🏗️ Leia `ARQUITETURA.md` para entender a estrutura
4. 🧪 Execute `python test_agent.py` para validar
5. 🎓 Faça os exercícios sugeridos em `INSTRUCOES.md`

---

## 🎓 Conceitos Principais

- **ReAct**: Reasoning (pensar) + Acting (agir)
- **Tool Calling**: LLM decide quando usar ferramentas
- **Pydantic**: Validação type-safe dos dados
- **LCEL**: LangChain Expression Language (moderno)

---

## 📞 Links Úteis

- [Documentação LangChain](https://python.langchain.com/)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

**Criado para o Bootcamp FIAP + Itaú** 🚀

*Dúvidas? Leia `INSTRUCOES.md` ou `ARQUITETURA.md`*
