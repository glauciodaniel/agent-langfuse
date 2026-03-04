# 📋 Instruções de Uso - O Analista Júnior

## ⚡ Início Rápido (5 minutos)

### Passo 1: Preparar o Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows Git Bash)
source venv/Scripts/activate

# Ou ativar (Windows CMD)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Configurar API Key

```bash
# Criar arquivo .env (copiar do exemplo)
cp env.example .env

# Editar .env e adicionar sua chave OpenAI
# Use seu editor preferido (VSCode, Notepad, etc)
# Substitua: OPENAI_API_KEY=sua-chave-aqui
```

**Obter chave OpenAI:**
1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie e cole no arquivo `.env`

### Passo 3: Executar

```bash
python main.py
```

---

## 🎯 Exemplos de Perguntas

### ✅ Perguntas que usam a ferramenta (Tool):

- "Quanto está a Petrobras?"
- "Qual o preço da Vale?"
- "Me diga a cotação do Itaú"
- "Preço da WEGE3"

### ✅ Perguntas de conhecimento geral (Sem Tool):

- "O que é um CDB?"
- "Explique o que são dividendos"
- "O que é a taxa Selic?"
- "Como funciona a bolsa de valores?"

---

## 🔍 Entendendo os Logs

Quando você faz uma pergunta, o agente mostra seu "processo de pensamento":

```
[🧠 PENSANDO] - O agente está processando sua pergunta

[🔧 AÇÃO] - O agente decidiu usar uma ferramenta
  └─ Argumentos: {'ticker': 'PETR4'}

[👁️ OBSERVAÇÃO] - Resultado da ferramenta
  Resultado: R$ 38.50

🤖 Analista Júnior: - Resposta final formatada
```

**Isso demonstra o Padrão ReAct:**
- **Reasoning** (Raciocínio): Decidir se precisa de uma ferramenta
- **Acting** (Ação): Executar a ferramenta
- **Observation** (Observação): Processar o resultado
- **Answer** (Resposta): Formular resposta final

---

## 🐛 Resolução de Problemas

### Erro: "OPENAI_API_KEY não encontrada"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Verifique se a chave está no formato: `OPENAI_API_KEY=sk-...`
3. Não use aspas ao redor da chave

### Erro: "No module named 'langchain_core'"

**Solução:**
```bash
# Certifique-se de que o venv está ativado
pip install -r requirements.txt
```

### Erro: "Ticker não encontrado"

**Solução:**
O mock só tem estas ações:
- PETR4 (Petrobras)
- VALE3 (Vale)
- ITUB4 (Itaú)
- BBDC4 (Bradesco)
- WEGE3 (WEG)
- ABEV3 (Ambev)

Use o código exato (ex: PETR4, não PETR3)

---

## 📚 Estrutura do Código (Para Estudar)

### 1. `market_mock.py` - Dados Simulados
- Dicionário com preços fixos
- Função simples de busca
- **Conceito**: Mock para desenvolvimento

### 2. `tools.py` - Ferramenta LangChain
- Decorador `@tool` para criar uma Tool
- Schema Pydantic para validação
- **Conceito**: Tool Calling moderno

### 3. `agent.py` - Cérebro do Agente
- Loop ReAct manual
- Bind de tools ao LLM
- **Conceito**: Padrão ReAct, Temperature

### 4. `main.py` - Interface CLI
- Loop interativo
- Logs formatados
- **Conceito**: CLI, visualização do processo

---

## 🎓 Exercícios Sugeridos

### Nível 1: Básico
1. Adicione mais ações ao `MOCK_STOCK_PRICES`
2. Mude as cores dos logs em `main.py`
3. Teste com diferentes perguntas

### Nível 2: Intermediário
1. Crie uma nova tool para calcular variação percentual
2. Adicione histórico de conversas (memória simples)
3. Mude para o modelo `gpt-4o` e compare resultados

### Nível 3: Avançado
1. Integre uma API real (Yahoo Finance)
2. Adicione logging em arquivo
3. Crie testes unitários para as tools

---

## 🚀 Próximos Passos

Após dominar este projeto:

1. **Aula 2**: Adicionar memória conversacional
2. **Aula 3**: Usar LangGraph para fluxos complexos
3. **Aula 4**: Implementar RAG para documentos financeiros

---

## 💡 Dicas

- Use `temperature=0` para precisão (já configurado)
- Use `temperature=0.7` para respostas mais criativas
- O modelo `gpt-4o` é mais preciso mas mais caro
- O modelo `gpt-3.5-turbo` é mais rápido e barato

---

## 📞 Suporte

Este é um projeto educacional. Para dúvidas:
1. Revise os comentários no código (docstrings)
2. Consulte a documentação do LangChain
3. Pergunte ao instrutor do Bootcamp

---

**Bom aprendizado! 🚀**
