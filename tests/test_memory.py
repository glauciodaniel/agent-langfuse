"""
Testes para o modulo de memoria.

Estes testes NAO requerem API da OpenAI.
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.memory import ConversationMemory, get_global_memory, clear_global_memory


def test_memory_creation():
    """Testa criacao de memoria vazia."""
    memory = ConversationMemory()
    assert len(memory) == 0


def test_memory_add_messages():
    """Testa adicao de mensagens."""
    memory = ConversationMemory()
    memory.add_user_message("Ola")
    memory.add_assistant_message("Oi!")
    assert len(memory) == 2


def test_memory_max_limit():
    """Testa limite de mensagens."""
    memory = ConversationMemory(max_messages=5)
    
    for i in range(10):
        memory.add_user_message(f"Mensagem {i}")
    
    assert len(memory) <= 5


def test_memory_clear():
    """Testa limpeza de memoria."""
    memory = ConversationMemory()
    memory.add_user_message("Teste")
    memory.add_assistant_message("Resposta")
    
    memory.clear()
    assert len(memory) == 0


def test_memory_get_messages():
    """Testa obtencao de copia das mensagens."""
    memory = ConversationMemory()
    memory.add_user_message("Teste")
    
    messages = memory.get_messages()
    assert len(messages) == 1
    
    # Modificar copia nao afeta original
    messages.append("Extra")
    assert len(memory) == 1


def test_global_memory():
    """Testa memoria global singleton."""
    clear_global_memory()
    
    memory1 = get_global_memory()
    memory1.add_user_message("Teste")
    
    memory2 = get_global_memory()
    assert len(memory2) == 1  # Mesma instancia
    
    clear_global_memory()
    memory3 = get_global_memory()
    assert len(memory3) == 0  # Limpa


if __name__ == "__main__":
    tests = [
        test_memory_creation,
        test_memory_add_messages,
        test_memory_max_limit,
        test_memory_clear,
        test_memory_get_messages,
        test_global_memory,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"[PASSOU] {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FALHOU] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERRO] {test.__name__}: {e}")
            failed += 1
    
    print(f"\nTotal: {passed} passaram, {failed} falharam")
