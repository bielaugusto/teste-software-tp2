import unittest
from biblioteca_models import (
    Pessoa, Autor, Usuario, ItemBibliografico, Livro, Revista, DVD,
    Emprestimo, Biblioteca, ConfiguracaoBiblioteca
)

class TestPessoa(unittest.TestCase):
    def test_criar_pessoa(self):
        p = Pessoa("Ana Silva", "ana@example.com")
        self.assertEqual(p.nome, "Ana Silva")
        self.assertEqual(p.email, "ana@example.com")

    def test_pessoa_info(self):
        p = Pessoa("Ana Silva", "ana@example.com")
        self.assertEqual(p.get_info(), {"nome": "Ana Silva", "email": "ana@example.com"})

    def test_pessoa_nome_invalido(self):
        with self.assertRaises(ValueError):
            Pessoa("", "ana@example.com")
        with self.assertRaises(ValueError):
            Pessoa(None, "ana@example.com")

    def test_pessoa_email_invalido(self):
        with self.assertRaises(ValueError):
            Pessoa("Ana", "anaexample.com")
        with self.assertRaises(ValueError):
            Pessoa("Ana", "")


class TestAutor(unittest.TestCase):
    def test_criar_autor(self):
        a = Autor("Carlos Z", "carlos@example.com", "Escritor famoso")
        self.assertEqual(a.nome, "Carlos Z")
        self.assertEqual(a.get_biografia(), "Escritor famoso")

    def test_autor_adicionar_livro(self):
        a = Autor("Carlos Z", "carlos@example.com")
        a.adicionar_livro_publicado("O Segredo")
        self.assertIn("O Segredo", a.livros_publicados)

    def test_autor_adicionar_livro_invalido(self):
        a = Autor("Carlos Z", "carlos@example.com")
        with self.assertRaises(ValueError):
            a.adicionar_livro_publicado("")


class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.autor = Autor("Test Autor", "autor@test.com")
        self.livro_disponivel = Livro("Livro Teste", 2023, "12345", self.autor)
        self.livro_indisponivel = Livro("Outro Livro", 2022, "67890", self.autor)
        self.livro_indisponivel.emprestar() # Torna indisponível
        self.usuario = Usuario("João Leitor", "joao@example.com", "MAT001")

    def test_criar_usuario(self):
        self.assertEqual(self.usuario.nome, "João Leitor")
        self.assertEqual(self.usuario.matricula, "MAT001")

    def test_usuario_pegar_livro_emprestado_sucesso(self):
        self.assertTrue(self.usuario.pegar_livro_emprestado(self.livro_disponivel))
        self.assertIn(self.livro_disponivel, self.usuario.livros_emprestados)
        self.assertFalse(self.livro_disponivel.esta_disponivel())

    def test_usuario_pegar_livro_emprestado_falha_indisponivel(self):
        self.assertFalse(self.usuario.pegar_livro_emprestado(self.livro_indisponivel))
        self.assertNotIn(self.livro_indisponivel, self.usuario.livros_emprestados)

    def test_usuario_devolver_livro(self):
        self.usuario.pegar_livro_emprestado(self.livro_disponivel)
        self.assertTrue(self.usuario.devolver_livro(self.livro_disponivel))
        self.assertNotIn(self.livro_disponivel, self.usuario.livros_emprestados)
        self.assertTrue(self.livro_disponivel.esta_disponivel())

    def test_usuario_devolver_livro_nao_emprestado(self):
        self.assertFalse(self.usuario.devolver_livro(self.livro_disponivel))


class TestItemBibliografico(unittest.TestCase):
    def test_criar_item(self):
        item = ItemBibliografico("Título Genérico", 2000)
        self.assertEqual(item.get_titulo(), "Título Genérico")
        self.assertEqual(item.get_ano_publicacao(), 2000)

    def test_item_titulo_invalido(self):
        with self.assertRaises(ValueError):
            ItemBibliografico("", 2000)

    def test_item_ano_invalido(self):
        with self.assertRaises(ValueError):
            ItemBibliografico("Título", 0)
        with self.assertRaises(ValueError):
            ItemBibliografico("Título", -1990)
        with self.assertRaises(ValueError):
            ItemBibliografico("Título", "abc")


