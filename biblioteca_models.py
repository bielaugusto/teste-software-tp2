class Pessoa:
    def __init__(self, nome, email):
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome inválido")
        if not email or "@" not in email:
            raise ValueError("Email inválido")
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"{self.nome} ({self.email})"

    def get_info(self):
        return {"nome": self.nome, "email": self.email}

class Autor(Pessoa):
    def __init__(self, nome, email, biografia=""):
        super().__init__(nome, email)
        self.biografia = biografia
        self.livros_publicados = []

    def adicionar_livro_publicado(self, livro_titulo):
        if not livro_titulo or not isinstance(livro_titulo, str):
            raise ValueError("Título do livro inválido")
        self.livros_publicados.append(livro_titulo)

    def get_biografia(self):
        return self.biografia

class Usuario(Pessoa):
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email)
        if not matricula or not isinstance(matricula, str):
            raise ValueError("Matrícula inválida")
        self.matricula = matricula
        self.livros_emprestados = []

    def __str__(self):
        return f"Usuário: {self.nome}, Matrícula: {self.matricula}"

    def pegar_livro_emprestado(self, livro):
        if livro.esta_disponivel():
            self.livros_emprestados.append(livro)
            livro.emprestar()
            return True
        return False

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            self.livros_emprestados.remove(livro)
            livro.devolver()
            return True
        return False

class ItemBibliografico:
    def __init__(self, titulo, ano_publicacao):
        if not titulo or not isinstance(titulo, str):
            raise ValueError("Título inválido")
        if not isinstance(ano_publicacao, int) or ano_publicacao <= 0:
            raise ValueError("Ano de publicação inválido")
        self.titulo = titulo
        self.ano_publicacao = ano_publicacao

    def get_titulo(self):
        return self.titulo

    def get_ano_publicacao(self):
        return self.ano_publicacao

class Livro(ItemBibliografico):
    def __init__(self, titulo, ano_publicacao, isbn, autor, genero="Não especificado"):
        super().__init__(titulo, ano_publicacao)
        if not isbn or not isinstance(isbn, str): # Simplificado, ISBN tem validação mais complexa
            raise ValueError("ISBN inválido")
        if not isinstance(autor, Autor):
            raise TypeError("Autor inválido")
        self.isbn = isbn
        self.autor = autor
        self.genero = genero
        self._disponivel = True

    def __str__(self):
        return f"'{self.titulo}' por {self.autor.nome}, ISBN: {self.isbn}"

    def esta_disponivel(self):
        return self._disponivel

    def emprestar(self):
        if self._disponivel:
            self._disponivel = False
            return True
        return False

    def devolver(self):
        self._disponivel = True

    def get_autor_nome(self):
        return self.autor.nome

class Revista(ItemBibliografico):
    def __init__(self, titulo, ano_publicacao, edicao, editora):
        super().__init__(titulo, ano_publicacao)
        self.edicao = edicao
        self.editora = editora

    def __str__(self):
        return f"Revista: {self.titulo}, Edição: {self.edicao}, Editora: {self.editora}"

    def get_editora(self):
        return self.editora

class DVD(ItemBibliografico):
    def __init__(self, titulo, ano_publicacao, duracao_minutos, diretor):
        super().__init__(titulo, ano_publicacao)
        if not isinstance(duracao_minutos, int) or duracao_minutos <=0:
            raise ValueError("Duração inválida")
        self.duracao_minutos = duracao_minutos
        self.diretor = diretor

    def get_duracao(self):
        return self.duracao_minutos

class Emprestimo:
    def __init__(self, usuario, item, data_emprestimo, data_devolucao_prevista):
        if not isinstance(usuario, Usuario):
            raise TypeError("Usuário inválido")
        if not isinstance(item, (Livro, DVD)): # Revistas podem não ser emprestáveis
            raise TypeError("Item inválido para empréstimo")
        self.usuario = usuario
        self.item = item
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista
        self.devolvido = False

    def registrar_devolucao(self, data_devolucao_real):
        self.devolvido = True
        self.item.devolver() 
        return f"Item {self.item.get_titulo()} devolvido por {self.usuario.nome} em {data_devolucao_real}."

    def esta_atrasado(self, data_atual):
        return not self.devolvido and data_atual > self.data_devolucao_prevista

class Biblioteca:
    def __init__(self, nome):
        self.nome = nome
        self.catalogo = []
        self.usuarios_registrados = []
        self.emprestimos_ativos = []

    def adicionar_item_catalogo(self, item):
        if not isinstance(item, ItemBibliografico):
            raise TypeError("Só é possível adicionar Itens Bibliográficos ao catálogo.")
        self.catalogo.append(item)

    def remover_item_catalogo(self, item_titulo):
        item_encontrado = self.buscar_item_por_titulo(item_titulo)
        if item_encontrado:
            self.catalogo.remove(item_encontrado)
            return True
        return False

    def registrar_usuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Só é possível registrar Usuários.")
        if any(u.matricula == usuario.matricula for u in self.usuarios_registrados):
            raise ValueError("Usuário com esta matrícula já registrado.")
        self.usuarios_registrados.append(usuario)

    def buscar_item_por_titulo(self, titulo):
        for item in self.catalogo:
            if item.get_titulo().lower() == titulo.lower():
                return item
        return None

    def buscar_usuario_por_matricula(self, matricula):
        for usuario in self.usuarios_registrados:
            if usuario.matricula == matricula:
                return usuario
        return None

    def realizar_emprestimo(self, matricula_usuario, titulo_item, data_emprestimo, data_devolucao_prevista):
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        item = self.buscar_item_por_titulo(titulo_item)

        if not usuario:
            return "Usuário não encontrado."
        if not item:
            return "Item não encontrado no catálogo."
        if not isinstance(item, (Livro, DVD)): # Exemplo: Revistas não podem ser emprestadas
            return "Este tipo de item não pode ser emprestado."
        if not item.esta_disponivel():
            return f"Item '{item.get_titulo()}' não está disponível para empréstimo."

        if usuario.pegar_livro_emprestado(item):
            novo_emprestimo = Emprestimo(usuario, item, data_emprestimo, data_devolucao_prevista)
            self.emprestimos_ativos.append(novo_emprestimo)
            return f"Empréstimo de '{item.get_titulo()}' para '{usuario.nome}' realizado com sucesso."
        else:
            return "Falha ao realizar empréstimo (verificar disponibilidade)."

    def registrar_devolucao_item(self, matricula_usuario, titulo_item, data_devolucao_real):
        emprestimo_ativo = None
        for emp in self.emprestimos_ativos:
            if emp.usuario.matricula == matricula_usuario and \
               emp.item.get_titulo() == titulo_item and \
               not emp.devolvido:
                emprestimo_ativo = emp
                break
        
        if not emprestimo_ativo:
            return "Empréstimo não encontrado ou já devolvido."

        usuario = emprestimo_ativo.usuario
        item = emprestimo_ativo.item
        
        usuario.devolver_livro(item) 
        
        return emprestimo_ativo.registrar_devolucao(data_devolucao_real)

class ConfiguracaoBiblioteca:
    def __init__(self, max_livros_por_usuario=5, dias_emprestimo_padrao=14):
        self.max_livros_por_usuario = max_livros_por_usuario
        self.dias_emprestimo_padrao = dias_emprestimo_padrao

    def get_max_livros_por_usuario(self):
        return self.max_livros_por_usuario

    def set_max_livros_por_usuario(self, novo_maximo):
        if not isinstance(novo_maximo, int) or novo_maximo < 0:
            raise ValueError("Número máximo de livros inválido.")
        self.max_livros_por_usuario = novo_maximo