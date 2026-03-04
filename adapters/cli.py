"""
Interface de Linha de Comando (CLI) do Agente.

Conceito Didatico - Adapter Pattern:
    O CLI e um "adapter" que conecta o core do agente
    ao mundo externo (terminal). Isso significa que:
    - O core nao sabe que esta rodando em um CLI
    - Poderiamos facilmente criar um adapter web/API
    - A logica de formatacao fica separada da logica de negocio
"""

import os
import uuid
from datetime import datetime
from core.agent import run_agent
from core.memory import get_global_memory, clear_global_memory
from core.config import validate_api_key, get_settings
from common.types import ExecutionLog


# =============================================================================
# FORMATACAO DO TERMINAL
# =============================================================================

class Colors:
    """Codigos ANSI para cores no terminal."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header() -> None:
    """Exibe cabecalho do programa."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}   O ANALISTA JUNIOR - Agente Financeiro Cognitivo{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}\n")
    
    print(f"{Colors.CYAN}Ola! Sou seu assistente financeiro junior.{Colors.END}")
    print(f"{Colors.CYAN}Posso consultar precos, comparar acoes e simular investimentos.{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Comandos:{Colors.END}")
    print(f"  - Digite sua pergunta normalmente")
    print(f"  - 'limpar' - Limpa memoria da conversa")
    print(f"  - 'memoria' - Status da memoria")
    print(f"  - 'config' - Mostra configuracoes")
    print(f"  - 'sair' - Encerra\n")
    
    print(f"{Colors.GREEN}Exemplos:{Colors.END}")
    print(f"  - Quanto esta a Petrobras?")
    print(f"  - Compare Itau e Bradesco")
    print(f"  - Simule 10 mil em Vale por 12 meses\n")
    
    # Mostrar modelo
    try:
        settings = get_settings()
        print(f"{Colors.BLUE}Modelo: {settings.model}{Colors.END}")
    except ValueError:
        pass
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_log(log: ExecutionLog) -> None:
    """
    Exibe um log de execucao formatado.
    
    Args:
        log: Log de execucao do agente
    """
    if log.type == "action":
        print(f"\n{Colors.YELLOW}[ACAO]{Colors.END} Usando: {Colors.BOLD}{log.tool}{Colors.END}")
        if log.args:
            print(f"  -> Args: {log.args}")
    
    elif log.type == "observation":
        print(f"{Colors.CYAN}[OBSERVACAO]{Colors.END} Dados obtidos")
    
    elif log.type == "error":
        print(f"{Colors.RED}[ERRO]{Colors.END} {log.content}")


def print_config() -> None:
    """Exibe configuracoes atuais."""
    try:
        settings = get_settings()
        print(f"\n{Colors.BLUE}Configuracoes atuais:{Colors.END}")
        for key, value in settings.to_dict().items():
            print(f"  - {key}: {value}")
        print()
    except ValueError as e:
        print(f"{Colors.RED}Erro: {e}{Colors.END}\n")


# =============================================================================
# LOOP PRINCIPAL
# =============================================================================

def run_cli() -> None:
    """
    Executa o loop principal da CLI.
    
    Fluxo:
    1. Valida configuracao (API key)
    2. Exibe cabecalho
    3. Loop aguardando input
    4. Processa comandos especiais ou executa agente
    5. Exibe resultado formatado
    """
    # Validar API key
    if not validate_api_key():
        print(f"{Colors.RED}ERRO: OPENAI_API_KEY nao configurada!{Colors.END}")
        print(f"\n{Colors.YELLOW}Por favor:{Colors.END}")
        print(f"1. Copie env.example para .env")
        print(f"2. Adicione sua chave: OPENAI_API_KEY=sk-...")
        print(f"3. Execute novamente\n")
        return
    
    # Exibir cabecalho
    print_header()
    
    # Gerar session_id unico para esta sessao do CLI
    # Formato: cli-YYYYMMDD-HHMMSS-UUID[:8]
    session_id = f"cli-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    print(f"{Colors.BLUE}Session ID: {session_id}{Colors.END}\n")
    
    # Obter memoria global
    memory = get_global_memory()
    
    # Loop principal
    while True:
        try:
            # Input do usuario
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}Voce:{Colors.END} ").strip()
            
            # Comandos especiais
            if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                print(f"\n{Colors.CYAN}Ate logo! Bons investimentos!{Colors.END}\n")
                break
            
            if user_input.lower() in ['limpar', 'clear']:
                clear_global_memory()
                memory = get_global_memory()
                print(f"\n{Colors.GREEN}Memoria limpa!{Colors.END}\n")
                continue
            
            if user_input.lower() in ['memoria', 'memory']:
                print(f"\n{Colors.BLUE}{memory.get_summary()}{Colors.END}\n")
                continue
            
            if user_input.lower() in ['config', 'configuracao']:
                print_config()
                continue
            
            if not user_input:
                continue
            
            # Executar agente
            print(f"\n{Colors.BLUE}[PENSANDO]{Colors.END} Processando...")
            
            response = run_agent(user_input, memory=memory, session_id=session_id)
            
            # Exibir logs (exceto answer)
            for log in response.logs:
                if log.type != "answer":
                    print_log(log)
            
            # Exibir resposta
            print(f"\n{Colors.BOLD}{Colors.GREEN}Analista:{Colors.END} {response.answer}\n")
            print(f"{Colors.BOLD}{'-'*60}{Colors.END}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}Interrompido. Ate logo!{Colors.END}\n")
            break
        
        except Exception as e:
            print(f"\n{Colors.RED}Erro: {e}{Colors.END}\n")
            print(f"{Colors.YELLOW}Tente novamente ou 'sair' para encerrar.{Colors.END}\n")
