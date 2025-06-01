# Teste e Manutenção de Software - Trabalho Prático 2  
## Sistema de Gerenciamento de Biblioteca Simplificado

Este repositório contém o desenvolvimento do **Trabalho Prático 2** da disciplina **Teste e Manutenção de Software**, ministrada pelo professor **Pedro Felipe**, na **Pontifícia Universidade Católica de Minas Gerais (PUC Minas)**.

O principal objetivo do trabalho foi desenvolver um sistema de software, criar casos de teste para ele e analisar a cobertura desses testes, aplicando os conceitos aprendidos em aula.

---

## Sobre o Sistema

O software implementado é um **Sistema de Gerenciamento de Biblioteca Simplificado**, que permite executar operações básicas como:

- Adicionar novos itens ao catálogo (livros, revistas, DVDs);
- Listar e buscar itens no catálogo;
- Remover itens do catálogo;
- Registrar novos usuários;
- Listar e buscar usuários;
- Realizar empréstimos de itens;
- Registrar devoluções;
- Listar empréstimos ativos;
- Visualizar e alterar configurações básicas da biblioteca (ex: máximo de livros por usuário).

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.x  
- **Testes Unitários:** `unittest` (módulo padrão do Python)  
- **Cobertura de Testes:** `coverage.py`

---

## Estrutura do Projeto
```bash
.
├── .coverage              # Arquivo gerado pelo coverage.py após a execução dos testes
├── README.md              # Este arquivo de descrição
├── Trabalho_pratico_p2.pdf  # Relatório detalhado do trabalho
├── biblioteca_models.py   # Classes do domínio da biblioteca
├── main.py                # Interface de linha de comando (CLI)
└── test_biblioteca.py     # Casos de teste unitários
```

**Descrição dos arquivos:**

- `biblioteca_models.py`: Define as classes principais (`Livro`, `Usuario`, `Biblioteca`, `Emprestimo`, etc.) e suas regras de negócio.
- `main.py`: Ponto de entrada do sistema, permitindo interação via terminal.
- `test_biblioteca.py`: Contém os testes desenvolvidos com `unittest` para validar as funcionalidades do sistema.
- `Trabalho_pratico_p2.pdf`: Documento com a descrição do trabalho, análise da cobertura, decisões de projeto e demais informações.
- `.coverage`: Arquivo binário gerado automaticamente pela ferramenta `coverage.py`.

---

## Como Executar

### Pré-requisitos

- Python 3.x instalado  
- Biblioteca `coverage` instalada (para análise de cobertura de testes). Instale com:

```bash
pip install coverage
```
### Executando a Aplicação
Para rodar o sistema via console:

```bash
python main.py
```

### Executando os Testes Unitários
Para executar a suíte de testes:

```bash
python -m unittest test_biblioteca.py
```

Ou, alternativamente:
```bash
python test_biblioteca.py
```

### Verificando a Cobertura dos Testes

1. Rode os testes com coleta de cobertura:
```bash
coverage run -m unittest test_biblioteca.py
```

2. Gere o relatório no terminal:
```bash
coverage report -m biblioteca_models.py
```

3. Gere um relatório em HTML(opcional):
```bash
python -m coverage html
```
Depois, abra o arquivo htmlcov/index.html no navegador para visualizar o relatório completo.

---

## Relatório do Trabalho
Para mais detalhes sobre o desenvolvimento, os critérios atendidos, a análise de cobertura e as decisões técnicas, consulte o documento:

<a href="Trabalho_pratico_p2.pdf">Trabalho_pratico_p2</a>

---

## Desenvolvido por
- Arthur Henrique de Oliveira Acácio
- Bernardo Silva Oliveira, Daniel Henrique Bicalho Dias
- Diogo Augusto Magalhães Marques
- Gabriel Augusto Lana Vidal
- Gustavo Meira Becattini
- Hebert Tadeu de Castro Liberato


