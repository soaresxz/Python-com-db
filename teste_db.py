# teste_db.py
import sqlite3
import os

DB_FILE = "banco_de_teste.db"
SQL_SCRIPT = """
CREATE TABLE livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    editora TEXT NOT NULL,
    categoria INTEGER NOT NULL,
    ano INTEGER,
    disponivel INTEGER NOT NULL DEFAULT 1 CHECK (disponivel IN (0, 1)),
    livro_status INTEGER NOT NULL DEFAULT 1
);
"""

# Garante que estamos começando do zero
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Arquivo antigo '{DB_FILE}' removido.")

print("--- Iniciando teste de criação de tabela ---")

try:
    # Conectando e criando a tabela
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("Executando o comando SQL...")
    cursor.execute(SQL_SCRIPT)
    conn.commit()
    conn.close()
    
    print("\n***********************************************")
    print(">>> SUCESSO! O script de teste funcionou!")
    print("O comando SQL está correto e a tabela foi criada.")
    print("***********************************************")

except sqlite3.OperationalError as e:
    print("\n****************************************************************")
    print(">>> FALHA! O erro ocorreu novamente no script de teste isolado.")
    print(f"Erro exato: {e}")
    print("Isso sugere fortemente que o problema pode ser a versão do")
    print("SQLite instalada no seu sistema. O comando está correto,")
    print("mas o 'motor' que o executa pode ser muito antigo.")
    print("****************************************************************")

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")