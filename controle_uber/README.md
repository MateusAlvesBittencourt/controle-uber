# Controle Uber

Aplicação GUI moderna para controle de ganhos e despesas com Uber, desenvolvida em Python com Tkinter e SQLite. Permite lançar corridas (receitas) e abastecimentos (despesas), visualizar resumos mensais e exportar dados para CSV.

## Funcionalidades

- **📝 Lançamentos**: Adicionar corridas (receitas) e abastecimentos (despesas) com validação de dados.
- **📊 Resumo mensal**: Estatísticas detalhadas como receita, lucro, quilômetros, litros, etc., com cálculo automático de metas.
- **📄 Exportar CSV**: Salvar relatórios mensais em formato CSV para análise externa.
- **🎨 Interface moderna**: Tema 'clam', tooltips informativos, ícones emoji, layout responsivo e cores suaves.
- **💾 Banco de dados local**: SQLite automático, sem necessidade de configuração externa.
- **🚀 Executável standalone**: .exe portátil para Windows, sem instalar Python.

## Estrutura do Projeto

```
controle_uber/
├── __init__.py          # Inicialização do pacote
├── app.py               # Classe principal da interface gráfica (GUI)
├── db.py                # Gerenciamento do banco de dados SQLite
├── utils.py             # Funções utilitárias (datas, formatação, cálculos)
├── ControleUber.py      # Ponto de entrada principal (launcher)
├── launcher.py          # Script alternativo para execução
├── README.md            # Este arquivo de documentação
├── requirements.txt     # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
└── dist/                # Pasta gerada com o executável (.exe)
    └── ControleUber.exe # Executável standalone
```

## Pré-requisitos

- **Python 3.6+** (para desenvolvimento/execução via código)
- **Tkinter** (incluído na maioria das instalações Python)
- **Git** (opcional, para versionamento)

## Instalação e Execução

### Opção 1: Executar via Código Fonte (Desenvolvimento)

1. **Clone ou baixe o repositório**:
   ```bash
   git clone https://github.com/MateusAlvesBittencourt/controle-uber.git
   cd controle-uber
   ```

2. **Instale dependências** (opcional, pois usa bibliotecas padrão):
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**:
   ```bash
   python -m controle_uber.ControleUber
   ```
   Ou:
   ```bash
   python ControleUber.py
   ```

### Opção 2: Executar o .exe Standalone (Usuário Final)

1. **Baixe o .exe**:
   - Vá para [Releases](https://github.com/MateusAlvesBittencourt/controle-uber/releases) no GitHub.
   - Baixe `ControleUber.exe` (ou gere você mesmo, veja abaixo).

2. **Execute**:
   - Clique duas vezes em `ControleUber.exe`.
   - Ou via terminal: `ControleUber.exe`

O banco `controle_uber.db` será criado automaticamente na mesma pasta do .exe.

## Como Criar o .exe (Empacotamento)

Para gerar o executável standalone:

1. **Instale PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Gere o .exe**:
   ```bash
   cd controle_uber
   pyinstaller --onefile --windowed launcher.py --hidden-import tkinter --hidden-import sqlite3 --name ControleUber
   ```

3. **Localização do .exe**:
   - O arquivo `ControleUber.exe` será criado em `controle_uber/dist/`.
   - Copie para qualquer pasta ou distribua.

**Nota**: O `--windowed` evita mostrar a janela do console. Para incluir dados existentes no .exe, use `--add-data "controle_uber.db;."`.

## Como Usar a Aplicação

1. **Aba "Lançamentos"**:
   - Adicione corridas: Data, valor (R$), quilômetros.
   - Adicione abastecimentos: Data, litros, preço por litro.
   - Exclua itens selecionados na tabela.

2. **Aba "Resumo"**:
   - Selecione mês e ano.
   - Visualize estatísticas: receita, gastos, lucro, etc.
   - Exporte dados mensais para CSV.

3. **Banco de Dados**:
   - Arquivo `controle_uber.db` (SQLite) na pasta do executável.
   - Dados persistem entre execuções.

## Desenvolvimento

### Modificar o Código
- `app.py`: Interface gráfica e lógica de negócio.
- `db.py`: Conexão e queries do banco.
- `utils.py`: Funções auxiliares.

### Testar Mudanças
```bash
python ControleUber.py
```

### Contribuir
1. Fork o repositório.
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`.
3. Commit: `git commit -m "Adiciona nova funcionalidade"`.
4. Push: `git push origin feature/nova-funcionalidade`.
5. Abra um Pull Request.

## Tecnologias Utilizadas

- **Python 3**: Linguagem principal.
- **Tkinter**: Interface gráfica.
- **SQLite**: Banco de dados local.
- **PyInstaller**: Empacotamento para .exe.

## Licença

Este projeto é open-source. Sinta-se à vontade para usar e modificar.

## Suporte

Para dúvidas ou bugs, abra uma issue no [GitHub](https://github.com/MateusAlvesBittencourt/controle-uber/issues).

---

**Desenvolvido por Mateus Alves Bittencourt** 🚗💨