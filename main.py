from database import init_db
import livro as livro_repo 

def _imprimir_livros(livros):
    """Função auxiliar para imprimir uma lista de livros de forma formatada."""
    if not livros:
        print("\nNenhum livro encontrado.")
        return

    print("\n--- Lista de Livros ---")
    for livro in livros:
        disponivel_str = "Sim" if livro["disponivel"] else "Não"
        status_str = livro_repo.Status(livro["livro_status"]).name
        print(
            f"ID: {livro['id']} | Título: {livro['titulo']} | Autor: {livro['autor']} | "
            f"Editora: {livro['editora']} | Ano: {livro['ano']} | "
            f"Disponível: {disponivel_str} | Status: {status_str}"
        )
    print("-----------------------\n")

def _adicionar_livro_ui():
    """Interface para adicionar um novo livro."""
    print("\n--- Adicionar Novo Livro ---")
    titulo = input("Título: ")
    autor = input("Autor: ")
    editora = input("Editora: ")

    print("Selecione a categoria:")
    for cat in livro_repo.Categoria:
        print(f"{cat.value} - {cat.name}")
    
    while True:
        try:
            categoria_id = int(input("Categoria: "))
            categoria = livro_repo.Categoria(categoria_id)
            break
        except (ValueError, KeyError):
            print("Opção de categoria inválida. Tente novamente.")

    while True:
        try:
            ano_str = input("Ano de Publicação (deixe em branco se não souber): ")
            ano = int(ano_str) if ano_str else None
            break
        except ValueError:
            print("Ano inválido. Por favor, insira um número.")
    
    novo_id = livro_repo.adicionar_livro(titulo, autor, editora, categoria, ano)
    if novo_id:
        print(f"\nLivro '{titulo}' adicionado com sucesso! (ID: {novo_id})")
    else:
        print("\nOcorreu um erro ao adicionar o livro.")

def _atualizar_status_ui():
    """Interface para atualizar a disponibilidade de um livro."""
    try:
        livro_id = int(input("\nDigite o ID do livro que deseja atualizar: "))
        novo_status_str = input("O livro está disponível? (s/n): ").lower()
        
        if novo_status_str not in ['s', 'n']:
            print("Opção inválida. Use 's' para sim ou 'n' para não.")
            return

        disponivel = True if novo_status_str == 's' else False
        
        if livro_repo.atu_disp(livro_id, disponivel):
            print("\nStatus de disponibilidade atualizado com sucesso!")
        else:
            print("\nID do livro não encontrado.")
    except ValueError:
        print("\nID inválido. Por favor, digite um número.")

def _remover_livro_ui():
    """Interface para marcar um livro como 'excluído' (soft delete)."""
    try:
        livro_id = int(input("\nDigite o ID do livro que deseja remover (remoção lógica): "))
        if livro_repo.deletar_livro_logico(livro_id):
            print(f"\nLivro ID {livro_id} foi removido com sucesso (marcado como excluído).")
        else:
            print("\nID do livro não encontrado.")
    except ValueError:
        print("\nID inválido. Por favor, digite um número.")

def _excluir_livro_ui():
    """Interface para excluir permanentemente um livro (hard delete)."""
    try:
        livro_id = int(input("\nDigite o ID do livro que deseja EXCLUIR PERMANENTEMENTE: "))
        confirmacao = input(f"Tem CERTEZA que deseja excluir o livro ID {livro_id} para sempre? Esta ação não pode ser desfeita. (s/n): ").lower()

        if confirmacao == 's':
            if livro_repo.deletar_fisico(livro_id):
                print(f"\nLivro ID {livro_id} foi excluído permanentemente.")
            else:
                print("\nID do livro não encontrado.")
        else:
            print("\nOperação cancelada.")
    except ValueError:
        print("\nID inválido. Por favor, digite um número.")


def menu_biblioteca():
    init_db()
    while True:
        print("\n=== Menu da Biblioteca ===")
        print("1 - Adicionar livro")
        print("2 - Listar todos os livros")
        print("3 - Buscar livro por título, autor ou editora")
        print("4 - Atualizar Disponibilidade do Livro")
        print("5 - Remover livro (Soft Delete)")
        print("6 - Excluir livro permanentemente (Hard Delete)")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            _adicionar_livro_ui()
        elif opcao == '2':
            livros = livro_repo.listar_livros()
            _imprimir_livros(livros)
        elif opcao == '3':
            termo = input("Digite o termo de busca: ")
            livros = livro_repo.buscar_livros(termo)
            _imprimir_livros(livros)
        elif opcao == '4':
            _atualizar_status_ui()
        elif opcao == '5':
            _remover_livro_ui()
        elif opcao == '6':
            _excluir_livro_ui()
        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_biblioteca()