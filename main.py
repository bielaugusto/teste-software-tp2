from biblioteca_models import (
    Pessoa, Autor, Usuario, ItemBibliografico, Livro, Revista, DVD,
    Emprestimo, Biblioteca, ConfiguracaoBiblioteca
)
from datetime import datetime, timedelta

def exibir_menu():

    print("\n--- Sistema de Gerenciamento de Biblioteca ---")
    print("1. Adicionar Livro ao Catálogo")
    print("2. Adicionar Revista ao Catálogo")
    print("3. Adicionar DVD ao Catálogo")
    print("4. Listar Todos os Itens do Catálogo")
    print("5. Buscar Item por Título")
    print("6. Remover Item do Catálogo")
    print("-------------------------------------------")
    print("7. Registrar Novo Usuário")
    print("8. Listar Usuários Registrados")
    print("9. Buscar Usuário por Matrícula")
    print("-------------------------------------------")
    print("10. Realizar Empréstimo")
    print("11. Registrar Devolução")
    print("12. Listar Empréstimos Ativos")
    print("-------------------------------------------")
    print("13. Ver Configurações da Biblioteca")
    print("14. Alterar Máximo de Livros por Usuário (Config.)")
    print("-------------------------------------------")
    print("0. Sair")
    print("-------------------------------------------")

