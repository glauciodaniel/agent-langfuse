# 📚 Índice de Documentação - O Analista Júnior

## 🚀 Começando

Novo no projeto? Comece aqui:

1. **[QUICK_START.md](QUICK_START.md)** ⚡
   - 3 comandos para começar
   - Estrutura visual do projeto
   - Exemplos rápidos

2. **[INSTRUCOES.md](INSTRUCOES.md)** 📖
   - Guia passo a passo completo
   - Resolução de problemas
   - Exercícios práticos

---

## 📖 Documentação Completa

### Para Usuários

- **[README.md](../README.md)** - Visão geral do projeto
  - O que é o projeto
  - Como instalar
  - Como usar
  - Exemplos de uso

- **[QUICK_START.md](QUICK_START.md)** - Início rápido
  - Setup em 3 comandos
  - Estrutura de arquivos
  - Comandos úteis

- **[INSTRUCOES.md](INSTRUCOES.md)** - Manual detalhado
  - Instalação passo a passo
  - Exemplos de perguntas
  - Troubleshooting
  - Exercícios sugeridos

### Para Desenvolvedores

- **[ARQUITETURA.md](ARQUITETURA.md)** - Documentação técnica
  - Fluxo de dados completo
  - Componentes detalhados
  - Padrão ReAct explicado
  - Como estender o projeto

- **[ESTRUTURA_PROJETO.txt](ESTRUTURA_PROJETO.txt)** - Mapa visual
  - Estrutura de arquivos
  - Fluxo de dados
  - Stack tecnológico
  - Métricas do projeto

---

## 💻 Código Fonte

### Módulos Principais

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| **[market_mock.py](../market_mock.py)** | Simulação de dados de mercado | ~50 |
| **[tools.py](../tools.py)** | Definição de ferramentas LangChain | ~60 |
| **[agent.py](../agent.py)** | Lógica do agente (cérebro ReAct) | ~150 |
| **[main.py](../main.py)** | Interface CLI interativa | ~130 |

### Scripts Auxiliares

| Arquivo | Descrição |
|---------|-----------|
| **[setup.py](../setup.py)** | Script de setup automatizado |
| **[test_agent.py](../test_agent.py)** | Suite de testes automatizados |

### Configuração

| Arquivo | Descrição |
|---------|-----------|
| **[requirements.txt](../requirements.txt)** | Dependências Python |
| **[env.example](../env.example)** | Template de configuração |
| **[.gitignore](../.gitignore)** | Arquivos ignorados pelo Git |

---

## 🎯 Guias por Objetivo

### "Quero usar o agente agora!"
1. [QUICK_START.md](QUICK_START.md) - 3 comandos
2. Execute: `python setup.py`
3. Execute: `python main.py`

### "Quero entender como funciona"
1. [INSTRUCOES.md](INSTRUCOES.md) - Conceitos básicos
2. [ARQUITETURA.md](ARQUITETURA.md) - Detalhes técnicos
3. Leia o código com os comentários

### "Quero modificar/estender"
1. [ARQUITETURA.md](ARQUITETURA.md) - Seção "Extensibilidade"
2. [agent.py](../agent.py) - Veja como adicionar tools
3. [test_agent.py](../test_agent.py) - Teste suas mudanças

### "Preciso resolver um problema"
1. [INSTRUCOES.md](INSTRUCOES.md) - Seção "Resolução de Problemas"
2. [QUICK_START.md](QUICK_START.md) - Seção "Problemas Comuns"
3. Execute: `python test_agent.py` para diagnóstico

---

## 📊 Fluxo de Leitura Recomendado

### Nível 1: Iniciante (30 min)
```
QUICK_START.md → README.md → Executar main.py
```

### Nível 2: Intermediário (1-2 horas)
```
INSTRUCOES.md → Ler código com comentários → Fazer exercícios
```

### Nível 3: Avançado (3+ horas)
```
ARQUITETURA.md → RESUMO_EXECUTIVO.md → Modificar código → Criar nova tool
```

---

## 🔍 Busca Rápida

### Conceitos

- **ReAct**: [ARQUITETURA.md](ARQUITETURA.md#padrão-react-em-ação)
- **Tool Calling**: [ARQUITETURA.md](ARQUITETURA.md#2-toolspy---camada-de-ferramentas)
- **Pydantic**: [tools.py](tools.py) + [ARQUITETURA.md](ARQUITETURA.md#por-que-pydantic)
- **Temperature**: [agent.py](agent.py) + [ARQUITETURA.md](ARQUITETURA.md#por-que-temperature0)

### Tarefas

- **Instalar**: [QUICK_START.md](QUICK_START.md#-3-comandos-para-começar)
- **Configurar API Key**: [INSTRUCOES.md](INSTRUCOES.md#passo-2-configurar-api-key)
- **Adicionar Tool**: [ARQUITETURA.md](ARQUITETURA.md#como-adicionar-uma-nova-tool)
- **Resolver Erros**: [INSTRUCOES.md](INSTRUCOES.md#-resolução-de-problemas)

### Exemplos

- **Consulta de Preço**: [README.md](README.md#consulta-de-preços-usa-tool)
- **Pergunta Geral**: [README.md](README.md#pergunta-de-conhecimento-geral-sem-tool)
- **Ticker Inválido**: [test_agent.py](test_agent.py) - função `test_invalid_ticker()`

---

## 🎓 Recursos de Aprendizado

### Documentação Oficial

- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Pydantic Docs](https://docs.pydantic.dev/)

### Papers Acadêmicos

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

### Próximas Aulas

- **Aula 2**: Memória Conversacional
- **Aula 3**: LangGraph para Fluxos Complexos
- **Aula 4**: RAG (Retrieval-Augmented Generation)

---

## 📞 Suporte

### Problemas Técnicos
1. Consulte [INSTRUCOES.md - Resolução de Problemas](INSTRUCOES.md#-resolução-de-problemas)
2. Execute `python test_agent.py` para diagnóstico
3. Verifique se todas as dependências estão instaladas

### Dúvidas Conceituais
1. Leia [ARQUITETURA.md](ARQUITETURA.md) para entender o design
2. Revise os comentários no código (docstrings)
3. Consulte o instrutor do Bootcamp

### Sugestões e Melhorias
- Este é um projeto educacional em evolução
- Feedback é bem-vindo!

---

## 📋 Checklist de Início

- [ ] Ler [QUICK_START.md](QUICK_START.md)
- [ ] Executar `python setup.py`
- [ ] Configurar OPENAI_API_KEY no `.env`
- [ ] Executar `python test_agent.py`
- [ ] Executar `python main.py`
- [ ] Testar com perguntas de exemplo
- [ ] Ler [INSTRUCOES.md](INSTRUCOES.md)
- [ ] Explorar o código fonte
- [ ] Fazer exercícios sugeridos
- [ ] Ler [ARQUITETURA.md](ARQUITETURA.md)

---

## 🎯 Objetivos de Aprendizado

Ao final deste projeto, você deve ser capaz de:

- ✅ Explicar o padrão ReAct
- ✅ Criar Tools customizadas com Pydantic
- ✅ Usar LangChain moderno (LCEL, bind_tools)
- ✅ Entender quando usar temperature=0 vs >0
- ✅ Debugar agentes com logs estruturados
- ✅ Estender o agente com novas funcionalidades

---

**Projeto desenvolvido para o Bootcamp FIAP + Itaú** 🚀  
**Aula 1: Agentes Cognitivos com Padrão ReAct**

*Use este índice como seu guia de navegação pela documentação!*
