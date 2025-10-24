# Controle Uber

Aplicação GUI moderna para controle de ganhos e despesas com Uber, usando SQLite para armazenamento local.

## Funcionalidades

- **Lançamentos**: Adicionar corridas (receitas) e abastecimentos (despesas) com interface intuitiva.
- **Resumo mensal**: Visualizar estatísticas detalhadas com emojis e formatação clara.
- **Exportar CSV**: Salvar dados mensais em arquivo CSV.
- **Interface moderna**: Tema 'clam', tooltips, ícones emoji, cores suaves e layout responsivo.

## Estrutura do Projeto

```
controle_uber/
├── __init__.py      # Exposição do pacote
├── app.py           # Classe principal da GUI
├── db.py            # Conexão e inicialização do banco SQLite
├── utils.py         # Funções utilitárias (datas, formatação)
├── ControleUber.py  # Ponto de entrada principal
├── README.md        # Este arquivo
└── requirements.txt # Dependências Python
```

## Como Executar

### Pré-requisitos

- Python 3.6 ou superior instalado.
- Tkinter (geralmente incluído no Python padrão).

### Passos

1. **Instalar dependências** (opcional, se houver):
   ```
   pip install -r requirements.txt
   ```

2. **Executar a aplicação**:
   - Abra o terminal no diretório `controle_uber`.
   - Execute:
     ```
     python -m controle_uber.ControleUber
     ```

   Ou diretamente:
   ```
   python ControleUber.py
   ```

3. **Executar o .exe (portátil)**:
   - O arquivo `ControleUber.exe` foi criado na pasta `dist/`.
   - Copie `ControleUber.exe` para qualquer computador Windows com Python instalado (ou use o .exe standalone).
   - Execute clicando duas vezes ou via terminal: `ControleUber.exe`.
   - O banco `controle_uber.db` será criado automaticamente na mesma pasta do .exe.

3. **Usar a aplicação**:
   - Na aba "Lançamentos", adicione corridas e abastecimentos.
   - Na aba "Resumo", selecione mês/ano e visualize estatísticas.
   - Exporte dados mensais para CSV se necessário.

## Banco de Dados

O aplicativo cria automaticamente um arquivo `controle_uber.db` (SQLite) na mesma pasta. Não é necessário configurar nada adicional.

## Desenvolvimento

Para modificar o código:
- `app.py`: Contém a interface gráfica e lógica de negócio.
- `db.py`: Gerencia a conexão com o banco.
- `utils.py`: Funções auxiliares para datas e formatação.

Teste mudanças executando `python ControleUber.py` e verificando se a aplicação abre corretamente.