def adicionar_livro(biblioteca):
    print("\n--- Adicionar Novo Livro ---")
    try:
        titulo = input("Título do Livro: ")
        ano = int(input("Ano de Publicação: "))
        isbn = input("ISBN: ")
        nome_autor = input("Nome do Autor: ")
        email_autor = input("Email do Autor: ")
        bio_autor = input("Biografia do Autor (opcional): ")
        genero = input("Gênero (opcional): ")

        autor = Autor(nome_autor, email_autor, bio_autor)
        livro = Livro(titulo, ano, isbn, autor, genero if genero else "Não especificado")
        biblioteca.adicionar_item_catalogo(livro)
        print(f"Livro '{titulo}' adicionado com sucesso!")
    except ValueError as e:
        print(f"Erro ao adicionar livro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def adicionar_revista(biblioteca):
    print("\n--- Adicionar Nova Revista ---")
    try:
        titulo = input("Título da Revista: ")
        ano = int(input("Ano de Publicação: "))
        edicao = input("Edição: ")
        editora = input("Editora: ")

        revista = Revista(titulo, ano, edicao, editora)
        biblioteca.adicionar_item_catalogo(revista)
        print(f"Revista '{titulo}' adicionada com sucesso!")
    except ValueError as e:
        print(f"Erro ao adicionar revista: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def adicionar_dvd(biblioteca):
    print("\n--- Adicionar Novo DVD ---")
    try:
        titulo = input("Título do DVD: ")
        ano = int(input("Ano de Lançamento: "))
        duracao = int(input("Duração (minutos): "))
        diretor = input("Diretor: ")

        dvd = DVD(titulo, ano, duracao, diretor)
        biblioteca.adicionar_item_catalogo(dvd)
        print(f"DVD '{titulo}' adicionado com sucesso!")
    except ValueError as e:
        print(f"Erro ao adicionar DVD: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def listar_itens_catalogo(biblioteca):
    print("\n--- Catálogo da Biblioteca ---")
    if not biblioteca.catalogo:
        print("Nenhum item no catálogo.")
        return
    for i, item in enumerate(biblioteca.catalogo):
        print(f"{i+1}. {item}")
        if isinstance(item, Livro):
            print(f"   Disponível: {'Sim' if item.esta_disponivel() else 'Não'}")

def buscar_item(biblioteca):
    print("\n--- Buscar Item por Título ---")
    titulo_busca = input("Digite o título do item: ")
    item = biblioteca.buscar_item_por_titulo(titulo_busca)
    if item:
        print("Item encontrado:")
        print(item)
        if isinstance(item, Livro):
             print(f"   Disponível: {'Sim' if item.esta_disponivel() else 'Não'}")
    else:
        print(f"Item com título '{titulo_busca}' não encontrado.")

def remover_item(biblioteca):
    print("\n--- Remover Item do Catálogo ---")
    titulo_remove = input("Digite o título do item a ser removido: ")
    if biblioteca.remover_item_catalogo(titulo_remove):
        print(f"Item '{titulo_remove}' removido com sucesso.")
    else:
        print(f"Item '{titulo_remove}' não encontrado ou não pôde ser removido.")

def registrar_usuario(biblioteca):
    print("\n--- Registrar Novo Usuário ---")
    try:
        nome = input("Nome do Usuário: ")
        email = input("Email do Usuário: ")
        matricula = input("Matrícula do Usuário: ")

        usuario = Usuario(nome, email, matricula)
        biblioteca.registrar_usuario(usuario)
        print(f"Usuário '{nome}' registrado com sucesso!")
    except ValueError as e:
        print(f"Erro ao registrar usuário: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def listar_usuarios(biblioteca):
    print("\n--- Usuários Registrados ---")
    if not biblioteca.usuarios_registrados:
        print("Nenhum usuário registrado.")
        return
    for i, usuario in enumerate(biblioteca.usuarios_registrados):
        print(f"{i+1}. {usuario}")

def buscar_usuario(biblioteca):
    print("\n--- Buscar Usuário por Matrícula ---")
    matricula_busca = input("Digite a matrícula do usuário: ")
    usuario = biblioteca.buscar_usuario_por_matricula(matricula_busca)
    if usuario:
        print("Usuário encontrado:")
        print(usuario)
    else:
        print(f"Usuário com matrícula '{matricula_busca}' não encontrado.")

def realizar_emprestimo(biblioteca, config_biblioteca):
    print("\n--- Realizar Empréstimo ---")
    matricula_usuario = input("Matrícula do Usuário: ")
    titulo_item = input("Título do Item a ser emprestado: ")
    
    # Data de empréstimo e devolução (simplificado)
    data_emprestimo_str = datetime.now().strftime("%Y-%m-%d")
    data_devolucao_prevista_str = (datetime.now() + timedelta(days=config_biblioteca.dias_emprestimo_padrao)).strftime("%Y-%m-%d")
    
    print(f"Data do Empréstimo: {data_emprestimo_str}")
    print(f"Data Prevista para Devolução: {data_devolucao_prevista_str}")

    resultado = biblioteca.realizar_emprestimo(matricula_usuario, titulo_item, data_emprestimo_str, data_devolucao_prevista_str)
    print(resultado)

def registrar_devolucao(biblioteca):
    print("\n--- Registrar Devolução ---")
    matricula_usuario = input("Matrícula do Usuário que está devolvendo: ")
    titulo_item = input("Título do Item devolvido: ")
    data_devolucao_real_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Data da Devolução: {data_devolucao_real_str}")

    resultado = biblioteca.registrar_devolucao_item(matricula_usuario, titulo_item, data_devolucao_real_str)
    print(resultado)

def listar_emprestimos_ativos(biblioteca):
    print("\n--- Empréstimos Ativos ---")
    ativos = [emp for emp in biblioteca.emprestimos_ativos if not emp.devolvido]
    if not ativos:
        print("Nenhum empréstimo ativo no momento.")
        return
    for i, emprestimo in enumerate(ativos):
        print(f"{i+1}. Usuário: {emprestimo.usuario.nome} ({emprestimo.usuario.matricula})")
        print(f"   Item: {emprestimo.item.get_titulo()}")
        print(f"   Data Empréstimo: {emprestimo.data_emprestimo}")
        print(f"   Devolução Prevista: {emprestimo.data_devolucao_prevista}")
        if emprestimo.esta_atrasado(datetime.now().strftime("%Y-%m-%d")):
            print("   Status: ATRASADO")
        print("-" * 20)

def ver_configuracoes(config_biblioteca):
    print("\n--- Configurações da Biblioteca ---")
    print(f"Máximo de livros por usuário: {config_biblioteca.get_max_livros_por_usuario()}")
    print(f"Dias de empréstimo padrão: {config_biblioteca.dias_emprestimo_padrao}")

def alterar_max_livros(config_biblioteca):
    print("\n--- Alterar Máximo de Livros por Usuário ---")
    try:
        novo_maximo = int(input(f"Novo valor para máximo de livros por usuário (atual: {config_biblioteca.get_max_livros_por_usuario()}): "))
        config_biblioteca.set_max_livros_por_usuario(novo_maximo)
        print("Máximo de livros alterado com sucesso!")
    except ValueError as e:
        print(f"Erro ao alterar configuração: {e}")


if __name__ == "__main__":
    minha_biblioteca = Biblioteca("Biblioteca Comunitária")
    config = ConfiguracaoBiblioteca() # Configurações padrão

    # dados iniciais para teste rápido
    try:
        autor1 = Autor("J.R.R. Tolkien", "tolkien@example.com")
        livro1 = Livro("O Senhor dos Anéis", 1954, "978-0618260274", autor1, "Fantasia")
        minha_biblioteca.adicionar_item_catalogo(livro1)

        autor2 = Autor("George Orwell", "orwell@example.com")
        livro2 = Livro("1984", 1949, "978-0451524935", autor2, "Distopia")
        minha_biblioteca.adicionar_item_catalogo(livro2)
        
        usuario1 = Usuario("Alice Wonderland", "alice@example.com", "USR001")
        minha_biblioteca.registrar_usuario(usuario1)
    except Exception as e:
        print(f"Erro ao popular dados iniciais: {e}")


    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_livro(minha_biblioteca)
        elif escolha == '2':
            adicionar_revista(minha_biblioteca)
        elif escolha == '3':
            adicionar_dvd(minha_biblioteca)
        elif escolha == '4':
            listar_itens_catalogo(minha_biblioteca)
        elif escolha == '5':
            buscar_item(minha_biblioteca)
        elif escolha == '6':
            remover_item(minha_biblioteca)
        elif escolha == '7':
            registrar_usuario(minha_biblioteca)
        elif escolha == '8':
            listar_usuarios(minha_biblioteca)
        elif escolha == '9':
            buscar_usuario(minha_biblioteca)
        elif escolha == '10':
            realizar_emprestimo(minha_biblioteca, config)
        elif escolha == '11':
            registrar_devolucao(minha_biblioteca)
        elif escolha == '12':
            listar_emprestimos_ativos(minha_biblioteca)
        elif escolha == '13':
            ver_configuracoes(config)
        elif escolha == '14':
            alterar_max_livros(config)
        elif escolha == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione Enter para continuar...")