class TestLivro(unittest.TestCase):
    def setUp(self):
        self.autor = Autor("Machado de Assis", "machado@abl.org.br")
        self.livro = Livro("Dom Casmurro", 1899, "978-85-359-0277-4", self.autor, "Romance")

    def test_criar_livro(self):
        self.assertEqual(self.livro.get_titulo(), "Dom Casmurro")
        self.assertEqual(self.livro.get_autor_nome(), "Machado de Assis")
        self.assertTrue(self.livro.esta_disponivel())

    def test_livro_emprestar_devolver(self):
        self.assertTrue(self.livro.emprestar())
        self.assertFalse(self.livro.esta_disponivel())
        self.assertFalse(self.livro.emprestar()) # Tentar emprestar de novo
        self.livro.devolver()
        self.assertTrue(self.livro.esta_disponivel())

    def test_livro_isbn_invalido(self):
        with self.assertRaises(ValueError):
            Livro("Titulo", 2000, "", self.autor)

    def test_livro_autor_invalido(self):
        with self.assertRaises(TypeError):
            Livro("Titulo", 2000, "123", "Não é um autor")


class TestRevista(unittest.TestCase):
    def test_criar_revista(self):
        revista = Revista("Superinteressante", 2023, "Edição 450", "Abril")
        self.assertEqual(revista.get_titulo(), "Superinteressante")
        self.assertEqual(revista.get_editora(), "Abril")


class TestDVD(unittest.TestCase):
    def test_criar_dvd(self):
        dvd = DVD("O Poderoso Chefão", 1972, 175, "Francis Ford Coppola")
        self.assertEqual(dvd.get_titulo(), "O Poderoso Chefão")
        self.assertEqual(dvd.get_duracao(), 175)

    def test_dvd_duracao_invalida(self):
        with self.assertRaises(ValueError):
            DVD("Filme", 2000, 0, "Diretor")
        with self.assertRaises(ValueError):
            DVD("Filme", 2000, -10, "Diretor")


