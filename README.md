# RH PM - Sistema de Gestão de Funcionários

Sistema CRUD em Python para gerenciamento de funcionários e departamentos com interfaces CLI e GUI.

## Execução

**Interface Gráfica (Recomendada):**
```bash
python main.py
```

**Interface CLI:**
```bash
python main.py cli
```

## Pré-requisitos

- Python 3.7+
- Pillow (instalado automaticamente)

```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
app/
├── bd/          # Banco de dados SQLite
├── models/      # Entidades (Funcionário, Departamento)
├── controllers/ # Lógica de negócio
└── views/       # Interfaces (CLI e GUI)
main.py          # Ponto de entrada
```

## Funcionalidades

### Funcionários
- Criar, editar, listar, remover
- Vincular a departamentos
- Filtrar por nome/cargo
- Status ativo/inativo

### Departamentos
- Criar, editar, listar, remover
- Proteção contra remoção com funcionários vinculados

### Interface Gráfica
- Interface moderna com Tkinter
- Filtros em tempo real
- Carregar bancos externos
- Zerar banco com confirmação
- Formatação de salários

## Banco de Exemplo

O projeto inclui um arquivo `rhPM_populado.db` com dados de exemplo (3 departamentos e 6 funcionários). Use o botão **"Carregar Banco"** na GUI para selecioná-lo.

## Entrega

## Entrega

**Arquivos necessários:**
- `app/` (código fonte)
- `main.py`
- `README.md`
- `requirements.txt`
- `rhPM_populado.db` (banco de exemplo)