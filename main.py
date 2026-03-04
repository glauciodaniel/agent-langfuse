#!/usr/bin/env python3
"""
O Analista Junior - Agente Financeiro Cognitivo

Ponto de entrada da aplicacao.

Conceito Didatico - Entry Point Limpo:
    O main.py deve ser simples e apenas "ligar os fios".
    Toda a logica fica nos modulos especificos.
"""

from adapters.cli import run_cli

if __name__ == "__main__":
    run_cli()
