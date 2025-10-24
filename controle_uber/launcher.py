#!/usr/bin/env python3
"""
Launcher para Controle Uber - executa a aplicação.
"""

import sys
import os

# Adicionar o diretório atual ao sys.path para encontrar o módulo controle_uber
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from controle_uber import App
    if __name__ == "__main__":
        App().mainloop()
except Exception as e:
    print(f"Erro ao executar: {e}")
    input("Pressione Enter para sair...")