class TestEmprestimo(unittest.TestCase):
    def setUp(self):
        self.autor = Autor("J.K. Rowling", "jk@hp.com")
        self.livro = Livro("Harry Potter", 1997, "123", self.autor)
        self.usuario = Usuario("Hermione", "hermione@hogwarts.com", "HOG001")
        self.emprestimo = Emprestimo(self.usuario, self.livro, "2023-01-01", "2023-01-15")

    def test_criar_emprestimo(self):
        self.assertEqual(self.emprestimo.usuario.nome, "Hermione")
        self.assertEqual(self.emprestimo.item.get_titulo(), "Harry Potter")
        self.assertFalse(self.emprestimo.devolvido)

    def test_emprestimo_registrar_devolucao(self):
        # Primeiro, o usuário precisa pegar o livro e o livro ser emprestado
        self.usuario.pegar_livro_emprestado(self.livro) # marca o livro como indisponível
        
        retorno = self.emprestimo.registrar_devolucao("2023-01-10")
        self.assertTrue(self.emprestimo.devolvido)
        self.assertTrue(self.livro.esta_disponivel()) # Livro deve estar disponível após devolução no empréstimo
        self.assertIn("devolvido por Hermione", retorno)

    def test_emprestimo_atrasado(self):
        self.assertFalse(self.emprestimo.esta_atrasado("2023-01-10"))
        self.assertTrue(self.emprestimo.esta_atrasado("2023-01-20"))
        self.emprestimo.devolvido = True
        self.assertFalse(self.emprestimo.esta_atrasado("2023-01-20")) # Não está atrasado se já devolvido


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca("Biblioteca Central")
        self.autor = Autor("George Orwell", "go@dystopian.com")
        self.livro1 = Livro("1984", 1949, "111", self.autor)
        self.livro2 = Livro("A Revolução dos Bichos", 1945, "222", self.autor)
        self.dvd1 = DVD("Matrix", 1999, 136, "Wachowskis")
        self.usuario1 = Usuario("Winston Smith", "winston@ex.com", "MINVER001")
        self.usuario2 = Usuario("Julia", "julia@ ex.com", "MINVER002")

        self.biblioteca.adicionar_item_catalogo(self.livro1)
        self.biblioteca.adicionar_item_catalogo(self.dvd1)
        self.biblioteca.registrar_usuario(self.usuario1)

    def test_adicionar_e_buscar_item(self):
        self.assertIsNotNone(self.biblioteca.buscar_item_por_titulo("1984"))
        self.assertIsNone(self.biblioteca.buscar_item_por_titulo("Livro Inexistente"))

    def test_remover_item_catalogo(self):
        self.assertTrue(self.biblioteca.remover_item_catalogo("1984"))
        self.assertIsNone(self.biblioteca.buscar_item_por_titulo("1984"))
        self.assertFalse(self.biblioteca.remover_item_catalogo("1984")) # Tentar remover de novo

    def test_registrar_e_buscar_usuario(self):
        self.assertIsNotNone(self.biblioteca.buscar_usuario_por_matricula("MINVER001"))
        self.assertIsNone(self.biblioteca.buscar_usuario_por_matricula("MAT999"))

    def test_registrar_usuario_duplicado(self):
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_usuario(Usuario("Winston Clone", "w2@oc.gov", "MINVER001"))

    def test_realizar_emprestimo_sucesso(self):
        resultado = self.biblioteca.realizar_emprestimo("MINVER001", "1984", "2023-03-10", "2023-03-24")
        self.assertIn("realizado com sucesso", resultado)
        self.assertFalse(self.livro1.esta_disponivel())
        self.assertEqual(len(self.biblioteca.emprestimos_ativos), 1)

    def test_realizar_emprestimo_item_indisponivel(self):
        self.biblioteca.realizar_emprestimo("MINVER001", "1984", "2023-03-10", "2023-03-24") # Empresta primeiro
        resultado = self.biblioteca.realizar_emprestimo("MINVER001", "1984", "2023-03-11", "2023-03-25")
        self.assertIn("não está disponível", resultado)

    def test_realizar_emprestimo_usuario_nao_encontrado(self):
        resultado = self.biblioteca.realizar_emprestimo("MAT999", "1984", "2023-03-10", "2023-03-24")
        self.assertEqual(resultado, "Usuário não encontrado.")

    def test_realizar_emprestimo_item_nao_encontrado(self):
        resultado = self.biblioteca.realizar_emprestimo("MINVER001", "Livro X", "2023-03-10", "2023-03-24")
        self.assertEqual(resultado, "Item não encontrado no catálogo.")

    def test_registrar_devolucao_item_sucesso(self):
        self.biblioteca.realizar_emprestimo("MINVER001", "1984", "2023-03-10", "2023-03-24")
        resultado = self.biblioteca.registrar_devolucao_item("MINVER001", "1984", "2023-03-15")
        self.assertIn("devolvido por Winston Smith", resultado)
        self.assertTrue(self.livro1.esta_disponivel())
        self.assertTrue(self.biblioteca.emprestimos_ativos[0].devolvido)

    def test_registrar_devolucao_item_nao_emprestado(self):
        resultado = self.biblioteca.registrar_devolucao_item("MINVER001", "1984", "2023-03-15")
        self.assertEqual(resultado, "Empréstimo não encontrado ou já devolvido.")


class TestConfiguracaoBiblioteca(unittest.TestCase):
    def test_criar_configuracao(self):
        config = ConfiguracaoBiblioteca(max_livros_por_usuario=3, dias_emprestimo_padrao=10)
        self.assertEqual(config.get_max_livros_por_usuario(), 3)
        self.assertEqual(config.dias_emprestimo_padrao, 10)

    def test_set_max_livros(self):
        config = ConfiguracaoBiblioteca()
        config.set_max_livros_por_usuario(7)
        self.assertEqual(config.get_max_livros_por_usuario(), 7)

    def test_set_max_livros_invalido(self):
        config = ConfiguracaoBiblioteca()
        with self.assertRaises(ValueError):
            config.set_max_livros_por_usuario(-1)
        with self.assertRaises(ValueError):
            config.set_max_livros_por_usuario("abc")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)